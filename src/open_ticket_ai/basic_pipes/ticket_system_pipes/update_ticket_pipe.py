from typing import Any

from injector import inject

from open_ticket_ai.basic_pipes.ticket_system_pipes.ticket_system_base_pipe_config import \
    RenderedTicketSystemBasePipeConfig, RawTicketSystemBasePipeConfig
from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.pipeline.base_pipe_config import _BasePipeConfig, RenderedPipeConfig, RawPipeConfig, PipeConfig
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket, UnifiedTicketBase


class RenderedTicketUpdatePipeConfig(RenderedTicketSystemBasePipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicketBase


class RawTicketUpdatePipeConfig(RawTicketSystemBasePipeConfig):
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicketBase

class UpdateTicketPipe(BasePipe[RawTicketUpdatePipeConfig, RenderedTicketUpdatePipeConfig]):
    async def _process(self) -> dict[str, Any]:
        await self.config.ticket_system.update_ticket(self.config.ticket_id, self.config.updated_ticket)
        return {}
