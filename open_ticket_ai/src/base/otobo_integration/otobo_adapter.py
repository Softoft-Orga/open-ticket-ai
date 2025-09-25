import logging

from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import TicketSearch, IdName, Ticket, Article, TicketUpdate

from open_ticket_ai.src.base.otobo_integration.models import TicketAdapter
from open_ticket_ai.src.core.config.config_models import OTOBOAdapterConfig
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicket,
    UnifiedTicketBase, UnifiedNote, UnifiedEntity,
)


def _to_id_name(entity: UnifiedEntity | None) -> IdName | None:
    if entity is None:
        return None
    return IdName(
        id=entity.id,
        name=entity.name,
    )


class OTOBOAdapter(TicketSystemAdapter):
    @inject
    def __init__(self, config: OTOBOAdapterConfig, otobo_client: OTOBOZnunyClient):
        self.config = config
        self.otobo_client = otobo_client
        self.logger = logging.getLogger(self.__class__.__name__)

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        search = TicketSearch(
            queues=[
                _to_id_name(criteria.queue)
            ]
            if criteria.queue
            else None,
            limit=criteria.limit
        )
        self.logger.debug("OTOBO search criteria: %s", search)
        tickets: list[Ticket] = await self.otobo_client.search_and_get(search)
        logging.info("OTOBO search returned %d tickets", len(tickets))
        return [TicketAdapter(t) for t in tickets]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        items = await self.find_tickets(criteria)
        return items[0] if items else None

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicketBase) -> bool:
        ticket = TicketUpdate(
            id=int(ticket_id),
            title=updates.subject,
            queue=_to_id_name(updates.queue),
            priority=_to_id_name(updates.priority),
            article=Article(subject=updates.note.subject, body=updates.note.body)
        )
        logging.info(ticket)
        await self.otobo_client.update_ticket(ticket)
        return True
