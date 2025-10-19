from typing import Any

from pydantic import Field

from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.base.ticket_system_integration.unified_models import UnifiedNote
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

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        ticket_id_str = str(self._params.ticket_id)

        self._logger.info(f"📌 Adding note to ticket: {ticket_id_str}")
        self._logger.debug(
            f"Note subject: {self._params.note.subject if hasattr(self._params.note, 'subject') else 'N/A'}"
        )

        note_preview = (
            str(self._params.note)[:100] + "..." if len(str(self._params.note)) > 100 else str(self._params.note)
        )
        self._logger.debug(f"Note preview: {note_preview}")

        try:
            await self._ticket_system.add_note(ticket_id_str, self._params.note)
            self._logger.info(f"✅ Successfully added note to ticket {ticket_id_str}")
            return PipeResult(succeeded=True, data={})
        except Exception as e:
            self._logger.error(f"❌ Failed to add note to ticket {ticket_id_str}: {e}", exc_info=True)
            raise
