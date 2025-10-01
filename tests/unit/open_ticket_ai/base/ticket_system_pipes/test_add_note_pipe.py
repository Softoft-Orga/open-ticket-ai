import pytest

from open_ticket_ai.base.ticket_system_pipes.add_note_pipe import AddNotePipe
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote
from tests.unit.factories import PipeConfigFactory, UnifiedNoteFactory


def test_add_note_pipe_calls_ticket_system(
        pipe_runner,
        empty_pipeline_context,
        mock_ticket_system_service,
) -> None:
    note = UnifiedNoteFactory.build()
    config = PipeConfigFactory.build(
        ticket_id="TCK-123",
        note=note.model_dump(),
    )

    result_context = pipe_runner(AddNotePipe, config, empty_pipeline_context)

    mock_ticket_system_service.add_note.assert_awaited_once()
    call_args = mock_ticket_system_service.add_note.call_args
    assert call_args[0][0] == "TCK-123"
    assert isinstance(call_args[0][1], UnifiedNote)
    assert "test_pipe" in result_context.pipes


@pytest.mark.parametrize("note_input,expected_body", [
    ("Simple string note", "Simple string note"),
    ({"body": "Dict note"}, "Dict note"),
])
def test_add_note_pipe_handles_different_inputs(
        pipe_runner,
        empty_pipeline_context,
        mock_ticket_system_service,
        note_input,
        expected_body,
) -> None:
    config = {
        "ticket_system_id": "test_system",
        "ticket_id": "TCK-123",
        "note": note_input,
    }

    pipe_runner(AddNotePipe, config, empty_pipeline_context)

    call_args = mock_ticket_system_service.add_note.call_args
    assert isinstance(call_args[0][1], UnifiedNote)
    assert call_args[0][1].body == expected_body


def test_add_note_pipe_handles_failure(
        pipe_runner,
        empty_pipeline_context,
        mock_ticket_system_service,
) -> None:
    mock_ticket_system_service.add_note.side_effect = RuntimeError("Service unavailable")

    config = {
        "ticket_system_id": "test_system",
        "ticket_id": "TCK-123",
        "note": "Test note",
    }

    result_context = pipe_runner(AddNotePipe, config, empty_pipeline_context)
    
    # Pipe should catch exception and return failed result
    pipe_result = list(result_context.pipes.values())[0]
    assert pipe_result.failed is True
    assert pipe_result.success is False
    assert "Service unavailable" in pipe_result.message


def test_add_note_pipe_skips_when_disabled(
        pipe_runner,
        empty_pipeline_context,
        mock_ticket_system_service,
) -> None:
    config = {
        "ticket_system_id": "test_system",
        "ticket_id": "TCK-123",
        "note": "Test note",
        "_if": False,
    }

    result_context = pipe_runner(AddNotePipe, config, empty_pipeline_context)

    mock_ticket_system_service.add_note.assert_not_called()
    assert result_context is empty_pipeline_context
