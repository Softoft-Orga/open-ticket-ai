from typing import Any

from open_ticket_ai import TicketSearchCriteria, UnifiedEntity, UnifiedNote, UnifiedTicket


class UnifiedTicketFactory:
    """Factory for creating UnifiedTicket test instances."""

    @staticmethod
    def build(
        ticket_id: str = "TEST-123",
        subject: str = "Test Ticket",
        queue_id: str = "1",
        queue_name: str = "Support",
        **kwargs: Any,
    ) -> UnifiedTicket:
        defaults = {
            "id": ticket_id,
            "subject": subject,
            "queue": UnifiedEntity(id=queue_id, name=queue_name),
            "body": f"Body for {subject}",
        }
        defaults.update(kwargs)
        return UnifiedTicket(**defaults)

    @staticmethod
    def build_batch(count: int = 3, **kwargs: Any) -> list[UnifiedTicket]:
        return [
            UnifiedTicketFactory.build(ticket_id=f"TEST-{i}", subject=f"Test Ticket {i}", **kwargs)
            for i in range(1, count + 1)
        ]


class UnifiedNoteFactory:
    """Factory for creating UnifiedNote test instances."""

    @staticmethod
    def build(body: str = "Test note content", **kwargs: Any) -> UnifiedNote:
        defaults = {"body": body}
        defaults.update(kwargs)
        return UnifiedNote(**defaults)


class TicketSearchCriteriaFactory:
    """Factory for creating TicketSearchCriteria test instances."""

    @staticmethod
    def build(
        queue_id: str = "1",
        queue_name: str = "Support",
        limit: int = 25,
        offset: int = 0,
        **kwargs: Any,
    ) -> TicketSearchCriteria:
        defaults = {
            "queue": UnifiedEntity(id=queue_id, name=queue_name),
            "limit": limit,
            "offset": offset,
        }
        defaults.update(kwargs)
        return TicketSearchCriteria(**defaults)


class TestPipe:
    def __init__(self, pipe_params):
        self.pipe_params = pipe_params

    async def process(self, context):
        return context
