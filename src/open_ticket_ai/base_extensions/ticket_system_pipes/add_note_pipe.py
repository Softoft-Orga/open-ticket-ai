from typing import Any

from injector import inject

from open_ticket_ai.base_extensions.pipe_configs import AddNotePipeConfig, AddNotePipeModel
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService


class AddNotePipe(Pipe[AddNotePipeModel]):
    """
    A pipe that adds a note to an existing ticket in the ticket system.
    """

    @inject
    def __init__(self, config: AddNotePipeConfig, ticket_system: TicketSystemService):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(self, context: PipelineContext, config: AddNotePipeModel) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")

        if not config.ticket_id:
            error_msg = "No ticket ID provided for add note operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        if not config.note:
            error_msg = "No note content provided for add note operation"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}

        try:
            self._logger.info(f"Adding note to ticket {config.ticket_id}: {config.note}")
            await self.ticket_system.add_note(config.ticket_id, config.note)
            self._logger.info("Note added successfully")
            return {"success": True}
        except Exception as e:
            error_msg = f"Failed to add note to ticket: {str(e)}"
            self._logger.error(error_msg)
            return {"success": False, "error": error_msg}
