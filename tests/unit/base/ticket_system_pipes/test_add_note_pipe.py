from __future__ import annotations

import pytest

from open_ticket_ai.base.pipes.ticket_system_pipes import (
    AddNoteParams,
    AddNotePipe,
    AddNotePipeConfig,
)
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote
from tests.unit.mocked_ticket_system import MockedTicketSystem


@pytest.mark.asyncio
async def test_add_note_pipe_adds_note_to_ticket(
    empty_pipeline_context: PipeContext,
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test that AddNotePipe successfully adds a note to a ticket."""
    config = AddNotePipeConfig(
        id="test_add_note",
        use="AddNotePipe",
        params=AddNoteParams(
            ticket_id="TICKET-1",
            note=UnifiedNote(body="This is a new note"),
        ).model_dump(),
    )

    pipe = AddNotePipe(mocked_ticket_system, config, logger_factory)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify the note was added to the ticket
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket is not None
    assert ticket.notes is not None
    assert len(ticket.notes) == 1
    assert ticket.notes[0].body == "This is a new note"

    # Verify pipe result
    pipe_result = result_context.pipes["test_add_note"]
    assert pipe_result.success is True
    assert pipe_result.failed is False


@pytest.mark.asyncio
async def test_add_note_pipe_with_note_object(
    empty_pipeline_context: PipeContext,
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test adding a note using a UnifiedNote object."""
    note = UnifiedNote(subject="Test Subject", body="Note body with subject")
    config = AddNotePipeConfig(
        id="test_add_note",
        use="AddNotePipe",
        params=AddNoteParams(
            ticket_id="TICKET-2",
            note=note,
        ).model_dump(),
    )

    pipe = AddNotePipe(mocked_ticket_system, config, logger_factory)
    await pipe.process(empty_pipeline_context)

    # Verify note was added with correct fields
    ticket = await mocked_ticket_system.get_ticket("TICKET-2")
    assert ticket is not None
    assert ticket.notes is not None
    assert len(ticket.notes) == 2  # Already has 1 note in fixture
    assert ticket.notes[1].subject == "Test Subject"
    assert ticket.notes[1].body == "Note body with subject"


@pytest.mark.asyncio
async def test_add_note_pipe_handles_failure(
    empty_pipeline_context: PipeContext,
    empty_mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test that pipe handles failure when ticket doesn't exist."""
    config = AddNotePipeConfig(
        id="test_add_note",
        use="AddNotePipe",
        params=AddNoteParams(
            ticket_id="NONEXISTENT-TICKET",
            note=UnifiedNote(body="Test note"),
        ).model_dump(),
    )

    pipe = AddNotePipe(empty_mocked_ticket_system, config, logger_factory)
    result_context = await pipe.process(empty_pipeline_context)

    # Pipe should return failed result (add_note returns False for nonexistent ticket)
    pipe_result = result_context.pipes["test_add_note"]
    assert pipe_result.success is False
    assert pipe_result.failed is True


@pytest.mark.asyncio
async def test_add_note_pipe_skips_when_disabled(
    empty_pipeline_context: PipeContext,
    mocked_ticket_system: MockedTicketSystem,
    logger_factory: LoggerFactory,
) -> None:
    """Test that pipe skips when disabled."""
    config = AddNotePipeConfig(
        id="test_add_note",
        use="AddNotePipe",
        if_=False,
        params=AddNoteParams(
            ticket_id="TICKET-1",
            note=UnifiedNote(body="Test note"),
        ).model_dump(),
    )

    pipe = AddNotePipe(mocked_ticket_system, config, logger_factory)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify pipe result
    # When disabled, the pipe should not execute and return original context
    assert result_context is empty_pipeline_context
    # Verify no note was added by checking the pipe result is not in the context
    assert "test_add_note" not in result_context.pipes
