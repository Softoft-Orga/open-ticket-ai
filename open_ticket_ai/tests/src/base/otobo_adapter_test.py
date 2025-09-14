"""This module contains unit tests for the OTOBOAdapter.

The tests include:
    - Testing the configuration of the OTOBOAdapterConfig
    - Testing the behavior of the OTOBOAdapter using a mocked OTOBO client

The tests are designed to run without requiring a real OTOBO server connection.
"""
import dataclasses

import pytest

pytest.importorskip("otobo")

import otobo
from otobo import OTOBOClient, OTOBOClientConfig

from open_ticket_ai.src.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.src.base.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig
from open_ticket_ai.src.core.config.config_models import SystemConfig


@dataclasses.dataclass
class MockedTicket:
    """Mocked ticket data structure for testing purposes.

    This class is used to simulate a ticket object with essential attributes.
    It is primarily used in unit tests to verify the behavior of the OTOBOAdapter.

    Attributes:
        id (str): Unique identifier for the ticket.
        title (str): Title of the ticket.
        description (str): Detailed description of the ticket.
        status (str): Current status of the ticket (e.g., 'open', 'closed').
        priority (str): Priority level of the ticket.
        queue (str): Queue to which the ticket belongs.
    """
    id: str
    title: str
    description: str
    status: str
    priority: str
    queue: str


# List of mocked tickets used for testing
"""List of mocked tickets used for testing.

This list contains several instances of `MockedTicket` that simulate
tickets in an OTOBO system. They are used in unit tests to verify the
behavior of the OTOBOAdapter and its interactions with the OTOBO client.
"""
TICKETS = [
    MockedTicket(
        id="1",
        title="Test Ticket 1",
        description="Description 1",
        status="open",
        priority="high",
        queue="default",
    ),
    MockedTicket(
        id="2",
        title="Test Ticket 2",
        description="Description 2",
        status="closed",
        priority="low",
        queue="default",
    ),
    MockedTicket(
        id="3",
        title="Test Ticket 3",
        description="Description 3",
        status="open",
        priority="medium",
        queue="default",
    ),
    MockedTicket(
        id="4",
        title="Test Ticket 4",
        description="Description 4",
        status="open",
        priority="medium",
        queue="misc",
    ),
]


class MockedOTOBOClient(OTOBOClient):
    def __init__(
        self,
        ticket_data: list[MockedTicket]
    ):
        super().__init__(
            OTOBOClientConfig(
                base_url="https://mocked.otobo.example.com",
                service="GenericTicketConnector",
                auth=None,
                operations={
                    otobo.TicketOperation.SEARCH: "/search",
                    otobo.TicketOperation.UPDATE: "/update",
                   otobo.TicketOperation.GET: "/get",
                },
            ),
        )
        self.ticket_data = ticket_data

    async def search_and_get(self, query):
        return

    async def update_ticket(self, payload):
        return await super().update_ticket(payload)


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
        "OTOBOServerConfig(server_address=https://otobo.example.com, "
        "webservice_name=GenericTicketConnector, search_operation_url=/search, "
        "update_operation_url=/update, get_operation_url=/get, username=root)"
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
