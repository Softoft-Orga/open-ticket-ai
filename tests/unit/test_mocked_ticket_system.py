
import pytest

from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)


@pytest.mark.asyncio
async def test_create_ticket(empty_mocked_ticket_system):
    ticket = UnifiedTicket(subject="Test ticket", body="Test body")

    ticket_id = await empty_mocked_ticket_system.create_ticket(ticket)

    assert ticket_id == "TICKET-1"
    assert empty_mocked_ticket_system.get_ticket_count() == 1


@pytest.mark.asyncio
async def test_get_ticket(mocked_ticket_system):
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")

    assert ticket is not None
    assert ticket.id == "TICKET-1"
    assert ticket.subject == "Test ticket 1"


@pytest.mark.asyncio
async def test_update_ticket(mocked_ticket_system):
    updates = UnifiedTicket(subject="Updated subject")

    success = await mocked_ticket_system.update_ticket("TICKET-1", updates)

    assert success is True

    # Verify the update
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket.subject == "Updated subject"
    assert ticket.body == "This is the first test ticket"  # Other fields unchanged


@pytest.mark.asyncio
async def test_add_note_to_ticket(mocked_ticket_system):
    note = UnifiedNote(subject="Test note", body="Note body")

    success = await mocked_ticket_system.add_note("TICKET-1", note)

    assert success is True

    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert len(ticket.notes) == 1
    assert ticket.notes[0].body == "Note body"
    assert ticket.notes[0].id == "NOTE-1"


@pytest.mark.asyncio
async def test_add_note_with_int_ticket_id(mocked_ticket_system):
    ticket = UnifiedTicket(id="123", subject="Numeric ID ticket")
    await mocked_ticket_system.create_ticket(ticket)

    note = UnifiedNote(body="Test note")
    success = await mocked_ticket_system.add_note(123, note)

    assert success is True


@pytest.mark.asyncio
async def test_find_tickets_by_queue(mocked_ticket_system):
    criteria = TicketSearchCriteria(
        queue=UnifiedEntity(id="1", name="Support"),
        limit=10,
    )

    tickets = await mocked_ticket_system.find_tickets(criteria)

    assert len(tickets) == 2
    assert all(t.queue.name == "Support" for t in tickets)


@pytest.mark.asyncio
async def test_find_first_ticket(mocked_ticket_system):
    criteria = TicketSearchCriteria(queue=UnifiedEntity(id="1"))

    ticket = await mocked_ticket_system.find_first_ticket(criteria)

    assert ticket is not None
    assert ticket.queue.id == "1"


@pytest.mark.asyncio
async def test_pagination(mocked_ticket_system):
    criteria = TicketSearchCriteria(limit=2, offset=1)

    tickets = await mocked_ticket_system.find_tickets(criteria)

    assert len(tickets) == 2


@pytest.mark.asyncio
async def test_update_nonexistent_ticket(empty_mocked_ticket_system):
    updates = UnifiedTicket(subject="Updated")

    success = await empty_mocked_ticket_system.update_ticket("TICKET-999", updates)

    assert success is False


@pytest.mark.asyncio
async def test_add_note_to_nonexistent_ticket(empty_mocked_ticket_system):
    note = UnifiedNote(body="Test")

    success = await empty_mocked_ticket_system.add_note("TICKET-999", note)

    assert success is False


def test_clear_all_data(mocked_ticket_system):
    assert mocked_ticket_system.get_ticket_count() == 3

    mocked_ticket_system.clear_all_data()

    assert mocked_ticket_system.get_ticket_count() == 0


def test_get_all_tickets(mocked_ticket_system):
    tickets = mocked_ticket_system.get_all_tickets()

    assert len(tickets) == 3
    assert all(isinstance(t, UnifiedTicket) for t in tickets)
