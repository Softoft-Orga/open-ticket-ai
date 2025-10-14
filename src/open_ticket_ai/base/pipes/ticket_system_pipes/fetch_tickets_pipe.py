from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsParams(BaseModel):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipeResultData(BaseModel):
    fetched_tickets: list[dict[str, Any]]


class FetchTicketsPipeConfig(PipeConfig):
    pass


class FetchTicketsPipe(Pipe):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        pipe_config: FetchTicketsPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if logger_factory is None:
            raise ValueError("logger_factory is required")
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.pipe_config = FetchTicketsPipeConfig.model_validate(pipe_config.model_dump())
        # Validate params at runtime
        self.validated_params = FetchTicketsParams.model_validate(self.params)
        self.ticket_system = ticket_system

    async def _process(self) -> PipeResult[FetchTicketsPipeResultData]:
        try:
            search_criteria = self.validated_params.ticket_search_criteria
            if search_criteria is None:
                search_criteria = TicketSearchCriteria()
            tickets = await self.ticket_system.find_tickets(search_criteria) or []
            # Convert UnifiedTicket objects to dicts
            tickets_dict = [ticket.model_dump() if hasattr(ticket, "model_dump") else ticket for ticket in tickets]
            return PipeResult[FetchTicketsPipeResultData](
                success=True,
                failed=False,
                data=FetchTicketsPipeResultData(fetched_tickets=tickets_dict),
            )
        except Exception as e:
            return PipeResult[FetchTicketsPipeResultData](
                success=False, failed=True, message=str(e), data=FetchTicketsPipeResultData(fetched_tickets=[])
            )
