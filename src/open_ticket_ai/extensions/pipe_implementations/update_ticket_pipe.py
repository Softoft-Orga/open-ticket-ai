import logging
from typing import Any, Dict

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket
from open_ticket_ai.extensions.pipe_implementations.pipe_configs import UpdateTicketPipeConfig


class UpdateTicketPipe(Pipe[UpdateTicketPipeConfig]):
    """
    A pipe that updates an existing ticket in the ticket system.
    """
    
    ConfigModel = UpdateTicketPipeConfig

    def __init__(self, config: UpdateTicketPipeConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(self, context: PipelineContext) -> Dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")
        
        if not self.config.ticket_id:
            error_msg = "No ticket ID provided for update operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not self.config.ticket:
            error_msg = "No ticket data provided for update operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            ticket_update = self._convert_to_unified_ticket(self.config.ticket)
            self._logger.info("Updating ticket: %s", ticket_update)
            await self.ticket_system.update_ticket(self.config.ticket_id, ticket_update)
            self._logger.info("Ticket updated successfully")
            return {"success": True}
        except Exception as e:
            error_msg = f"Failed to update ticket: {str(e)}"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def _convert_to_unified_ticket(self, ticket_dict: Dict[str, Any]) -> UnifiedTicket:
        return UnifiedTicket(**ticket_dict)
