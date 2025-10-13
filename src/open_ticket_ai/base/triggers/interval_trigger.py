import asyncio
from typing import Any

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
    def __init__(self, config: TriggerDefinition, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, *args, **kwargs)
        # Validate params at runtime
        validated_params = IntervalTriggerParams.model_validate(self.params)
        self.seconds_interval: float = (
            validated_params.days * 86400
            + validated_params.hours * 3600
            + validated_params.minutes * 60
            + validated_params.seconds
            + validated_params.milliseconds / 1000
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
            await asyncio.sleep(self.seconds_interval)
            self.notify()
