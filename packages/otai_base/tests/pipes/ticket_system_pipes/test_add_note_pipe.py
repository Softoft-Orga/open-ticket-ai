import pytest
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote
from packages.otai_base.src.otai_base.pipes.ticket_system_pipes import (
    AddNoteParams,
    AddNotePipe,
)
from pydantic import ValidationError

EXPECTED_TICKET_NOTE_COUNT = 2


@pytest.mark.parametrize("ticket_id", ["TICKET-1", "TICKET-2", "TICKET-3"])
@pytest.mark.asyncio
async def test_add_note_pipe_adds_note_to_ticket(mocked_ticket_system, logger_factory, ticket_id):
    new_note = UnifiedNote(subject=f"New note for {ticket_id}", body="Test note body")

    config = PipeConfig(
        id=f"add_note_to_{ticket_id}",
        use="open_ticket_ai.otai_base.pipes.ticket_system_pipes.add_note_pipe.AddNotePipe",
        params={"ticket_id": ticket_id, "note": new_note.model_dump()},
    )

    pipe = AddNotePipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    result = await pipe._process()
    assert result.succeeded is True

    ticket = await mocked_ticket_system.get_ticket(ticket_id)
    assert ticket is not None
    assert ticket.notes is not None

    note_subjects = [note.subject for note in ticket.notes]
    assert f"New note for {ticket_id}" in note_subjects

    if ticket_id == "TICKET-2":
        assert len(ticket.notes) == EXPECTED_TICKET_NOTE_COUNT
        assert "Initial note" in note_subjects
        assert f"New note for {ticket_id}" in note_subjects


def test_add_note_pipe_validation_subject_int():
    with pytest.raises(ValidationError):
        AddNoteParams(ticket_id="TICKET-1", note={"subject": 123, "body": "Test"})


def test_add_note_pipe_validation_subject_dict():
    with pytest.raises(ValidationError):
        AddNoteParams(ticket_id="TICKET-1", note={"subject": {"key": "value"}, "body": "Test"})
