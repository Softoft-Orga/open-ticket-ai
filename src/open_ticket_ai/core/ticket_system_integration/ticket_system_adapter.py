from abc import ABC, abstractmethod

from ..config.registerable import RegisterableClass, RawRegisterableConfig, RenderedRegistrableConfig
from .unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class TicketSystemService[RawConfigT: RawRegisterableConfig, RenderedConfigT: RenderedRegistrableConfig](
    RegisterableClass[RawConfigT, RenderedConfigT], ABC
):
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
