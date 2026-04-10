from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class SimpleSequentialRunner(Pipe):
    """Runs ``run_pipe`` only when ``trigger`` succeeds."""

    def __init__(self, pipe_id: str, trigger: Pipe, run_pipe: Pipe) -> None:
        super().__init__(pipe_id)
        self._trigger = trigger
        self._run_pipe = run_pipe

    async def _process(self, context: PipeContext) -> PipeResult:
        trigger_result = await self._trigger.process(context)
        if trigger_result.has_succeeded():
            return await self._run_pipe.process(context)
        return PipeResult.skipped(f"Trigger did not fire: {trigger_result.message}")
