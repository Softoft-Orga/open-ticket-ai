from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.unified_registry import UnifiedRegistry
from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote


class AddNotePipeConfig(BaseModel):
    ticket_system_id: str
    ticket_id: str | int
    note: str | UnifiedNote | dict[str, Any]


class AddNotePipe(ConfigurablePipe):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.config = AddNotePipeConfig(**config)
        registry = UnifiedRegistry.get_registry_instance()
        self.ticket_system: TicketSystemService = registry.get_instance(self.config.ticket_system_id)
        
        if isinstance(self.config.note, dict):
            self.note = UnifiedNote.model_validate(self.config.note)
        elif isinstance(self.config.note, str):
            self.note = UnifiedNote(content=self.config.note)
        else:
            self.note = self.config.note

    async def _process(self) -> dict[str, Any]:
        await self.ticket_system.add_note(self.config.ticket_id, self.note)
        return {}
