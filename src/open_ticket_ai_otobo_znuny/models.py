from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket

from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)


def _to_unified_entity(id_name: IdName | None) -> UnifiedEntity | None:
    if id_name is None:
        return None
    return UnifiedEntity(
        id=id_name.id,
        name=id_name.name,
    )


class NoteAdapter(UnifiedNote):
    def __init__(self, article: Article):
        super().__init__(
            body=article.body or "",
            subject=article.subject,
        )


class TicketAdapter(UnifiedTicket):
    def __init__(self, ticket: Ticket):
        super().__init__(
            id=str(ticket.id) if ticket.id is not None else "",
            subject=ticket.title or "",
            body=self._get_unified_body(ticket),
            queue=_to_unified_entity(ticket.queue),
            priority=_to_unified_entity(ticket.priority),
            notes=self._get_unified_notes_list(ticket),
        )

    def _get_unified_body(self, ticket: Ticket) -> str:
        notes = self._get_unified_notes_list(ticket)
        return notes[0].body if notes else ""

    def _get_unified_notes_list(self, ticket: Ticket) -> list[UnifiedNote]:
        return [NoteAdapter(a) for a in self._articles_as_list(ticket)]

    def _articles_as_list(self, ticket: Ticket) -> list[Article]:
        return ticket.articles or []
