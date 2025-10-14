from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.renderable.renderable import EmptyModel
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNoteParams(BaseModel):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipeConfig(PipeConfig):
    params: AddNoteParams


class AddNotePipe(Pipe):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        config: AddNotePipeConfig,
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(config, logger_factory=logger_factory)
        self._config = AddNotePipeConfig.model_validate(config.model_dump())
        self._ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        ticket_id_str = str(self._config.params.ticket_id)
        await self._ticket_system.add_note(ticket_id_str, self._config.params.note)
        return PipeResult(success=True, data={})
