from typing import Any

from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import (
    Article,
    Ticket,
    TicketSearch,
    TicketUpdate,
)

from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)
from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import (
    RenderedOTOBOZnunyTSServiceParams,
    otobo_ticket_to_unified_ticket,
    unified_entity_to_id_name,
)


class OTOBOZnunyTicketSystemService(TicketSystemService):
    @staticmethod
    def get_params_model() -> type[RenderedOTOBOZnunyTSServiceParams]:
        return RenderedOTOBOZnunyTSServiceParams

    @inject
    def __init__(
            self,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._client: OTOBOZnunyClient | None = None
        self.initialize()

    @property
    def client(self) -> OTOBOZnunyClient:
        if self._client is None:
            raise RuntimeError("Client not initialized. Call initialize() first.")
        return self._client

    def _recreate_client(self) -> OTOBOZnunyClient:
        self._client = OTOBOZnunyClient(config=self._config.params.to_client_config())
        self._logger.info("Recreated OTOBO client")
        self._logger.info(self._config.params.get_basic_auth().model_dump(with_secrets=True))
        self._client.login(self._config.params.get_basic_auth())
        return self._client

    def initialize(self) -> None:
        self._recreate_client()

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        search = TicketSearch(
            queues=[unified_entity_to_id_name(criteria.queue)] if criteria.queue else None, limit=criteria.limit
        )
        self._logger.debug(f"OTOBO search criteria: {search}")
        tickets: list[Ticket] = await self.client.search_and_get(search)
        self._logger.info(f"OTOBO search returned {len(tickets)} tickets")
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
        self._logger.info(str(ticket))
        await self.client.update_ticket(ticket)
        return True

    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        return await self.update_ticket(
            ticket_id, UnifiedTicket(notes=[UnifiedNote(subject=note.subject, body=note.body)])
        )
