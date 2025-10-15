import time
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.orchestration.orchestrator_models import TriggerConfig
from open_ticket_ai.core.orchestration.trigger import Trigger


class IntervalTriggerParams(RootModel[timedelta]): ...


class IntervalTrigger(Trigger[IntervalTriggerParams]):
    def _should_trigger(self) -> bool:
        self.current_nanos = time.time_ns()
        if self.current_nanos - self.last_time_fired >= self.nano_seconds_interval:
            self.last_time_fired = self.current_nanos
            return True
        return False

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return IntervalTriggerParams

    def __init__(self, config: TriggerConfig, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, *args, **kwargs)
        self.last_time_fired = time.time_ns()
        self.nano_seconds_interval: float = (
            self._params.days * 86400 * 1e9
            + self._params.hours * 3600 * 1e9
            + self._params.minutes * 60 * 1e9
            + self._params.seconds * 1e9
            + self._params.milliseconds * 1e6
        )
