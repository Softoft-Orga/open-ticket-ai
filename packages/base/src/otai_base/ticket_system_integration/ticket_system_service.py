from abc import ABC, abstractmethod

from open_ticket_ai.core.injectables.injectable import Injectable

from .unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class TicketSystemService(Injectable, ABC):
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
    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        pass
