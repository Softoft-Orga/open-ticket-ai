from __future__ import annotations

from typing import Any, ClassVar

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)


class MockedTicketSystem(TicketSystemService):
    ParamsModel: ClassVar[type[StrictBaseModel]] = StrictBaseModel
    _tickets: ClassVar[dict[str, UnifiedTicket]] = {}

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    async def create_ticket(self, ticket: UnifiedTicket) -> str:
        if ticket.id is None:
            raise RuntimeError("Ticket id is required")
        self._tickets[ticket.id] = ticket
        return ticket.id

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        if ticket_id not in self._tickets:
            return False

        existing_ticket = self._tickets[ticket_id]
        update_data = updates.model_dump(exclude_unset=True, exclude_none=True)
        self._tickets[ticket_id] = UnifiedTicket.model_validate(existing_ticket.model_dump() | update_data)
        return True

    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        ticket = self._tickets.get(ticket_id)
        return ticket.model_copy(deep=True) if ticket else None

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        results = [
            ticket.model_copy(deep=True)
            for ticket in self._tickets.values()
            if self._matches_criteria(ticket, criteria)
        ]
        return results[criteria.offset : criteria.offset + criteria.limit]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        for ticket in self._tickets.values():
            if self._matches_criteria(ticket, criteria):
                return ticket.model_copy(deep=True)
        return None

    async def add_note(self, ticket_id: str | int, note: UnifiedNote) -> bool:
        ticket_id_str = str(ticket_id)

        if ticket_id_str not in self._tickets:
            return False

        ticket = self._tickets[ticket_id_str]

        if ticket.notes is None:
            ticket.notes = []

        note_id = note.id or "note-" + str(len(ticket.notes) + 1)
        note_copy = note.model_copy(update={"id": note_id})
        ticket.notes.append(note_copy)
        return True

    def _matches_criteria(self, ticket: UnifiedTicket, criteria: TicketSearchCriteria) -> bool:
        if criteria.queue is not None:
            if ticket.queue is None:
                return False
            if criteria.queue.id is not None and ticket.queue.id != criteria.queue.id:
                return False
            if criteria.queue.name is not None and ticket.queue.name != criteria.queue.name:
                return False

        return True

    def add_test_ticket(self, **kwargs: Any) -> str:
        ticket = UnifiedTicket(**kwargs)
        if ticket.id is None:
            raise RuntimeError("Ticket id is required")
        self._tickets[ticket.id] = ticket
        return ticket.id

    def get_all_tickets(self) -> list[UnifiedTicket]:
        return [ticket.model_copy(deep=True) for ticket in self._tickets.values()]

    def clear_all_data(self) -> None:
        self._tickets.clear()

    def get_ticket_count(self) -> int:
        return len(self._tickets)
