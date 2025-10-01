from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketPipeConfig(BaseModel):
    ticket_id: str | int
    updated_ticket: UnifiedTicket


class UpdateTicketPipe(Pipe):
    def __init__(self, ticket_system: TicketSystemService, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.ticket_system = ticket_system
        pipe_config = UpdateTicketPipeConfig.model_validate(config)
        self.ticket_id = pipe_config.ticket_id
        self.updated_ticket = pipe_config.updated_ticket

    async def _process(self) -> PipeResult:
        try:
            await self.ticket_system.update_ticket(self.ticket_id, self.updated_ticket)
            return PipeResult(success=True, failed=False, data={})
        except Exception as e:
            return PipeResult(success=False, failed=True, data={"error": str(e)})
