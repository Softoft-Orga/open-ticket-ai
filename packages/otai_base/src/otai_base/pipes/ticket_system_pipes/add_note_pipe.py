from collections.abc import Callable

from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedNote

from otai_base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe

type ContextResolver[T] = T | Callable[[PipeContext], T]


def _resolve[T](value: ContextResolver[T], context: PipeContext) -> T:
    return value(context) if callable(value) else value


class AddNotePipe(TicketSystemPipe):
    def __init__(
        self,
        pipe_id: str,
        ticket_system: TicketSystemService,
        get_ticket_id: ContextResolver[str],
        get_note: ContextResolver[UnifiedNote],
    ) -> None:
        super().__init__(pipe_id, ticket_system)
        self._get_ticket_id = get_ticket_id
        self._get_note = get_note

    async def _process(self, context: PipeContext) -> PipeResult:
        ticket_id = str(_resolve(self._get_ticket_id, context))
        note = _resolve(self._get_note, context)
        self._logger.info(f"Adding note to ticket {ticket_id}")
        await self._ticket_system.add_note(ticket_id, note)
        return PipeResult.success()
