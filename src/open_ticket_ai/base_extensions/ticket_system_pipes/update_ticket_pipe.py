from typing import Any

from injector import inject

from open_ticket_ai.base_extensions.pipe_configs import (
    UpdateTicketPipeConfig,
    UpdateTicketPipeModel,
)
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketPipe(Pipe[UpdateTicketPipeModel]):
    """
    A pipe that updates an existing ticket in the ticket system.
    """

    @inject
    def __init__(self, config: UpdateTicketPipeConfig, ticket_system: TicketSystemService):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(
        self, context: PipelineContext, config: UpdateTicketPipeModel
    ) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")

        if not config.ticket_id:
            error_msg = "No ticket ID provided for update operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not config.ticket:
            error_msg = "No ticket data provided for update operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            ticket_update = self._convert_to_unified_ticket(config.ticket)
            self._logger.info(f"Updating ticket: {ticket_update}")
            await self.ticket_system.update_ticket(config.ticket_id, ticket_update)
            self._logger.info("Ticket updated successfully")
            return {"success": True}
        except Exception as e:
            error_msg = f"Failed to update ticket: {str(e)}"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def _convert_to_unified_ticket(self, ticket_dict: dict[str, Any]) -> UnifiedTicket:
        return UnifiedTicket(**ticket_dict)
