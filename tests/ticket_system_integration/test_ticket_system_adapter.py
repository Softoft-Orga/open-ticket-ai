import inspect
import os
import sys

import pytest

# Ensure the project root is on the import path so the ``open_ticket_ai``
# package can be resolved when tests are executed from the ``tests`` folder.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote,
    UnifiedPriority,
    UnifiedQueue,
    UnifiedTicket,
)
from open_ticket_ai.src.core.config.config_models import SystemConfig
from otobo import OTOBOClient, OTOBOClientConfig, TicketSearchRequest, TicketUpdateRequest
from otobo.models.request_models import AuthData
from otobo.models.ticket_models import TicketBase, ArticleDetail


class DummyClient(OTOBOClient):
    """Dummy OTOBO client implementation for testing purposes."""

    def __init__(self):
        super().__init__(
            OTOBOClientConfig(
                base_url="http://x",
                service="GenericTicketConnector",
                auth=AuthData(UserLogin="", Password=""),
                operations={},
            )
        )
        self.created = None
        self.updated = None
        self.notes = []

    async def search_and_get(self, query: TicketSearchRequest):
        ticket = TicketBase(
            TicketID=1,
            Title="Dummy",
            QueueID=2,
            Queue="Support",
            PriorityID=3,
            Priority="High",
            Article=[ArticleDetail(Body="Body", Subject="Subject")],
        )
        return [ticket]

    async def update_ticket(self, payload: TicketUpdateRequest):
        self.updated = payload
        return True

    async def create_ticket(self, payload):
        self.created = payload
        return 1

    async def add_note(self, ticket_id, note):
        self.notes.append((ticket_id, note))
        return True


@pytest.fixture
def adapter():
    return OTOBOAdapter(SystemConfig(id="d", provider_key="d"), DummyClient())


def test_adapter_is_abstract():
    """TicketSystemAdapter should define the expected abstract methods."""

    assert inspect.isabstract(TicketSystemAdapter)
    methods = [
        "find_tickets",
        "find_first_ticket",
        "create_ticket",
        "update_ticket",
        "add_note",
    ]
    for name in methods:
        assert getattr(TicketSystemAdapter, name)


def test_otobo_adapter_implements_interface(adapter):
    """Concrete adapter should implement all interface methods."""

    for name in [
        "find_tickets",
        "find_first_ticket",
        "create_ticket",
        "update_ticket",
        "add_note",
    ]:
        assert callable(getattr(adapter, name))


def test_find_first_ticket_returns_unified_model(adapter):
    """Ensure that find_first_ticket returns a UnifiedTicket instance."""

    criteria = TicketSearchCriteria(queue=UnifiedQueue(name="Support"))
    import asyncio

    ticket = asyncio.get_event_loop().run_until_complete(
        adapter.find_first_ticket(criteria)
    )
    assert ticket.id == "1"
    assert ticket.queue.name == "Support"
    assert ticket.notes[0].body == "Body"


def test_unified_ticket_roundtrip():
    """UnifiedTicket should retain nested data when dumped."""

    queue = UnifiedQueue(id="1", name="Q")
    priority = UnifiedPriority(id="2", name="High")
    note = UnifiedNote(subject="s", body="b")
    ticket = UnifiedTicket(
        id="42",
        subject="Subj",
        body="Body",
        queue=queue,
        priority=priority,
        notes=[note],
    )
    dumped = ticket.model_dump()
    assert dumped["queue"]["name"] == "Q"
    assert dumped["notes"][0]["body"] == "b"
