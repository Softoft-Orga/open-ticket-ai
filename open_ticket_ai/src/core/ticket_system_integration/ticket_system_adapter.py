# FILE_PATH: open_ticket_ai\src\ce\ticket_system_integration\ticket_system_adapter.py
from abc import ABC, abstractmethod

from injector import inject

from open_ticket_ai.src.core.config.config_models import SystemConfig
from open_ticket_ai.src.core.mixins.registry_providable_instance import (
    Providable,
)
from .unified_models import (
    TicketSearchCriteria,
    UnifiedNote, UnifiedTicket, UnifiedTicketUpdate,
)


class TicketSystemAdapter(Providable, ABC):
    @inject
    def __init__(self, config: SystemConfig):
        super().__init__(config)
        self.config = config

    @abstractmethod
    async def update_ticket(self, ticket_id: str, updates: UnifiedTicketUpdate) -> bool:
        pass

    @abstractmethod
    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        pass

    @abstractmethod
    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        pass
