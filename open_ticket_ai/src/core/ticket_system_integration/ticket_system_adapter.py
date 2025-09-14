"""Abstract adapter for ticket system integrations.

Concrete adapters implement the asynchronous methods defined here to interact
with a specific ticket system (e.g. OTOBO).  The interface is intentionally
minimal so that higher level components can operate on a unified set of
operations regardless of the underlying system.
"""
from abc import ABC, abstractmethod
from injector import inject

from open_ticket_ai.src.core.config.config_models import SystemConfig
from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable
from .unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
    UnifiedTicketUpdate,
)


class TicketSystemAdapter(Providable, ABC):
    """Base class for all ticket system adapters."""

    @inject
    def __init__(self, config: SystemConfig | None):
        super().__init__(config)
        self.config = config

    # ------------------------------------------------------------------
    # CRUD like operations
    # ------------------------------------------------------------------
    @abstractmethod
    async def create_ticket(self, ticket_data: UnifiedTicket) -> UnifiedTicket:
        """Create a new ticket in the external system."""
        raise NotImplementedError

    @abstractmethod
    async def update_ticket(self, ticket_id: str, updates: UnifiedTicketUpdate) -> bool:
        """Update an existing ticket and return ``True`` on success."""
        raise NotImplementedError

    @abstractmethod
    async def add_note(self, ticket_id: str, note: UnifiedNote) -> UnifiedNote:
        """Attach a note to an existing ticket."""
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Search operations
    # ------------------------------------------------------------------
    @abstractmethod
    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        """Return all tickets matching ``criteria``."""
        raise NotImplementedError

    @abstractmethod
    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        """Return the first ticket matching ``criteria`` or ``None``."""
        raise NotImplementedError
