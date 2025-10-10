

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult, RenderedPipeConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketPipeConfig(RenderedPipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicket


class UpdateTicketPipe(Pipe):
    def __init__(self, ticket_system: TicketSystemService, config: UpdateTicketPipeConfig, *args, **kwargs) -> None:
        super().__init__(config)
        self.ticket_system = ticket_system
        self.pipe_config = UpdateTicketPipeConfig.model_validate(config.model_dump())

    async def _process(self) -> PipeResult:
        try:
            success = await self.ticket_system.update_ticket(
                self.pipe_config.ticket_id, self.pipe_config.updated_ticket
            )
            if not success:
                return PipeResult(success=False, failed=True, message="Failed to update ticket", data={})
            return PipeResult(success=True, failed=False, data={})
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data={})
