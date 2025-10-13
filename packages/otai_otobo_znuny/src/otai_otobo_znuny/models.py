from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket  # type: ignore[import-untyped]
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import BaseModel, SecretStr


def _to_unified_entity(id_name: IdName | None) -> UnifiedEntity | None:
    if id_name is None:
        return None
    return UnifiedEntity(
        id=str(id_name.id),
        name=id_name.name,
    )


def unified_entity_to_id_name(unified_entity: UnifiedEntity) -> IdName:
    return IdName(
        id=unified_entity.id,
        name=unified_entity.name,
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


class RenderedOTOBOZnunyTicketsystemServiceConfig(BaseModel):
    password: SecretStr
    base_url: str
    username: str = "open_ticket_ai"
    webservice_name: str = "OpenTicketAI"
    operation_urls: dict[str, str] = {
        TicketOperation.SEARCH.value: "ticket-search",
        TicketOperation.GET.value: "ticket-get",
        TicketOperation.UPDATE.value: "ticket-update",
    }

    @property
    def operation_url_map(self) -> dict[TicketOperation, str]:
        return {TicketOperation(key): value for key, value in self.operation_urls.items()}

    def get_basic_auth(self) -> BasicAuth:
        return BasicAuth(user_login=self.username, password=self.password)

    def to_client_config(self) -> ClientConfig:
        return ClientConfig(
            base_url=self.base_url,
            webservice_name=self.webservice_name,
            operation_url_map=self.operation_url_map,
        )
