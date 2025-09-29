from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from open_ticket_ai.basic_pipes.ticket_system_pipes.fetch_tickets_pipe import (
    FetchTicketsPipe,
)
from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedTicket,
)


@pytest.fixture
def pipeline_context() -> Context:
    return Context(pipes={}, config={})


@pytest.fixture
def search_criteria() -> TicketSearchCriteria:
    return TicketSearchCriteria(
        queue=UnifiedEntity(id="42", name="Support"),
        limit=25,
        offset=5,
    )


@pytest.fixture
def ticket_service() -> MagicMock:
    service = MagicMock(spec=TicketSystemService)
    service.find_tickets = AsyncMock()
    return service


@pytest.fixture
def mock_registry(ticket_service: MagicMock) -> MagicMock:
    mock_reg = MagicMock(spec=UnifiedRegistry)
    mock_reg.get_instance.return_value = ticket_service
    return mock_reg


@pytest.fixture
def pipe_config_dict(search_criteria: TicketSearchCriteria) -> dict:
    return {
        "name": "ticket_fetcher",
        "use": "open_ticket_ai.basic_pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        "ticket_system_id": "test_ticket_system",
        "ticket_search_criteria": search_criteria.model_dump(),
        "when": True,
        "steps": [],
    }


def _build_ticket(ticket_id: int, subject: str) -> UnifiedTicket:
    return UnifiedTicket(
        id=str(ticket_id),
        subject=subject,
        queue=UnifiedEntity(id="42", name="Support"),
        body=f"Body for {subject}",
    )


def test_process_serializes_results(
        pipe_config_dict: dict,
        ticket_service: MagicMock,
        pipeline_context: Context,
        mock_registry: MagicMock,
        search_criteria: TicketSearchCriteria,
) -> None:
    expected_tickets = [_build_ticket(1, "First"), _build_ticket(2, "Second")]
    ticket_service.find_tickets.return_value = expected_tickets

    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        pipe = FetchTicketsPipe(pipe_config_dict)

        result_context = asyncio.run(pipe.process(pipeline_context))

        mock_registry.get_instance.assert_called_once_with("test_ticket_system")

        state = result_context.pipes["ticket_fetcher"]
        assert state["found_tickets"] == [ticket.model_dump() for ticket in expected_tickets]

        assert ticket_service.find_tickets.await_count == 1
        args, _ = ticket_service.find_tickets.await_args
        criteria = args[0]
        assert isinstance(criteria, TicketSearchCriteria)
        assert criteria.queue.id == "42"
        assert criteria.limit == 25
        assert criteria.offset == 5


def test_process_without_results_returns_empty_list(
        pipe_config_dict: dict,
        ticket_service: MagicMock,
        pipeline_context: Context,
        mock_registry: MagicMock,
) -> None:
    ticket_service.find_tickets.return_value = []

    with patch.object(UnifiedRegistry, "get_registry_instance", return_value=mock_registry):
        pipe = FetchTicketsPipe(pipe_config_dict)

        result_context = asyncio.run(pipe.process(pipeline_context))

        assert result_context.pipes["ticket_fetcher"] == {"found_tickets": []}
