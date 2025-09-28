import asyncio
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import httpx
from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket, TicketSearch, TicketUpdate
from tenacity import (
    RetryCallState,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
    UnifiedTicketBase,
)
from open_ticket_ai_otobo_znuny.models import TicketAdapter
from open_ticket_ai_otobo_znuny.otobo_znuny_ticket_system_service_config import (
    RenderedOTOBOZnunyTicketsystemServiceConfig,
)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

retry_logger = logging.getLogger("tenacity.retry")
retry_logger.setLevel(logging.WARNING)


def _to_id_name(entity: UnifiedEntity | None) -> IdName | None:
    if entity is None:
        return None
    return IdName(
        id=entity.id,
        name=entity.name,
    )


def _before_sleep_recreate_client(retry_state: RetryCallState) -> None:
    before_sleep_log(retry_logger, logging.WARNING)(retry_state)

    if retry_state.args and hasattr(retry_state.args[0], "_recreate_client"):
        adapter_instance = retry_state.args[0]
        try:
            asyncio.run(adapter_instance._recreate_client())
        except RuntimeError:
            loop = asyncio.get_running_loop()
            task = loop.create_task(adapter_instance._recreate_client())
            loop.run_until_complete(task)


def otobo_retry() -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, max=10),
            retry=retry_if_exception_type(
                (
                    httpx.ConnectError,
                    httpx.RemoteProtocolError,
                    httpx.ReadTimeout,
                    httpx.WriteTimeout,
                    httpx.PoolTimeout,
                    httpx.HTTPStatusError,
                    httpx.TransportError,
                )
            ),
            before_sleep=_before_sleep_recreate_client,
            reraise=True,
        )
        async def wrapper(self: "OTOBOZnunyTicketSystemService", *args: Any, **kwargs: Any) -> Any:
            try:
                return await func(self, *args, **kwargs)
            except Exception:
                self.logger.exception(f"Operation {func.__name__} failed after retries")
                raise

        return wrapper

    return decorator


@UnifiedRegistry.register_service_class()
class OTOBOZnunyTicketSystemService(TicketSystemService):
    @inject
    def __init__(self, config: RenderedOTOBOZnunyTicketsystemServiceConfig):
        self.config = config
        self._client: OTOBOZnunyClient | None = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def client(self) -> OTOBOZnunyClient:
        if self._client is None:
            msg = "Client not initialized. Call initialize() first."
            raise RuntimeError(msg)
        return self._client

    async def _recreate_client(self) -> OTOBOZnunyClient:
        self._client = OTOBOZnunyClient(config=self.config.to_client_config())
        self.logger.info("Recreated OTOBO client")
        self._client.login(self.config.get_basic_auth())
        return self._client

    async def initialize(self) -> None:
        await self._recreate_client()

    @otobo_retry()
    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        search = TicketSearch(queues=[_to_id_name(criteria.queue)] if criteria.queue else None, limit=criteria.limit)
        self.logger.debug("OTOBO search criteria: %s", search)
        tickets: list[Ticket] = await self.client.search_and_get(search)
        self.logger.info("OTOBO search returned %d tickets", len(tickets))
        return [TicketAdapter(t) for t in tickets]

    @otobo_retry()
    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        items = await self.find_tickets(criteria)
        return items[0] if items else None

    @otobo_retry()
    async def get_ticket(self, ticket_id: str) -> UnifiedTicket | None:
        ticket: Ticket = await self.client.get_ticket(int(ticket_id))
        return TicketAdapter(ticket)

    @otobo_retry()
    async def update_ticket(self, ticket_id: str, updates: UnifiedTicketBase) -> bool:
        ticket = TicketUpdate(
            id=int(ticket_id),
            title=updates.subject,
            queue=_to_id_name(updates.queue),
            priority=_to_id_name(updates.priority),
            article=Article(subject=updates.note.subject, body=updates.note.body),
        )
        logging.info(ticket)
        await self.client.update_ticket(ticket)
        return True

    @otobo_retry()
    async def add_note(self, ticket_id: str, note: UnifiedNote) -> bool:
        ticket = TicketUpdate(id=int(ticket_id), article=Article(subject=note.subject, body=note.body))
        await self.client.update_ticket(ticket)
        return True
