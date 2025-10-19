from typing import Any

from pydantic import Field

from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.base.ticket_system_integration.unified_models import TicketSearchCriteria
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class FetchTicketsParams(StrictBaseModel):
    ticket_search_criteria: TicketSearchCriteria = Field(
        description="Search criteria including queue, limit, and offset for querying tickets from the ticket system."
    )


class FetchTicketsPipe(TicketSystemPipe[FetchTicketsParams]):
    @staticmethod
    def get_params_model() -> type[FetchTicketsParams]:
        return FetchTicketsParams

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        search_criteria = self._params.ticket_search_criteria
        return PipeResult(
            succeeded=True,
            data={
                "fetched_tickets": (await self._ticket_system.find_tickets(search_criteria)),
            },
        )
