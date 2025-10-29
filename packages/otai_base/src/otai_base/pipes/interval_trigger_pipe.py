import datetime
from datetime import timedelta
from typing import Any, ClassVar

from open_ticket_ai import Pipe, StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from pydantic import BaseModel, Field


class IntervalTriggerParams(StrictBaseModel):
    interval: timedelta = Field(description="Time interval between trigger executions specified as a timedelta object.")


class IntervalTrigger(Pipe[IntervalTriggerParams]):
    ParamsModel: ClassVar[type[BaseModel]] = IntervalTriggerParams

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.last_time_fired: datetime.datetime = datetime.datetime.now(tz=datetime.UTC)

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        if datetime.datetime.now(tz=datetime.UTC) - self.last_time_fired >= self._params.interval:
            self.last_time_fired = datetime.datetime.now(tz=datetime.UTC)
            return PipeResult.success()
        return PipeResult.failure("Interval not reached yet.")
