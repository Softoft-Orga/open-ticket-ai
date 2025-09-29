from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketPipeConfig(BaseModel):
    ticket_system_id: str
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicket


class UpdateTicketPipe(ConfigurablePipe):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.config = UpdateTicketPipeConfig(**config)
        registry = UnifiedRegistry.get_registry_instance()
        self.ticket_system: TicketSystemService = registry.get_instance(self.config.ticket_system_id)

        if isinstance(self.config.updated_ticket, dict):
            self.updated_ticket = UnifiedTicket.model_validate(self.config.updated_ticket)
        elif isinstance(self.config.updated_ticket, str):
            self.updated_ticket = UnifiedTicket(subject=self.config.updated_ticket)
        else:
            self.updated_ticket = self.config.updated_ticket

    async def _process(self) -> dict[str, Any]:
        await self.ticket_system.update_ticket(
            self.config.ticket_id,
            self.updated_ticket
        )
        return {}
