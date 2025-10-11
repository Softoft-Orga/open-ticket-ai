from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.registerable import Renderable
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNoteParams(BaseModel):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipeConfig(Renderable[AddNoteParams]):
    pass


class AddNotePipe(Pipe):
    def __init__(
        self, ticket_system: TicketSystemService, pipe_params: AddNotePipeConfig, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(pipe_params)
        self.ticket_system = ticket_system
        if isinstance(pipe_params, dict):
            self.config = AddNotePipeConfig.model_validate(pipe_params)
        elif isinstance(pipe_params, AddNotePipeConfig):
            self.config = pipe_params
        else:
            self.config = AddNotePipeConfig.model_validate(pipe_params.model_dump())

    async def _process(self) -> PipeResult:
        try:
            success = await self.ticket_system.add_note(self.config.params.ticket_id, self.config.params.note)
            if not success:
                return PipeResult(success=False, failed=True, message="Failed to add note to ticket", data={})
            return PipeResult(success=True, failed=False, data={})
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data={})
