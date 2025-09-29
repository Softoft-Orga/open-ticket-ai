import logging

from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket, TicketSearch, TicketUpdate

from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from open_ticket_ai.otobo_znuny.models import otobo_ticket_to_unified_ticket
from open_ticket_ai.otobo_znuny.otobo_znuny_ticket_system_service_config import (
    RenderedOTOBOZnunyTicketsystemServiceConfig,
)


def _to_id_name(entity: UnifiedEntity | None) -> IdName | None:
    if entity is None:
        return None
    return IdName(
        id=entity.id,
        name=entity.name,
    )


class OTOBOZnunyTicketSystemService(TicketSystemService):
    @inject
    def __init__(self, config: RenderedOTOBOZnunyTicketsystemServiceConfig, ):
        super().__init__(config)
        self.config = config
        self._client: OTOBOZnunyClient | None = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def client(self) -> OTOBOZnunyClient:
        if self._client is None:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        return self._client

    async def _recreate_client(self) -> OTOBOZnunyClient:
        self._client = OTOBOZnunyClient(config=self.config.to_client_config())
        self.logger.info("Recreated OTOBO client")
        self._client.login(self.config.get_basic_auth())
        return self._client

    async def initialize(self) -> None:
        await self._recreate_client()

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        search = TicketSearch(queues=[_to_id_name(criteria.queue)] if criteria.queue else None, limit=criteria.limit)
        self.logger.debug("OTOBO search criteria: %s", search)
        tickets: list[Ticket] = await self.client.search_and_get(search)
        self.logger.info("OTOBO search returned %d tickets", len(tickets))
        return [otobo_ticket_to_unified_ticket(t) for t in tickets]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        items = await self.find_tickets(criteria)
        return items[0] if items else None

    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        return otobo_ticket_to_unified_ticket(await self.client.get_ticket(int(ticket_id)))

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        ticket = TicketUpdate(
            id=int(ticket_id),
            title=updates.subject,
            queue=_to_id_name(updates.queue),
            priority=_to_id_name(updates.priority),
            article=Article(subject=updates.notes[-1].subject, body=updates.notes[-1].body),
        )
        logging.info(ticket)
        await self.client.update_ticket(ticket)
        return True

    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        return await self.update_ticket(ticket_id,
                                        UnifiedTicket(notes=[UnifiedNote(subject=note.subject, body=note.body)]))
