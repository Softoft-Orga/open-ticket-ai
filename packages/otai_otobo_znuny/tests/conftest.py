from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai import InjectableConfig, LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedEntity
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket
from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import (
    OTOBOZnunyTSServiceParams,
)
from packages.otai_otobo_znuny.src.otai_otobo_znuny.oto_znuny_ts_service import (
    OTOBOZnunyTicketSystemService,
)


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
def logger_factory():
    return create_logger_factory(LoggingConfig(level="DEBUG"))


@pytest.fixture
def service(mock_client, service_params, logger_factory):
    service_instance = OTOBOZnunyTicketSystemService.__new__(OTOBOZnunyTicketSystemService)
    service_config = InjectableConfig(
        id="test_service",
        use="packages.otai_otobo_znuny.src.otai_otobo_znuny.oto_znuny_ts_service.OTOBOZnunyTicketSystemService",
        params=service_params.model_dump(),
    )
    service_instance._config = service_config
    service_instance._logger_factory = logger_factory
    service_instance._logger = logger_factory.create(service_config.id)
    service_instance._client = mock_client
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
