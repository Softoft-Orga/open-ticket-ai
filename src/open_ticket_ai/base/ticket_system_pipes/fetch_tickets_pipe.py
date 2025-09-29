from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsPipeConfig(BaseModel):
    ticket_system_id: str
    ticket_search_criteria: str | TicketSearchCriteria | dict[str, Any] | None = None


class FetchTicketsPipe(ConfigurablePipe):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        pipe_config = FetchTicketsPipeConfig(**config)
        registry = UnifiedRegistry.get_registry_instance()
        self.ticket_system: TicketSystemService = registry.get_instance(pipe_config.ticket_system_id)

        if isinstance(pipe_config.ticket_search_criteria, dict):
            self.search_criteria = TicketSearchCriteria.model_validate(pipe_config.ticket_search_criteria)
        else:
            self.search_criteria = pipe_config.ticket_search_criteria

    async def _process(self) -> dict[str, Any]:
        tickets = await self.ticket_system.find_tickets(self.search_criteria) or []
        return {"found_tickets": [ticket.model_dump() for ticket in tickets]}
