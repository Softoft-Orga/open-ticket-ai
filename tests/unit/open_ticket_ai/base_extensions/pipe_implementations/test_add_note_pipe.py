"""Tests for :mod:`open_ticket_ai.base_extensions.ticket_system_pipes.add_note_pipe`."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.base_extensions.pipe_configs import RawTicketAddNotePipeConfig
from open_ticket_ai.base_extensions.ticket_system_pipes.add_note_pipe import AddNotePipe
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


@pytest.fixture
def sample_note() -> UnifiedNote:
    """Return a reusable note instance for tests."""

    return UnifiedNote(subject="Test Subject", body="Test Body")


@pytest.fixture
def sample_config(sample_note: UnifiedNote) -> RawTicketAddNotePipeConfig:
    """Return a raw pipe config for the add note pipe."""

    return RawTicketAddNotePipeConfig(
        name="test_add_note",
        use="open_ticket_ai.base_extensions.ticket_system_pipes.add_note_pipe.AddNotePipe",
        ticket_id="TCK-123",
        note=sample_note,
    )


@pytest.fixture
def rendered_config_factory(sample_note: UnifiedNote):
    """Build rendered configurations returned by the pipe during processing."""

    def _factory(**overrides: object) -> SimpleNamespace:
        base_data = {
            "name": "test_add_note",
            "use": "open_ticket_ai.base_extensions.ticket_system_pipes.add_note_pipe.AddNotePipe",
            "when": True,
            "ticket_id": "TCK-123",
            "note": sample_note,
        }
        base_data.update(overrides)
        return SimpleNamespace(**base_data)

    return _factory


@pytest.fixture
def sample_context() -> PipelineContext:
    """Return an empty pipeline context."""

    return PipelineContext(pipes={}, config={})


@pytest.fixture
def mock_ticket_system() -> MagicMock:
    """Return a mock for :class:`TicketSystemService`."""

    return MagicMock(spec=TicketSystemService)


def test_init_assigns_ticket_system(sample_config: RawTicketAddNotePipeConfig, mock_ticket_system: MagicMock) -> None:
    """The pipe should keep a reference to the injected ticket system service."""

    pipe = AddNotePipe(sample_config, mock_ticket_system)

    assert pipe.ticket_system is mock_ticket_system
    assert pipe._BasePipe__raw_pipe_config is sample_config  # type: ignore[attr-defined]


class TestAddNotePipeProcess:
    """Tests covering :meth:`AddNotePipe.process`."""

    def test_process_adds_note(
        self,
        sample_config: RawTicketAddNotePipeConfig,
        sample_context: PipelineContext,
        mock_ticket_system: MagicMock,
        rendered_config_factory,
    ) -> None:
        """Processing should delegate to the ticket system and record an empty result."""

        mock_ticket_system.add_note = AsyncMock(return_value=True)
        pipe = AddNotePipe(sample_config, mock_ticket_system)
        pipe._current_context = sample_context
        rendered_config = rendered_config_factory()
        object.__setattr__(
            pipe._BasePipe__raw_pipe_config,  # type: ignore[attr-defined]
            "render",
            MagicMock(return_value=rendered_config),
        )

        result_context = asyncio.run(pipe.process(sample_context))

        assert result_context.pipes["test_add_note"] == {}
        await_args = mock_ticket_system.add_note.await_args
        assert await_args.args[0] == "TCK-123"
        assert await_args.args[1] is rendered_config.note

    def test_process_raises_on_failure(
        self,
        sample_config: RawTicketAddNotePipeConfig,
        sample_context: PipelineContext,
        mock_ticket_system: MagicMock,
        rendered_config_factory,
    ) -> None:
        """Exceptions from the ticket system should bubble up."""

        mock_ticket_system.add_note = AsyncMock(side_effect=RuntimeError("cannot add note"))
        pipe = AddNotePipe(sample_config, mock_ticket_system)
        pipe._current_context = sample_context
        object.__setattr__(
            pipe._BasePipe__raw_pipe_config,  # type: ignore[attr-defined]
            "render",
            MagicMock(return_value=rendered_config_factory()),
        )

        with pytest.raises(RuntimeError, match="cannot add note"):
            asyncio.run(pipe.process(sample_context))

        mock_ticket_system.add_note.assert_awaited_once()

    def test_process_skips_when_condition_false(
        self,
        sample_config: RawTicketAddNotePipeConfig,
        sample_context: PipelineContext,
        mock_ticket_system: MagicMock,
        rendered_config_factory,
    ) -> None:
        """The pipe should be skipped when the rendered config disables execution."""

        mock_ticket_system.add_note = AsyncMock()
        pipe = AddNotePipe(sample_config, mock_ticket_system)
        pipe._current_context = sample_context
        rendered_config = rendered_config_factory(when=False)
        object.__setattr__(
            pipe._BasePipe__raw_pipe_config,  # type: ignore[attr-defined]
            "render",
            MagicMock(return_value=rendered_config),
        )

        result_context = asyncio.run(pipe.process(sample_context))

        assert result_context is sample_context
        mock_ticket_system.add_note.assert_not_called()
