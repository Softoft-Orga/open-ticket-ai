import pytest

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote
from tests.mocked_ticket_system import MockedTicketSystem

pytestmark = [pytest.mark.integration]


@pytest.fixture
def integration_empty_pipe_context() -> PipeContext:
    return PipeContext.empty()


@pytest.fixture
def integration_mocked_ticket_system() -> MockedTicketSystem:
    system = MockedTicketSystem()
    system.clear_all_data()

    system.add_test_ticket(
        id="TICKET-INT-001",
        subject="Integration test ticket 1",
        body="This is a test ticket for integration testing",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
        notes=[],
    )
    system.add_test_ticket(
        id="TICKET-INT-002",
        subject="Integration test ticket 2",
        body="Another test ticket with high priority",
        queue=UnifiedEntity(id="2", name="Development"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[
            UnifiedNote(id="NOTE-1", subject="Test note", body="This is a test note"),
        ],
    )

    yield system
    system.clear_all_data()
