import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicket,
)
from otobo_znuny.mappers import _to_id_name
from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import RenderedOTOBOZnunyTSServiceParams
from packages.otai_otobo_znuny.src.otai_otobo_znuny.oto_znuny_ts_service import (
    OTOBOZnunyTicketSystemService,
)


class TestToIdName:
    def test_returns_none_for_none_input(self):
        result = _to_id_name(None, None)

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
        return RenderedOTOBOZnunyTSServiceParams.model_validate(config_dict)

    @pytest.fixture
    def service(self, config):
        with patch(
            "packages.otai_otobo_znuny.src.otai_otobo_znuny."
            "oto_znuny_ts_service.OTOBOZnunyTicketSystemService._recreate_client"
        ):
            return OTOBOZnunyTicketSystemService(config)

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
        with patch(
            "packages.otai_otobo_znuny.src.otai_otobo_znuny.models.otobo_ticket_to_unified_ticket"
        ) as mock_convert:
            mock_convert.side_effect = lambda ticket: UnifiedTicket(
                id=str(ticket.id),
                subject=ticket.title,
            )
            yield mock_convert

    def test_initialization(self, service, config):
        assert service._config == config
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
            "packages.otai_otobo_znuny.src.otai_otobo_znuny.oto_znuny_ts_service.OTOBOZnunyClient"
        ) as MockClientClass:
            MockClientClass.return_value = mock_client

            result = service._recreate_client()

            assert result == mock_client
            assert service._client == mock_client
            MockClientClass.assert_called_once_with(config=service._config.to_client_config())
            mock_client.login.assert_called_once()
            login_arg = mock_client.login.call_args.args[0]
            assert login_arg.user_login == service._config.username

    def test_initialize(self, service, mock_client):
        with patch.object(service, "_recreate_client") as mock_recreate:
            mock_recreate.return_value = mock_client

            service.initialize()

            mock_recreate.assert_called_once()

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

    def test_find_first_ticket_returns_none_when_empty(self, service, mock_client):
        service._client = mock_client
        mock_client.search_and_get.return_value = []

        criteria = TicketSearchCriteria()

        result = asyncio.run(service.find_first_ticket(criteria))

        assert result is None

    def test_inheritance_from_ticket_system_service(self, service):
        assert isinstance(service, TicketSystemService)
        assert hasattr(service, "find_tickets")
        assert hasattr(service, "find_first_ticket")
        assert hasattr(service, "get_ticket")
        assert hasattr(service, "update_ticket")
        assert hasattr(service, "add_note")
