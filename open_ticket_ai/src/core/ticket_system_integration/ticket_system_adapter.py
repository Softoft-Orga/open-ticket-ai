# FILE_PATH: open_ticket_ai\src\ce\ticket_system_integration\ticket_system_adapter.py
from abc import ABC, abstractmethod

from injector import inject

from .unified_models import (
    TicketSearchCriteria,
    UnifiedTicket, )


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
