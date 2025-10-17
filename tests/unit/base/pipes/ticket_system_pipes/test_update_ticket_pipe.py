import pytest
from pydantic import ValidationError

from open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe import (
    UpdateTicketParams,
    UpdateTicketPipe,
)
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket

pytestmark = [pytest.mark.unit]


@pytest.mark.parametrize(
    ("ticket_id", "updates"),
    [
        ("TICKET-1", {"subject": "Updated subject"}),
        ("TICKET-2", {"subject": "New subject"}),
    ],
)
async def test_update_ticket_single_field(mocked_ticket_system, logger_factory, ticket_id, updates):
    original_ticket = await mocked_ticket_system.get_ticket(ticket_id)
    assert original_ticket is not None

    config = PipeConfig(
        id="update-ticket-pipe",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe.UpdateTicketPipe",
        params={
            "ticket_id": ticket_id,
            "updated_ticket": updates,
        },
    )

    pipe = UpdateTicketPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True

    updated_ticket = await mocked_ticket_system.get_ticket(ticket_id)
    assert updated_ticket is not None
    assert updated_ticket.subject == updates["subject"]
    assert updated_ticket.queue == original_ticket.queue
    assert updated_ticket.priority == original_ticket.priority


@pytest.mark.parametrize(
    ("ticket_id", "updates"),
    [
        (
            "TICKET-1",
            {
                "subject": "Updated subject and priority",
                "priority": {"id": "5", "name": "High"},
            },
        ),
        (
            "TICKET-2",
            {
                "subject": "Updated subject and queue",
                "queue": {"id": "1", "name": "Support"},
            },
        ),
        (
            "TICKET-3",
            {
                "subject": "All fields updated",
                "queue": {"id": "2", "name": "Development"},
                "priority": {"id": "3", "name": "Medium"},
            },
        ),
    ],
)
async def test_update_ticket_multiple_fields(mocked_ticket_system, logger_factory, ticket_id, updates):
    original_ticket = await mocked_ticket_system.get_ticket(ticket_id)
    assert original_ticket is not None

    config = PipeConfig(
        id="update-ticket-pipe",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe.UpdateTicketPipe",
        params={
            "ticket_id": ticket_id,
            "updated_ticket": updates,
        },
    )

    pipe = UpdateTicketPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is True

    updated_ticket = await mocked_ticket_system.get_ticket(ticket_id)
    assert updated_ticket is not None
    assert updated_ticket.subject == updates["subject"]

    if "priority" in updates:
        assert updated_ticket.priority is not None
        assert updated_ticket.priority.id == updates["priority"]["id"]
        assert updated_ticket.priority.name == updates["priority"]["name"]

    if "queue" in updates:
        assert updated_ticket.queue is not None
        assert updated_ticket.queue.id == updates["queue"]["id"]
        assert updated_ticket.queue.name == updates["queue"]["name"]


def test_update_ticket_validation_subject_dict():
    with pytest.raises(ValidationError):
        UpdateTicketParams(
            ticket_id="TICKET-1",
            updated_ticket=UnifiedTicket(subject={"key": "value"}),
        )


def test_update_ticket_validation_priority_list():
    with pytest.raises(ValidationError):
        UpdateTicketParams(
            ticket_id="TICKET-1",
            updated_ticket=UnifiedTicket(priority=["high"]),
        )


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("subject", {"key": "value"}),
        ("subject", ["item1", "item2"]),
        ("subject", 12345),
        ("queue", "not_an_entity"),
        ("priority", "not_an_entity"),
        ("id", {"key": "value"}),
        ("id", ["item"]),
    ],
)
def test_update_ticket_validation_invalid_types(field_name, invalid_value):
    with pytest.raises(ValidationError):
        UpdateTicketParams(
            ticket_id="TICKET-1",
            updated_ticket=UnifiedTicket(**{field_name: invalid_value}),
        )


async def test_update_ticket_nonexistent_id(mocked_ticket_system, logger_factory):
    config = PipeConfig(
        id="update-ticket-pipe",
        use="open_ticket_ai.base.pipes.ticket_system_pipes.update_ticket_pipe.UpdateTicketPipe",
        params={
            "ticket_id": "TICKET-999",
            "updated_ticket": {
                "subject": "This should fail",
            },
        },
    )

    pipe = UpdateTicketPipe(
        config=config,
        logger_factory=logger_factory,
        ticket_system=mocked_ticket_system,
    )

    context = PipeContext()
    result = await pipe.process(context)

    assert result.succeeded is False
    assert "Failed" in result.message or "failed" in result.message
