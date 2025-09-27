import logging
import os
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast

import httpx
from injector import inject
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket, TicketSearch, TicketUpdate
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import SecretStr
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential

# Type variable for generic return type
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

# Configure retry logger
retry_logger = logging.getLogger("tenacity.retry")
retry_logger.setLevel(logging.WARNING)

from open_ticket_ai.core.dependency_injection.registry import TicketSystemRegistry
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedTicket,
    UnifiedTicketBase,
)
from open_ticket_ai_otobo_znuny.models import TicketAdapter
from open_ticket_ai_otobo_znuny.otobo_adapter_config import OTOBOAdapterConfig


def _to_id_name(entity: UnifiedEntity | None) -> IdName | None:
    if entity is None:
        return None
    return IdName(
        id=entity.id,
        name=entity.name,
    )


def otobo_retry() -> Callable[[F], F]:
    """Decorator factory for retrying OTOBO API calls."""

    def decorator(func: F) -> F:
        @wraps(func)
        @retry(
            stop=stop_after_attempt(3),  # 3 retries
            wait=wait_exponential(multiplier=1, max=10),  # 1s, 2s, 4s, 8s, max 10s
            retry=retry_if_exception_type((
                    httpx.ConnectError,
                    httpx.RemoteProtocolError,
                    httpx.ReadTimeout,
                    httpx.WriteTimeout,
                    httpx.PoolTimeout
            )),
            before_sleep=before_sleep_log(retry_logger, logging.WARNING),
            reraise=True
        )
        async def wrapper(self: 'OTOBOAdapter', *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except Exception as e:
                self.logger.warning(f"Error in {func.__name__}: {str(e)}")
                if hasattr(self, '_recreate_client'):
                    await self._recreate_client()
                raise

        return cast(F, wrapper)

    return decorator


@TicketSystemRegistry.register("otobo")
class OTOBOAdapter(TicketSystemAdapter):
    @inject
    def __init__(self, config: dict[str, Any]):
        self.config = OTOBOAdapterConfig.model_validate(config)
        self._client: Optional[OTOBOZnunyClient] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def client(self) -> OTOBOZnunyClient:
        """Lazy initialization of the OTOBO client."""
        if self._client is None:
            self._client = self.create_otobo_client()
        return self._client

    async def _recreate_client(self) -> None:
        """Recreate the OTOBO client."""
        if self._client is not None:
            # Close existing client session if it exists
            if hasattr(self._client, '_client') and self._client._client:
                try:
                    await self._client._client.aclose()
                except Exception as e:
                    self.logger.warning(f"Error closing existing client: {e}")
        self._client = self.create_otobo_client()

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

    def create_basic_auth(self) -> BasicAuth:
        password = os.getenv(self.config.password_env_var)
        return BasicAuth(user_login=self.config.username, password=SecretStr(password))

    def create_otobo_client(self) -> OTOBOZnunyClient:
        limits = httpx.Limits(max_keepalive_connections=100, max_connections=1_000)
        client = httpx.AsyncClient(limits=limits, timeout=60.0)
        otobo_znuny_client = OTOBOZnunyClient(
            config=ClientConfig(
                base_url=self.config.server_address,
                webservice_name=self.config.webservice_name,
                operation_url_map={
                    TicketOperation.SEARCH.value: self.config.search_operation_url,
                    TicketOperation.GET.value: self.config.get_operation_url,
                    TicketOperation.UPDATE.value: self.config.update_operation_url,
                },
            ),
            client=client,
        )
        otobo_znuny_client.login(self.create_basic_auth())
        return otobo_znuny_client
