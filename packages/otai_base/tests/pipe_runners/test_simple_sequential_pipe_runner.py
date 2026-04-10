from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult

from otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner

pytestmark = [pytest.mark.unit]


class SuccessTrigger(Pipe):
    def __init__(self) -> None:
        super().__init__("trigger")

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.success(message="ok")


class FailTrigger(Pipe):
    def __init__(self) -> None:
        super().__init__("trigger")

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.failure("not yet")


async def test_simple_sequential_runner_runs_when_trigger_succeeds():
    run_pipe = MagicMock(spec=Pipe)
    run_pipe.pipe_id = "main"
    run_pipe.process = AsyncMock(return_value=PipeResult.success(data={"x": 1}))

    runner = SimpleSequentialRunner("runner", SuccessTrigger(), run_pipe)
    result = await runner.process(PipeContext.empty())

    run_pipe.process.assert_awaited_once()
    assert result.succeeded
    assert result.data["x"] == 1


async def test_simple_sequential_runner_skips_run_when_trigger_fails():
    run_pipe = MagicMock(spec=Pipe)
    run_pipe.pipe_id = "main"
    run_pipe.process = AsyncMock()

    runner = SimpleSequentialRunner("runner", FailTrigger(), run_pipe)
    result = await runner.process(PipeContext.empty())

    run_pipe.process.assert_not_awaited()
    assert not result.has_succeeded()
    assert result.was_skipped
