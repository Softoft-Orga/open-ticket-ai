from typing import Self

from otobo.domain_models.ticket_models import Ticket, Article
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    UnifiedNote,
    UnifiedPriority,
    UnifiedQueue,
    UnifiedTicket,
)


class QueueAdapter(UnifiedQueue):
    @classmethod
    def from_ticket(cls, ticket: Ticket) -> Self:
        q = ticket.queue
        return cls(
            id=str(q.id) if q and q.id is not None else None,
            name=q.name if q and q.name else "",
        )


class PriorityAdapter(UnifiedPriority):
    @classmethod
    def from_ticket(cls, ticket: Ticket) -> Self:
        p = ticket.priority
        return cls(
            id=str(p.id) if p and p.id is not None else None,
            name=p.name if p and p.name else "",
        )


class NoteAdapter(UnifiedNote):
    def __init__(self, article: Article):
        super().__init__(
            body=article.body or "",
            subject=article.subject or "",
        )


class TicketAdapter(UnifiedTicket):
    def __init__(self, ticket: Ticket):
        super().__init__(
            id=str(ticket.id) if ticket.id is not None else "",
            subject=ticket.title or "",
            body=self._get_unified_body(ticket),
            queue=QueueAdapter.from_ticket(ticket),
            priority=PriorityAdapter.from_ticket(ticket),
            notes=self._get_unified_notes_list(ticket),
        )

    def _get_unified_body(self, ticket: Ticket) -> str:
        notes = self._get_unified_notes_list(ticket)
        return notes[0].body if notes else ""

    def _get_unified_notes_list(self, ticket: Ticket) -> list[UnifiedNote]:
        return [NoteAdapter(a) for a in self._articles_as_list(ticket)]

    def _articles_as_list(self, ticket: Ticket) -> list[Article]:
        return ticket.articles or []
