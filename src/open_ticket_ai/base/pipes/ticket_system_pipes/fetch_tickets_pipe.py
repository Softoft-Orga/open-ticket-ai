from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedTicket


class FetchTicketsParams(BaseModel):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipeResultData(BaseModel):
    fetched_tickets: list[UnifiedTicket]


class FetchTicketsPipeConfig(PipeConfig):
    params: FetchTicketsParams


class FetchTicketsPipe(Pipe):
    def __init__(
        self,
        ticket_system: TicketSystemService,
        config: FetchTicketsPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if logger_factory is None:
            raise ValueError("logger_factory is required")
        super().__init__(config, logger_factory=logger_factory)
        self._config = FetchTicketsPipeConfig.model_validate(config.model_dump())
        self._ticket_system = ticket_system

    async def _process(self) -> PipeResult:
        search_criteria = self._config.params.ticket_search_criteria
        tickets = await self._ticket_system.find_tickets(search_criteria)
        return PipeResult(
            success=True,
            data={
                "fetched_tickets": tickets,
            },
        )
