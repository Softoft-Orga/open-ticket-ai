from typing import Any, ClassVar
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel

from open_ticket_ai.base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult


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
    return factory


@pytest.fixture
def empty_context():
    """Create an empty pipe context for testing."""
    return PipeContext(pipe_results={}, params={})


@pytest.mark.asyncio
async def test_pipe_runs_when_trigger_succeeds(logger_factory, mock_pipe_factory, empty_context):
    """Test that the main pipe runs when the trigger succeeds."""
    # Create the trigger and main pipe
    trigger_config = PipeConfig(
        id="trigger",
        use="tests.unit.base.pipe_runners.test_simple_sequential_pipe_runner.AlwaysSucceedingTrigger",
        params={},
    )
    trigger = AlwaysSucceedingTrigger(config=trigger_config, logger_factory=logger_factory)

    # Create a mock for the main pipe
    mock_main_pipe = MagicMock()
    mock_main_pipe.process = AsyncMock(return_value=PipeResult.success(message="Main pipe executed"))

    # Configure the mock factory to return our pipes
    mock_pipe_factory.create_pipe.side_effect = lambda config, *args, **kwargs: (
        trigger if config.id == "trigger" else mock_main_pipe
    )

    # Create the SimpleSequentialRunner
    runner_config = PipeConfig(
        id="runner",
        use="open_ticket_ai.base.pipe_runners.simple_sequential_pipe_runner.SimpleSequentialRunner",
        params={"on": trigger_config.model_dump(), "run": {"id": "main", "use": "some.pipe", "params": {}}},
    )
    runner = SimpleSequentialRunner(config=runner_config, logger_factory=logger_factory, pipe_factory=mock_pipe_factory)

    # Run the runner
    result = await runner.process(empty_context)

    # Verify the main pipe was called
    mock_main_pipe.process.assert_called_once()
    assert result.has_succeeded(), "Runner should succeed when both trigger and main pipe succeed"

    # Verify context.parent is set correctly
    call_args = mock_main_pipe.process.call_args
    context_passed = call_args[0][0] if call_args else None
    assert context_passed is not None, "Context should be passed to main pipe"
    assert context_passed.parent is not None, "Context parent should be set"


@pytest.mark.asyncio
async def test_pipe_not_run_when_trigger_fails(logger_factory, mock_pipe_factory, empty_context):
    """Test that the main pipe does NOT run when the trigger fails."""
    # Create the trigger
    trigger_config = PipeConfig(
        id="trigger",
        use="tests.unit.base.pipe_runners.test_simple_sequential_pipe_runner.AlwaysFailingTrigger",
        params={},
    )
    trigger = AlwaysFailingTrigger(config=trigger_config, logger_factory=logger_factory)

    # Create a mock for the main pipe
    mock_main_pipe = MagicMock()
    mock_main_pipe.process = AsyncMock(return_value=PipeResult.success(message="Main pipe executed"))

    # Configure the mock factory to return our pipes
    mock_pipe_factory.create_pipe.side_effect = lambda config, *args, **kwargs: (
        trigger if config.id == "trigger" else mock_main_pipe
    )

    # Create the SimpleSequentialRunner
    runner_config = PipeConfig(
        id="runner",
        use="open_ticket_ai.base.pipe_runners.simple_sequential_pipe_runner.SimpleSequentialRunner",
        params={"on": trigger_config.model_dump(), "run": {"id": "main", "use": "some.pipe", "params": {}}},
    )
    runner = SimpleSequentialRunner(config=runner_config, logger_factory=logger_factory, pipe_factory=mock_pipe_factory)

    # Run the runner
    result = await runner.process(empty_context)

    # Verify the main pipe was NOT called
    mock_main_pipe.process.assert_not_called()
    assert result.was_skipped, "Runner should return skipped result when trigger fails"


@pytest.mark.asyncio
async def test_context_parent_is_sequential_runner_params(logger_factory, mock_pipe_factory, empty_context):
    """Test that the context passed to pipes has correct parent set to params."""
    # Create the trigger
    trigger_config = PipeConfig(
        id="trigger",
        use="tests.unit.base.pipe_runners.test_simple_sequential_pipe_runner.AlwaysSucceedingTrigger",
        params={},
    )
    trigger = AlwaysSucceedingTrigger(config=trigger_config, logger_factory=logger_factory)

    # Create a mock for the main pipe that captures the context
    captured_context = None

    async def capture_context(context: PipeContext):
        nonlocal captured_context
        captured_context = context
        return PipeResult.success(message="Main pipe executed")

    mock_main_pipe = MagicMock()
    mock_main_pipe.process = AsyncMock(side_effect=capture_context)

    # Configure the mock factory to return our pipes
    mock_pipe_factory.create_pipe.side_effect = lambda config, *args, **kwargs: (
        trigger if config.id == "trigger" else mock_main_pipe
    )

    # Create the SimpleSequentialRunner
    runner_config = PipeConfig(
        id="runner",
        use="open_ticket_ai.base.pipe_runners.simple_sequential_pipe_runner.SimpleSequentialRunner",
        params={"on": trigger_config.model_dump(), "run": {"id": "main", "use": "some.pipe", "params": {}}},
    )
    runner = SimpleSequentialRunner(config=runner_config, logger_factory=logger_factory, pipe_factory=mock_pipe_factory)

    # Run the runner
    await runner.process(empty_context)

    # Verify context parent is set correctly
    assert captured_context is not None, "Context should have been captured"
    assert captured_context.parent is not None, "Context parent should be set"
    # The parent should be the params dict from the original context
    assert isinstance(captured_context.parent, dict), "Context parent should be a dict (params)"
