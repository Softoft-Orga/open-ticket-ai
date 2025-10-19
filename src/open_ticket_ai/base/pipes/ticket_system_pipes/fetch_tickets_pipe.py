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

        self._logger.info(
            f"🔍 Fetching tickets with criteria: queue={search_criteria.queue}, limit={search_criteria.limit}"
        )
        self._logger.debug(f"Full search criteria: {search_criteria.model_dump()}")

        try:
            tickets = await self._ticket_system.find_tickets(search_criteria)

            self._logger.info(f"📥 Retrieved {len(tickets)} ticket(s)")

            if tickets:
                self._logger.debug(f"Ticket IDs: {[t.id for t in tickets]}")
            else:
                self._logger.debug("No tickets found matching criteria")

            return PipeResult(
                succeeded=True,
                data={
                    "fetched_tickets": tickets,
                },
            )
        except Exception as e:
            self._logger.error(f"❌ Failed to fetch tickets: {e}", exc_info=True)
            raise
