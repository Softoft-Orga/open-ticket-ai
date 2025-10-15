from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsParams(BaseModel):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipe(Pipe):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return FetchTicketsParams

    def __init__(
            self,
            ticket_system: TicketSystemService,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        search_criteria = self._params.ticket_search_criteria
        return PipeResult(
            success=True,
            data={
                "fetched_tickets": (await self._ticket_system.find_tickets(search_criteria)),
            },
        )
