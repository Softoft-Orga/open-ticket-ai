from __future__ import annotations

from typing import Any, ClassVar

from open_ticket_ai import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote
from pydantic import Field, BaseModel, ConfigDict

from otai_base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe


class AddNoteParams(BaseModel):
    model_config = ConfigDict(extra="allow")
    ticket_id: str | int = Field(
        description=(
            "Identifier of the ticket to which the note should be added, accepting either string or integer format."
        )
    )
    note: UnifiedNote = Field(
        description="Note content including subject and body to be added to the specified ticket."
    )


class AddNotePipe(TicketSystemPipe[AddNoteParams]):
    ParamsModel: ClassVar[type[AddNoteParams]] = AddNoteParams

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        ticket_id_str = str(self._params.ticket_id)

        self._logger.info(f"📌 Adding note to ticket: {ticket_id_str}")
        self._logger.debug(
            f"Note subject: {self._params.note.subject if hasattr(self._params.note, 'subject') else 'N/A'}"
        )

        note_preview = self._preview_note(self._params.note)
        self._logger.debug(f"Note preview: {note_preview}")

        await self._ticket_system.add_note(ticket_id_str, self._params.note)
        self._logger.info(f"✅ Successfully added note to ticket {ticket_id_str}")
        return PipeResult(succeeded=True, data={})

    def _preview_note(self, note: UnifiedNote) -> str:
        note_str = str(note)
        if len(note_str) <= _NOTE_PREVIEW_LIMIT:
            return note_str
        return f"{note_str[:_NOTE_PREVIEW_LIMIT]}..."


_NOTE_PREVIEW_LIMIT = 100
