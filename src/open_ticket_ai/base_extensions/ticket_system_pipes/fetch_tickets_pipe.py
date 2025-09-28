from typing import Any

from injector import inject

from open_ticket_ai.base_extensions.pipe_configs import RawTicketFetchPipeConfig
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemService
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class FetchTicketsPipe(BasePipe[RawTicketFetchPipeConfig]):
    """A pipe that fetches tickets from the ticket system based on search criteria."""

    @staticmethod
    def get_raw_config_model_type() -> type[RawPipeConfig]:
        return RawTicketFetchPipeConfig

    @inject
    def __init__(self, config: RawTicketFetchPipeConfig, ticket_system: TicketSystemService):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def _process(self) -> dict[str, Any]:
        tickets = await self.ticket_system.find_tickets(self.config.)

        if not tickets:
            return {"found_tickets": []}

        self._logger.info(f"Found {len(tickets)} tickets")
        return {"found_tickets": [ticket.model_dump() for ticket in tickets]}

    def _convert_to_search_criteria(
        self, criteria: dict[str, Any] | TicketSearchCriteria
    ) -> TicketSearchCriteria:
        if isinstance(criteria, TicketSearchCriteria):
            return criteria
        return TicketSearchCriteria(**criteria)
