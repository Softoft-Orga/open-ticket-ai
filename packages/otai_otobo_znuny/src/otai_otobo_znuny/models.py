from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket  # type: ignore[import-untyped]


def _to_unified_entity(id_name: IdName | None) -> UnifiedEntity | None:
    if id_name is None:
        return None
    return UnifiedEntity(
        id=str(id_name.id),
        name=id_name.name,
    )


def otobo_article_to_unified_note(article: Article) -> UnifiedNote:
    return UnifiedNote(
        body=article.body or "",
        subject=article.subject,
    )


def otobo_ticket_to_unified_ticket(ticket: Ticket) -> UnifiedTicket:
    return UnifiedTicket(
        id=str(ticket.id) if ticket.id is not None else "",
        subject=ticket.title or "",
        queue=_to_unified_entity(ticket.queue),
        priority=_to_unified_entity(ticket.priority),
        notes=[otobo_article_to_unified_note(a) for a in ticket.articles or []],
        body=ticket.articles[0].body if ticket.articles else "",
    )
