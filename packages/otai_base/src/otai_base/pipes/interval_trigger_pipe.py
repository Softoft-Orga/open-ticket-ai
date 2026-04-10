import datetime

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class IntervalTrigger(Pipe):
    """Succeeds at most once per ``interval_seconds``."""

    def __init__(self, pipe_id: str, interval_seconds: float) -> None:
        super().__init__(pipe_id)
        self._interval = datetime.timedelta(seconds=interval_seconds)
        self._last_fired = datetime.datetime.now(tz=datetime.UTC)

    async def _process(self, context: PipeContext) -> PipeResult:
        now = datetime.datetime.now(tz=datetime.UTC)
        if now - self._last_fired >= self._interval:
            self._last_fired = now
            return PipeResult.success()
        return PipeResult.failure("Interval not reached yet.")
