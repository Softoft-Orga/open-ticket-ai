from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNoteParams(BaseModel):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipeResultData(BaseModel):
    note_added: bool


class AddNotePipeConfig(PipeConfig):
    pass


class AddNotePipe(Pipe):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        pipe_config: AddNotePipeConfig,
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.pipe_config = AddNotePipeConfig.model_validate(pipe_config.model_dump())
        # Validate params at runtime
        self.validated_params = AddNoteParams.model_validate(self.params)
        self.ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        try:
            ticket_id_str = str(self.validated_params.ticket_id)
            success = await self.ticket_system.add_note(ticket_id_str, self.validated_params.note)
            if not success:
                return PipeResult(
                    success=False,
                    failed=True,
                    message="Failed to add note to ticket",
                    data=AddNotePipeResultData(note_added=False),
                )
            return PipeResult(success=True, failed=False, data=AddNotePipeResultData(note_added=True))
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data=AddNotePipeResultData(note_added=False))
