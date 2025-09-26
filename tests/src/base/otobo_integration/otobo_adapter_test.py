import pytest

from otobo import (
    OTOBOClient,
    OTOBOClientConfig,
    TicketOperation,
    TicketSearchRequest,
    TicketUpdateRequest,
)
from otobo_znuny.models.request_models import AuthData
from otobo_znuny.models.ticket_models import TicketBase, TicketDetailOutput, ArticleDetail

from open_ticket_ai.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.base.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig
from open_ticket_ai.core.config.config_models import SystemConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedQueue,
    UnifiedPriority,
    UnifiedTicket,
)


TICKETS = [
    TicketDetailOutput(
        TicketID=1,
        Title="Test Ticket 1",
        Queue="default",
        QueueID=1,
        Priority="high",
        PriorityID=1,
        Article=[ArticleDetail(From="u1@example.com", Subject="Test Ticket 1", Body="Body 1")],
        DynamicField=[],
    ),
    TicketDetailOutput(
        TicketID=2,
        Title="Test Ticket 2",
        Queue="default",
        QueueID=1,
        Priority="low",
        PriorityID=2,
        Article=[ArticleDetail(From="u2@example.com", Subject="Test Ticket 2", Body="Body 2")],
        DynamicField=[],
    ),
    TicketDetailOutput(
        TicketID=3,
        Title="Test Ticket 3",
        Queue="misc",
        QueueID=2,
        Priority="medium",
        PriorityID=3,
        Article=[ArticleDetail(From="u3@example.com", Subject="Test Ticket 3", Body="Body 3")],
        DynamicField=[],
    ),
]


class MockedOTOBOClient(OTOBOClient):
    def __init__(self, ticket_data: list[TicketBase]):
        super().__init__(
            OTOBOClientConfig(
                base_url="https://mocked.otobo.example.com",
                service="GenericTicketConnector",
                auth=AuthData(UserLogin="mockuser", Password="mockpass"),
                operations={
                    TicketOperation.SEARCH: "/search",
                    TicketOperation.UPDATE: "/update",
                    TicketOperation.GET: "/get",
                },
            )
        )
        self.ticket_data = ticket_data
        self.updated_payload: TicketUpdateRequest | None = None

    async def search_and_get(self, query: TicketSearchRequest):
        results = self.ticket_data
        if query.QueueIDs:
            results = [t for t in results if t.QueueID in query.QueueIDs]
        if query.Queues:
            results = [t for t in results if t.Queue in query.Queues]
        return results

    async def update_ticket(self, payload: TicketUpdateRequest):
        self.updated_payload = payload
        return True


@pytest.fixture
def adapter_and_client():
    client = MockedOTOBOClient(TICKETS)
    config = SystemConfig(id="dummy", provider_key="dummy", params={})
    adapter = OTOBOAdapter(config=config, otobo_client=client)
    return adapter, client


def test_config_str_and_password(monkeypatch):
    monkeypatch.setenv("OTOBO_PASS", "s3cret")
    cfg = OTOBOAdapterConfig(
        server_address="https://otobo.example.com",
        webservice_name="GenericTicketConnector",
        search_operation_url="/search",
        update_operation_url="/update",
        get_operation_url="/get",
        username="root",
        password_env_var="OTOBO_PASS",
    )
    expected = (
        "server_address='https://otobo.example.com' "
        "webservice_name='GenericTicketConnector' search_operation_url='/search' "
        "update_operation_url='/update' get_operation_url='/get' "
        "username='root' password_env_var='OTOBO_PASS'"
    )
    assert str(cfg) == expected
    assert cfg.password == "s3cret"


def test_config_password_missing_env(monkeypatch):
    monkeypatch.delenv("MISSING_ENV", raising=False)
    cfg = OTOBOAdapterConfig(
        server_address="s",
        webservice_name="w",
        search_operation_url="s",
        update_operation_url="u",
        get_operation_url="g",
        username="user",
        password_env_var="MISSING_ENV",
    )
    with pytest.raises(ValueError):
        _ = cfg.password


@pytest.mark.asyncio
async def test_find_tickets_filters_by_queue(adapter_and_client):
    adapter, _ = adapter_and_client
    criteria = TicketSearchCriteria(queue=UnifiedQueue(name="default"))
    tickets = await adapter.find_tickets(criteria)
    print(tickets)
    assert len(tickets) == 2
    subjects = {t.subject for t in tickets}
    assert subjects == {"Test Ticket 1", "Test Ticket 2"}


@pytest.mark.asyncio
async def test_update_ticket_payload_sent(adapter_and_client):
    adapter, client = adapter_and_client
    updates = UnifiedTicket(
        subject="Updated",
        queue=UnifiedQueue(id="2", name="misc"),
        priority=UnifiedPriority(id="5", name="low"),
    )
    result = await adapter.update_ticket("1", updates)
    assert result is True
    assert client.updated_payload is not None
    assert client.updated_payload.TicketID == 1
    assert client.updated_payload.Ticket.Title == "Updated"
    assert client.updated_payload.Ticket.QueueID == 2
    assert client.updated_payload.Ticket.PriorityID == 5
