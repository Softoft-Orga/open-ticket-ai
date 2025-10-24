from typing import Any, ClassVar
from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai import LoggerFactory, Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from pydantic import BaseModel

from otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner


class EmptyParams(BaseModel):
    pass


class AlwaysSucceedingTrigger(Pipe[EmptyParams]):
    ParamsModel: ClassVar[type[BaseModel]] = EmptyParams

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)

    async def _process(self, _: PipeContext) -> PipeResult:
        return PipeResult.success(message="Trigger succeeded")


class AlwaysFailingTrigger(Pipe[EmptyParams]):
    ParamsModel: ClassVar[type[BaseModel]] = EmptyParams

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)

    async def _process(self, _: PipeContext) -> PipeResult:
        return PipeResult.failure(message="Trigger failed")


@pytest.fixture
def mock_pipe_factory():
    """Create a mock PipeFactory that can render pipes."""
    factory = MagicMock()
    factory.create_pipe = AsyncMock()
    return factory


@pytest.fixture
def empty_context():
    """Create an empty pipe context for testing."""
    return PipeContext(pipe_results={}, params={})


@pytest.fixture
def succeeding_trigger_config():
    return PipeConfig(
        id="trigger",
        use="tests.unit.otai_base.pipe_runners.test_simple_sequential_pipe_runner.AlwaysSucceedingTrigger",
        params={},
    )


@pytest.fixture
def failing_trigger_config():
    return PipeConfig(
        id="trigger",
        use="tests.unit.otai_base.pipe_runners.test_simple_sequential_pipe_runner.AlwaysFailingTrigger",
        params={},
    )


@pytest.fixture
def mock_main_pipe():
    mock_pipe = MagicMock()
    mock_pipe.process = AsyncMock(return_value=PipeResult.success(message="Main pipe executed"))
    return mock_pipe


def create_runner(
    trigger_config: PipeConfig,
    logger_factory: LoggerFactory,
    mock_pipe_factory: MagicMock,
    trigger_instance: Pipe[Any],
    mock_main_pipe: MagicMock,
) -> SimpleSequentialRunner:
    async def create_pipe_side_effect(config, *args, **kwargs):
        return trigger_instance if config.id == "trigger" else mock_main_pipe

    mock_pipe_factory.create_pipe.side_effect = create_pipe_side_effect

    runner_config = PipeConfig(
        id="runner",
        use="open_ticket_ai.otai_base.pipe_runners.simple_sequential_pipe_runner.SimpleSequentialRunner",
        params={"on": trigger_config.model_dump(), "run": {"id": "main", "use": "some.pipe", "params": {}}},
    )
    return SimpleSequentialRunner(config=runner_config, logger_factory=logger_factory, pipe_factory=mock_pipe_factory)


@pytest.mark.asyncio
async def test_pipe_runs_when_trigger_succeeds(
    logger_factory, mock_pipe_factory, empty_context, succeeding_trigger_config, mock_main_pipe
):
    trigger = AlwaysSucceedingTrigger(config=succeeding_trigger_config, logger_factory=logger_factory)
    runner = create_runner(succeeding_trigger_config, logger_factory, mock_pipe_factory, trigger, mock_main_pipe)

    result = await runner.process(empty_context)

    mock_main_pipe.process.assert_called_once()
    assert result.has_succeeded(), "Runner should succeed when both trigger and main pipe succeed"

    call_args = mock_main_pipe.process.call_args
    context_passed = call_args[0][0] if call_args else None
    assert context_passed is not None, "Context should be passed to main pipe"


@pytest.mark.asyncio
async def test_pipe_not_run_when_trigger_fails(
    logger_factory, mock_pipe_factory, empty_context, failing_trigger_config, mock_main_pipe
):
    trigger = AlwaysFailingTrigger(config=failing_trigger_config, logger_factory=logger_factory)
    runner = create_runner(failing_trigger_config, logger_factory, mock_pipe_factory, trigger, mock_main_pipe)

    result = await runner.process(empty_context)

    mock_main_pipe.process.assert_not_called()
    assert not result.has_succeeded(), "Runner should fail when trigger fails"
