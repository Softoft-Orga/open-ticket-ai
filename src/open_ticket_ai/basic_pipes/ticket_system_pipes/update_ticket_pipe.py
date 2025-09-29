from typing import Any

from open_ticket_ai.basic_pipes.ticket_system_pipes.ticket_system_base_pipe_config import (
    RawTicketSystemBasePipeConfig,
    RenderedTicketSystemBasePipeConfig,
)
from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicketBase


class RenderedTicketUpdatePipeConfig(RenderedTicketSystemBasePipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicketBase


class RawTicketUpdatePipeConfig(RawTicketSystemBasePipeConfig):
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicketBase


class UpdateTicketPipe(ConfigurablePipe[RawTicketUpdatePipeConfig, RenderedTicketUpdatePipeConfig]):
    async def _process(self) -> dict[str, Any]:
        await self.config.ticket_system.update_ticket(self.config.ticket_id, self.config.updated_ticket)
        return {}
