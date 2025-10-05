import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from otobo_znuny.domain_models.ticket_models import IdName, Ticket, TicketSearch, TicketUpdate
from pydantic import SecretStr

from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from open_ticket_ai_otobo_znuny_plugin.otobo_znuny_ticket_system_service import _to_id_name, \
    OTOBOZnunyTicketSystemService
from open_ticket_ai_otobo_znuny_plugin.otobo_znuny_ticket_system_service_config import \
    RenderedOTOBOZnunyTicketsystemServiceConfig


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
    def config_dict(self):
        return {
            "password": "test_password",
            "base_url": "https://test.otobo.com",
            "username": "test_user",
            "webservice_name": "TestService",
        }

    @pytest.fixture
    def config(self, config_dict):
        return RenderedOTOBOZnunyTicketsystemServiceConfig.model_validate(config_dict)

    @pytest.fixture
    def service(self, config_dict):
        with patch("open_ticket_ai_otobo_znuny_plugin.otobo_znuny_ticket_system_service.OTOBOZnunyTicketSystemService._recreate_client"):
            return OTOBOZnunyTicketSystemService(config_dict)


    @pytest.fixture
    def mock_client(self):
        client = Mock()
        client.login = Mock()
        client.search_and_get = AsyncMock()
        client.get_ticket = AsyncMock()
        client.update_ticket = AsyncMock()
        return client

    @pytest.fixture
    def patch_ticket_conversion(self):
        with patch("open_ticket_ai_otobo_znuny_plugin.otobo_znuny_ticket_system_service.otobo_ticket_to_unified_ticket") as mock_convert:
            mock_convert.side_effect = lambda ticket: UnifiedTicket(
                id=str(ticket.id),
                subject=ticket.title,
            )
            yield mock_convert

    def test_initialization(self, service, config):
        assert service.config == config
        assert service._client is None
        assert service.logger is not None

    def test_client_property_raises_when_not_initialized(self, service):
        with pytest.raises(RuntimeError, match="Client not initialized"):
            _ = service.client

    def test_client_property_returns_client_when_initialized(self, service, mock_client):
        service._client = mock_client

        assert service.client == mock_client

    def test_recreate_client(self, service, mock_client):
        with patch(
            "open_ticket_ai_otobo_znuny_plugin.otobo_znuny_ticket_system_service.OTOBOZnunyClient") as MockClientClass:
            MockClientClass.return_value = mock_client

            result = service._recreate_client()

            assert result == mock_client
            assert service._client == mock_client
            MockClientClass.assert_called_once_with(config=service.config.to_client_config())
            mock_client.login.assert_called_once()
            login_arg = mock_client.login.call_args.args[0]
            assert login_arg.user_login == service.config.username

    def test_initialize(self, service, mock_client):
        with patch.object(service, "_recreate_client") as mock_recreate:
            mock_recreate.return_value = mock_client

            service.initialize()

            mock_recreate.assert_called_once()

    def test_find_tickets_with_queue(self, service, mock_client, patch_ticket_conversion):
        service._client = mock_client

        mock_tickets = [
            Ticket(id=1, title="Ticket 1", queue=IdName(id="1", name="Queue1")),
            Ticket(id=2, title="Ticket 2", queue=IdName(id="1", name="Queue1")),
        ]
        mock_client.search_and_get.return_value = mock_tickets

        criteria = TicketSearchCriteria(queue=UnifiedEntity(id="1", name="Queue1"), limit=10)

        results = asyncio.run(service.find_tickets(criteria))

        assert len(results) == 2
        mock_client.search_and_get.assert_awaited_once()
        call_args = mock_client.search_and_get.call_args.args[0]
        assert isinstance(call_args, TicketSearch)
        assert call_args.limit == 10
        assert len(call_args.queues) == 1
        assert isinstance(call_args.queues[0], IdName)
        assert call_args.queues[0].id == 1
        assert patch_ticket_conversion.call_count == 2

    def test_find_tickets_without_queue(self, service, mock_client, patch_ticket_conversion):
        service._client = mock_client
        mock_client.search_and_get.return_value = []

        criteria = TicketSearchCriteria(limit=5)

        results = asyncio.run(service.find_tickets(criteria))

        assert results == []
        call_args = mock_client.search_and_get.call_args.args[0]
        assert call_args.queues is None
        assert call_args.limit == 5
        patch_ticket_conversion.assert_not_called()

    def test_find_first_ticket_returns_first(self, service, mock_client, patch_ticket_conversion):
        service._client = mock_client

        mock_tickets = [
            Ticket(id=1, title="First"),
            Ticket(id=2, title="Second"),
        ]
        mock_client.search_and_get.return_value = mock_tickets

        criteria = TicketSearchCriteria()

        result = asyncio.run(service.find_first_ticket(criteria))

        assert result is not None
        assert result.id == "1"
        assert result.subject == "First"
        assert patch_ticket_conversion.call_count == 2

    def test_find_first_ticket_returns_none_when_empty(self, service, mock_client):
        service._client = mock_client
        mock_client.search_and_get.return_value = []

        criteria = TicketSearchCriteria()

        result = asyncio.run(service.find_first_ticket(criteria))

        assert result is None

    def test_get_ticket(self, service, mock_client, patch_ticket_conversion):
        service._client = mock_client

        mock_ticket = Ticket(id=123, title="Test Ticket")
        mock_client.get_ticket.return_value = mock_ticket

        result = asyncio.run(service.get_ticket("123"))

        assert result is not None
        assert result.id == "123"
        mock_client.get_ticket.assert_awaited_once_with(123)
        patch_ticket_conversion.assert_called_once_with(mock_ticket)

    def test_update_ticket(self, service, mock_client):
        service._client = mock_client

        updates = UnifiedTicket(
            subject="Updated Title",
            queue=UnifiedEntity(id="3", name="Technical"),
            priority=UnifiedEntity(id="4", name="Low"),
            notes=[UnifiedNote(subject="Update Note", body="Note body")],
        )

        result = asyncio.run(service.update_ticket("456", updates))

        assert result is True

        mock_client.update_ticket.assert_awaited_once()
        call_args = mock_client.update_ticket.call_args.args[0]
        assert isinstance(call_args, TicketUpdate)
        assert call_args.id == 456
        assert call_args.title == "Updated Title"
        assert call_args.queue.id == 3
        assert call_args.priority.id == 4
        assert call_args.article.subject == "Update Note"
        assert call_args.article.body == "Note body"

    def test_add_note(self, service, mock_client):
        service._client = mock_client

        note = UnifiedNote(subject="New Note", body="This is a new note body")

        result = asyncio.run(service.add_note("789", note))

        assert result is True

        mock_client.update_ticket.assert_awaited_once()
        call_args = mock_client.update_ticket.call_args.args[0]
        assert isinstance(call_args, TicketUpdate)
        assert call_args.id == 789
        assert call_args.article.subject == "New Note"
        assert call_args.article.body == "This is a new note body"

    def test_inheritance_from_ticket_system_service(self, service):
        assert isinstance(service, TicketSystemService)
        assert hasattr(service, "find_tickets")
        assert hasattr(service, "find_first_ticket")
        assert hasattr(service, "get_ticket")
        assert hasattr(service, "update_ticket")
        assert hasattr(service, "add_note")
