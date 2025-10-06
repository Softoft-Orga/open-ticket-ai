import pytest

from open_ticket_ai.base.ticket_system_pipes.add_note_pipe import AddNotePipe
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


@pytest.mark.asyncio
async def test_add_note_pipe_adds_note_to_ticket(
    empty_pipeline_context,
    mocked_ticket_system,
):
    """Test that AddNotePipe successfully adds a note to a ticket."""
    config = {
        "id": "test_add_note",
        "use": "AddNotePipe",
        "_if": True,
        "ticket_id": "TICKET-1",
        "note": {"body": "This is a new note"},
    }

    pipe = AddNotePipe(mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify the note was added to the ticket
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert len(ticket.notes) == 1
    assert ticket.notes[0].body == "This is a new note"

    # Verify pipe result
    pipe_result = result_context.pipes["test_add_note"]
    assert pipe_result.success is True
    assert pipe_result.failed is False


@pytest.mark.asyncio
async def test_add_note_pipe_with_note_object(
    empty_pipeline_context,
    mocked_ticket_system,
):
    """Test adding a note using a UnifiedNote object."""
    note = UnifiedNote(subject="Test Subject", body="Note body with subject")
    config = {
        "id": "test_add_note",
        "use": "AddNotePipe",
        "_if": True,
        "ticket_id": "TICKET-2",
        "note": note,
    }

    pipe = AddNotePipe(mocked_ticket_system, config)
    await pipe.process(empty_pipeline_context)

    # Verify note was added with correct fields
    ticket = await mocked_ticket_system.get_ticket("TICKET-2")
    assert len(ticket.notes) == 2  # Already has 1 note in fixture
    assert ticket.notes[1].subject == "Test Subject"
    assert ticket.notes[1].body == "Note body with subject"


@pytest.mark.asyncio
async def test_add_note_pipe_handles_failure(
    empty_pipeline_context,
    empty_mocked_ticket_system,
):
    """Test that pipe handles failure when ticket doesn't exist."""
    config = {
        "id": "test_add_note",
        "use": "AddNotePipe",
        "_if": True,
        "ticket_id": "NONEXISTENT-TICKET",
        "note": {"body": "Test note"},
    }

    pipe = AddNotePipe(empty_mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Pipe should return failed result (add_note returns False for nonexistent ticket)
    pipe_result = result_context.pipes["test_add_note"]
    assert pipe_result.success is False
    assert pipe_result.failed is True


@pytest.mark.asyncio
async def test_add_note_pipe_skips_when_disabled(
    empty_pipeline_context,
    mocked_ticket_system,
):
    """Test that pipe skips when disabled."""
    config = {
        "id": "test_add_note",
        "use": "AddNotePipe",
        "if": False,
        "ticket_id": "TICKET-1",
        "note": {"body": "Test note"},
    }

    pipe = AddNotePipe(mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify pipe result
    # When disabled, the pipe should not execute and return original context
    assert result_context is empty_pipeline_context
    # Verify no note was added by checking the pipe result is not in the context
    assert "test_add_note" not in result_context.pipes
