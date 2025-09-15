# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\basic_ticket_fetcher.py
import logging

from injector import inject

from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.base.pipe_implementations.ticket_fetcher.models import QueueTicketFetcherOutput
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.pipeline.status import PipelineStatus
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedQueue


class QueueTicketFetcher(Pipe[EmptyDataModel, QueueTicketFetcherOutput]):
    InputModel = EmptyDataModel
    OutputModel = QueueTicketFetcherOutput

    @inject
    def __init__(self, config: OpenTicketAIConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(self, context: PipelineContext[EmptyDataModel]) -> PipelineContext[QueueTicketFetcherOutput]:
        self.logger.info(f"Fetching ticket from queue {self.config.filter_by_queue}")
        ticket = await self.ticket_system.find_first_ticket(
            TicketSearchCriteria(queue=UnifiedQueue(name=self.config.filter_by_queue))
        )
        if not ticket:
            return PipelineContext(
                meta_info=MetaInfo(
                    status=PipelineStatus.STOPPED,
                    error_message=f"No ticket found in queue '{self.config.filter_by_queue}'",
                    failed_pipe=self.__class__.__name__
                ),
                data=None
            )
        self.logger.info(f"Fetched ticket {ticket.id}")
        return PipelineContext(
            meta_info=context.meta_info,
            data=QueueTicketFetcherOutput(ticket=ticket)
        )
