from typing import Any

from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria
from open_ticket_ai.base_extensions.pipe_implementations.pipe_configs import FetchTicketsPipeConfig


class FetchTicketsPipe(Pipe[FetchTicketsPipeConfig]):
    ConfigModel = FetchTicketsPipeConfig

    def __init__(self, config: FetchTicketsPipeConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(self, context: PipelineContext) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")

        if not self.config.ticket_search_criteria:
            error_msg = "No search criteria provided for fetch operation"
            self._logger.error(error_msg)
            return {"_status": "error", "_error": error_msg}

        search_criteria = self._convert_to_search_criteria(self.config.ticket_search_criteria)
        tickets = await self.ticket_system.find_tickets(search_criteria)

        if not tickets:
            return {"found_tickets": []}

        self._logger.info("Found %d tickets", len(tickets))
        return {"found_tickets": [ticket.model_dump() for ticket in tickets]}

    def _convert_to_search_criteria(self, criteria_dict: dict[str, Any] | TicketSearchCriteria) -> TicketSearchCriteria:
        if isinstance(criteria_dict, TicketSearchCriteria):
            return criteria_dict
        return TicketSearchCriteria(**criteria_dict)
