from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote

from otai_base.pipes.ticket_system_pipes.add_note_pipe import AddNotePipe

pytestmark = [pytest.mark.unit]


@pytest.fixture
def ticket_system() -> MagicMock:
    m = MagicMock(spec=TicketSystemService)
    m.add_note = AsyncMock(return_value=True)
    return m


async def test_add_note_pipe_static_resolvers(ticket_system: MagicMock):
    note = UnifiedNote(subject="Hi", body="Body")
    pipe = AddNotePipe("note", ticket_system, "T-9", note)

    result = await pipe.process(PipeContext.empty())

    assert result.succeeded
    ticket_system.add_note.assert_awaited_once_with("T-9", note)


async def test_add_note_pipe_callable_resolvers(ticket_system: MagicMock):
    ctx = PipeContext.empty().with_pipe_result(
        "fetch",
        PipeResult.success(data={"ticket_id": "dynamic-id"}),
    )
    note = UnifiedNote(body="N")

    pipe = AddNotePipe(
        "note",
        ticket_system,
        lambda c: c.get_result("fetch", "ticket_id"),
        lambda _c: note,
    )

    result = await pipe.process(ctx)

    assert result.succeeded
    ticket_system.add_note.assert_awaited_once_with("dynamic-id", note)
