import datetime
from datetime import timedelta
from typing import Any

from pydantic import BaseModel, Field

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class IntervalTriggerParams(StrictBaseModel):
    interval: timedelta = Field(description="Time interval between trigger executions specified as a timedelta object.")


class IntervalTrigger(Pipe[IntervalTriggerParams]):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return IntervalTriggerParams

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.last_time_fired: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)

    def _process(self, *_: Any, **__: Any) -> PipeResult:
        if datetime.datetime.now(tz=datetime.UTC) - self.last_time_fired >= self._params.interval:
            self.last_time_fired = datetime.datetime.now(tz=datetime.UTC)
            return PipeResult.success()
        return PipeResult.failure("Interval not reached yet.")
