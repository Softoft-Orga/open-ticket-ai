from typing import Any

from pydantic import Field

from open_ticket_ai.base.pipes.ticket_system_pipes.ticket_system_pipe import TicketSystemPipe
from open_ticket_ai.base.ticket_system_integration.unified_models import UnifiedTicket
from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class UpdateTicketParams(StrictBaseModel):
    ticket_id: str | int = Field(description="Unique identifier of the ticket to be updated in the ticket system.")
    updated_ticket: UnifiedTicket = Field(
        description="Updated ticket data containing the fields and values to apply to the existing ticket."
    )


class UpdateTicketPipe(TicketSystemPipe[UpdateTicketParams]):
    @staticmethod
    def get_params_model() -> type[UpdateTicketParams]:
        return UpdateTicketParams

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        self._logger.info(f"📝 Updating ticket: {self._params.ticket_id}")
        self._logger.debug(f"Update data: {self._params.updated_ticket.model_dump(exclude_none=True)}")

        success = await self._ticket_system.update_ticket(
            ticket_id=str(self._params.ticket_id),
            updates=self._params.updated_ticket,
        )
        return PipeResult(
            succeeded=success,
        )
