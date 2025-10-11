from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.registerable import Renderable
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketParams(BaseModel):
    ticket_id: str | int
    updated_ticket: UnifiedTicket


class UpdateTicketPipeConfig(Renderable[UpdateTicketParams]):
    pass


class UpdateTicketPipe(Pipe):
    def __init__(
        self, ticket_system: TicketSystemService, pipe_params: UpdateTicketPipeConfig, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(pipe_params)
        self.ticket_system = ticket_system
        if isinstance(pipe_params, dict):
            self.config = UpdateTicketPipeConfig.model_validate(pipe_params)
        elif isinstance(pipe_params, UpdateTicketPipeConfig):
            self.config = pipe_params
        else:
            self.config = UpdateTicketPipeConfig.model_validate(pipe_params.model_dump())

    async def _process(self) -> PipeResult:
        try:
            success = await self.ticket_system.update_ticket(
                self.config.params.ticket_id, self.config.params.updated_ticket
            )
            if not success:
                return PipeResult(success=False, failed=True, message="Failed to update ticket", data={})
            return PipeResult(success=True, failed=False, data={})
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data={})
