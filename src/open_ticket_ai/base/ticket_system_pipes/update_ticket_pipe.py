from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketPipeConfig(BaseModel):
    ticket_system_id: str
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicket


class UpdateTicketPipe(Pipe):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        pipe_config = UpdateTicketPipeConfig(**config)
        registry = UnifiedRegistry.get_registry_instance()
        self.ticket_system: TicketSystemService = registry.get_instance(pipe_config.ticket_system_id)
        self.ticket_id = pipe_config.ticket_id

        if isinstance(pipe_config.updated_ticket, dict):
            self.updated_ticket = UnifiedTicket.model_validate(pipe_config.updated_ticket)
        elif isinstance(pipe_config.updated_ticket, str):
            self.updated_ticket = UnifiedTicket(subject=pipe_config.updated_ticket)
        else:
            self.updated_ticket = pipe_config.updated_ticket

    async def _process(self) -> PipeResult:
        await self.ticket_system.update_ticket(
            self.ticket_id,
            self.updated_ticket
        )
        return PipeResult(
            success=True,
            failed=False,
            message=f"Ticket {self.ticket_id} updated",
            data={},
        )
