from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket

from open_ticket_ai.pipes.ticket_system_pipes.update_ticket_pipe import UpdateTicketPipe

pytestmark = [pytest.mark.unit]


@pytest.fixture
def ticket_system() -> MagicMock:
    m = MagicMock(spec=TicketSystemService)
    m.update_ticket = AsyncMock(return_value=True)
    return m


async def test_update_ticket_pipe_static_resolvers(ticket_system: MagicMock):
    updates = UnifiedTicket(subject="New")
    pipe = UpdateTicketPipe("upd", ticket_system, "T-1", updates)

    result = await pipe.process(PipeContext.empty())

    assert result.succeeded
    ticket_system.update_ticket.assert_awaited_once_with(ticket_id="T-1", updates=updates)


async def test_update_ticket_pipe_callable_resolvers(ticket_system: MagicMock):
    ctx = PipeContext.empty().with_pipe_result(
        "fetch",
        PipeResult.success(
            data={"fetched_tickets": [UnifiedTicket(id="tid", subject="S").model_dump()]},
        ),
    )
    updates = UnifiedTicket(subject="U")

    pipe = UpdateTicketPipe(
        "upd",
        ticket_system,
        lambda c: c.get_result("fetch", "fetched_tickets")[0]["id"],
        lambda _c: updates,
    )

    result = await pipe.process(ctx)

    assert result.succeeded
    ticket_system.update_ticket.assert_awaited_once_with(ticket_id="tid", updates=updates)
