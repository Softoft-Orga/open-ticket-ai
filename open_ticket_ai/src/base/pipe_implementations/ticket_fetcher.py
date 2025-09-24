# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\basic_ticket_fetcher.py
import logging
from typing import Sequence

from open_ticket_ai.src.core.config.pipe_configs import (
    TicketFetcherConfig,
    TicketFilterConfig,
)
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.pipeline.status import PipelineStatus
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedQueue


def ticket_filters_to_search_criteria(
    filters: Sequence[TicketFilterConfig],
) -> TicketSearchCriteria:
    """
    Converts a list of filter dictionaries into a TicketSearchCriteria object.

    Args:
        filters: A list of filter dictionaries, e.g.,
                 [{'field': 'queue', 'operator': 'equals', 'value': 'Support'}]
        limit: The maximum number of results to return.

    Returns:
        A TicketSearchCriteria object ready for use.
    """
    # Filter for dictionaries where the 'operator' is 'equals'
    equal_filters = [f for f in filters if f.operator == 'equals']

    # Create a dictionary from the filtered list for easy lookups
    equal_filters_dict = {f.field: f.value for f in equal_filters}

    # Instantiate the UnifiedQueue Pydantic model
    unified_queue_filter = (
        UnifiedQueue(
            name=equal_filters_dict.get('queue_name'),
            id=equal_filters_dict.get('queue_id'),
        )
        if 'queue_name' in equal_filters_dict or 'queue_id' in equal_filters_dict
        else None
    )

    # Instantiate and return the TicketSearchCriteria Pydantic model
    return TicketSearchCriteria(
        queue=unified_queue_filter,
        limit=1
    )


class TicketFetcher(Pipe):
    def __init__(self, config: TicketFetcherConfig, ticket_system: TicketSystemAdapter):
        self.config = config
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(self, context: PipelineContext[dict]) -> PipelineContext[dict]:
        filters = self.config.filters
        output_field = self.config.output_field

        self.logger.info(f"Fetching tickets with filters: {filters}")
        search_criteria = ticket_filters_to_search_criteria(filters)
        self.logger.info(f"Search criteria: {search_criteria}")
        tickets = await self.ticket_system.find_tickets(search_criteria)

        if not tickets:
            self.logger.warning(f"No tickets found for filters: {filters}")
            return PipelineContext(
                meta_info=MetaInfo(
                    status=PipelineStatus.STOPPED,
                    error_message=f"No ticket found for filters: '{filters}'",
                    failed_pipe=self.__class__.__name__
                ),
                data=context.data
            )

        ticket_dict = tickets[0].model_dump()

        self.logger.info(f"Fetched ticket {ticket_dict['subject']}")
        return PipelineContext(
            meta_info=context.meta_info,
            data=context.data | {output_field: ticket_dict}
        )
