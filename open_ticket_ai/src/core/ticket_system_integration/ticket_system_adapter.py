# FILE_PATH: open_ticket_ai\src\ce\ticket_system_integration\ticket_system_adapter.py
from abc import ABC, abstractmethod

from .unified_models import (
    TicketSearchCriteria,
    UnifiedTicket, UnifiedNote, )


class TicketSystemAdapter(ABC):

    @abstractmethod
    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        pass

    @abstractmethod
    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        pass

    @abstractmethod
    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        pass

    @abstractmethod
    async def add_note_to_ticket(self, ticket_id: str, note: UnifiedNote) -> bool:
        pass
