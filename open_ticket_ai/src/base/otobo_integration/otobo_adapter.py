import logging

from injector import inject
from otobo import TicketSearchRequest, TicketUpdateRequest, OTOBOClient, TicketDetailOutput
from otobo.models.ticket_models import TicketBase

from open_ticket_ai.src.core.config.config_models import SystemConfig
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedNote, UnifiedTicket, UnifiedTicketBase,
)
from open_ticket_ai.src.base.otobo_integration.models import TicketAdapter


class OTOBOAdapter(TicketSystemAdapter):
    @staticmethod
    def get_description() -> str:
        return "Adapter for OTOBO ticket system integration, providing methods to retrieve and update tickets."

    @inject
    def __init__(self, config: SystemConfig | None, otobo_client: OTOBOClient):
        super().__init__(config)
        self.otobo_client = otobo_client

    async def find_tickets(self, criteria: TicketSearchCriteria) -> list[UnifiedTicket]:
        query = TicketSearchRequest()
        if criteria.queue and criteria.queue.id:
            query.QueueIDs = [int(criteria.queue.id)]
        if criteria.queue and criteria.queue.name:
            query.Queues = [criteria.queue.name]
        result: list[TicketDetailOutput] = await self.otobo_client.search_and_get(query=query)
        logging.info("OTOBO search result: %s", result)
        return [TicketAdapter(ticket) for ticket in result]

    async def find_first_ticket(self, criteria: TicketSearchCriteria) -> UnifiedTicket | None:
        result = await self.find_tickets(criteria)
        return result[0] if len(result) >= 1 else None

    async def update_ticket(self, ticket_id: str, updates: UnifiedTicketBase) -> bool:
        update_params = TicketUpdateRequest(
            TicketID=int(ticket_id),
            Ticket=TicketBase(
                Title=updates.subject,
                QueueID=updates.queue.id if updates.queue and updates.queue.id else None,
                Queue=updates.queue.name if updates.queue and updates.queue.name else None,
                PriorityID=updates.priority.id if updates.priority and updates.priority.id else None,
                Priority=updates.priority.name if updates.priority and updates.priority.name else None,
            ),
        )
        await self.otobo_client.update_ticket(payload=update_params)
        return True
