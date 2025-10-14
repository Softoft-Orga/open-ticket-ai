from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketParams(BaseModel):
    ticket_id: str
    updated_ticket: UnifiedTicket


class UpdateTicketPipeConfig(PipeConfig):
    params: UpdateTicketParams


class UpdateTicketPipe(Pipe):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        config: UpdateTicketPipeConfig,
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(config, logger_factory=logger_factory)
        self._config = UpdateTicketPipeConfig.model_validate(config.model_dump())
        self._ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        success = await self._ticket_system.update_ticket(
            ticket_id=self._config.params.ticket_id,
            updates=self._config.params.updated_ticket,
        )
        if not success:
            return PipeResult(
                success=False,
                message="Failed to update ticket",
            )
        return PipeResult(success=True)
