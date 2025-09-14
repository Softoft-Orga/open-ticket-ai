# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\basic_ticket_fetcher.py
from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.base.pipe_implementations.ticket_fetcher.models import QueueTicketFetcherOutput
from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


class QueueTicketFetcher(Pipe[EmptyDataModel, QueueTicketFetcherOutput]):

    def __init__(self, config: ProvidableConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.fetcher_config = config
        self.ticket_system = ticket_system

    def process(self, context: PipelineContext) -> PipelineContext:

        filters = self.fetcher_config.params.get("filters", [])

        supported_fields = set(SearchCriteria.__fields__.keys())
        search_kwargs: dict = {}

        if filters:
            for flt in filters:
                attr = flt.get("attribute")
                value = flt.get("value")
                if attr not in supported_fields:
                    context.stop_pipeline()
                    context.error_message = f"Unsupported filter attribute: {attr}"
                    context.failed_pipe = self.__class__.__name__
                    return context
                if attr == "queue":
                    search_kwargs["queue"] = UnifiedQueue(name=value)
                elif attr == "user":
                    search_kwargs["user"] = UnifiedUser(name=value)
                else:
                    search_kwargs[attr] = value
        else:
            search_kwargs["id"] = context.ticket_id

        criteria = SearchCriteria(**search_kwargs)

        ticket = self.ticket_system.find_first_ticket(criteria)
        if not ticket:
            context.stop_pipeline()
            context.error_message = "No ticket found"
            context.failed_pipe = self.__class__.__name__
            return context

        if hasattr(ticket, "model_dump"):
            ticket_data = ticket.model_dump()
        else:
            ticket_data = ticket

        context.data.update(ticket_data)
        context.ticket_id = ticket_data.get("id") or ticket_data.get("TicketID", context.ticket_id)
        return context

    @staticmethod
    def get_description() -> str:
        """Provides a static description of this pipe's functionality.

        Returns:
            str: A static description of the pipe's purpose and behavior.
        """
        return (
            "Basic ticket fetcher that retrieves ticket data from a source. "
            "It is a placeholder for a more complex implementation."
        )
