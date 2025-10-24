import asyncio
import contextlib
from datetime import timedelta
from typing import Any, ClassVar
from unittest.mock import MagicMock

import pytest
from open_ticket_ai import LoggerFactory, Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from pydantic import BaseModel

from otai_base.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator


class EmptyParams(BaseModel):
    pass


class SpyPipe(Pipe[EmptyParams]):
    ParamsModel: ClassVar[type[BaseModel]] = EmptyParams

    def __init__(self, config: PipeConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, logger_factory, *args, **kwargs)
        self.call_count = 0
        self.captured_contexts = []

    async def _process(self, context: PipeContext) -> PipeResult:
        self.call_count += 1
        self.captured_contexts.append(context)
        return PipeResult.success(message=f"Pipe {self._config.id} executed")


@pytest.fixture
def mock_pipe_factory():
    """Create a mock PipeFactory that can render spy pipes."""
    factory = MagicMock()
    return factory


@pytest.fixture
def empty_context():
    """Create an empty pipe context for testing."""
    return PipeContext(pipe_results={}, params={})


@pytest.fixture
def orchestrator_setup(logger_factory, mock_pipe_factory):
    """Create configured orchestrator with spy pipes for testing."""
    spy_pipe1 = SpyPipe(config=PipeConfig(id="pipe1", use="test.pipe1", params={}), logger_factory=logger_factory)
    spy_pipe2 = SpyPipe(config=PipeConfig(id="pipe2", use="test.pipe2", params={}), logger_factory=logger_factory)

    async def create_pipe_async(config, *args, **kwargs):
        return spy_pipe1 if config.id == "pipe1" else spy_pipe2

    mock_pipe_factory.create_pipe = create_pipe_async

    orchestrator_config = PipeConfig(
        id="orchestrator",
        use="open_ticket_ai.otai_base.pipes.orchestrators.simple_sequential_orchestrator.SimpleSequentialOrchestrator",
        params={
            "orchestrator_sleep": timedelta(seconds=0.001),
            "steps": [
                PipeConfig(id="pipe1", use="test.pipe1", params={}),
                PipeConfig(id="pipe2", use="test.pipe2", params={}),
            ],
        },
    )

    orchestrator = SimpleSequentialOrchestrator(
        config=orchestrator_config, logger_factory=logger_factory, pipe_factory=mock_pipe_factory
    )

    return orchestrator, spy_pipe1, spy_pipe2


@pytest.mark.asyncio
async def test_continuous_execution_with_keyboard_interrupt(orchestrator_setup, empty_context):
    """Test continuous execution loop with KeyboardInterrupt."""
    orchestrator, spy_pipe1, spy_pipe2 = orchestrator_setup

    async def run_orchestrator():
        with contextlib.suppress(asyncio.CancelledError):
            await orchestrator.process(empty_context)

    task = asyncio.create_task(run_orchestrator())
    await asyncio.sleep(1.0)
    task.cancel()

    with contextlib.suppress(asyncio.CancelledError):
        await task

    assert spy_pipe1.call_count > 1, (
        f"Pipe 1 should be called multiple times, but was called {spy_pipe1.call_count} times"
    )
    assert spy_pipe2.call_count > 1, (
        f"Pipe 2 should be called multiple times, but was called {spy_pipe2.call_count} times"
    )


@pytest.mark.asyncio
async def test_context_isolation(orchestrator_setup, empty_context):
    """Test context isolation between pipes."""
    orchestrator, spy_pipe1, spy_pipe2 = orchestrator_setup

    async def run_orchestrator():
        with contextlib.suppress(asyncio.CancelledError):
            await orchestrator.process(empty_context)

    task = asyncio.create_task(run_orchestrator())
    await asyncio.sleep(0.1)
    task.cancel()

    with contextlib.suppress(asyncio.CancelledError):
        await task

    assert len(spy_pipe1.captured_contexts) > 0, "Pipe 1 should have captured contexts"
    assert len(spy_pipe2.captured_contexts) > 0, "Pipe 2 should have captured contexts"

    for context in spy_pipe1.captured_contexts:
        assert context.parent_params is not None, "Context parent should be set"
        assert context.pipe_results == {}, "Context pipe_results should be empty (isolated)"

    for context in spy_pipe2.captured_contexts:
        assert context.parent_params is not None, "Context parent should be set"
        assert context.pipe_results == {}, "Context pipe_results should be empty (isolated)"
