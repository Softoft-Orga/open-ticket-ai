import pytest
from open_ticket_ai.open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
)
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket

from open_ticket_ai_otobo_znuny_plugin.open_ticket_ai_otobo_znuny_plugin.models import (
    _to_unified_entity,
    otobo_article_to_unified_note,
    otobo_ticket_to_unified_ticket,
)


class TestToUnifiedEntity:
    def test_converts_id_name_to_unified_entity(self):
        id_name = IdName(id=123, name="Test Entity")
        result = _to_unified_entity(id_name)

        assert result is not None
        assert result.id == "123"
        assert result.name == "Test Entity"
        assert isinstance(result, UnifiedEntity)

    def test_returns_none_for_none_input(self):
        result = _to_unified_entity(None)
        assert result is None


class TestNoteAdapter:
    def test_creates_note_with_body_and_subject(self):
        article = Article(body="This is the body", subject="This is the subject")

        note = otobo_article_to_unified_note(article)

        assert note.body == "This is the body"
        assert note.subject == "This is the subject"
        assert isinstance(note, UnifiedNote)

    def test_handles_none_body(self):
        article = Article(body=None, subject="Subject only")

        note = otobo_article_to_unified_note(article)

        assert note.body == ""
        assert note.subject == "Subject only"

    def test_handles_empty_body(self):
        article = Article(body="", subject="Subject with empty body")

        note = otobo_article_to_unified_note(article)

        assert note.body == ""
        assert note.subject == "Subject with empty body"


class TestTicketAdapter:
    @pytest.fixture
    def basic_ticket(self):
        return Ticket(
            id=456,
            title="Test Ticket",
            queue=IdName(id=1, name="Support Queue"),
            priority=IdName(id=3, name="High"),
            articles=[],
        )

    @pytest.fixture
    def ticket_with_articles(self):
        return Ticket(
            id=789,
            title="Ticket with Articles",
            queue=IdName(id=2, name="Technical Queue"),
            priority=IdName(id=2, name="Medium"),
            articles=[
                Article(body="First article body", subject="First subject"),
                Article(body="Second article body", subject="Second subject"),
                Article(body="Third article body", subject="Third subject"),
            ],
        )

    def test_creates_ticket_adapter_with_basic_fields(self, basic_ticket):
        adapter = otobo_ticket_to_unified_ticket(basic_ticket)

        assert adapter.id == "456"
        assert adapter.subject == "Test Ticket"
        assert adapter.queue is not None
        assert adapter.queue.id == "1"
        assert adapter.queue.name == "Support Queue"
        assert adapter.priority is not None
        assert adapter.priority.id == "3"
        assert adapter.priority.name == "High"

    def test_handles_none_ticket_id(self):
        # noinspection PyTypeChecker
        ticket = Ticket(id=1, title="No ID Ticket")

        adapter = otobo_ticket_to_unified_ticket(ticket)

        assert adapter.id == "1"
        assert adapter.subject == "No ID Ticket"

    def test_handles_none_title(self):
        ticket = Ticket(id=123, title=None)

        adapter = otobo_ticket_to_unified_ticket(ticket)

        assert adapter.id == "123"
        assert adapter.subject == ""

    def test_handles_none_queue_and_priority(self):
        ticket = Ticket(id=999, title="Minimal Ticket", queue=None, priority=None)

        adapter = otobo_ticket_to_unified_ticket(ticket)

        assert adapter.queue is None
        assert adapter.priority is None

    def test_notes_property_returns_adapted_articles(self, ticket_with_articles):
        adapter = otobo_ticket_to_unified_ticket(ticket_with_articles)

        notes = adapter.notes

        assert len(notes) == 3
        assert all(isinstance(note, UnifiedNote) for note in notes)
        assert notes[0].body == "First article body"
        assert notes[0].subject == "First subject"
        assert notes[1].body == "Second article body"
        assert notes[2].body == "Third article body"

    def test_notes_property_handles_no_articles(self, basic_ticket):
        adapter = otobo_ticket_to_unified_ticket(basic_ticket)

        notes = adapter.notes

        assert notes == []

    def test_notes_property_handles_none_articles(self):
        ticket = Ticket(id=111, title="No Articles", articles=[])

        adapter = otobo_ticket_to_unified_ticket(ticket)

        notes = adapter.notes

        assert notes == []

    def test_body_property_returns_first_article_body(self, ticket_with_articles):
        adapter = otobo_ticket_to_unified_ticket(ticket_with_articles)

        body = adapter.body

        assert body == "First article body"

    def test_body_property_returns_empty_string_when_no_notes(self, basic_ticket):
        adapter = otobo_ticket_to_unified_ticket(basic_ticket)

        body = adapter.body

        assert body == ""

    @pytest.mark.parametrize(
        "ticket_id,expected_id_str",
        [
            (0, "0"),
            (1, "1"),
            (999999, "999999"),
            (-1, "-1"),
        ],
    )
    def test_various_ticket_ids(self, ticket_id, expected_id_str):
        ticket = Ticket(id=ticket_id, title="Test")
        adapter = otobo_ticket_to_unified_ticket(ticket)

        assert adapter.id == expected_id_str
