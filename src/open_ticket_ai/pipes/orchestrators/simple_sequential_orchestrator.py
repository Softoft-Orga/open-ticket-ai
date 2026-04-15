from __future__ import annotations

import asyncio
from typing import Any

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class SimpleSequentialOrchestrator(Pipe):
    """Infinite loop that runs steps sequentially, retrying on error."""

    def __init__(
        self,
        pipe_id: str,
        steps: list[Pipe],
        *,
        sleep: float = 0.01,
        exception_sleep: float = 5.0,
        always_retry: bool = True,
    ) -> None:
        super().__init__(pipe_id)
        self._steps = steps
        self._sleep = sleep
        self._exception_sleep = exception_sleep
        self._always_retry = always_retry

    def to_descriptor(self) -> dict[str, Any]:
        return {
            **super().to_descriptor(),
            "children": [step.to_descriptor() for step in self._steps],
        }

    @classmethod
    def polling(
        cls,
        pipe_id: str,
        interval_seconds: float,
        steps: list[Pipe],
        *,
        sleep: float = 0.01,
        exception_sleep: float = 5.0,
        always_retry: bool = True,
    ) -> SimpleSequentialOrchestrator:
        """Convenience: orchestrator that polls on a fixed interval.

        Internally wires an IntervalTrigger + SimpleSequentialRunner + CompositePipe
        so callers don't have to nest three layers manually.
        """
        from open_ticket_ai.pipes.composite_pipe import CompositePipe
        from open_ticket_ai.pipes.interval_trigger_pipe import IntervalTrigger
        from open_ticket_ai.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner

        return cls(
            pipe_id=pipe_id,
            steps=[
                SimpleSequentialRunner(
                    pipe_id=f"{pipe_id}_runner",
                    trigger=IntervalTrigger(
                        pipe_id=f"{pipe_id}_trigger",
                        interval_seconds=interval_seconds,
                    ),
                    run_pipe=CompositePipe(
                        pipe_id=f"{pipe_id}_pipeline",
                        steps=steps,
                    ),
                ),
            ],
            sleep=sleep,
            exception_sleep=exception_sleep,
            always_retry=always_retry,
        )

    async def _process(self, context: PipeContext) -> PipeResult:
        while True:
            try:
                self._logger.debug("Orchestrator cycle started")
                for step in self._steps:
                    await step.process(context)
                await asyncio.sleep(self._sleep)
            except Exception:
                self._logger.exception("Orchestrator encountered an error")
                if not self._always_retry:
                    raise
                await asyncio.sleep(self._exception_sleep)
