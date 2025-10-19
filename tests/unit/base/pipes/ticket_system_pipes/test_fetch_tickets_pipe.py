import pytest

from open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe import FetchTicketsPipe
from open_ticket_ai.base.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
)
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig

pytestmark = [pytest.mark.unit]


@pytest.mark.parametrize(
    ("queue_id", "expected_ticket_ids"),
    [
        ("1", ["TICKET-1", "TICKET-3"]),
        ("2", ["TICKET-2"]),
    ],
)
async def test_fetch_tickets_by_queue_id(mocked_ticket_system, logger_factory, queue_id, expected_ticket_ids):
    search_criteria = TicketSearchCriteria(queue=UnifiedEntity(id=queue_id))

    config = PipeConfig(
        id="fetch-tickets-by-queue-id",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert len(fetched_tickets) == len(expected_ticket_ids)

    actual_ticket_ids = [ticket.id for ticket in fetched_tickets]
    assert set(actual_ticket_ids) == set(expected_ticket_ids)

    for ticket in fetched_tickets:
        assert ticket.queue is not None
        assert ticket.queue.id == queue_id


@pytest.mark.parametrize(
    ("queue_name", "expected_count"),
    [
        ("Support", 2),
        ("Development", 1),
    ],
)
async def test_fetch_tickets_by_queue_name(mocked_ticket_system, logger_factory, queue_name, expected_count):
    search_criteria = TicketSearchCriteria(queue=UnifiedEntity(name=queue_name))

    config = PipeConfig(
        id="fetch-tickets-by-queue-name",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert len(fetched_tickets) == expected_count

    for ticket in fetched_tickets:
        assert ticket.queue is not None
        assert ticket.queue.name == queue_name


@pytest.mark.parametrize(
    ("queue_id", "queue_name", "expected_ticket_ids"),
    [
        ("1", "Support", ["TICKET-1", "TICKET-3"]),
        ("2", "Development", ["TICKET-2"]),
    ],
)
async def test_fetch_tickets_by_both_id_and_name(
    mocked_ticket_system, logger_factory, queue_id, queue_name, expected_ticket_ids
):
    search_criteria = TicketSearchCriteria(queue=UnifiedEntity(id=queue_id, name=queue_name))

    config = PipeConfig(
        id="fetch-tickets-by-both-id-and-name",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert len(fetched_tickets) == len(expected_ticket_ids)

    actual_ticket_ids = [ticket.id for ticket in fetched_tickets]
    assert set(actual_ticket_ids) == set(expected_ticket_ids)

    for ticket in fetched_tickets:
        assert ticket.queue is not None
        assert ticket.queue.id == queue_id
        assert ticket.queue.name == queue_name


async def test_fetch_tickets_pagination_limit(mocked_ticket_system, logger_factory):
    search_criteria = TicketSearchCriteria(limit=2, offset=0)

    config = PipeConfig(
        id="fetch-tickets-pagination-limit",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert len(fetched_tickets) == 2


async def test_fetch_tickets_pagination_offset(mocked_ticket_system, logger_factory):
    all_tickets_criteria = TicketSearchCriteria(limit=10, offset=0)
    all_tickets_config = PipeConfig(
        id="fetch-all-tickets",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": all_tickets_criteria.model_dump()},
    )
    all_tickets_pipe = FetchTicketsPipe(
        config=all_tickets_config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )
    all_tickets_result = await all_tickets_pipe.process(PipeContext())
    all_tickets = all_tickets_result.data["fetched_tickets"]
    first_ticket_id = all_tickets[0].id

    offset_criteria = TicketSearchCriteria(limit=10, offset=1)
    offset_config = PipeConfig(
        id="fetch-tickets-with-offset",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": offset_criteria.model_dump()},
    )
    offset_pipe = FetchTicketsPipe(
        config=offset_config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    offset_result = await offset_pipe.process(PipeContext())

    assert offset_result.succeeded is True
    fetched_tickets = offset_result.data["fetched_tickets"]
    assert len(fetched_tickets) == 2

    fetched_ticket_ids = [ticket.id for ticket in fetched_tickets]
    assert first_ticket_id not in fetched_ticket_ids


async def test_fetch_tickets_pagination_limit_and_offset(mocked_ticket_system, logger_factory):
    search_criteria = TicketSearchCriteria(limit=1, offset=1)

    config = PipeConfig(
        id="fetch-tickets-limit-and-offset",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert len(fetched_tickets) == 1


@pytest.mark.parametrize(
    ("queue_id", "queue_name"),
    [
        ("99", None),
        (None, "NonExistent"),
    ],
)
async def test_fetch_tickets_empty_queue(mocked_ticket_system, logger_factory, queue_id, queue_name):
    search_criteria = TicketSearchCriteria(queue=UnifiedEntity(id=queue_id, name=queue_name))

    config = PipeConfig(
        id="fetch-tickets-empty-queue",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert fetched_tickets == []


async def test_fetch_tickets_mismatched_id_name(mocked_ticket_system, logger_factory):
    search_criteria = TicketSearchCriteria(queue=UnifiedEntity(id="1", name="Development"))

    config = PipeConfig(
        id="fetch-tickets-mismatched",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert fetched_tickets == []


async def test_fetch_tickets_no_queue_filter(mocked_ticket_system, logger_factory):
    search_criteria = TicketSearchCriteria(queue=None)

    config = PipeConfig(
        id="fetch-tickets-no-filter",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.fetch_tickets_pipe.FetchTicketsPipe",
        params={"ticket_search_criteria": search_criteria.model_dump()},
    )

    pipe = FetchTicketsPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True
    fetched_tickets = result.data["fetched_tickets"]
    assert len(fetched_tickets) == 3

    ticket_ids = [ticket.id for ticket in fetched_tickets]
    assert set(ticket_ids) == {"TICKET-1", "TICKET-2", "TICKET-3"}

    for ticket in fetched_tickets:
        assert ticket.id is not None
        assert ticket.subject is not None
        assert ticket.queue is not None
        assert ticket.priority is not None
