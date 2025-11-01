from dataclasses import dataclass

import pytest
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote, UnifiedTicket
from otobo_znuny.util.otobo_errors import OTOBOError


@dataclass(frozen=True)
class FindTicketsScenario:
    has_tickets: bool
    expected_count: int


FIND_TICKETS_SCENARIOS: tuple[FindTicketsScenario, ...] = (
    FindTicketsScenario(True, 1),
    FindTicketsScenario(False, 0),
)


@dataclass(frozen=True)
class FindFirstTicketScenario:
    has_tickets: bool
    expected_id: str | None


FIND_FIRST_TICKET_SCENARIOS: tuple[FindFirstTicketScenario, ...] = (
    FindFirstTicketScenario(True, "123"),
    FindFirstTicketScenario(False, None),
)


@pytest.mark.asyncio
@pytest.mark.parametrize("scenario", FIND_TICKETS_SCENARIOS)
async def test_find_tickets(
    service, mock_client, sample_otobo_ticket, sample_search_criteria, scenario: FindTicketsScenario
):
    mock_client.search_and_get.return_value = [sample_otobo_ticket] if scenario.has_tickets else []
    results = await service.find_tickets(sample_search_criteria)
    assert len(results) == scenario.expected_count
    if results:
        assert results[0].id == "123"


@pytest.mark.asyncio
async def test_find_tickets_error(service, mock_client, sample_search_criteria):
    mock_client.search_and_get.side_effect = OTOBOError("500", "Internal Server Error")
    with pytest.raises(OTOBOError):
        await service.find_tickets(sample_search_criteria)


@pytest.mark.asyncio
@pytest.mark.parametrize("scenario", FIND_FIRST_TICKET_SCENARIOS)
async def test_find_first_ticket(
    service, mock_client, sample_otobo_ticket, sample_search_criteria, scenario: FindFirstTicketScenario
):
    mock_client.search_and_get.return_value = [sample_otobo_ticket] if scenario.has_tickets else []
    result = await service.find_first_ticket(sample_search_criteria)
    if scenario.expected_id:
        assert result.id == scenario.expected_id
    else:
        assert result is None


@pytest.mark.asyncio
async def test_find_first_ticket_error(service, mock_client, sample_search_criteria):
    mock_client.search_and_get.side_effect = OTOBOError("404", "Not Found")
    with pytest.raises(OTOBOError):
        await service.find_first_ticket(sample_search_criteria)


@pytest.mark.asyncio
async def test_get_ticket(service, mock_client, sample_otobo_ticket):
    mock_client.get_ticket.return_value = sample_otobo_ticket
    result = await service.get_ticket("123")
    assert result.id == "123"
    mock_client.get_ticket.assert_called_once_with(123)


@pytest.mark.asyncio
async def test_get_ticket_error(service, mock_client):
    mock_client.get_ticket.side_effect = OTOBOError("404", "Ticket not found")
    with pytest.raises(OTOBOError):
        await service.get_ticket("999")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "has_note",
    [True, False],
)
async def test_update_ticket(service, mock_client, sample_otobo_ticket, has_note):
    mock_client.update_ticket.return_value = sample_otobo_ticket
    updates = UnifiedTicket(
        subject="Updated",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="High"),
        notes=[UnifiedNote(subject="Note", body="Body")] if has_note else None,
    )

    result = await service.update_ticket("123", updates)

    assert result is True
    call_args = mock_client.update_ticket.call_args[0][0]
    assert call_args.id == 123
    if has_note:
        assert call_args.article is not None
    else:
        assert call_args.article is None


@pytest.mark.asyncio
async def test_update_ticket_error(service, mock_client):
    mock_client.update_ticket.side_effect = OTOBOError("403", "Permission denied")
    updates = UnifiedTicket(
        subject="Updated",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="High"),
    )
    with pytest.raises(OTOBOError):
        await service.update_ticket("123", updates)


@pytest.mark.asyncio
async def test_create_ticket(service, mock_client, sample_otobo_ticket):
    mock_client.create_ticket.return_value = sample_otobo_ticket
    new_ticket = UnifiedTicket(
        subject="New Ticket",
        body="This is a new ticket",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="High"),
    )

    result = await service.create_ticket(new_ticket)

    assert result == "123"
    call_args = mock_client.create_ticket.call_args[0][0]
    assert call_args.title == "New Ticket"
    assert call_args.queue.id == 1
    assert call_args.queue.name == "Support"
    assert call_args.priority.id == 3
    assert call_args.priority.name == "High"
    assert call_args.article is not None
    assert call_args.article.subject == "New Ticket"
    assert call_args.article.body == "This is a new ticket"
    assert call_args.article.content_type == "text/plain"


@pytest.mark.asyncio
async def test_create_ticket_minimal(service, mock_client, sample_otobo_ticket):
    mock_client.create_ticket.return_value = sample_otobo_ticket
    new_ticket = UnifiedTicket(
        subject="Minimal Ticket",
    )

    result = await service.create_ticket(new_ticket)

    assert result == "123"
    call_args = mock_client.create_ticket.call_args[0][0]
    assert call_args.title == "Minimal Ticket"
    assert call_args.queue is None
    assert call_args.priority is None
    assert call_args.article is not None
    assert call_args.article.subject == "Minimal Ticket"
    assert call_args.article.body == ""


@pytest.mark.asyncio
async def test_create_ticket_error(service, mock_client):
    mock_client.create_ticket.side_effect = OTOBOError("400", "Invalid ticket data")
    new_ticket = UnifiedTicket(
        subject="Failed Ticket",
        queue=UnifiedEntity(id="1", name="Support"),
    )
    with pytest.raises(OTOBOError):
        await service.create_ticket(new_ticket)
