from unittest.mock import AsyncMock, MagicMock

import pytest
from open_ticket_ai.base.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
)
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket
from otobo_znuny.util.otobo_errors import OTOBOError
from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import (
    RenderedOTOBOZnunyTSServiceParams,
)
from packages.otai_otobo_znuny.src.otai_otobo_znuny.oto_znuny_ts_service import (
    OTOBOZnunyTicketSystemService,
)


@pytest.fixture
def mock_client():
    mock = MagicMock(spec=OTOBOZnunyClient)
    mock.login = MagicMock()
    mock.search_and_get = AsyncMock()
    mock.get_ticket = AsyncMock()
    mock.update_ticket = AsyncMock()
    return mock


@pytest.fixture
def service_params():
    return RenderedOTOBOZnunyTSServiceParams(
        base_url="http://test.example.com",
        username="test_user",
        password="test_password",
        webservice_name="TestService",
    )


@pytest.fixture
def logger_factory():
    return create_logger_factory(LoggingConfig(level="DEBUG"))


@pytest.fixture
def service(mock_client, service_params, logger_factory):
    service_instance = OTOBOZnunyTicketSystemService.__new__(OTOBOZnunyTicketSystemService)
    service_config = InjectableConfig(
        id="test_service",
        use="packages.otai_otobo_znuny.src.otai_otobo_znuny.oto_znuny_ts_service.OTOBOZnunyTicketSystemService",
        params=service_params.model_dump(),
    )
    service_instance._config = service_config
    service_instance._logger_factory = logger_factory
    service_instance._logger = logger_factory.create(service_config.id)
    service_instance._client = mock_client
    return service_instance


@pytest.fixture
def sample_otobo_ticket():
    return Ticket(
        id=123,
        title="Test Ticket",
        queue=IdName(id=1, name="Support"),
        priority=IdName(id=3, name="High"),
        articles=[
            Article(subject="First article", body="This is the first article body")
        ],
    )


@pytest.fixture
def sample_unified_ticket():
    return UnifiedTicket(
        id="123",
        subject="Test Ticket",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="High"),
        body="This is the first article body",
        notes=[UnifiedNote(subject="First article", body="This is the first article body")],
    )


@pytest.fixture
def sample_search_criteria():
    return TicketSearchCriteria(
        queue=UnifiedEntity(id="1", name="Support"),
        limit=10,
    )


class TestFindTickets:
    @pytest.mark.asyncio
    async def test_find_tickets_success(self, service, mock_client, sample_otobo_ticket, sample_search_criteria):
        mock_client.search_and_get.return_value = [sample_otobo_ticket]

        results = await service.find_tickets(sample_search_criteria)

        assert len(results) == 1
        assert results[0].id == "123"
        assert results[0].subject == "Test Ticket"
        assert results[0].queue.id == "1"
        assert results[0].priority.id == "3"
        mock_client.search_and_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_tickets_empty_result(self, service, mock_client, sample_search_criteria):
        mock_client.search_and_get.return_value = []

        results = await service.find_tickets(sample_search_criteria)

        assert len(results) == 0
        mock_client.search_and_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_tickets_error(self, service, mock_client, sample_search_criteria):
        mock_client.search_and_get.side_effect = OTOBOError("500", "Internal Server Error")

        with pytest.raises(OTOBOError) as exc_info:
            await service.find_tickets(sample_search_criteria)

        assert exc_info.value.code == "500"
        assert exc_info.value.message == "Internal Server Error"

    @pytest.mark.asyncio
    async def test_find_tickets_multiple_results(
        self, service, mock_client, sample_otobo_ticket, sample_search_criteria
    ):
        ticket2 = Ticket(
            id=456,
            title="Another Ticket",
            queue=IdName(id=2, name="Development"),
            priority=IdName(id=2, name="Medium"),
            articles=[Article(subject="Article", body="Body")],
        )
        mock_client.search_and_get.return_value = [sample_otobo_ticket, ticket2]

        results = await service.find_tickets(sample_search_criteria)

        assert len(results) == 2
        assert results[0].id == "123"
        assert results[1].id == "456"

    @pytest.mark.asyncio
    async def test_find_tickets_without_queue(self, service, mock_client, sample_otobo_ticket):
        criteria = TicketSearchCriteria(limit=5)
        mock_client.search_and_get.return_value = [sample_otobo_ticket]

        results = await service.find_tickets(criteria)

        assert len(results) == 1
        mock_client.search_and_get.assert_called_once()
        call_args = mock_client.search_and_get.call_args[0][0]
        assert call_args.queues is None
        assert call_args.limit == 5


class TestFindFirstTicket:
    @pytest.mark.asyncio
    async def test_find_first_ticket_success(self, service, mock_client, sample_otobo_ticket, sample_search_criteria):
        mock_client.search_and_get.return_value = [sample_otobo_ticket]

        result = await service.find_first_ticket(sample_search_criteria)

        assert result is not None
        assert result.id == "123"
        assert result.subject == "Test Ticket"

    @pytest.mark.asyncio
    async def test_find_first_ticket_empty_result(self, service, mock_client, sample_search_criteria):
        mock_client.search_and_get.return_value = []

        result = await service.find_first_ticket(sample_search_criteria)

        assert result is None

    @pytest.mark.asyncio
    async def test_find_first_ticket_error(self, service, mock_client, sample_search_criteria):
        mock_client.search_and_get.side_effect = OTOBOError("404", "Not Found")

        with pytest.raises(OTOBOError) as exc_info:
            await service.find_first_ticket(sample_search_criteria)

        assert exc_info.value.code == "404"

    @pytest.mark.asyncio
    async def test_find_first_ticket_returns_first_of_many(
        self, service, mock_client, sample_otobo_ticket, sample_search_criteria
    ):
        ticket2 = Ticket(
            id=456,
            title="Second Ticket",
            queue=IdName(id=1, name="Support"),
            priority=IdName(id=1, name="Low"),
            articles=[Article(subject="S", body="B")],
        )
        mock_client.search_and_get.return_value = [sample_otobo_ticket, ticket2]

        result = await service.find_first_ticket(sample_search_criteria)

        assert result is not None
        assert result.id == "123"


class TestGetTicket:
    @pytest.mark.asyncio
    async def test_get_ticket_success(self, service, mock_client, sample_otobo_ticket):
        mock_client.get_ticket.return_value = sample_otobo_ticket

        result = await service.get_ticket("123")

        assert result is not None
        assert result.id == "123"
        assert result.subject == "Test Ticket"
        mock_client.get_ticket.assert_called_once_with(123)

    @pytest.mark.asyncio
    async def test_get_ticket_error(self, service, mock_client):
        mock_client.get_ticket.side_effect = OTOBOError("404", "Ticket not found")

        with pytest.raises(OTOBOError) as exc_info:
            await service.get_ticket("999")

        assert exc_info.value.code == "404"
        assert exc_info.value.message == "Ticket not found"

    @pytest.mark.asyncio
    async def test_get_ticket_converts_id_to_int(self, service, mock_client, sample_otobo_ticket):
        mock_client.get_ticket.return_value = sample_otobo_ticket

        await service.get_ticket("456")

        mock_client.get_ticket.assert_called_once_with(456)


class TestUpdateTicket:
    @pytest.mark.asyncio
    async def test_update_ticket_success(self, service, mock_client, sample_otobo_ticket):
        mock_client.update_ticket.return_value = sample_otobo_ticket
        updates = UnifiedTicket(
            subject="Updated Subject",
            queue=UnifiedEntity(id="2", name="Development"),
            priority=UnifiedEntity(id="5", name="Critical"),
        )

        result = await service.update_ticket("123", updates)

        assert result is True
        mock_client.update_ticket.assert_called_once()
        call_args = mock_client.update_ticket.call_args[0][0]
        assert call_args.id == 123
        assert call_args.title == "Updated Subject"
        assert call_args.queue.name == "Development"
        assert call_args.priority.name == "Critical"

    @pytest.mark.asyncio
    async def test_update_ticket_with_note(self, service, mock_client, sample_otobo_ticket):
        mock_client.update_ticket.return_value = sample_otobo_ticket
        updates = UnifiedTicket(
            subject="Subject",
            queue=UnifiedEntity(id="1", name="Support"),
            priority=UnifiedEntity(id="3", name="High"),
            notes=[UnifiedNote(subject="Note Subject", body="Note Body")],
        )

        result = await service.update_ticket("123", updates)

        assert result is True
        call_args = mock_client.update_ticket.call_args[0][0]
        assert call_args.article is not None
        assert call_args.article.subject == "Note Subject"
        assert call_args.article.body == "Note Body"

    @pytest.mark.asyncio
    async def test_update_ticket_without_note(self, service, mock_client, sample_otobo_ticket):
        mock_client.update_ticket.return_value = sample_otobo_ticket
        updates = UnifiedTicket(
            subject="Updated Subject",
            queue=UnifiedEntity(id="1", name="Support"),
            priority=UnifiedEntity(id="3", name="High"),
        )

        result = await service.update_ticket("123", updates)

        assert result is True
        call_args = mock_client.update_ticket.call_args[0][0]
        assert call_args.article is None

    @pytest.mark.asyncio
    async def test_update_ticket_error(self, service, mock_client):
        mock_client.update_ticket.side_effect = OTOBOError("403", "Permission denied")
        updates = UnifiedTicket(
            subject="Updated",
            queue=UnifiedEntity(id="1", name="Support"),
            priority=UnifiedEntity(id="3", name="High"),
        )

        with pytest.raises(OTOBOError) as exc_info:
            await service.update_ticket("123", updates)

        assert exc_info.value.code == "403"

    @pytest.mark.asyncio
    async def test_update_ticket_with_multiple_notes_uses_last(self, service, mock_client, sample_otobo_ticket):
        mock_client.update_ticket.return_value = sample_otobo_ticket
        updates = UnifiedTicket(
            subject="Subject",
            queue=UnifiedEntity(id="1", name="Support"),
            priority=UnifiedEntity(id="3", name="High"),
            notes=[
                UnifiedNote(subject="First", body="First body"),
                UnifiedNote(subject="Second", body="Second body"),
                UnifiedNote(subject="Last", body="Last body"),
            ],
        )

        await service.update_ticket("123", updates)

        call_args = mock_client.update_ticket.call_args[0][0]
        assert call_args.article is not None
        assert call_args.article.subject == "Last"
        assert call_args.article.body == "Last body"


class TestAddNote:
    @pytest.mark.asyncio
    async def test_add_note_success(self, service, mock_client, sample_otobo_ticket):
        mock_client.update_ticket.return_value = sample_otobo_ticket
        note = UnifiedNote(subject="New Note", body="This is a new note")

        with pytest.raises(AttributeError):
            await service.add_note("123", note)

    @pytest.mark.asyncio
    async def test_add_note_error(self, service, mock_client):
        mock_client.update_ticket.side_effect = OTOBOError("500", "Server error")
        note = UnifiedNote(subject="Note", body="Body")

        with pytest.raises(AttributeError):
            await service.add_note("123", note)

    @pytest.mark.asyncio
    async def test_add_note_without_body(self, service, mock_client, sample_otobo_ticket):
        mock_client.update_ticket.return_value = sample_otobo_ticket
        note = UnifiedNote(subject="Just a subject", body="")

        with pytest.raises(AttributeError):
            await service.add_note("123", note)
