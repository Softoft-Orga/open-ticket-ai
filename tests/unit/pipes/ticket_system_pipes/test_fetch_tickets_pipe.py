from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedTicket

from open_ticket_ai.pipes.ticket_system_pipes.fetch_tickets_pipe import FetchTicketsPipe

pytestmark = [pytest.mark.unit]


@pytest.fixture
def ticket_system() -> MagicMock:
    m = MagicMock(spec=TicketSystemService)
    m.find_tickets = AsyncMock()
    return m


async def test_fetch_tickets_pipe_returns_dicts(ticket_system: MagicMock):
    tickets = [
        UnifiedTicket(id="1", subject="A"),
        UnifiedTicket(id="2", subject="B"),
    ]
    ticket_system.find_tickets.return_value = tickets
    criteria = TicketSearchCriteria(limit=10)

    pipe = FetchTicketsPipe("fetch", ticket_system, criteria)
    result = await pipe.process(PipeContext.empty())

    assert result.succeeded
    fetched = result.data["fetched_tickets"]
    assert fetched == [t.model_dump() for t in tickets]
    ticket_system.find_tickets.assert_awaited_once_with(criteria)


async def test_fetch_tickets_pipe_empty_fail_on_empty(ticket_system: MagicMock):
    ticket_system.find_tickets.return_value = []
    pipe = FetchTicketsPipe("fetch", ticket_system, TicketSearchCriteria(), fail_on_empty=True)

    result = await pipe.process(PipeContext.empty())

    assert result.has_failed()
    assert "No tickets" in result.message


async def test_fetch_tickets_pipe_empty_allow(ticket_system: MagicMock):
    ticket_system.find_tickets.return_value = []
    pipe = FetchTicketsPipe("fetch", ticket_system, TicketSearchCriteria(), fail_on_empty=False)

    result = await pipe.process(PipeContext.empty())

    assert result.succeeded
    assert result.data["fetched_tickets"] == []
