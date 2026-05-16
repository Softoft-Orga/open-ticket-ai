from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote
from tests.mocked_ticket_system import MockedTicketSystem

pytestmark = [pytest.mark.unit]


class SimplePipe(Pipe):
    def __init__(self, pipe_id: str = "simple", value: str = "default_value") -> None:
        super().__init__(pipe_id)
        self.value = value

    async def _process(self, context: PipeContext) -> PipeResult:
        return PipeResult.success(data={"value": self.value})


@pytest.fixture
def empty_pipeline_context() -> PipeContext:
    return PipeContext.empty()


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    mock.get_ticket = AsyncMock(return_value={})
    return mock


@pytest.fixture
def empty_mocked_ticket_system() -> MockedTicketSystem:
    return MockedTicketSystem()


@pytest.fixture(scope="function")
def mocked_ticket_system() -> MockedTicketSystem:
    system = MockedTicketSystem()
    system.clear_all_data()

    system.add_test_ticket(
        id="TICKET-1",
        subject="Test ticket 1",
        body="This is the first test ticket",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
        notes=[],
    )
    system.add_test_ticket(
        id="TICKET-2",
        subject="Test ticket 2",
        body="This is the second test ticket",
        queue=UnifiedEntity(id="2", name="Development"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[
            UnifiedNote(id="NOTE-1", subject="Initial note", body="First note on ticket 2"),
        ],
    )
    system.add_test_ticket(
        id="TICKET-3",
        subject="Urgent issue",
        body="This needs immediate attention",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[],
    )

    yield system
    system.clear_all_data()
