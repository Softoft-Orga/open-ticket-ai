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


class FetchTicketsPipeConfig(PipeConfig[FetchTicketsParams]):
    pass


class FetchTicketsPipe(Pipe[FetchTicketsParams]):
    params_class = FetchTicketsParams

    def __init__(
        self,
        ticket_system: TicketSystemService,
        pipe_config: FetchTicketsPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.ticket_system = ticket_system

    async def _process(self) -> PipeResult[FetchTicketsPipeResultData]:
        try:
            search_criteria = self.params.ticket_search_criteria
            if search_criteria is None:
                search_criteria = TicketSearchCriteria()
            tickets = await self.ticket_system.find_tickets(search_criteria) or []
            return PipeResult[FetchTicketsPipeResultData](
                success=True,
                failed=False,
                data=FetchTicketsPipeResultData(fetched_tickets=[ticket for ticket in tickets]),
            )
        except Exception as e:
            return PipeResult[FetchTicketsPipeResultData](
                success=False, failed=True, message=str(e), data=FetchTicketsPipeResultData(fetched_tickets=[])
            )
