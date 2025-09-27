import logging
from typing import Any, Dict

from open_ticket_ai.core.pipeline.base_pipe_state import BasePipeState
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicket,
)
from open_ticket_ai.extensions.pipe_implementations.pipe_configs import TicketSystemServiceConfig


class TicketSystemService(Pipe[TicketSystemServiceConfig, BasePipeState]):
    ConfigModel = TicketSystemServiceConfig

    def __init__(self, config: TicketSystemServiceConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(self.__class__.__name__)

    async def _process(self, rendered_config: TicketSystemServiceConfig) -> Dict[str, Any]:
        self.logger.info(f"Running {self.__class__.__name__}")
        operation = rendered_config.operation.lower()

        if operation == "find":
            return await self._handle_find_operation(rendered_config)
        elif operation == "update":
            return await self._handle_update_operation(rendered_config)
        else:
            error_msg = f"Unsupported operation: {operation}"
            self.logger.error(error_msg)
            return {"_status": "error", "_error": error_msg, "_failed_pipe": self.__class__.__name__}

    async def _handle_find_operation(self, config: TicketSystemServiceConfig) -> Dict[str, Any]:
        if not config.ticket_search_criteria:
            error_msg = "No search criteria provided for find operation"
            self.logger.error(error_msg)
            return {"_status": "error", "_error": error_msg}

        search_criteria = self._convert_to_search_criteria(config.ticket_search_criteria)
        tickets = await self.ticket_system.find_tickets(search_criteria)

        if not tickets:
            return {"found_tickets": []}
        self.logger.info("Found %d tickets", len(tickets))
        return {"found_tickets": [ticket.model_dump() for ticket in tickets]}

    async def _handle_update_operation(self, config: TicketSystemServiceConfig) -> Dict[str, Any]:
        if not config.ticket_id:
            error_msg = "No ticket ID provided for update operation"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not config.ticket:
            error_msg = "No ticket data provided for update operation"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            ticket_update = self._convert_to_unified_ticket(config.ticket)
            self.logger.info("Updating ticket: %s", ticket_update)
            await self.ticket_system.update_ticket(config.ticket_id, ticket_update)
            self.logger.info("Ticket updated successfully")
            return {"success": True}
        except Exception as e:
            error_msg = f"Failed to update ticket: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def _convert_to_search_criteria(self, criteria_dict: Dict[str, Any] | TicketSearchCriteria) -> TicketSearchCriteria:
        return TicketSearchCriteria(**criteria_dict)

    def _convert_to_unified_ticket(self, ticket_dict: Dict[str, Any]) -> UnifiedTicket:
        return UnifiedTicket(**ticket_dict)
