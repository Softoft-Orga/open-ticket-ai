from abc import ABC

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService


class TicketSystemPipe(Pipe, ABC):
    def __init__(self, pipe_id: str, ticket_system: TicketSystemService) -> None:
        super().__init__(pipe_id)
        self._ticket_system = ticket_system
