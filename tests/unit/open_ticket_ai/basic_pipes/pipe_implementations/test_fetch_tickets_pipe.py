from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

from open_ticket_ai.basic_pipes.ticket_system_pipes.fetch_tickets_pipe import (
    FetchTicketsPipe,
    RenderedTicketFetchPipeConfig,
)
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedTicket,
)


@pytest.fixture
def pipeline_context() -> Context:
    return Context(pipes={}, config={})


@pytest.fixture
def rendered_config(ticket_service: AsyncMock) -> RenderedTicketFetchPipeConfig:
    return RenderedTicketFetchPipeConfig(
        id="ticket_fetcher",
        use="open_ticket_ai.basic_pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        ticket_system=ticket_service,
        ticket_search_criteria=TicketSearchCriteria(
            queue=UnifiedEntity(id=42, name="Support"),
            limit=25,
            offset=5,
        ),
        when=True,
        steps=[],
    )


@pytest.fixture
def renderable_config(rendered_config: RenderedTicketFetchPipeConfig, frozen_config_factory):
    return frozen_config_factory(rendered_config)


@pytest.fixture
def ticket_service() -> AsyncMock:
    service = AsyncMock()
    service.find_tickets = AsyncMock()
    return service


def _build_ticket(ticket_id: int, subject: str) -> UnifiedTicket:
    return UnifiedTicket(
        id=ticket_id,
        subject=subject,
        queue=UnifiedEntity(id=42, name="Support"),
        body=f"Body for {subject}",
    )


def test_process_serializes_results(
        renderable_config, ticket_service: AsyncMock, pipeline_context: Context
) -> None:
    expected_tickets = [_build_ticket(1, "First"), _build_ticket(2, "Second")]
    ticket_service.find_tickets.return_value = expected_tickets

    pipe = FetchTicketsPipe(renderable_config)

    result_context = asyncio.run(pipe.process(pipeline_context))

    state = result_context.pipes["ticket_fetcher"]
    assert state["found_tickets"] == [ticket.model_dump() for ticket in expected_tickets]

    assert ticket_service.find_tickets.await_count == 1
    args, _ = ticket_service.find_tickets.await_args
    criteria = args[0]
    assert isinstance(criteria, TicketSearchCriteria)
    assert criteria.queue.id == 42
    assert criteria.limit == 25
    assert criteria.offset == 5


def test_process_without_results_returns_empty_list(
        renderable_config, ticket_service: AsyncMock, pipeline_context: Context
) -> None:
    ticket_service.find_tickets.return_value = []
    pipe = FetchTicketsPipe(renderable_config)

    result_context = asyncio.run(pipe.process(pipeline_context))

    assert result_context.pipes["ticket_fetcher"] == {"found_tickets": []}


def test_process_without_search_criteria_returns_error(
        ticket_service: AsyncMock, pipeline_context: Context, frozen_config_factory
) -> None:
    rendered_config = RenderedTicketFetchPipeConfig(
        id="ticket_fetcher",
        use="open_ticket_ai.basic_pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        ticket_system=ticket_service,
        ticket_search_criteria=None,
        when=True,
        steps=[],
    )
    config = frozen_config_factory(rendered_config)
    pipe = FetchTicketsPipe(config)

    result_context = asyncio.run(pipe.process(pipeline_context))

    state = result_context.pipes["ticket_fetcher"]
    assert "found_tickets" in state
    ticket_service.find_tickets.assert_awaited_once_with(None)
