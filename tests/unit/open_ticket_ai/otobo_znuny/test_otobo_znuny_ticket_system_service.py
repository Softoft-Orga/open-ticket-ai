from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import (
    IdName,
    Ticket,
    TicketSearch,
    TicketUpdate,
)
from pydantic import SecretStr

from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
    UnifiedTicketBase,
)
from open_ticket_ai.otobo_znuny.otobo_znuny_ticket_system_service import (
    OTOBOZnunyTicketSystemService,
    _to_id_name,
)
from open_ticket_ai.otobo_znuny.otobo_znuny_ticket_system_service_config import (
    RawOTOBOZnunyTicketsystemServiceConfig,
    RenderedOTOBOZnunyTicketsystemServiceConfig,
)


class TestToIdName:
    def test_converts_unified_entity_to_id_name(self):
        entity = UnifiedEntity(id="123", name="Test Entity")
        result = _to_id_name(entity)

        assert isinstance(result, IdName)
        assert result.id == 123
        assert result.name == "Test Entity"

    def test_returns_none_for_none_input(self):
        result = _to_id_name(None)
        assert result is None


class TestOTOBOZnunyTicketSystemService:
    @pytest.fixture
    def config(self):
        return RenderedOTOBOZnunyTicketsystemServiceConfig(
            password=SecretStr("test_password"),
            base_url="https://test.otobo.com",
            username="test_user",
            webservice_name="TestService",
        )

    @pytest.fixture
    def service(self, config):
        return OTOBOZnunyTicketSystemService(config)

    @pytest.fixture(autouse=True)
    def patch_ticket_adapter(self, monkeypatch):
        def adapter(ticket: Ticket) -> UnifiedTicket:
            queue = None
            if ticket.queue is not None:
                queue = UnifiedEntity(
                    id=str(ticket.queue.id) if ticket.queue.id is not None else None,
                    name=ticket.queue.name,
                )

            priority = None
            if ticket.priority is not None:
                priority = UnifiedEntity(
                    id=str(ticket.priority.id) if ticket.priority.id is not None else None,
                    name=ticket.priority.name,
                )

            return UnifiedTicket(
                id=str(ticket.id) if ticket.id is not None else "",
                subject=ticket.title or "",
                queue=queue,
                priority=priority,
                note=None,
                body="",
            )

        monkeypatch.setattr(
            "open_ticket_ai.otobo_znuny.otobo_znuny_ticket_system_service.TicketAdapter",
            adapter,
        )

    def test_config_model_types(self):
        assert OTOBOZnunyTicketSystemService.get_raw_config_model_type() is RawOTOBOZnunyTicketsystemServiceConfig
        assert (
            OTOBOZnunyTicketSystemService.get_rendered_config_model_type()
            is RenderedOTOBOZnunyTicketsystemServiceConfig
        )

    def test_needs_raw_config(self):
        assert OTOBOZnunyTicketSystemService.needs_raw_config() is False

    @pytest.fixture
    def mock_client(self):
        client = Mock(spec=OTOBOZnunyClient)
        client.login = Mock()
        client.search_and_get = AsyncMock()
        client.get_ticket = AsyncMock()
        client.update_ticket = AsyncMock()
        return client

    def test_initialization(self, service, config):
        assert service._rendered_config == config
        assert service._client is None
        assert service.logger is not None

    def test_client_property_raises_when_not_initialized(self, service):
        with pytest.raises(RuntimeError, match="Client not initialized"):
            _ = service.client

    @pytest.mark.asyncio
    async def test_client_property_returns_client_when_initialized(self, service, mock_client):
        service._client = mock_client
        assert service.client == mock_client

    @pytest.mark.asyncio
    async def test_recreate_client(self, service, mock_client):
        with patch("open_ticket_ai.otobo_znuny.otobo_znuny_ticket_system_service.OTOBOZnunyClient") as MockClientClass:
            MockClientClass.return_value = mock_client

            result = await service._recreate_client()

            assert result == mock_client
            assert service._client == mock_client
            MockClientClass.assert_called_once_with(config=service._rendered_config.to_client_config())
            mock_client.login.assert_called_once_with(service._rendered_config.get_basic_auth())

    @pytest.mark.asyncio
    async def test_initialize(self, service, mock_client):
        with patch.object(service, "_recreate_client", new_callable=AsyncMock) as mock_recreate:
            mock_recreate.return_value = mock_client

            await service.initialize()

            mock_recreate.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_tickets_with_queue(self, service, mock_client):
        service._client = mock_client

        mock_tickets = [
            Ticket(id=1, title="Ticket 1", queue=IdName(id="1", name="Queue1")),
            Ticket(id=2, title="Ticket 2", queue=IdName(id="1", name="Queue1")),
        ]
        mock_client.search_and_get.return_value = mock_tickets

        criteria = TicketSearchCriteria(queue=UnifiedEntity(id="1", name="Queue1"), limit=10)

        results = await service.find_tickets(criteria)

        assert len(results) == 2
        assert all(isinstance(t, UnifiedTicket) for t in results)
        assert results[0].id == "1"
        assert results[1].id == "2"

        mock_client.search_and_get.assert_called_once()
        call_args = mock_client.search_and_get.call_args[0][0]
        assert isinstance(call_args, TicketSearch)
        assert call_args.limit == 10
        assert len(call_args.queues) == 1
        assert call_args.queues[0].id == 1

    @pytest.mark.asyncio
    async def test_find_tickets_without_queue(self, service, mock_client):
        service._client = mock_client
        mock_client.search_and_get.return_value = []

        criteria = TicketSearchCriteria(limit=5)

        results = await service.find_tickets(criteria)

        assert results == []

        call_args = mock_client.search_and_get.call_args[0][0]
        assert call_args.queues is None
        assert call_args.limit == 5

    @pytest.mark.asyncio
    async def test_find_first_ticket_returns_first(self, service, mock_client):
        service._client = mock_client

        mock_tickets = [
            Ticket(id=1, title="First"),
            Ticket(id=2, title="Second"),
        ]
        mock_client.search_and_get.return_value = mock_tickets

        criteria = TicketSearchCriteria()

        result = await service.find_first_ticket(criteria)

        assert result is not None
        assert result.id == "1"
        assert result.subject == "First"

    @pytest.mark.asyncio
    async def test_find_first_ticket_returns_none_when_empty(self, service, mock_client):
        service._client = mock_client
        mock_client.search_and_get.return_value = []

        criteria = TicketSearchCriteria()

        result = await service.find_first_ticket(criteria)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_ticket(self, service, mock_client):
        service._client = mock_client

        mock_ticket = Ticket(
            id=123, title="Test Ticket", queue=IdName(id="2", name="Support"), priority=IdName(id="3", name="High")
        )
        mock_client.get_ticket.return_value = mock_ticket

        result = await service.get_ticket("123")

        assert result is not None
        assert result.id == "123"
        assert result.subject == "Test Ticket"
        assert result.queue.name == "Support"
        assert result.priority.name == "High"

        mock_client.get_ticket.assert_called_once_with(123)

    @pytest.mark.asyncio
    async def test_update_ticket(self, service, mock_client):
        service._client = mock_client

        updates = UnifiedTicketBase(
            subject="Updated Title",
            queue=UnifiedEntity(id="3", name="Technical"),
            priority=UnifiedEntity(id="4", name="Low"),
            note=UnifiedNote(subject="Update Note", body="Note body"),
        )

        result = await service.update_ticket("456", updates)

        assert result is True

        mock_client.update_ticket.assert_called_once()
        call_args = mock_client.update_ticket.call_args[0][0]
        assert isinstance(call_args, TicketUpdate)
        assert call_args.id == 456
        assert call_args.title == "Updated Title"
        assert call_args.queue.id == 3
        assert call_args.priority.id == 4
        assert call_args.article.subject == "Update Note"
        assert call_args.article.body == "Note body"

    @pytest.mark.asyncio
    async def test_add_note(self, service, mock_client):
        service._client = mock_client

        note = UnifiedNote(subject="New Note", body="This is a new note body")

        result = await service.add_note("789", note)

        assert result is True

        mock_client.update_ticket.assert_called_once()
        call_args = mock_client.update_ticket.call_args[0][0]
        assert isinstance(call_args, TicketUpdate)
        assert call_args.id == 789
        assert call_args.article.subject == "New Note"
        assert call_args.article.body == "This is a new note body"

    @pytest.mark.asyncio
    async def test_retry_on_http_errors(self, service, mock_client):
        service._client = mock_client

        mock_client.get_ticket.side_effect = [
            httpx.ConnectError("First attempt failed"),
            httpx.ReadTimeout("Second attempt timeout"),
            Ticket(id=999, title="Success after retries"),
        ]

        with patch.object(service, "_recreate_client", new_callable=AsyncMock) as mock_recreate:
            mock_recreate.return_value = mock_client

            original_before_sleep = service.get_ticket.retry.before_sleep
            service.get_ticket.retry.before_sleep = lambda state: None
            try:
                result = await service.get_ticket("999")
            finally:
                service.get_ticket.retry.before_sleep = original_before_sleep

            assert result is not None
            assert result.id == "999"
            assert mock_client.get_ticket.call_count == 3

    @pytest.mark.asyncio
    async def test_inheritance_from_ticket_system_service(self, service):
        assert isinstance(service, TicketSystemService)
        assert hasattr(service, "find_tickets")
        assert hasattr(service, "find_first_ticket")
        assert hasattr(service, "get_ticket")
        assert hasattr(service, "update_ticket")
        assert hasattr(service, "add_note")
