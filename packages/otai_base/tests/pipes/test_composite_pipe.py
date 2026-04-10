from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult

from otai_base.pipes.composite_pipe import CompositePipe

pytestmark = [pytest.mark.unit]


class SimplePipe(Pipe):
    def __init__(self, pipe_id: str, value: str = "default") -> None:
        super().__init__(pipe_id)
        self._value = value

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.success(data={"value": self._value})


async def test_composite_pipe_empty_steps():
    composite = CompositePipe("composite", [])
    result = await composite.process(PipeContext.empty())

    assert result.succeeded
    assert result.data == {}


async def test_composite_pipe_multi_step_union_of_data():
    steps = [
        SimplePipe("step1", "A"),
        SimplePipe("step2", "B"),
    ]
    composite = CompositePipe("composite", steps)

    result = await composite.process(PipeContext.empty())

    assert result.succeeded
    assert result.data == {"value": "B"}


async def test_composite_pipe_failure_stops_remaining_steps():
    ok = SimplePipe("ok", "done")
    failing = MagicMock(spec=Pipe)
    failing.pipe_id = "fail"
    failing.process = AsyncMock(return_value=PipeResult.failure("no"))

    spy = SimplePipe("never", "x")
    spy.process = AsyncMock()

    composite = CompositePipe("composite", [ok, failing, spy])
    result = await composite.process(PipeContext.empty())

    assert failing.process.await_count == 1
    spy.process.assert_not_awaited()
    assert result.succeeded
    assert result.data == {"value": "done"}
