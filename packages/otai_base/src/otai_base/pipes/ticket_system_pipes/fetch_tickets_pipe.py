from typing import Any, ClassVar

from open_ticket_ai import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria
from pydantic import Field

from otai_base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe


class FetchTicketsParams(StrictBaseModel):
    ticket_search_criteria: TicketSearchCriteria = Field(
        description="Search criteria including queue, limit, and offset for querying tickets from the ticket system."
    )


class FetchTicketsPipe(TicketSystemPipe[FetchTicketsParams]):
    ParamsModel: ClassVar[type[FetchTicketsParams]] = FetchTicketsParams

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        search_criteria = self._params.ticket_search_criteria
        return PipeResult(
            succeeded=True,
            data={
                "fetched_tickets": (await self._ticket_system.find_tickets(search_criteria)),
            },
        )
