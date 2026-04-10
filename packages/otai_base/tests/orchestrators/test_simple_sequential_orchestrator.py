import asyncio

import pytest
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult

import otai_base.pipes.orchestrators.simple_sequential_orchestrator as orchestrator_module
from otai_base.pipes.orchestrators.simple_sequential_orchestrator import SimpleSequentialOrchestrator

pytestmark = [pytest.mark.unit]


class CountingPipe(Pipe):
    def __init__(self, pipe_id: str, counter: list[int]) -> None:
        super().__init__(pipe_id)
        self._counter = counter

    async def _process(self, context: PipeContext) -> PipeResult:
        self._counter[0] += 1
        return PipeResult.success()


async def test_simple_sequential_orchestrator_runs_cycles_until_sleep_stops(monkeypatch):
    counts = [0]
    steps = [CountingPipe("a", counts), CountingPipe("b", counts)]
    orch = SimpleSequentialOrchestrator("orch", steps, sleep=0.01, exception_sleep=1.0)

    sleep_calls = 0

    async def short_sleep(_delay: float) -> None:
        nonlocal sleep_calls
        sleep_calls += 1
        if sleep_calls >= 3:
            raise asyncio.CancelledError()

    monkeypatch.setattr(orchestrator_module.asyncio, "sleep", short_sleep)
    with pytest.raises(asyncio.CancelledError):
        await orch.process(PipeContext.empty())

    assert counts[0] >= 4
    assert sleep_calls == 3


async def test_simple_sequential_orchestrator_retries_after_step_error(monkeypatch):
    class FlakyPipe(Pipe):
        def __init__(self, pipe_id: str, fails_left: list[int]) -> None:
            super().__init__(pipe_id)
            self._fails_left = fails_left

        async def _process(self, context: PipeContext) -> PipeResult:
            if self._fails_left[0] > 0:
                self._fails_left[0] -= 1
                raise RuntimeError("boom")
            return PipeResult.success()

    fails = [2]
    steps = [FlakyPipe("flaky", fails), CountingPipe("ok", [0])]
    orch = SimpleSequentialOrchestrator(
        "orch",
        steps,
        sleep=0.01,
        exception_sleep=0.01,
        always_retry=True,
    )

    sleep_calls = 0

    async def stop_after_enough_sleeps(_delay: float) -> None:
        nonlocal sleep_calls
        sleep_calls += 1
        if sleep_calls >= 20:
            raise asyncio.CancelledError()

    monkeypatch.setattr(orchestrator_module.asyncio, "sleep", stop_after_enough_sleeps)
    with pytest.raises(asyncio.CancelledError):
        await orch.process(PipeContext.empty())

    assert fails[0] == 0
