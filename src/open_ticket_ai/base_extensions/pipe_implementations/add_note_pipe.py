from typing import Any

from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.base_extensions.pipe_implementations.pipe_configs import AddNotePipeConfig


class AddNotePipe(Pipe[AddNotePipeConfig]):
    """
    A pipe that adds a note to an existing ticket in the ticket system.
    """

    ConfigModel = AddNotePipeConfig

    def __init__(self, config: AddNotePipeConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(self, context: PipelineContext) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")

        if not self.config.ticket_id:
            error_msg = "No ticket ID provided for add note operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not self.config.note:
            error_msg = "No note content provided for add note operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            self._logger.info("Adding note to ticket %s: %s", self.config.ticket_id, self.config.note)
            await self.ticket_system.add_note(self.config.ticket_id, self.config.note)
            self._logger.info("Note added successfully")
            return {"success": True}
        except Exception as e:
            error_msg = f"Failed to add note to ticket: {str(e)}"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}
