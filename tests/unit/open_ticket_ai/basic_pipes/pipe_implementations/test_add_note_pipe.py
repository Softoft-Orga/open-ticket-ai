import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.basic_pipes.ticket_system_pipes.add_note_pipe import (
    AddNotePipe,
    RenderedTicketAddNotePipeConfig,
)
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote
from tests.conftest import create_frozen_renderable_config
RenderedTicketAddNotePipeConfig.model_rebuild()

@pytest.fixture
def mock_ticket_system() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.add_note = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def sample_note() -> UnifiedNote:
    return UnifiedNote(subject="Test Subject", body="Test Body")


@pytest.fixture
def mock_config(sample_note: UnifiedNote, mock_ticket_system: MagicMock) -> MagicMock:
    rendered_config = RenderedTicketAddNotePipeConfig(
        id="test_add_note",
        use="open_ticket_ai.basic_pipes.ticket_system_pipes.add_note_pipe.AddNotePipe",
        when=True,
        ticket_id="TCK-123",
        note=sample_note,
        ticket_system=mock_ticket_system,
    )

    mock = MagicMock()
    mock.get_rendered_config.return_value = rendered_config
    return mock


@pytest.fixture
def frozen_config(
        sample_note: UnifiedNote, mock_ticket_system: MagicMock
):
    rendered_config = RenderedTicketAddNotePipeConfig(
        id="test_add_note",
        use="open_ticket_ai.basic_pipes.ticket_system_pipes.add_note_pipe.AddNotePipe",
        when=True,
        ticket_id="TCK-123",
        note=sample_note,
        ticket_system=mock_ticket_system,
    )
    return create_frozen_renderable_config(rendered_config)


@pytest.fixture
def sample_context() -> Context:
    """Return an empty pipeline context."""
    return Context(pipes={}, config={})


def test_add_note_pipe_calls_ticket_system(
        mock_config: MagicMock,
        sample_context: Context,
        mock_ticket_system: MagicMock,
        sample_note: UnifiedNote,
) -> None:
    pipe = AddNotePipe(mock_config)

    result_context = asyncio.run(pipe.process(sample_context))

    mock_ticket_system.add_note.assert_awaited_once_with("TCK-123", sample_note)

    assert result_context.pipes["test_add_note"] == {}


def test_add_note_pipe_handles_failure(
        mock_config: MagicMock,
        sample_context: Context,
        mock_ticket_system: MagicMock,
) -> None:
    mock_ticket_system.add_note.side_effect = RuntimeError("Service unavailable")

    pipe = AddNotePipe(mock_config)

    # Verify the exception bubbles up
    with pytest.raises(RuntimeError, match="Service unavailable"):
        asyncio.run(pipe.process(sample_context))

    mock_ticket_system.add_note.assert_awaited_once()


def test_add_note_pipe_with_frozen_config(
        frozen_config,
        sample_context: Context,
        mock_ticket_system: MagicMock,
        sample_note: UnifiedNote,
) -> None:
    pipe = AddNotePipe(frozen_config)

    result_context = asyncio.run(pipe.process(sample_context))

    mock_ticket_system.add_note.assert_awaited_once_with("TCK-123", sample_note)
    assert result_context.pipes["test_add_note"] == {}


def test_add_note_pipe_skips_when_disabled(
        mock_config: MagicMock,
        sample_context: Context,
        mock_ticket_system: MagicMock,
        sample_note: UnifiedNote,
) -> None:
    disabled_config = RenderedTicketAddNotePipeConfig(
        id="test_add_note",
        use="open_ticket_ai.basic_pipes.ticket_system_pipes.add_note_pipe.AddNotePipe",
        when=False,
        ticket_id="TCK-123",
        note=sample_note,
        ticket_system=mock_ticket_system,
    )
    mock_config.get_rendered_config.return_value = disabled_config

    pipe = AddNotePipe(mock_config)

    result_context = asyncio.run(pipe.process(sample_context))

    mock_ticket_system.add_note.assert_not_called()

    assert result_context is sample_context
