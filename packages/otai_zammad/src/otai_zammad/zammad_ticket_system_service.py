from __future__ import annotations

from collections.abc import Iterable
from typing import Any, ClassVar

import httpx
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedTicket,
)

from otai_zammad.models import (
    ZammadArticle,
    ZammadTicket,
    ZammadTSServiceParams,
    merge_ticket_with_articles,
    unified_note_to_zammad_article,
    unified_ticket_to_zammad_create,
    unified_ticket_to_zammad_update,
    zammad_ticket_to_unified_ticket,
)


class ZammadTicketsystemService(TicketSystemService):
    ParamsModel: ClassVar[type[ZammadTSServiceParams]] = ZammadTSServiceParams

    API_TICKETS_SEARCH: ClassVar[str] = "/api/v1/tickets/search"
    API_TICKETS: ClassVar[str] = "/api/v1/tickets"
    API_TICKET_BY_ID: ClassVar[str] = "/api/v1/tickets/{ticket_id}"
    API_TICKET_ARTICLES_LIST: ClassVar[str] = "/api/v1/ticket_articles/by_ticket/{ticket_id}"
    API_TICKET_ARTICLES_CREATE: ClassVar[str] = "/api/v1/ticket_articles"

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._owns_client = client is None
        self._client: httpx.AsyncClient | None = client or self._create_client()
        self._logger.debug(f"ZammadTicketsystemService initialized with base_url={self._params.base_url}")

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._logger.debug("Creating new AsyncClient for Zammad requests")
            self._client = self._create_client()
            self._owns_client = True
        return self._client

    def _create_client(self) -> httpx.AsyncClient:
        headers = {
            "Authorization": self._params.auth_header(),
            "Accept": "application/json",
        }
        client_kwargs: dict[str, Any] = {
            "base_url": str(self._params.base_url),
            "headers": headers,
            "verify": self._params.verify,
        }
        if self._params.timeout is not None:
            client_kwargs["timeout"] = self._params.timeout
        loggable_kwargs = {k: v for k, v in client_kwargs.items() if k != "headers"}
        self._logger.debug(f"Creating AsyncClient with kwargs: {loggable_kwargs}")
        return httpx.AsyncClient(**client_kwargs)

    async def aclose(self) -> None:
        if self._client is not None and self._owns_client:
            self._logger.debug("Closing AsyncClient for Zammad")
            await self._client.aclose()
        self._client = None

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        self._logger.debug(f"Searching Zammad tickets with criteria={criteria.model_dump()}")
        params: dict[str, Any] = {
            "limit": criteria.limit,
            "offset": criteria.offset,
            "expand": "articles",
        }
        queue_filter = None
        if criteria.queue:
            queue_filter = criteria.queue.name or criteria.queue.id
        query = "*" if not queue_filter else f'group:"{queue_filter}"'
        params["query"] = query

        response = await self.client.get(self.API_TICKETS_SEARCH, params=params)
        response.raise_for_status()
        payload = response.json()
        raw_tickets = self._extract_ticket_entries(payload)

        unified = await self._process_raw_tickets_to_unified(raw_tickets)
        self._logger.debug(f"Zammad search returned {len(unified)} ticket(s)")
        return unified

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        tickets = await self.find_tickets(criteria)
        ticket = tickets[0] if tickets else None
        if ticket:
            self._logger.debug(f"Found first ticket with id={ticket.id}")
        else:
            self._logger.debug(f"No tickets found for criteria={criteria.model_dump()}")
        return ticket

    async def _process_raw_tickets_to_unified(self, raw_tickets: list[Any]) -> list[UnifiedTicket]:
        unified: list[UnifiedTicket] = []
        for raw in raw_tickets:
            ticket = await self._coerce_to_ticket(raw)
            if ticket is None:
                continue
            if not ticket.articles:
                articles = await self._fetch_articles(ticket.id)
                ticket = merge_ticket_with_articles(ticket, articles)
            unified.append(zammad_ticket_to_unified_ticket(ticket))
        return unified


    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        self._logger.info(f"Fetching Zammad ticket id={ticket_id}")
        ticket = await self._get_ticket(int(ticket_id))
        if ticket is None:
            self._logger.warning(f"Ticket id={ticket_id} not found")
            return None
        return zammad_ticket_to_unified_ticket(ticket)

    async def create_ticket(self, ticket: UnifiedTicket) -> str:
        payload = unified_ticket_to_zammad_create(ticket)
        print("payload get: " + str(payload))
        response = await self.client.post(self.API_TICKETS, json=payload.model_dump(exclude_none=True))
        response.raise_for_status()
        data = response.json()
        print("get response" + str(data))
        ticket_id = self._extract_ticket_id(data)
        self._logger.info(f"Created Zammad ticket id={ticket_id}")
        return ticket_id

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicket) -> bool:
        payload = unified_ticket_to_zammad_update(updates)
        if payload.has_updates():
            response = await self.client.put(
                self.API_TICKET_BY_ID.format(ticket_id=ticket_id),
                json=payload.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            self._logger.debug(f"Updated ticket fields for id={ticket_id}")

        if updates.notes:
            note = updates.notes[-1]
            self._logger.debug(f"Appending note to ticket id={ticket_id} during update")
            await self.add_note(ticket_id, note)

        return True

    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        payload = unified_note_to_zammad_article(note, int(ticket_id))
        response = await self.client.post(
            self.API_TICKET_ARTICLES_CREATE.format(ticket_id=ticket_id),
            json=payload.model_dump(exclude_none=True),
        )
        response.raise_for_status()
        self._logger.info(f"Added note to Zammad ticket id={ticket_id}")
        return True

    async def _coerce_to_ticket(self, payload: Any) -> ZammadTicket | None:
        if isinstance(payload, dict):
            return await self._hydrate_ticket(payload)
        if isinstance(payload, int):
            return await self._get_ticket(payload)
        if isinstance(payload, str) and payload.isdigit():
            return await self._get_ticket(int(payload))
        self._logger.warning(f"Skipping unsupported ticket payload: {payload}")
        return None

    async def _hydrate_ticket(self, payload: dict[str, Any]) -> ZammadTicket:
        ticket = ZammadTicket.model_validate(payload)
        if not ticket.articles and ticket.article_ids:
            articles = await self._fetch_articles(ticket.id)
            ticket = merge_ticket_with_articles(ticket, articles)
        return ticket

    async def _get_ticket(self, ticket_id: int) -> ZammadTicket | None:
        url = self.API_TICKET_BY_ID.format(ticket_id=ticket_id)
        response = await self.client.get(
            url, params={"expand": "articles"}
        )
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        ticket = ZammadTicket.model_validate(response.json())
        if not ticket.articles:
            articles = await self._fetch_articles(ticket.id)
            ticket = merge_ticket_with_articles(ticket, articles)
        return ticket

    async def _fetch_articles(self, ticket_id: int) -> list[ZammadArticle]:
        response = await self.client.get(self.API_TICKET_ARTICLES_LIST.format(ticket_id=ticket_id))
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict):
            articles_data: Iterable[Any] = data.get("articles", [])
        else:
            articles_data = data
        return [ZammadArticle.model_validate(item) for item in articles_data if isinstance(item, dict)]

    @staticmethod
    def _extract_ticket_entries(payload: Any) -> list[Any]:
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ("tickets", "results", "objects"):
                items = payload.get(key)
                if isinstance(items, list):
                    return items
        return []

    @staticmethod
    def _extract_ticket_id(payload: Any) -> str:
        if isinstance(payload, dict):
            if "id" in payload:
                return str(payload["id"])
            if "ticket_id" in payload:
                return str(payload["ticket_id"])
        if isinstance(payload, int):
            return str(payload)
        if isinstance(payload, str):
            return payload
        raise ValueError("Unable to extract ticket id from response payload")
