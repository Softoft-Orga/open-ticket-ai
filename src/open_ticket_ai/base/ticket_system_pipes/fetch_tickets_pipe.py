from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult, RenderedPipeConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsPipeConfig(RenderedPipeConfig):
    ticket_search_criteria: TicketSearchCriteria | None = None


class FetchTicketsPipe(Pipe):
    def __init__(self, ticket_system: TicketSystemService, config: FetchTicketsPipeConfig, *args, **kwargs) -> None:
        super().__init__(config)
        self.ticket_system = ticket_system
        self.pipe_config = FetchTicketsPipeConfig.model_validate(config.model_dump())

    async def _process(self) -> PipeResult:
        try:
            tickets = await self.ticket_system.find_tickets(self.pipe_config.ticket_search_criteria) or []
            return PipeResult(
                success=True,
                failed=False,
                data={"value": [ticket.model_dump() for ticket in tickets]},
            )
        except Exception as e:
            return PipeResult(success=False, failed=True, message=str(e), data={"value": []})
