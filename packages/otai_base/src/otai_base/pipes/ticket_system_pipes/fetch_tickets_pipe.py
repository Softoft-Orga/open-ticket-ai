from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria

from otai_base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe


class FetchTicketsPipe(TicketSystemPipe):
    def __init__(
        self,
        pipe_id: str,
        ticket_system: TicketSystemService,
        search_criteria: TicketSearchCriteria,
        *,
        fail_on_empty: bool = True,
    ) -> None:
        super().__init__(pipe_id, ticket_system)
        self._search_criteria = search_criteria
        self._fail_on_empty = fail_on_empty

    async def _process(self, context: PipeContext) -> PipeResult:
        tickets = await self._ticket_system.find_tickets(self._search_criteria)
        if not tickets and self._fail_on_empty:
            return PipeResult.failure("No tickets found matching search criteria")
        return PipeResult.success(
            data={"fetched_tickets": [t.model_dump() for t in tickets]},
        )
