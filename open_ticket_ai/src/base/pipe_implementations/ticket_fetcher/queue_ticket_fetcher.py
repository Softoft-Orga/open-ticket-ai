# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\basic_ticket_fetcher.py
from injector import inject

from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.base.pipe_implementations.ticket_fetcher.models import QueueTicketFetcherOutput
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import TicketSearchCriteria, UnifiedQueue


class QueueTicketFetcher(Pipe[EmptyDataModel, QueueTicketFetcherOutput]):
    InputModel = EmptyDataModel
    OutputModel = QueueTicketFetcherOutput
    @inject
    def __init__(self, config: OpenTicketAIConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system

    async def process(self, context: PipelineContext[EmptyDataModel]) -> PipelineContext[QueueTicketFetcherOutput]:

        ticket = await self.ticket_system.find_first_ticket(
            TicketSearchCriteria(queue=UnifiedQueue(name=self.config.filter_by_queue))
        )
        if not ticket:
            context.stop_pipeline()
            context.error_message = "No ticket found"
            context.failed_pipe = self.__class__.__name__
            raise RuntimeError("No ticket found")
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=QueueTicketFetcherOutput(ticket=ticket)
        )
        return new_context
