from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketParams(BaseModel):
    ticket_id: str
    updated_ticket: UnifiedTicket


class UpdateTicketPipeConfig(PipeConfig):
    params: UpdateTicketParams


class UpdateTicketPipe(Pipe):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return UpdateTicketParams

    def __init__(
            self,
            ticket_system: TicketSystemService,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        success = await self._ticket_system.update_ticket(
            ticket_id=self._params.ticket_id,
            updates=self._params.updated_ticket,
        )
        return PipeResult(
            success=success,
            message="Updated Ticket" if success else "Failed to update ticket",
        )
