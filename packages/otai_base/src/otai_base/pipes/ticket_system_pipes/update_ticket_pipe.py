from collections.abc import Callable

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket

from otai_base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe

type ContextResolver[T] = T | Callable[[PipeContext], T]


def _resolve[T](value: ContextResolver[T], context: PipeContext) -> T:
    return value(context) if callable(value) else value


class UpdateTicketPipe(TicketSystemPipe):
    def __init__(
        self,
        pipe_id: str,
        ticket_system: TicketSystemService,
        get_ticket_id: ContextResolver[str],
        get_updates: ContextResolver[UnifiedTicket],
    ) -> None:
        super().__init__(pipe_id, ticket_system)
        self._get_ticket_id = get_ticket_id
        self._get_updates = get_updates

    async def _process(self, context: PipeContext) -> PipeResult:
        ticket_id = _resolve(self._get_ticket_id, context)
        updates = _resolve(self._get_updates, context)
        self._logger.info(f"Updating ticket {ticket_id}")
        success = await self._ticket_system.update_ticket(
            ticket_id=str(ticket_id),
            updates=updates,
        )
        return PipeResult(succeeded=success)
