from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipeline.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNoteParams(StrictBaseModel):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipe(TicketSystemPipe[AddNoteParams]):
    @staticmethod
    def get_params_model() -> type[AddNoteParams]:
        return AddNoteParams

    async def _process(self) -> PipeResult:
        ticket_id_str = str(self._params.ticket_id)
        await self._ticket_system.add_note(ticket_id_str, self._config.params.note)
        return PipeResult(succeeded=True, data={})
