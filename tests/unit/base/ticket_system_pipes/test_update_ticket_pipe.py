from __future__ import annotations

import pytest

from open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe import (
    UpdateTicketParams,
    UpdateTicketPipe,
    UpdateTicketPipeConfig,
)
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket
from tests.unit.mocked_ticket_system import MockedTicketSystem


@pytest.mark.asyncio
async def test_update_ticket_updates_subject(
    empty_pipeline_context: PipeContext,
    mocked_ticket_system: MockedTicketSystem,
) -> None:
    """Test that UpdateTicketPipe successfully updates ticket subject."""
    config = UpdateTicketPipeConfig(
        id="test_update",
        use="UpdateTicketPipe",
        params=UpdateTicketParams(
            ticket_id="TICKET-1",
            updated_ticket=UnifiedTicket(subject="Updated Subject"),
        ),
    )

    pipe = UpdateTicketPipe(mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify ticket was updated
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket.subject == "Updated Subject"
    assert ticket.body == "This is the first test ticket"  # Other fields unchanged

    # Verify pipe result
    pipe_result = result_context.pipes["test_update"]
    assert pipe_result.success is True
    assert pipe_result.failed is False


@pytest.mark.asyncio
async def test_update_ticket_updates_multiple_fields(
    empty_pipeline_context: PipeContext,
    mocked_ticket_system: MockedTicketSystem,
) -> None:
    """Test that UpdateTicketPipe can update multiple fields."""
    config = UpdateTicketPipeConfig(
        id="test_update",
        use="UpdateTicketPipe",
        params=UpdateTicketParams(
            ticket_id="TICKET-2",
            updated_ticket=UnifiedTicket(
                subject="New Subject",
                body="New body text",
            ),
        ),
    )

    pipe = UpdateTicketPipe(mocked_ticket_system, config)
    await pipe.process(empty_pipeline_context)

    # Verify both fields were updated
    ticket = await mocked_ticket_system.get_ticket("TICKET-2")
    assert ticket.subject == "New Subject"
    assert ticket.body == "New body text"
    assert ticket.queue.name == "Development"  # Queue unchanged


@pytest.mark.asyncio
async def test_update_ticket_handles_nonexistent_ticket(
    empty_pipeline_context: PipeContext,
    empty_mocked_ticket_system: MockedTicketSystem,
) -> None:
    """Test that pipe handles updating a nonexistent ticket."""
    config = UpdateTicketPipeConfig(
        id="test_update",
        use="UpdateTicketPipe",
        params=UpdateTicketParams(
            ticket_id="NONEXISTENT-TICKET",
            updated_ticket=UnifiedTicket(subject="Updated"),
        ),
    )

    pipe = UpdateTicketPipe(empty_mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Pipe should return failed result
    pipe_result = result_context.pipes["test_update"]
    assert pipe_result.failed is True
    assert pipe_result.success is False
