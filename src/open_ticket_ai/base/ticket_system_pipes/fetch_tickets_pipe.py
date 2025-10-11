from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.registerable import Renderable
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsParams(BaseModel):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipeConfig(Renderable[FetchTicketsParams]):
    pass


class FetchTicketsPipe(Pipe):
    def __init__(
        self, ticket_system: TicketSystemService, pipe_params: FetchTicketsPipeConfig, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(pipe_params)
        self.ticket_system = ticket_system
        if isinstance(pipe_params, dict):
            self.config = FetchTicketsPipeConfig.model_validate(pipe_params)
        elif isinstance(pipe_params, FetchTicketsPipeConfig):
            self.config = pipe_params
        else:
            self.config = FetchTicketsPipeConfig.model_validate(pipe_params.model_dump())

    async def _process(self) -> PipeResult:
        try:
            tickets = await self.ticket_system.find_tickets(self.config.params.ticket_search_criteria) or []
            return PipeResult(
                success=True,
                failed=False,
                data={"value": [ticket.model_dump() for ticket in tickets]},
            )
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data={"value": []})
