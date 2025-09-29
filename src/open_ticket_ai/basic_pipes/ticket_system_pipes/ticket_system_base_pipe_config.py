from pydantic import ConfigDict

from open_ticket_ai.core.pipeline.configurable_pipe_config import RawPipeConfig, RenderedPipeConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService


class RenderedTicketSystemBasePipeConfig(RenderedPipeConfig):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ticket_system: TicketSystemService


class RawTicketSystemBasePipeConfig(RawPipeConfig):
    ticket_system: str
