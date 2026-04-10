import asyncio

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
