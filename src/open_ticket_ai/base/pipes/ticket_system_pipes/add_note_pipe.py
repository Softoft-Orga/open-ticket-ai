from pydantic import Field

from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.base.ticket_system_integration import UnifiedNote
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class AddNoteParams(StrictBaseModel):
    ticket_id: str | int = Field(
        description=(
            "Identifier of the ticket to which the note should be added, accepting either string or integer format."
        )
    )
    note: UnifiedNote = Field(
        description="Note content including subject and body to be added to the specified ticket."
    )


class AddNotePipe(TicketSystemPipe[AddNoteParams]):
    @staticmethod
    def get_params_model() -> type[AddNoteParams]:
        return AddNoteParams

    async def _process(self) -> PipeResult:
        ticket_id_str = str(self._params.ticket_id)
        await self._ticket_system.add_note(ticket_id_str, self._config.params.note)
        return PipeResult(succeeded=True, data={})
