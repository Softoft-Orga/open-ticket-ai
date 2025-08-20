from datetime import datetime

from open_ticket_ai.src.ticket_system_integration.unified_models import (
    UnifiedUser,
    UnifiedQueue,
    UnifiedPriority,
    UnifiedStatus,
    UnifiedNote,
    UnifiedTicket,
    SearchCriteria,
)


def test_unified_ticket_construction():
    """Test the construction and attribute relationships of UnifiedTicket objects.

    This test verifies that:
    1. UnifiedTicket objects can be properly instantiated with all required components
    2. Attribute references between related objects are correctly maintained
    3. Nested object attributes are accessible through the ticket instance

    Steps performed:
    - Creates sample UnifiedUser, UnifiedQueue, UnifiedPriority, UnifiedStatus, and UnifiedNote objects
    - Constructs a UnifiedTicket using these components
    - Asserts that:
        a) The ticket owner's email matches the created user's email
        b) The note's author reference points to the same user instance as the ticket owner
    """
    user = UnifiedUser(id=1, name="Bob", email="bob@example.com")
    queue = UnifiedQueue(id=2, name="Support")
    prio = UnifiedPriority(id=3, name="High")
    status = UnifiedStatus(id=4, name="Open")
    note = UnifiedNote(
        id="n1",
        body="Hello",
        created_at=datetime.utcnow(),
        is_internal=False,
        author=user,
    )
    ticket = UnifiedTicket(
        id="t1",
        subject="Issue",
        body="Body",
        custom_fields={},
        queue=queue,
        priority=prio,
        status=status,
        owner=user,
        notes=[note],
    )
    assert ticket.owner.email == "bob@example.com"
    assert ticket.notes[0].author is user


def test_search_criteria():
    """Test the construction and attribute access of TicketSearchCriteria objects.

    This test verifies that:
    1. TicketSearchCriteria objects can be properly instantiated with various parameters
    2. Nested object attributes are correctly stored and accessible

    Steps performed:
    - Creates sample UnifiedUser and UnifiedQueue objects
    - Constructs a TicketSearchCriteria instance using these objects
    - Asserts that the queue name stored in the criteria matches the created queue's name
    """
    user = UnifiedUser(id=1, name="Bob")
    queue = UnifiedQueue(id=2, name="Support")
    criteria = SearchCriteria(id="1", subject="hi", queue=queue, user=user)
    assert criteria.queue.name == "Support"
