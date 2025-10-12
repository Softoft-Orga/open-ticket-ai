from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNotePipeConfig(PipeConfig):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipe(Pipe):
    def __init__(
        self, ticket_system: TicketSystemService, pipe_params: AddNotePipeConfig, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(pipe_params)
        self.ticket_system = ticket_system
        self.pipe_config = pipe_params

    async def _process(self) -> PipeResult:
        try:
            success = await self.ticket_system.add_note(self.pipe_config.ticket_id, self.pipe_config.note)
            if not success:
                return PipeResult(success=False, failed=True, message="Failed to add note to ticket", data=BaseModel())
            return PipeResult(success=True, failed=False, data=BaseModel())
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data=BaseModel())
