from abc import ABC, abstractmethod
from typing import Any, final

from pydantic import BaseModel

from open_ticket_ai.core.orchestration.trigger_observer import TriggerObserver
from open_ticket_ai.core.renderable.renderable import Renderable


class Trigger[ParamsT: BaseModel](Renderable[ParamsT], ABC):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._observer: TriggerObserver | None = None

    @final
    def attach(self, observer: TriggerObserver) -> None:
        self._observer = observer

    @final
    def detach(self) -> None:
        self._observer = None

    @final
    async def run(self) -> None:
        if self._should_trigger() and self._observer:
            await self._observer.on_trigger_fired()

    @abstractmethod
    def _should_trigger(self) -> bool:
        pass
