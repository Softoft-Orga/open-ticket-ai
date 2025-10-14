from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNoteParams(BaseModel):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipe(Pipe):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return AddNoteParams

    def __init__(
        self,
        ticket_system: TicketSystemService,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        ticket_id_str = str(self._params.ticket_id)
        await self._ticket_system.add_note(ticket_id_str, self._config.params.note)
        return PipeResult(success=True, data={})
