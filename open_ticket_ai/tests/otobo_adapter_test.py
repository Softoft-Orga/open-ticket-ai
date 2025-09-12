"""This module contains unit tests for the OTOBOAdapter.

The tests include:
    - Testing the configuration of the OTOBOAdapterConfig
    - Testing the behavior of the OTOBOAdapter using a mocked OTOBO client

The tests are designed to run without requiring a real OTOBO server connection.
"""
import dataclasses

import otobo
from otobo import OTOBOClient, OTOBOClientConfig
import pytest

from open_ticket_ai.src.core.config.config_models import SystemConfig
from open_ticket_ai.src.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.src.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig


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
    """Mocked OTOBOAdapter for testing purposes.

    This class is used to create an instance of OTOBOAdapter with a mocked OTOBOClient.
    It allows testing without requiring a real OTOBO server connection.

    Attributes:
        ticket_data (list[MockedTicket]): List of mocked tickets used for testing.
    """

    @staticmethod
    def get_description() -> str:
        """Returns a static description string for the mocked client.

        Returns:
            str: The description string.
        """
        return "Mocked OTOBO adapter for testing purposes."

    def __init__(
        self,
        ticket_data: list[MockedTicket]
    ):
        """Initializes the mocked OTOBO client.

        Args:
            ticket_data (list[MockedTicket]): A list of mocked tickets to be used for testing.
        """
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
        """Mocks the search_and_get operation.

        This method is a placeholder and does nothing.

        Args:
            query: The search query.
        """
        return

    async def update_ticket(self, payload):
        """Updates a ticket by delegating to the parent class method.

        Args:
            payload (dict): The ticket update payload.

        Returns:
            The result of the update operation from the parent class.
        """
        return await super().update_ticket(payload)


@pytest.fixture
def adapter_and_client():
    """Fixture that provides an instance of OTOBOAdapter and a mocked OTOBOClient.

    Returns:
        tuple: A tuple containing:
            adapter (OTOBOAdapter): Configured OTOBOAdapter instance
            client (AsyncMock): Mocked OTOBOClient instance
    """
    client = MockedOTOBOClient(TICKETS)
    config = SystemConfig(id="dummy", provider_key="dummy", params={})
    adapter = OTOBOAdapter(config=config, otobo_client=client)
    return adapter, client


def test_config_str_and_password(monkeypatch):
    """Test the string representation and password retrieval of OTOBOAdapterConfig.

    This test verifies two aspects of the OTOBOAdapterConfig:
      1. The `__str__` method returns a string that excludes the password value.
      2. The password property correctly retrieves the password from an environment variable.

    Args:
        monkeypatch: Pytest fixture for safely patching environment variables.

    Steps:
        - Set an environment variable for the password.
        - Create an instance of OTOBOAdapterConfig with the environment variable name for the password.
        - Check that the string representation of the config does not include the password.
        - Check that the password property returns the value from the environment variable.
    """
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
    """Test that OTOBOAdapterConfig raises an error when the password environment variable is missing.

    This test ensures that when the environment variable specified for the password is not set,
    accessing the password property of OTOBOAdapterConfig raises a ValueError.

    Args:
        monkeypatch: Pytest fixture for safely patching environment variables.

    Steps:
        - Ensure the environment variable (which is set to a non-existent one) is deleted.
        - Create an instance of OTOBOAdapterConfig with the non-existent environment variable for the password.
        - Attempt to access the password property and expect a ValueError.
    """
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
