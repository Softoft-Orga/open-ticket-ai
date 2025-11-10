from dataclasses import dataclass

import pytest
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote, UnifiedTicket
from otobo_znuny.domain_models.ticket_models import Article, TicketCreate, TicketSearch, TicketUpdate
from otobo_znuny.util.otobo_errors import OTOBOError

from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import otobo_ticket_to_unified_ticket


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
) -> None:
    mock_client.search_and_get.return_value = [sample_otobo_ticket] if scenario.has_tickets else []

    results = await service.find_tickets(sample_search_criteria)

    assert len(results) == scenario.expected_count
    if results:
        assert isinstance(results[0], UnifiedTicket)
        assert results[0].id == str(sample_otobo_ticket.id)


@pytest.mark.asyncio
async def test_find_tickets_accepts_kwargs(service, mock_client, sample_otobo_ticket) -> None:
    mock_client.search_and_get.return_value = [sample_otobo_ticket]

    results = await service.find_tickets(queue={"id": "1", "name": "Support"}, limit=5)

    assert len(results) == 1
    assert isinstance(results[0], UnifiedTicket)
    assert results[0].queue and results[0].queue.id == "1"
    search: TicketSearch = mock_client.search_and_get.call_args[0][0]
    assert isinstance(search, TicketSearch)
    assert search.limit == 5
    assert search.queues and search.queues[0].id == 1


@pytest.mark.asyncio
async def test_find_tickets_error(service, mock_client, sample_search_criteria) -> None:
    mock_client.search_and_get.side_effect = OTOBOError("500", "Internal Server Error")

    with pytest.raises(OTOBOError):
        await service.find_tickets(sample_search_criteria)


@pytest.mark.asyncio
@pytest.mark.parametrize("scenario", FIND_FIRST_TICKET_SCENARIOS)
async def test_find_first_ticket(
    service, mock_client, sample_otobo_ticket, sample_search_criteria, scenario: FindFirstTicketScenario
) -> None:
    mock_client.search_and_get.return_value = [sample_otobo_ticket] if scenario.has_tickets else []

    result = await service.find_first_ticket(sample_search_criteria)

    if scenario.expected_id is None:
        assert result is None
    else:
        assert isinstance(result, UnifiedTicket)
        assert result.id == scenario.expected_id


@pytest.mark.asyncio
async def test_find_first_ticket_error(service, mock_client, sample_search_criteria) -> None:
    mock_client.search_and_get.side_effect = OTOBOError("404", "Not Found")

    with pytest.raises(OTOBOError):
        await service.find_first_ticket(sample_search_criteria)


@pytest.mark.asyncio
async def test_get_ticket(service, mock_client, sample_otobo_ticket) -> None:
    mock_client.get_ticket.return_value = sample_otobo_ticket

    result = await service.get_ticket("123")

    assert isinstance(result, UnifiedTicket)
    assert result.id == str(sample_otobo_ticket.id)
    mock_client.get_ticket.assert_called_once_with(123)


@pytest.mark.asyncio
async def test_get_ticket_error(service, mock_client) -> None:
    mock_client.get_ticket.side_effect = OTOBOError("404", "Ticket not found")

    with pytest.raises(OTOBOError):
        await service.get_ticket("999")


@pytest.mark.asyncio
@pytest.mark.parametrize("has_note", [True, False])
async def test_update_ticket(service, mock_client, has_note) -> None:
    updates = UnifiedTicket(
        subject="Updated",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="High"),
        notes=[UnifiedNote(subject="Note", body="Body")] if has_note else None,
    )

    result = await service.update_ticket("123", updates)

    assert result is True
    update_payload: TicketUpdate = mock_client.update_ticket.call_args[0][0]
    assert isinstance(update_payload, TicketUpdate)
    assert update_payload.id == 123
    if has_note:
        assert isinstance(update_payload.article, Article)
    else:
        assert update_payload.article is None


@pytest.mark.asyncio
async def test_update_ticket_accepts_kwargs(service, mock_client) -> None:
    await service.update_ticket("123", subject="New subject")

    update_payload: TicketUpdate = mock_client.update_ticket.call_args[0][0]
    assert update_payload.title == "New subject"


@pytest.mark.asyncio
async def test_update_ticket_error(service, mock_client) -> None:
    mock_client.update_ticket.side_effect = OTOBOError("403", "Permission denied")

    with pytest.raises(OTOBOError):
        await service.update_ticket("123", subject="Updated")


@pytest.mark.asyncio
async def test_create_ticket(service, mock_client, sample_otobo_ticket) -> None:
    mock_client.create_ticket.return_value = sample_otobo_ticket
    new_ticket = UnifiedTicket(
        subject="New Ticket",
        body="This is a new ticket",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="High"),
    )

    result = await service.create_ticket(new_ticket)

    assert isinstance(result, UnifiedTicket)
    assert result.id == str(sample_otobo_ticket.id)
    payload: TicketCreate = mock_client.create_ticket.call_args[0][0]
    assert isinstance(payload, TicketCreate)
    assert payload.title == "New Ticket"
    assert payload.queue and payload.queue.id == 1
    assert payload.priority and payload.priority.id == 3
    assert payload.article.subject == "New Ticket"
    assert payload.article.body == "This is a new ticket"


@pytest.mark.asyncio
async def test_create_ticket_accepts_kwargs(service, mock_client, sample_otobo_ticket) -> None:
    mock_client.create_ticket.return_value = sample_otobo_ticket

    result = await service.create_ticket(
        subject="Ticket via kwargs",
        body="Body",
        queue={"id": "2", "name": "Support"},
    )

    assert isinstance(result, UnifiedTicket)
    assert result.queue and result.queue.id == str(sample_otobo_ticket.queue.id)
    payload: TicketCreate = mock_client.create_ticket.call_args[0][0]
    assert payload.title == "Ticket via kwargs"
    assert payload.queue and payload.queue.id == 2


@pytest.mark.asyncio
async def test_create_ticket_requires_subject(service, mock_client) -> None:
    with pytest.raises(ValueError):
        await service.create_ticket(body="Missing subject")


@pytest.mark.asyncio
async def test_create_ticket_error(service, mock_client) -> None:
    mock_client.create_ticket.side_effect = OTOBOError("400", "Invalid ticket data")

    with pytest.raises(OTOBOError):
        await service.create_ticket(subject="Failed Ticket")


@pytest.mark.asyncio
async def test_add_note(service, mock_client) -> None:
    result = await service.add_note("123", UnifiedNote(subject="Update", body="Body"))

    assert result is True
    update_payload: TicketUpdate = mock_client.update_ticket.call_args[0][0]
    assert update_payload.article and update_payload.article.subject == "Update"


@pytest.mark.asyncio
async def test_add_note_accepts_kwargs(service, mock_client) -> None:
    await service.add_note("123", subject="Kwarg note", body="Body")

    update_payload: TicketUpdate = mock_client.update_ticket.call_args[0][0]
    assert update_payload.article and update_payload.article.subject == "Kwarg note"


def test_converter_to_unified_ticket(sample_otobo_ticket) -> None:
    unified = otobo_ticket_to_unified_ticket(sample_otobo_ticket)

    assert unified.subject == sample_otobo_ticket.title
    assert unified.id == str(sample_otobo_ticket.id)
