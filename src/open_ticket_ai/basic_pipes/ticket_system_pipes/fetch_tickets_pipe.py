from typing import Any

from open_ticket_ai.basic_pipes.ticket_system_pipes.ticket_system_base_pipe_config import (
    RawTicketSystemBasePipeConfig,
    RenderedTicketSystemBasePipeConfig,
)
from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class RawTicketFetchPipeConfig(RawTicketSystemBasePipeConfig):
    ticket_search_criteria: str | TicketSearchCriteria | dict[str, Any] | None = None


class RenderedTicketFetchPipeConfig(RenderedTicketSystemBasePipeConfig):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipe(ConfigurablePipe[RawTicketFetchPipeConfig, RenderedTicketFetchPipeConfig]):
    async def _process(self) -> dict[str, Any]:
        tickets = await self.config.ticket_system.find_tickets(self.config.ticket_search_criteria) or []
        return {"found_tickets": [ticket.model_dump() for ticket in tickets]}
