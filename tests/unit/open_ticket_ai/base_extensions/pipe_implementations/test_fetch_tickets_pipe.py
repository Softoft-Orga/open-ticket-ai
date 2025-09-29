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

from open_ticket_ai.base_extensions.pipe_configs import RawTicketFetchPipeConfig
from open_ticket_ai.base_extensions.ticket_system_pipes.fetch_tickets_pipe import FetchTicketsPipe
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedTicket,
)


@pytest.fixture
def pipeline_context() -> PipelineContext:
    return PipelineContext(pipes={}, config={})


@pytest.fixture
def raw_config() -> RawTicketFetchPipeConfig:
    return RawTicketFetchPipeConfig(
        name="ticket_fetcher",
        use="open_ticket_ai.base_extensions.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        ticket_search_criteria=TicketSearchCriteria(
            queue=UnifiedEntity(id=42, name="Support"),
            limit=25,
            offset=5,
        ),
    )


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
    raw_config: RawTicketFetchPipeConfig, ticket_service: AsyncMock, pipeline_context: PipelineContext
) -> None:
    expected_tickets = [_build_ticket(1, "First"), _build_ticket(2, "Second")]
    ticket_service.find_tickets.return_value = expected_tickets

    pipe = FetchTicketsPipe(raw_config, ticket_service)

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
    raw_config: RawTicketFetchPipeConfig, ticket_service: AsyncMock, pipeline_context: PipelineContext
) -> None:
    ticket_service.find_tickets.return_value = []
    pipe = FetchTicketsPipe(raw_config, ticket_service)

    result_context = asyncio.run(pipe.process(pipeline_context))

    assert result_context.pipes["ticket_fetcher"] == {"found_tickets": []}


def test_process_without_search_criteria_returns_error(
    ticket_service: AsyncMock, pipeline_context: PipelineContext
) -> None:
    raw_config = RawTicketFetchPipeConfig(
        name="ticket_fetcher",
        use="open_ticket_ai.base_extensions.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        ticket_search_criteria=None,
    )
    pipe = FetchTicketsPipe(raw_config, ticket_service)

    result_context = asyncio.run(pipe.process(pipeline_context))

    state = result_context.pipes["ticket_fetcher"]
    assert state["_status"] == "error"
    assert "No search criteria" in state["_error"]
    ticket_service.find_tickets.assert_not_awaited()


def test_convert_to_search_criteria_from_dict(
    raw_config: RawTicketFetchPipeConfig, ticket_service: AsyncMock
) -> None:
    pipe = FetchTicketsPipe(raw_config, ticket_service)

    criteria = pipe._convert_to_search_criteria(
        {
            "queue": {"id": 99, "name": "Escalations"},
            "limit": 10,
            "offset": 2,
        }
    )

    assert isinstance(criteria, TicketSearchCriteria)
    assert criteria.queue.id == 99
    assert criteria.queue.name == "Escalations"
    assert criteria.limit == 10
    assert criteria.offset == 2


def test_convert_to_search_criteria_passthrough(
    raw_config: RawTicketFetchPipeConfig, ticket_service: AsyncMock
) -> None:
    pipe = FetchTicketsPipe(raw_config, ticket_service)
    criteria = TicketSearchCriteria(queue=UnifiedEntity(id=7, name="VIP"), limit=5, offset=0)

    result = pipe._convert_to_search_criteria(criteria)

    assert result is criteria


def test_convert_to_search_criteria_rejects_strings(
    raw_config: RawTicketFetchPipeConfig, ticket_service: AsyncMock
) -> None:
    pipe = FetchTicketsPipe(raw_config, ticket_service)

    with pytest.raises(TypeError, match="Unsupported ticket search criteria type"):
        pipe._convert_to_search_criteria("queue=1")
