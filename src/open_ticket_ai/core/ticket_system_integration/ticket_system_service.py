from typing import Any

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class TicketSystemService(Injectable):
    """Base contract for ticket system integrations.

    Implementations provide coroutine methods that operate on
    :class:`~open_ticket_ai.core.ticket_system_integration.unified_models.UnifiedTicket`
    data while remaining flexible enough to accept platform-specific keyword
    arguments. Each method accepts ``**kwargs`` so adapters can surface the
    parameters required by the upstream SDK, yet they must always return unified
    models to keep downstream templates and configuration portable across ticket
    systems.

    Adapters are responsible for translating between their native models and the
    unified representations exposed here.
    """

    async def create_ticket(
        self,
        ticket: UnifiedTicket | None = None,
        **kwargs: Any,
    ) -> UnifiedTicket:  # pragma: no cover - interface contract
        raise NotImplementedError("Ticket system adapters must implement 'create_ticket'.")

    async def update_ticket(
        self,
        ticket_id: str,
        updates: UnifiedTicket | None = None,
        **kwargs: Any,
    ) -> bool:  # pragma: no cover - interface contract
        raise NotImplementedError("Ticket system adapters must implement 'update_ticket'.")

    async def find_tickets(
        self,
        criteria: TicketSearchCriteria | None = None,
        **kwargs: Any,
    ) -> list[UnifiedTicket]:  # pragma: no cover - interface contract
        raise NotImplementedError("Ticket system adapters must implement 'find_tickets'.")

    async def find_first_ticket(
        self,
        criteria: TicketSearchCriteria | None = None,
        **kwargs: Any,
    ) -> UnifiedTicket | None:  # pragma: no cover - interface contract
        raise NotImplementedError("Ticket system adapters must implement 'find_first_ticket'.")

    async def get_ticket(
        self,
        ticket_id: str,
    ) -> UnifiedTicket | None:  # pragma: no cover - interface contract
        raise NotImplementedError("Ticket system adapters must implement 'get_ticket'.")

    async def add_note(
        self,
        ticket_id: str,
        note: UnifiedNote | None = None,
        **kwargs: Any,
    ) -> bool:  # pragma: no cover - interface contract
        raise NotImplementedError("Ticket system adapters must implement 'add_note'.")
