from otobo import ArticleDetail, TicketCommon, TicketDetailOutput

from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    UnifiedNote,
    UnifiedPriority,
    UnifiedQueue,
    UnifiedTicket,
)


class QueueAdapter(UnifiedQueue):
    """Adapter for converting OTOBO queue details to unified queue format."""

    @classmethod
    def from_otobo_ticket(cls, ticket: TicketCommon) -> 'QueueAdapter':
        """Create a QueueAdapter from an OTOBO ticket."""
        return cls(
            id=str(ticket.QueueID) if ticket.QueueID else None,
            name=ticket.Queue if ticket.Queue else "",
        )


class PriorityAdapter(UnifiedPriority):
    """Adapter for converting OTOBO priority details to unified priority format."""

    @classmethod
    def from_otobo_ticket(cls, ticket: TicketCommon) -> 'PriorityAdapter':
        """Create a PriorityAdapter from an OTOBO ticket."""
        return cls(
            id=str(ticket.PriorityID) if ticket.PriorityID else None,
            name=ticket.Priority if ticket.Priority else "",
        )


class NoteAdapter(UnifiedNote):
    """Adapter for converting OTOBO article details to unified note format."""

    def __init__(self, article: ArticleDetail):
        super().__init__(
            body=article.Body or "",
            subject=article.Subject or "",
        )


class TicketAdapter(UnifiedTicket):

    def __init__(self, ticket: TicketDetailOutput):
        super().__init__(
            id=str(ticket.TicketID),
            subject=ticket.Title or "",
            body=self.get_unified_body(ticket),
            queue=QueueAdapter.from_otobo_ticket(ticket),
            priority=PriorityAdapter.from_otobo_ticket(ticket),
            notes=self.get_unified_notes_list(ticket),
        )

    def get_unified_body(self, ticket) -> str:
        return self.get_unified_notes_list(ticket)[0].body if self.get_unified_notes_list(ticket) else ""

    def get_unified_notes_list(self, ticket) -> list[UnifiedNote]:
        """Convert OTOBO articles to a list of unified notes."""
        return [NoteAdapter(article) for article in self.get_otobo_articles_as_list(ticket)]

    def get_otobo_articles_as_list(self, ticket) -> list[ArticleDetail]:
        if not ticket.Article:
            return []
        elif isinstance(ticket.Article, list):
            return ticket.Article
        else:
            return [ticket.Article]
