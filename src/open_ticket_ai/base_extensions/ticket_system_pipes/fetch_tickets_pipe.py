from typing import Any

from injector import inject

from open_ticket_ai.base_extensions.pipe_configs import (
    FetchTicketsPipeConfig,
    FetchTicketsPipeModel,
)
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsPipe(Pipe[FetchTicketsPipeModel]):
    """A pipe that fetches tickets from the ticket system based on search criteria."""

    @inject
    def __init__(self, config: FetchTicketsPipeConfig, ticket_system: TicketSystemService):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(
        self, context: PipelineContext, config: FetchTicketsPipeModel
    ) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")

        if not config.ticket_search_criteria:
            error_msg = "No search criteria provided for fetch operation"
            self._logger.error(error_msg)
            return {"_status": "error", "_error": error_msg}

        search_criteria = self._convert_to_search_criteria(config.ticket_search_criteria)
        tickets = await self.ticket_system.find_tickets(search_criteria)

        if not tickets:
            return {"found_tickets": []}

        self._logger.info(f"Found {len(tickets)} tickets")
        return {"found_tickets": [ticket.model_dump() for ticket in tickets]}

    def _convert_to_search_criteria(
        self, criteria: dict[str, Any] | TicketSearchCriteria
    ) -> TicketSearchCriteria:
        if isinstance(criteria, TicketSearchCriteria):
            return criteria
        return TicketSearchCriteria(**criteria)
