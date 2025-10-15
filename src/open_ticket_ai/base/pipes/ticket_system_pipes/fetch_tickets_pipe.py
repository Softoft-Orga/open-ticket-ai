from pydantic import BaseModel

from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipeline.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsParams(StrictBaseModel):
    ticket_search_criteria: TicketSearchCriteria


class FetchTicketsPipe(TicketSystemPipe[FetchTicketsParams]):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return FetchTicketsParams

    async def _process(self) -> PipeResult:
        search_criteria = self._params.ticket_search_criteria
        return PipeResult(
            succeeded=True,
            data={
                "fetched_tickets": (await self._ticket_system.find_tickets(search_criteria)),
            },
        )
