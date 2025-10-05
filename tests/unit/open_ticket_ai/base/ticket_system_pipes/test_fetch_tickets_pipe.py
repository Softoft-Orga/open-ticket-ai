from __future__ import annotations

import pytest

from open_ticket_ai.base.ticket_system_pipes.fetch_tickets_pipe import FetchTicketsPipe


@pytest.mark.asyncio
async def test_fetch_tickets_finds_tickets_by_queue(
    empty_pipeline_context,
    mocked_ticket_system,
):
    """Test that FetchTicketsPipe finds tickets by queue."""
    config = {
        "id": "test_fetch",
        "use": "FetchTicketsPipe",
        "_if": True,
        "ticket_search_criteria": {
            "queue": {"id": "1", "name": "Support"},
            "limit": 10,
        },
    }

    pipe = FetchTicketsPipe(mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify pipe result
    pipe_result = result_context.pipes["test_fetch"]
    assert pipe_result.success is True
    assert pipe_result.failed is False

    # Verify found tickets
    found_tickets = pipe_result.data["found_tickets"]
    assert len(found_tickets) == 2  # TICKET-1 and TICKET-3 are in Support queue
    assert all(t["queue"]["name"] == "Support" for t in found_tickets)


@pytest.mark.asyncio
async def test_fetch_tickets_with_pagination(
    empty_pipeline_context,
    mocked_ticket_system,
):
    """Test that FetchTicketsPipe respects pagination."""
    config = {
        "id": "test_fetch",
        "use": "FetchTicketsPipe",
        "_if": True,
        "ticket_search_criteria": {
            "limit": 2,
            "offset": 1,
        },
    }

    pipe = FetchTicketsPipe(mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify pagination worked
    pipe_result = result_context.pipes["test_fetch"]
    found_tickets = pipe_result.data["found_tickets"]
    assert len(found_tickets) == 2  # Limited to 2


@pytest.mark.asyncio
async def test_fetch_tickets_returns_empty_when_no_matches(
    empty_pipeline_context,
    mocked_ticket_system,
):
    """Test that FetchTicketsPipe returns empty list when no tickets match."""
    config = {
        "id": "test_fetch",
        "use": "FetchTicketsPipe",
        "_if": True,
        "ticket_search_criteria": {
            "queue": {"id": "999", "name": "Nonexistent"},
        },
    }

    pipe = FetchTicketsPipe(mocked_ticket_system, config)
    result_context = await pipe.process(empty_pipeline_context)

    # Verify empty result
    pipe_result = result_context.pipes["test_fetch"]
    assert pipe_result.success is True
    found_tickets = pipe_result.data["found_tickets"]
    assert len(found_tickets) == 0
