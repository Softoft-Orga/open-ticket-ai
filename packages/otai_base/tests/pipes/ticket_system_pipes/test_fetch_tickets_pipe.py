import pytest
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedEntity
from packages.otai_base.src.otai_base.pipes.ticket_system_pipes import FetchTicketsPipe

pytestmark = [pytest.mark.unit]

TOTAL_TICKETS = 3


async def _fetch_tickets(mocked_ticket_system, logger_factory, search_criteria: TicketSearchCriteria):
    config = PipeConfig(
        id="fetch-tickets",
        use="open_ticket_ai.otai_base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )
    pipe = FetchTicketsPipe(config=config, logger_factory=logger_factory, ticket_system=mocked_ticket_system)
    result = await pipe.process(PipeContext())
    assert result.succeeded is True
    return result.data["fetched_tickets"]


@pytest.mark.parametrize(
    ("queue_id", "queue_name", "expected_ids"),
    [
        ("1", None, ["TICKET-1", "TICKET-3"]),
        ("2", None, ["TICKET-2"]),
        (None, "Support", ["TICKET-1", "TICKET-3"]),
        (None, "Development", ["TICKET-2"]),
        ("1", "Support", ["TICKET-1", "TICKET-3"]),
        ("1", "Development", []),
    ],
)
async def test_fetch_tickets_by_queue(mocked_ticket_system, logger_factory, queue_id, queue_name, expected_ids):
    criteria = TicketSearchCriteria(queue=UnifiedEntity(id=queue_id, name=queue_name))
    tickets = await _fetch_tickets(mocked_ticket_system, logger_factory, criteria)
    assert [t.id for t in tickets] == expected_ids


@pytest.mark.parametrize(
    ("limit", "offset", "expected_count"),
    [
        (2, 0, 2),
        (1, 1, 1),
        (10, 1, 2),
    ],
)
async def test_fetch_tickets_pagination(mocked_ticket_system, logger_factory, limit, offset, expected_count):
    criteria = TicketSearchCriteria(limit=limit, offset=offset)
    tickets = await _fetch_tickets(mocked_ticket_system, logger_factory, criteria)
    assert len(tickets) == expected_count


@pytest.mark.parametrize(
    ("queue_id", "queue_name"),
    [("99", None), (None, "NonExistent")],
)
async def test_fetch_tickets_empty_results(mocked_ticket_system, logger_factory, queue_id, queue_name):
    criteria = TicketSearchCriteria(queue=UnifiedEntity(id=queue_id, name=queue_name))
    tickets = await _fetch_tickets(mocked_ticket_system, logger_factory, criteria)
    assert tickets == []


async def test_fetch_tickets_no_filter(mocked_ticket_system, logger_factory):
    criteria = TicketSearchCriteria(queue=None)
    tickets = await _fetch_tickets(mocked_ticket_system, logger_factory, criteria)
    assert len(tickets) == TOTAL_TICKETS
    assert {t.id for t in tickets} == {"TICKET-1", "TICKET-2", "TICKET-3"}
