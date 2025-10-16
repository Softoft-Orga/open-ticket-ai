import datetime
from datetime import timedelta
from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.orchestration.orchestrator_models import TriggerConfig
from open_ticket_ai.core.orchestration.trigger import Trigger


class IntervalTriggerParams(StrictBaseModel):
    interval: timedelta = Field(default_factory=timedelta, description="Interval in seconds")


class IntervalTrigger(Trigger[IntervalTriggerParams]):

    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return IntervalTriggerParams

    def __init__(self, config: TriggerConfig, *args: Any, **kwargs: Any) -> None:
        super().__init__(config, *args, **kwargs)
        self.last_time_fired: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)

    def _should_trigger(self) -> bool:
        if datetime.datetime.now(tz=datetime.UTC) - self.last_time_fired >= self._params.interval:
            self.last_time_fired = datetime.datetime.now(tz=datetime.UTC)
            return True
        return False
