from typing import Any, ClassVar

from injector import inject
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import (
    Article,
    Ticket,
    TicketCreate,
    TicketSearch,
    TicketUpdate,
)

from otai_otobo_znuny.models import (
    OTOBOZnunyTSServiceParams,
    otobo_ticket_to_unified_ticket,
    unified_entity_to_id_name,
)


class OTOBOZnunyTicketSystemService(TicketSystemService):
    ParamsModel: ClassVar[type[OTOBOZnunyTSServiceParams]] = OTOBOZnunyTSServiceParams

    @inject
    def __init__(
        self,
        client: OTOBOZnunyClient | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._client: OTOBOZnunyClient | None = client
        self._logger.debug("🎫 OTOBOZnunyTicketSystemService initializing")
        self._initialize()

    @property
    def client(self) -> OTOBOZnunyClient:
        if self._client is None:
            self._logger.error("❌ Client not initialized")
            raise RuntimeError("Client not initialized. Call initialize() first.")
        return self._client

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        self._logger.debug(f"🔍 Searching tickets with criteria: queue={criteria.queue}, limit={criteria.limit}")

        search = TicketSearch(
            queues=[unified_entity_to_id_name(criteria.queue)] if criteria.queue else None,
            limit=criteria.limit,
        )
        self._logger.debug(f"OTOBO search object: {search.model_dump()}")
        tickets: list[Ticket] = await self.client.search_and_get(search)
        self._logger.debug(f"📥 OTOBO search returned {len(tickets)} ticket(s)")

        if tickets:
            self._logger.debug(f"Ticket IDs: {[t.id for t in tickets]}")

        unified = [otobo_ticket_to_unified_ticket(t) for t in tickets]
        return unified

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        self._logger.debug("🔍 Finding first ticket matching criteria")
        items = await self.find_tickets(criteria)
        result = items[0] if items else None

        if result:
            self._logger.debug(f"Found ticket: {result.id}")
        else:
            self._logger.debug("No tickets found")

        return result

    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        self._logger.info(f"🎫 Fetching ticket by ID: {ticket_id}")

        try:
            ticket = await self.client.get_ticket(int(ticket_id))
            self._logger.info(f"✅ Retrieved ticket {ticket_id}")
            return otobo_ticket_to_unified_ticket(ticket)
        except Exception as e:
            self._logger.error(f"❌ Failed to get ticket {ticket_id}: {e}", exc_info=True)
            raise

    async def create_ticket(self, ticket: UnifiedTicket) -> str:
        ticket = TicketCreate(
            title=ticket.subject,
            queue=unified_entity_to_id_name(ticket.queue) if ticket.queue else None,
            priority=unified_entity_to_id_name(ticket.priority) if ticket.priority else None,
            article=Article(
                subject=ticket.subject,
                body=ticket.body or "",
                content_type="text/plain",
            ),
        )
        ticket_response: Ticket = await self.client.create_ticket(ticket)
        return str(ticket_response.id)

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        self._logger.info(f"📝 Updating ticket {ticket_id} in OTOBO/Znuny")
        self._logger.debug(f"Updates: {updates.model_dump(exclude_none=True)}")

        article = None
        if updates.notes and len(updates.notes) > 0:
            if len(updates.notes) > 1:
                self._logger.warning(
                    f"⚠️  Multiple notes provided for ticket update; only the last one will be added. "
                    f"Total notes provided: {len(updates.notes)}"
                )
            self._logger.debug(f"Adding article/note: {updates.notes[-1].subject}")
            article = Article(subject=updates.notes[0].subject, body=updates.notes[0].body, content_type="text/plain")

        ticket = TicketUpdate(
            id=int(ticket_id),
            title=updates.subject,
            queue=unified_entity_to_id_name(updates.queue) if updates.queue else None,
            priority=unified_entity_to_id_name(updates.priority) if updates.priority else None,
            article=article,
        )

        self._logger.debug(f"OTOBO ticket update object: {ticket.model_dump(exclude_none=True)}")

        try:
            await self.client.update_ticket(ticket)
        except Exception as e:
            self._logger.error(f"❌ Failed to update ticket {ticket_id}: {e}", exc_info=True)
            raise
        else:
            self._logger.info(f"✅ Successfully updated ticket {ticket_id} in OTOBO/Znuny")
            return True

    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        self._logger.info(f"📌 Adding note to ticket {ticket_id}")
        self._logger.debug(f"Note: subject='{note.subject}', body_length={len(note.body) if note.body else 0}")

        return await self.update_ticket(
            ticket_id, UnifiedTicket(notes=[UnifiedNote(subject=note.subject, body=note.body)])
        )

    def _recreate_client(self) -> OTOBOZnunyClient:
        self._logger.debug("🔄 Recreating OTOBO client")
        self._logger.debug(f"Base URL: {self._params.to_client_config().base_url}")

        self._client = OTOBOZnunyClient(config=self._params.to_client_config())

        auth_info = self._params.get_basic_auth().model_dump(with_secrets=True)
        self._logger.debug(f"Authentication: user={auth_info.get('username', 'N/A')}")

        self._client.login(self._params.get_basic_auth())
        self._logger.debug("✅ OTOBO client recreated and logged in")

        return self._client

    def _initialize(self) -> None:
        self._logger.debug("⚙️  Initializing OTOBO/Znuny ticket system service")
        self._recreate_client()
        self._logger.debug("✅ OTOBO/Znuny ticket system service initialized")
