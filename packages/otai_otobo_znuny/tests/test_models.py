from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedEntity, UnifiedNote
from otobo_znuny.domain_models.ticket_models import Article, IdName, Ticket
from packages.otai_otobo_znuny.src.otai_otobo_znuny.models import (
    _to_unified_entity,
    otobo_article_to_unified_note,
    otobo_ticket_to_unified_ticket,
)


def test_to_unified_entity():
    id_name = IdName(id=123, name="Test Entity")
    result = _to_unified_entity(id_name)
    assert result is not None
    assert result.id == "123"
    assert result.name == "Test Entity"
    assert isinstance(result, UnifiedEntity)


def test_note_adapter():
    article = Article(body="This is the body", subject="This is the subject")
    note = otobo_article_to_unified_note(article)
    assert note.body == "This is the body"
    assert note.subject == "This is the subject"
    assert isinstance(note, UnifiedNote)


def test_ticket_adapter():
    ticket = Ticket(
        id=456,
        title="Test Ticket",
        queue=IdName(id=1, name="Support Queue"),
        priority=IdName(id=3, name="High"),
        articles=[Article(body="First body", subject="First subject")],
    )
    adapter = otobo_ticket_to_unified_ticket(ticket)
    assert adapter.id == "456"
    assert adapter.subject == "Test Ticket"
    assert adapter.queue.id == "1"
    assert adapter.priority.id == "3"
    assert len(adapter.notes) == 1
    assert adapter.body == "First body"
