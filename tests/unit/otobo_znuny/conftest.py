from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedEntity
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket
from open_ticket_ai.otobo_znuny.models import OTOBOZnunyTSServiceParams
from open_ticket_ai.otobo_znuny.oto_znuny_ts_service import OTOBOZnunyTicketSystemService


@pytest.fixture
def mock_client():
    mock = MagicMock(spec=OTOBOZnunyClient)
    mock.login = MagicMock()
    mock.search_and_get = AsyncMock()
    mock.get_ticket = AsyncMock()
    mock.create_ticket = AsyncMock()
    mock.update_ticket = AsyncMock()
    return mock


@pytest.fixture
def service_params():
    return OTOBOZnunyTSServiceParams(
        base_url="http://test.example.com",
        username="test_user",
        password="test_password",
        webservice_name="TestService",
    )


@pytest.fixture
def service(mock_client, service_params):
    service_instance = OTOBOZnunyTicketSystemService.__new__(OTOBOZnunyTicketSystemService)
    service_instance._params = service_params
    service_instance._client = mock_client
    import logging
    service_instance._logger = logging.getLogger("test_otobo_znuny")
    return service_instance


@pytest.fixture
def sample_otobo_ticket():
    return Ticket(
        id=123,
        title="Test Ticket",
        queue=IdName(id=1, name="Support"),
        priority=IdName(id=3, name="High"),
        articles=[Article(subject="First article", body="This is the first article body")],
    )


@pytest.fixture
def sample_search_criteria():
    return TicketSearchCriteria(
        queue=UnifiedEntity(id="1", name="Support"),
        limit=10,
    )
