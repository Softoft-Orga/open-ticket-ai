"""In-memory mocked ticket system for testing."""

from __future__ import annotations

import asyncio
from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class MockedTicketSystem(TicketSystemService):
    """In-memory ticket system mock that maintains state with ticket objects.

    Provides realistic, stateful testing without external dependencies.
    Maintains tickets and notes as dict objects in memory.
    """

    def __init__(self, config: dict[str, Any] | BaseModel, *args, **kwargs) -> None:
        super().__init__(config, *args, **kwargs)
        self._tickets: dict[str, UnifiedTicket] = {}
        self._ticket_counter: int = 1

    async def create_ticket(self, ticket: UnifiedTicket) -> str:
        """Create a new ticket and return its ID."""
        ticket_id = ticket.id or f"TICKET-{self._ticket_counter}"
        self._ticket_counter += 1

        # Deep copy to avoid external mutations
        ticket_copy = ticket.model_copy(deep=True)
        ticket_copy.id = ticket_id

        # Initialize notes list if not present
        if ticket_copy.notes is None:
            ticket_copy.notes = []

        self._tickets[ticket_id] = ticket_copy
        return ticket_id

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        """Update an existing ticket with new values."""
        if ticket_id not in self._tickets:
            return False

        existing_ticket = self._tickets[ticket_id]

        # Update only provided fields (non-None values)
        update_data = updates.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            if field != "id":  # Don't allow ID changes
                setattr(existing_ticket, field, value)

        return True

    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        """Get a ticket by ID."""
        ticket = self._tickets.get(ticket_id)
        return ticket.model_copy(deep=True) if ticket else None

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        """Find tickets matching the search criteria."""
        results = [
            ticket.model_copy(deep=True)
            for ticket in self._tickets.values()
            if self._matches_criteria(ticket, criteria)
        ]

        # Apply pagination
        offset = criteria.offset or 0
        limit = criteria.limit or 10
        return results[offset : offset + limit]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        """Find the first ticket matching the criteria."""
        for ticket in self._tickets.values():
            if self._matches_criteria(ticket, criteria):
                return ticket.model_copy(deep=True)
        return None

    async def add_note(self, ticket_id: str | int, note: UnifiedNote) -> bool:
        """Add a note to a ticket."""
        ticket_id_str = str(ticket_id)

        if ticket_id_str not in self._tickets:
            return False

        ticket = self._tickets[ticket_id_str]

        # Initialize notes list if not present
        if ticket.notes is None:
            ticket.notes = []

        # Assign note ID if not present
        note_copy = note.model_copy(deep=True)
        if note_copy.id is None:
            note_copy.id = f"NOTE-{len(ticket.notes) + 1}"

        ticket.notes.append(note_copy)
        return True

    def _matches_criteria(self, ticket: UnifiedTicket, criteria: TicketSearchCriteria) -> bool:
        """Check if a ticket matches the search criteria."""
        # Check queue
        if criteria.queue is not None:
            if ticket.queue is None:
                return False
            if criteria.queue.id is not None and ticket.queue.id != criteria.queue.id:
                return False
            if criteria.queue.name is not None and ticket.queue.name != criteria.queue.name:
                return False

        return True

    # Utility methods for testing

    def add_test_ticket(self, **kwargs) -> str:
        """Add a test ticket with provided fields. Returns ticket ID."""
        ticket = UnifiedTicket(**kwargs)

        return asyncio.run(self.create_ticket(ticket))

    def get_all_tickets(self) -> list[UnifiedTicket]:
        """Get all tickets in the system."""
        return [ticket.model_copy(deep=True) for ticket in self._tickets.values()]

    def clear_all_data(self) -> None:
        """Clear all tickets from the system."""
        self._tickets.clear()
        self._ticket_counter = 1

    def get_ticket_count(self) -> int:
        """Get the total number of tickets."""
        return len(self._tickets)
