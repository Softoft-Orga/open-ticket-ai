from typing import Any

from injector import inject

from open_ticket_ai.basic_pipes.pipe_configs import RawTicketAddNotePipeConfig
from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService


class AddNotePipe(BasePipe[RawTicketAddNotePipeConfig]):
    """
    A pipe that adds a note to an existing ticket in the ticket system.
    """

    @staticmethod
    def get_raw_config_model_type() -> type[RawPipeConfig]:
        return RawTicketAddNotePipeConfig

    @inject
    def __init__(self, config: RawTicketAddNotePipeConfig, ticket_system: TicketSystemService):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(self) -> dict[str, Any]:
        await self.ticket_system.add_note(self.config.ticket_id, self.config.note)
        self._logger.info("Note added successfully")
        return {}
