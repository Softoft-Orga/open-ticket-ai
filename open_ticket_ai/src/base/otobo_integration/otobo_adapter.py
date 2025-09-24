import logging
from typing import Self

from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import TicketSearch, IdName, Ticket, Article, TicketUpdate

from open_ticket_ai.src.core.config.config_models import OTOBOAdapterConfig
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicket,
    UnifiedTicketBase, UnifiedNote,
)
from open_ticket_ai.src.base.otobo_integration.models import TicketAdapter


class OTOBOAdapter(TicketSystemAdapter):
    @inject
    def __init__(self, config: OTOBOAdapterConfig, otobo_client: OTOBOZnunyClient):
        self.config = config
        self.otobo_client = otobo_client

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        search = TicketSearch(
            queues=[
                IdName(
                    id=int(criteria.queue.id) if criteria.queue and criteria.queue.id else None,
                    name=criteria.queue.name if criteria.queue and criteria.queue.name else None,
                )
            ]
            if getattr(criteria, "queue", None)
            else None,
            limit=criteria.limit
        )
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
            queue=IdName(
                id=int(updates.queue.id) if updates.queue and updates.queue.id else None,
                name=updates.queue.name if updates.queue and updates.queue.name else None,
            )
            if updates.queue
            else None,
            priority=IdName(
                id=int(updates.priority.id) if updates.priority and updates.priority.id else None,
                name=updates.priority.name if updates.priority and updates.priority.name else None,
            )
            if updates.priority
            else None,
        )
        await self.otobo_client.update_ticket(ticket)
        return True

    async def add_note_to_ticket(self, ticket_id: str, note: UnifiedNote) -> bool:
        updated = await self.otobo_client.update_ticket(
            TicketUpdate(
                id=int(ticket_id),
                article=Article(subject=note.subject, body=note.body, content_type="text/plain; charset=utf-8"),
            )
        )
        return True
