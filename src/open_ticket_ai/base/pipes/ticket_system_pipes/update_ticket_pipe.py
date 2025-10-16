from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipeline.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketParams(StrictBaseModel):
    ticket_id: str
    updated_ticket: UnifiedTicket


class UpdateTicketPipe(TicketSystemPipe[UpdateTicketParams]):
    @staticmethod
    def get_params_model() -> type[UpdateTicketParams]:
        return UpdateTicketParams

    async def _process(self) -> PipeResult:
        success = await self._ticket_system.update_ticket(
            ticket_id=self._params.ticket_id,
            updates=self._params.updated_ticket,
        )
        return PipeResult(
            succeeded=success,
            message="Updated Ticket" if success else "Failed to update ticket",
        )
