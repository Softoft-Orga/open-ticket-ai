from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNotePipeConfig(BaseModel):
    ticket_id: str | int
    note: UnifiedNote


class AddNotePipe(Pipe):
    def __init__(self, ticket_system: TicketSystemService, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.ticket_system = ticket_system
        
        # Normalize note input to UnifiedNote
        note_input = config.get("note")
        if isinstance(note_input, str):
            # String input - treat as note body
            config["note"] = {"body": note_input}
        elif isinstance(note_input, dict):
            # Dict input - ensure it's a proper UnifiedNote dict
            pass
        # If it's already a UnifiedNote instance, Pydantic will handle it
        
        pipe_config = AddNotePipeConfig.model_validate(config)
        self.ticket_id = pipe_config.ticket_id
        self.note = pipe_config.note

    async def _process(self) -> PipeResult:
        try:
            await self.ticket_system.add_note(self.ticket_id, self.note)
            return PipeResult(success=True, failed=False, data={})
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data={})
