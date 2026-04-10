from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote

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
    mock.find_tickets = AsyncMock(return_value=[])
    return mock
