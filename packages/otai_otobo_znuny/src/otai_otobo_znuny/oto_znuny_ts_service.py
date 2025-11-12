from typing import Any, ClassVar

from injector import inject
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedNote, UnifiedTicket
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

    async def find_tickets(
        self,
        criteria: TicketSearchCriteria | None = None,
        **criteria_kwargs: Any,
    ) -> list[UnifiedTicket]:
        search_criteria = self._resolve_search_criteria(criteria, criteria_kwargs)
        queue_info = search_criteria.queue.model_dump() if search_criteria.queue else None
        self._logger.debug(
            f"🔍 Searching tickets with criteria: queue={queue_info}, limit={search_criteria.limit}"
        )

        search = TicketSearch(
            queues=[unified_entity_to_id_name(search_criteria.queue)] if search_criteria.queue else None,
            limit=search_criteria.limit,
        )
        self._logger.debug(f"OTOBO search object: {search.model_dump()}")
        tickets: list[Ticket] = await self.client.search_and_get(search)
        self._logger.debug(f"📥 OTOBO search returned {len(tickets)} ticket(s)")

        if tickets:
            self._logger.debug(f"Ticket IDs: {[t.id for t in tickets]}")

        return [otobo_ticket_to_unified_ticket(ticket) for ticket in tickets]

    async def find_first_ticket(
        self,
        criteria: TicketSearchCriteria | None = None,
        **criteria_kwargs: Any,
    ) -> UnifiedTicket | None:
        self._logger.debug("🔍 Finding first ticket matching criteria")
        items = await self.find_tickets(criteria, **criteria_kwargs)
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
            return otobo_ticket_to_unified_ticket(ticket) if ticket else None
        except Exception as e:
            self._logger.error(f"❌ Failed to get ticket {ticket_id}: {e}", exc_info=True)
            raise

    async def create_ticket(
        self,
        ticket: UnifiedTicket | None = None,
        **ticket_kwargs: Any,
    ) -> UnifiedTicket:
        unified_ticket = self._resolve_unified_ticket(ticket, ticket_kwargs)
        if not unified_ticket.subject:
            raise ValueError("Ticket subject is required to create an OTOBO/Znuny ticket.")
        payload = TicketCreate(
            title=unified_ticket.subject,
            queue=unified_entity_to_id_name(unified_ticket.queue) if unified_ticket.queue else None,
            priority=unified_entity_to_id_name(unified_ticket.priority) if unified_ticket.priority else None,
            article=Article(
                subject=unified_ticket.subject,
                body=unified_ticket.body or "",
            ),
        )
        created_ticket: Ticket = await self.client.create_ticket(payload)
        return otobo_ticket_to_unified_ticket(created_ticket)

    async def update_ticket(
        self,
        ticket_id: str,
        updates: UnifiedTicket | None = None,
        **update_kwargs: Any,
    ) -> bool:
        resolved_updates = self._resolve_unified_ticket(updates, update_kwargs)
        self._logger.info(f"📝 Updating ticket {ticket_id} in OTOBO/Znuny")
        self._logger.debug(f"Updates: {resolved_updates.model_dump(exclude_none=True)}")

        article = None
        if resolved_updates.notes and len(resolved_updates.notes) > 0:
            if len(resolved_updates.notes) > 1:
                self._logger.warning(
                    f"⚠️  Multiple notes provided for ticket update; only the last one will be added. "
                    f"Total notes provided: {len(resolved_updates.notes)}"
                )
            latest_note = resolved_updates.notes[-1]
            self._logger.debug(f"Adding article/note: {latest_note.subject}")
            article = Article(
                subject=latest_note.subject,
                body=latest_note.body
            )

        ticket = TicketUpdate(
            id=int(ticket_id),
            title=resolved_updates.subject,
            queue=unified_entity_to_id_name(resolved_updates.queue) if resolved_updates.queue else None,
            priority=unified_entity_to_id_name(resolved_updates.priority) if resolved_updates.priority else None,
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

    async def add_note(
        self,
        ticket_id: str,
        note: UnifiedNote | None = None,
        **note_kwargs: Any,
    ) -> bool:
        resolved_note = self._resolve_note(note, note_kwargs)
        self._logger.info(f"📌 Adding note to ticket {ticket_id}")
        body_length = len(resolved_note.body) if resolved_note.body else 0
        self._logger.debug(
            f"Note: subject='{resolved_note.subject}', body_length={body_length}"
        )

        return await self.update_ticket(
            ticket_id,
            notes=[resolved_note],
        )

    def _resolve_search_criteria(
        self,
        criteria: TicketSearchCriteria | None,
        criteria_kwargs: dict[str, Any],
    ) -> TicketSearchCriteria:
        if criteria is not None:
            return criteria
        if criteria_kwargs:
            return TicketSearchCriteria.model_validate(criteria_kwargs)
        return TicketSearchCriteria()

    def _resolve_unified_ticket(
        self,
        ticket: UnifiedTicket | None,
        ticket_kwargs: dict[str, Any],
    ) -> UnifiedTicket:
        if ticket is not None:
            return ticket
        if ticket_kwargs:
            return UnifiedTicket.model_validate(ticket_kwargs)
        raise ValueError("Ticket details must be provided either as a UnifiedTicket or keyword arguments.")

    def _resolve_note(
        self,
        note: UnifiedNote | None,
        note_kwargs: dict[str, Any],
    ) -> UnifiedNote:
        if note is not None:
            return note
        if note_kwargs:
            return UnifiedNote.model_validate(note_kwargs)
        raise ValueError("Note details must be provided either as a UnifiedNote or keyword arguments.")

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
