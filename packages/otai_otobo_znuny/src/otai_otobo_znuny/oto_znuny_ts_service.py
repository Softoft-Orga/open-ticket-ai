from typing import Any

from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient  # type: ignore[import-untyped]
from otobo_znuny.domain_models.ticket_models import (  # type: ignore[import-untyped]
    Article,
    Ticket,
    TicketSearch,
    TicketUpdate,
)
from otobo_znuny.mappers import _to_id_name  # type: ignore[import-untyped]

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)
from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import (
    otobo_ticket_to_unified_ticket,
    unified_entity_to_id_name, OTOBOZnunyTSConfig,
)


class OTOBOZnunyTicketSystemService(TicketSystemService):
    @inject
    def __init__(
            self,
            config: OTOBOZnunyTSConfig,
            logger_factory: LoggerFactory | None = None,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        super().__init__(config, *args, **kwargs)
        self._config = OTOBOZnunyTSConfig.model_validate(config.model_dump())
        self._client: OTOBOZnunyClient | None = None
        self.logger = logger_factory.get_logger(self.__class__.__name__)
        self.initialize()

    @property
    def client(self) -> OTOBOZnunyClient:
        if self._client is None:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        return self._client

    def _recreate_client(self) -> OTOBOZnunyClient:
        self._client = OTOBOZnunyClient(config=self._config.params.to_client_config())
        self.logger.info("Recreated OTOBO client")
        self.logger.info(self._config.params.get_basic_auth().model_dump(with_secrets=True))
        self._client.login(self._config.params.get_basic_auth())
        return self._client

    def initialize(self) -> None:
        self._recreate_client()

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        search = TicketSearch(queues=[unified_entity_to_id_name(criteria.queue)] if criteria.queue else None,
                              limit=criteria.limit)
        self.logger.debug(f"OTOBO search criteria: {search}")
        tickets: list[Ticket] = await self.client.search_and_get(search)
        self.logger.info(f"OTOBO search returned {len(tickets)} tickets")
        return [otobo_ticket_to_unified_ticket(t) for t in tickets]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        items = await self.find_tickets(criteria)
        return items[0] if items else None

    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        return otobo_ticket_to_unified_ticket(await self.client.get_ticket(int(ticket_id)))

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        article = None
        if updates.notes and len(updates.notes) > 0:
            article = Article(subject=updates.notes[-1].subject, body=updates.notes[-1].body)

        ticket = TicketUpdate(
            id=int(ticket_id),
            title=updates.subject,
            queue=unified_entity_to_id_name(updates.queue),
            priority=unified_entity_to_id_name(updates.priority),
            article=article,
        )
        self.logger.info(str(ticket))
        await self.client.update_ticket(ticket)
        return True

    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        return await self.update_ticket(
            ticket_id, UnifiedTicket(notes=[UnifiedNote(subject=note.subject, body=note.body)])
        )
