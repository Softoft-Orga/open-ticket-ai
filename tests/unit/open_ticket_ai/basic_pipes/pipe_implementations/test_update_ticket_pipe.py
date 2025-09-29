"""Unit tests for the UpdateTicketPipe behaviour."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.base_extensions import pipe_configs
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedTicket


@dataclass
class UpdateTicketPipeModelStub:
    """Minimal stub mirroring the fields used by ``UpdateTicketPipe``."""

    ticket_id: str | int | None
    ticket: dict[str, Any] | None


# Ensure the update ticket module can import the expected symbols even though the
# real implementations are not available in this trimmed test environment.
class UpdateTicketPipeConfigStub:  # pragma: no cover - attribute shim for import
    pass


if not hasattr(pipe_configs, "UpdateTicketPipeConfig"):
    pipe_configs.UpdateTicketPipeConfig = UpdateTicketPipeConfigStub  # type: ignore[attr-defined]

if not hasattr(pipe_configs, "UpdateTicketPipeModel"):
    pipe_configs.UpdateTicketPipeModel = UpdateTicketPipeModelStub  # type: ignore[attr-defined]

update_ticket_module = importlib.import_module("open_ticket_ai.base_extensions.ticket_system_pipes.update_ticket_pipe")
UpdateTicketPipe = update_ticket_module.UpdateTicketPipe


class ConcreteUpdateTicketPipe(UpdateTicketPipe):
    """Concrete subclass used only for testing to satisfy abstract base requirements."""

    @staticmethod
    def get_raw_config_model_type():  # pragma: no cover - only required for instantiation
        return UpdateTicketPipeConfigStub


@pytest.fixture
def pipeline_context() -> PipelineContext:
    """Return a fresh pipeline context for each test."""

    return PipelineContext(pipes={}, config={})


@pytest.fixture
def mock_ticket_system() -> MagicMock:
    """Create an async-capable ticket system mock."""

    ticket_system = MagicMock()
    ticket_system.update_ticket = AsyncMock()
    return ticket_system


@pytest.fixture
def update_pipe(mock_ticket_system: MagicMock) -> ConcreteUpdateTicketPipe:
    """Initialise the pipe with a mocked ticket system without relying on BasePipe."""

    pipe = ConcreteUpdateTicketPipe.__new__(ConcreteUpdateTicketPipe)
    pipe.ticket_system = mock_ticket_system
    pipe._logger = MagicMock()
    return pipe


class TestUpdateTicketPipe:
    """Behavioural tests for ``UpdateTicketPipe``."""

    @pytest.mark.asyncio
    async def test_process_success(
        self,
        update_pipe: UpdateTicketPipe,
        pipeline_context: PipelineContext,
        mock_ticket_system: MagicMock,
    ) -> None:
        ticket_payload = {
            "id": 42,
            "subject": "Updated subject",
            "body": "Updated body",
            "queue": {"id": 7, "name": "Support"},
        }
        config = UpdateTicketPipeModelStub(ticket_id="123", ticket=ticket_payload)

        result = await update_pipe._process(pipeline_context, config)

        assert result == {"success": True}
        mock_ticket_system.update_ticket.assert_awaited_once()
        call_args = mock_ticket_system.update_ticket.await_args
        assert call_args.args[0] == "123"
        assert isinstance(call_args.args[1], UnifiedTicket)
        assert call_args.args[1].subject == "Updated subject"
        assert call_args.args[1].queue == UnifiedEntity(id=7, name="Support")

    @pytest.mark.asyncio
    async def test_process_missing_ticket_id(
        self,
        update_pipe: UpdateTicketPipe,
        pipeline_context: PipelineContext,
        mock_ticket_system: MagicMock,
    ) -> None:
        config = UpdateTicketPipeModelStub(ticket_id=None, ticket={"subject": "data"})

        result = await update_pipe._process(pipeline_context, config)

        assert result == {
            "success": False,
            "error": "No ticket ID provided for update operation",
        }
        mock_ticket_system.update_ticket.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_missing_ticket_data(
        self,
        update_pipe: UpdateTicketPipe,
        pipeline_context: PipelineContext,
        mock_ticket_system: MagicMock,
    ) -> None:
        config = UpdateTicketPipeModelStub(ticket_id="123", ticket=None)

        result = await update_pipe._process(pipeline_context, config)

        assert result == {
            "success": False,
            "error": "No ticket data provided for update operation",
        }
        mock_ticket_system.update_ticket.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_handles_ticket_system_error(
        self,
        update_pipe: UpdateTicketPipe,
        pipeline_context: PipelineContext,
        mock_ticket_system: MagicMock,
    ) -> None:
        mock_ticket_system.update_ticket.side_effect = Exception("API unavailable")
        config = UpdateTicketPipeModelStub(
            ticket_id="123",
            ticket={"subject": "data"},
        )

        result = await update_pipe._process(pipeline_context, config)

        assert result == {
            "success": False,
            "error": "Failed to update ticket: API unavailable",
        }
        mock_ticket_system.update_ticket.assert_awaited_once()

    def test_convert_to_unified_ticket(
        self,
        update_pipe: UpdateTicketPipe,
    ) -> None:
        ticket_payload = {
            "id": 5,
            "subject": "Subject",
            "body": "Body",
            "queue": {"id": 2, "name": "Sales"},
        }

        unified_ticket = update_pipe._convert_to_unified_ticket(ticket_payload)

        assert isinstance(unified_ticket, UnifiedTicket)
        assert unified_ticket.id == 5
        assert unified_ticket.queue == UnifiedEntity(id=2, name="Sales")
        assert unified_ticket.body == "Body"
