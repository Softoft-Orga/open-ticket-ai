from __future__ import annotations

from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.trigger_observer import TriggerObserver
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext


class PipeRunner(TriggerObserver):
    def __init__(self, runner_id: str, pipe: Pipe, logger_factory: LoggerFactory) -> None:
        self._id = runner_id
        self._pipe = pipe
        self._logger = logger_factory.create(f"{self.__class__.__name__}.{runner_id}")

    async def on_trigger_fired(self) -> None:
        await self.execute()

    async def execute(self) -> None:
        await self._pipe.process(PipeContext())
