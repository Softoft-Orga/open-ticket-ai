from typing import Any

from open_ticket_ai.basic_pipes.ticket_system_pipes.ticket_system_base_pipe_config import (
    RawTicketSystemBasePipeConfig,
    RenderedTicketSystemBasePipeConfig,
)
from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class RenderedTicketAddNotePipeConfig(RenderedTicketSystemBasePipeConfig):
    ticket_id: str | int
    note: UnifiedNote


class RawTicketAddNotePipeConfig(RawTicketSystemBasePipeConfig):
    ticket_id: str | int
    note: str | UnifiedNote | dict[str, Any]


class AddNotePipe(ConfigurablePipe[RawTicketAddNotePipeConfig, RenderedTicketAddNotePipeConfig]):
    async def _process(self) -> dict[str, Any]:
        await self.config.ticket_system.add_note(self.config.ticket_id, self.config.note)
        return {}
