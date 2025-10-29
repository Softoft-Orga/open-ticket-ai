import pytest

from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)


@pytest.mark.asyncio
async def test_get_ticket(mocked_ticket_system):
    ticket = await mocked_ticket_system.get_ticket("TICKET-1")
    assert ticket is not None
    assert ticket.id == "TICKET-1"


@pytest.mark.asyncio
async def test_update_ticket(mocked_ticket_system):
    updates = UnifiedTicket(subject="Updated subject")
    success = await mocked_ticket_system.update_ticket("TICKET-1", updates)
    assert success is True


@pytest.mark.asyncio
async def test_add_note(mocked_ticket_system):
    note = UnifiedNote(subject="Test note", body="Note body")
    success = await mocked_ticket_system.add_note("TICKET-1", note)
    assert success is True


@pytest.mark.asyncio
async def test_find_tickets(mocked_ticket_system):
    criteria = TicketSearchCriteria(queue=UnifiedEntity(id="1", name="Support"), limit=10)
    tickets = await mocked_ticket_system.find_tickets(criteria)
    assert len(tickets) == 2
