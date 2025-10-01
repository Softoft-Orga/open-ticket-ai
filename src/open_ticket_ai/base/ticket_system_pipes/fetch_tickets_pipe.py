from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsPipeConfig(BaseModel):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipe(Pipe):
    def __init__(self, ticket_system: TicketSystemService, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.ticket_system = ticket_system
        pipe_config = FetchTicketsPipeConfig.model_validate(config)
        self.search_criteria = pipe_config.ticket_search_criteria

    async def _process(self) -> PipeResult:
        try:
            tickets = await self.ticket_system.find_tickets(self.search_criteria) or []
            return PipeResult(
                success=True,
                failed=False,
                data={"found_tickets": [ticket.model_dump() for ticket in tickets]},
            )
        except Exception as e:
            return PipeResult(success=False, failed=True, data={"error": str(e)})
