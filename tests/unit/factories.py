from typing import Any

from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
    UnifiedTicket,
    TicketSearchCriteria,
)


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
            UnifiedTicketFactory.build(
                ticket_id=f"TEST-{i}",
                subject=f"Test Ticket {i}",
                **kwargs
            )
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


class PipeConfigFactory:
    """Factory for creating pipe configuration dictionaries."""

    @staticmethod
    def build(
            name: str = "test_pipe",
            pipe_class: str = "TestPipe",
            ticket_system_id: str = "test_system",
            **kwargs: Any,
    ) -> dict[str, Any]:
        defaults = {
            "name": name,
            "use": pipe_class,
            "when": True,
            "steps": [],
            "ticket_system_id": ticket_system_id,
        }
        defaults.update(kwargs)
        return defaults
