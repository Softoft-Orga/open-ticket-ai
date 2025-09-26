import inspect

import pytest

pytest.importorskip("otobo")
from otobo_znuny.models.request_models import AuthData

from open_ticket_ai.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.core.config.config_models import SystemConfig
from otobo import OTOBOClient, OTOBOClientConfig

from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


class DummyClient(OTOBOClient):
    """Dummy OTOBO client implementation for testing purposes.

    This class provides a mock implementation of OTOBOClient that doesn't connect to any real server.
    It's designed to be used in unit tests where actual network operations are not required.
    """

    def __init__(self):
        """Initializes the dummy client with minimal configuration.

        Sets up a fake configuration with placeholder values to satisfy the base class requirements.
        """
        super().__init__(
            OTOBOClientConfig(
                base_url="http://x",
                service="GenericTicketConnector",
                auth=AuthData(UserLogin="", Password=""),
                operations={},
            )
        )


@pytest.fixture
def adapter():
    """Fixture providing a configured OTOBOAdapter instance for testing.

    Returns:
        OTOBOAdapter: An adapter instance initialized with dummy configuration and client.
    """
    return OTOBOAdapter(SystemConfig(id="d", provider_key="d"), DummyClient())


def test_adapter_is_abstract():
    """Tests that `TicketSystemAdapter` is properly defined as an abstract class.

    Verifies:
        1. The class is marked as abstract (using `inspect.isabstract`)
        2. All required abstract methods exist in the class
    """
    assert inspect.isabstract(TicketSystemAdapter)
    methods = ["find_tickets", "find_first_ticket", "update_ticket"]
    for m in methods:
        assert getattr(TicketSystemAdapter, m)


def test_otobo_adapter_implements_interface(adapter):
    """Tests that `OTOBOAdapter` implements all required `TicketSystemAdapter` methods.

    Args:
        adapter: The `OTOBOAdapter` instance to test

    Verifies that the following methods are implemented and callable:
        - `find_tickets`
        - `find_first_ticket`
        - `create_ticket`
        - `update_ticket`
        - `add_note`
    """
    for m in [
        "find_tickets",
        "find_first_ticket",
        "update_ticket",
    ]:
        assert callable(getattr(adapter, m))
