from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNotePipeConfig(BaseModel):
    ticket_system_id: str
    ticket_id: str | int
    note: str | UnifiedNote | dict[str, Any]


class AddNotePipe(Pipe):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        pipe_config = AddNotePipeConfig(**config)
        registry = UnifiedRegistry.get_registry_instance()
        self.ticket_system: TicketSystemService = registry.get_instance(pipe_config.ticket_system_id)
        self.ticket_id = pipe_config.ticket_id

        if isinstance(pipe_config.note, dict):
            self.note = UnifiedNote.model_validate(pipe_config.note)
        elif isinstance(pipe_config.note, str):
            self.note = UnifiedNote(body=pipe_config.note)
        else:
            self.note = pipe_config.note

    async def _process(self) -> dict[str, Any]:
        await self.ticket_system.add_note(self.ticket_id, self.note)
        return {}
