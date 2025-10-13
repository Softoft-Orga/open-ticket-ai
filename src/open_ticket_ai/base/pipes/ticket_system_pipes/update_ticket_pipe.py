from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import UnifiedTicket


class UpdateTicketParams(BaseModel):
    ticket_id: str | int
    updated_ticket: UnifiedTicket


class UpdateTicketPipeResultData(BaseModel):
    ticket_updated: bool


class UpdateTicketPipeConfig(PipeConfig):
    pass


class UpdateTicketPipe(Pipe):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        pipe_config: UpdateTicketPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if logger_factory is None:
            raise ValueError("logger_factory is required")
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.pipe_config = UpdateTicketPipeConfig.model_validate(pipe_config.model_dump())
        # Validate params at runtime
        self.validated_params = UpdateTicketParams.model_validate(self.params)
        self.ticket_system = ticket_system

    async def _process(self) -> PipeResult[UpdateTicketPipeResultData]:
        try:
            ticket_id_str = str(self.validated_params.ticket_id)
            success = await self.ticket_system.update_ticket(ticket_id_str, self.validated_params.updated_ticket)
            if not success:
                return PipeResult[UpdateTicketPipeResultData](
                    success=False,
                    failed=True,
                    message="Failed to update ticket",
                    data=UpdateTicketPipeResultData(ticket_updated=False),
                )
            return PipeResult[UpdateTicketPipeResultData](
                success=True, failed=False, data=UpdateTicketPipeResultData(ticket_updated=True)
            )
        except Exception as e:
            return PipeResult[UpdateTicketPipeResultData](
                success=False, failed=True, message=str(e), data=UpdateTicketPipeResultData(ticket_updated=False)
            )
