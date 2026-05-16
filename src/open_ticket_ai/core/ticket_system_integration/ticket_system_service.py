from abc import ABC
from typing import Any

from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class TicketSystemService(ABC):
    """Base contract for ticket system integrations.

    Implementations provide coroutine methods that operate on unified ticket
    models while remaining flexible enough to accept platform-specific keyword
    arguments.
    """

    async def create_ticket(
        self,
        ticket: UnifiedTicket | None = None,
        **kwargs: Any,
    ) -> UnifiedTicket:
        raise NotImplementedError

    async def update_ticket(
        self,
        ticket_id: str,
        updates: UnifiedTicket | None = None,
        **kwargs: Any,
    ) -> bool:
        raise NotImplementedError

    async def find_tickets(
        self,
        criteria: TicketSearchCriteria | None = None,
        **kwargs: Any,
    ) -> list[UnifiedTicket]:
        raise NotImplementedError

    async def find_first_ticket(
        self,
        criteria: TicketSearchCriteria | None = None,
        **kwargs: Any,
    ) -> UnifiedTicket | None:
        raise NotImplementedError

    async def get_ticket(
        self,
        ticket_id: str,
    ) -> UnifiedTicket | None:
        raise NotImplementedError

    async def add_note(
        self,
        ticket_id: str,
        note: UnifiedNote | None = None,
        **kwargs: Any,
    ) -> bool:
        raise NotImplementedError
