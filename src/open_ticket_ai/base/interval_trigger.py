import asyncio

from pydantic import BaseModel

from open_ticket_ai.core.orchestration.orchestrator_config import TriggerDefinition
from open_ticket_ai.core.orchestration.trigger import Trigger


class IntervalTriggerParams(BaseModel):
    milliseconds: int = 0
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0


class IntervalTrigger(Trigger):
    def __init__(self, trigger_def: TriggerDefinition[IntervalTriggerParams]) -> None:
        super().__init__(trigger_def)
        params = trigger_def.params
        self.interval = (
            params.days * 86400 +
            params.hours * 3600 +
            params.minutes * 60 +
            params.seconds +
            params.milliseconds / 1000
        )
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())

    def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None

    async def _run(self) -> None:
        while self._running:
            await asyncio.sleep(self.interval)
            self.notify()
