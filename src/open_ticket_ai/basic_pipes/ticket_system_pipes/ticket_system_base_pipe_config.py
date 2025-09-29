from open_ticket_ai.core.pipeline.base_pipe_config import RenderedPipeConfig, RawPipeConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService


class RenderedTicketSystemBasePipeConfig(RenderedPipeConfig):
    ticket_system: TicketSystemService


class RawTicketSystemBasePipeConfig(RawPipeConfig):
    ticket_system: str
