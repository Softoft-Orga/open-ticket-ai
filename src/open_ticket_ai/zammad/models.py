from __future__ import annotations

from typing import Any

from pydantic import AnyHttpUrl, ConfigDict, Field, SecretStr

from open_ticket_ai import StrictBaseModel
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)


class ZammadTSServiceParams(StrictBaseModel):
    base_url: AnyHttpUrl = Field(description="Base URL of the Zammad instance for API requests.")
    access_token: SecretStr = Field(description="Personal access token used for authenticating against Zammad API.")
    timeout: float | None = Field(
        default=None,
        gt=0,
        description="Optional request timeout (in seconds) applied to HTTP requests.",
    )
    verify: bool | str = Field(
        default=True,
        description="TLS verification flag or path to CA bundle used for HTTPS requests.",
    )

    def auth_header(self) -> str:
        return f"Token token={self.access_token.get_secret_value()}"


class ZammadArticle(StrictBaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int | None = None
    subject: str | None = None
    body: str | None = None
    type: str | None = None
    content_type: str | None = None
    internal: bool | None = None


class ZammadTicket(StrictBaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    title: str | None = None
    group: str | None = None
    priority: str | None = None
    state: str | None = None
    article_ids: list[int] | None = None
    articles: list[ZammadArticle] | None = None


class ZammadArticleCreate(StrictBaseModel):
    ticket_id: int | None = None
    subject: str = ""
    body: str = ""
    type: str = "note"
    content_type: str = "text/plain"
    internal: bool = False


class ZammadTicketCreate(StrictBaseModel):
    title: str
    group: str | None = None
    priority: str | None = None
    article: ZammadArticleCreate
    customer: str | None = None


class ZammadTicketUpdate(StrictBaseModel):
    title: str | None = None
    group: str | None = None
    priority: str | None = None

    def has_updates(self) -> bool:
        return any(value is not None for value in self.model_dump().values())


def _value_from_unified_entity(entity: UnifiedEntity | None) -> str | None:
    if entity is None:
        return None
    if entity.name:
        return entity.name
    return entity.id


def _unified_entity_from_value(value: str | None) -> UnifiedEntity | None:
    if not value:
        return None
    return UnifiedEntity(id=value, name=value)


def zammad_article_to_unified_note(article: ZammadArticle) -> UnifiedNote:
    return UnifiedNote(
        id=str(article.id) if article.id is not None else None,
        subject=article.subject or "",
        body=article.body or "",
    )


def zammad_ticket_to_unified_ticket(ticket: ZammadTicket) -> UnifiedTicket:
    notes = [zammad_article_to_unified_note(article) for article in ticket.articles or []]
    body = notes[0].body if notes else ""
    return UnifiedTicket(
        id=str(ticket.id),
        subject=ticket.title or "",
        queue=_unified_entity_from_value(ticket.group),
        priority=_unified_entity_from_value(ticket.priority),
        notes=notes,
        body=body,
    )


def unified_note_to_zammad_article(note: UnifiedNote, ticket_id: int | None = None) -> ZammadArticleCreate:
    return ZammadArticleCreate(
        ticket_id=ticket_id,
        subject=note.subject or "",
        body=note.body or "",
    )


def unified_ticket_to_zammad_create(ticket: UnifiedTicket) -> ZammadTicketCreate:
    article = UnifiedNote(subject=ticket.subject or "", body=ticket.body or "")
    return ZammadTicketCreate(
        title=ticket.subject or "",
        group=_value_from_unified_entity(ticket.queue),
        priority=_value_from_unified_entity(ticket.priority),
        article=unified_note_to_zammad_article(article),
        customer=_value_from_unified_entity(ticket.customer),
    )


def unified_ticket_to_zammad_update(ticket: UnifiedTicket) -> ZammadTicketUpdate:
    return ZammadTicketUpdate(
        title=ticket.subject,
        group=_value_from_unified_entity(ticket.queue),
        priority=_value_from_unified_entity(ticket.priority),
    )


def merge_ticket_with_articles(ticket: ZammadTicket, articles: list[ZammadArticle] | None) -> ZammadTicket:
    payload: dict[str, Any] = {}
    if articles is not None:
        payload["articles"] = articles
    if not payload:
        return ticket
    return ticket.model_copy(update=payload)
