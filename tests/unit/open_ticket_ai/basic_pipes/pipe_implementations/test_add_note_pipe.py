import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from open_ticket_ai.basic_pipes.ticket_system_pipes.add_note_pipe import (
    AddNotePipe,
)
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


@pytest.fixture
def mock_ticket_system() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.add_note = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def sample_note() -> UnifiedNote:
    return UnifiedNote(content="Test Note Content")


@pytest.fixture
def pipe_config_dict(sample_note: UnifiedNote) -> dict:
    return {
        "name": "test_add_note",
        "use": "open_ticket_ai.basic_pipes.ticket_system_pipes.add_note_pipe.AddNotePipe",
        "when": True,
        "steps": [],
        "ticket_system_id": "test_ticket_system",
        "ticket_id": "TCK-123",
        "note": sample_note.model_dump(),
    }


@pytest.fixture
def mock_registry(mock_ticket_system: MagicMock) -> MagicMock:
    mock_reg = MagicMock(spec=UnifiedRegistry)
    mock_reg.get_instance.return_value = mock_ticket_system
    return mock_reg


@pytest.fixture
def sample_context() -> Context:
    """Return an empty pipeline context."""
    return Context(pipes={}, config={})


def test_add_note_pipe_calls_ticket_system(
        pipe_config_dict: dict,
        sample_context: Context,
        mock_ticket_system: MagicMock,
        sample_note: UnifiedNote,
        mock_registry: MagicMock,
) -> None:
    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        pipe = AddNotePipe(pipe_config_dict)

        result_context = asyncio.run(pipe.process(sample_context))

        mock_registry.get_instance.assert_called_once_with("test_ticket_system")
        mock_ticket_system.add_note.assert_awaited_once()

        # Check the note argument - it should be a UnifiedNote instance
        call_args = mock_ticket_system.add_note.call_args
        assert call_args[0][0] == "TCK-123"
        assert isinstance(call_args[0][1], UnifiedNote)

        assert result_context.pipes["test_add_note"] == {}


def test_add_note_pipe_handles_failure(
        pipe_config_dict: dict,
        sample_context: Context,
        mock_ticket_system: MagicMock,
        mock_registry: MagicMock,
) -> None:
    mock_ticket_system.add_note.side_effect = RuntimeError("Service unavailable")

    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        pipe = AddNotePipe(pipe_config_dict)

        # Verify the exception bubbles up
        with pytest.raises(RuntimeError, match="Service unavailable"):
            asyncio.run(pipe.process(sample_context))

        mock_ticket_system.add_note.assert_awaited_once()


def test_add_note_pipe_with_string_note(
        sample_context: Context,
        mock_ticket_system: MagicMock,
        mock_registry: MagicMock,
) -> None:
    config = {
        "name": "test_add_note",
        "use": "AddNotePipe",
        "when": True,
        "steps": [],
        "ticket_system_id": "test_ticket_system",
        "ticket_id": "TCK-123",
        "note": "Simple string note",
    }

    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        pipe = AddNotePipe(config)

        result_context = asyncio.run(pipe.process(sample_context))

        # Check the note was converted to UnifiedNote
        call_args = mock_ticket_system.add_note.call_args
        assert isinstance(call_args[0][1], UnifiedNote)
        assert call_args[0][1].content == "Simple string note"

        assert result_context.pipes["test_add_note"] == {}


def test_add_note_pipe_skips_when_disabled(
        pipe_config_dict: dict,
        sample_context: Context,
        mock_ticket_system: MagicMock,
        mock_registry: MagicMock,
) -> None:
    pipe_config_dict["when"] = False

    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        pipe = AddNotePipe(pipe_config_dict)

        result_context = asyncio.run(pipe.process(sample_context))

        mock_ticket_system.add_note.assert_not_called()

        assert result_context is sample_context
