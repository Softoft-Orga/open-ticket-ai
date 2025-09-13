# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\basic_ticket_fetcher.py
from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.ticket_system_integration.ticket_system_adapter import (
    TicketSystemAdapter,
)
from open_ticket_ai.src.ticket_system_integration.unified_models import (
    SearchCriteria,
    UnifiedQueue,
    UnifiedUser,
)


class BasicTicketFetcher(Pipe):
    """Simple fetcher that loads ticket data using the ticket system adapter.

    This pipe retrieves ticket information from an external ticket system using
    the provided adapter. It serves as a placeholder for more complex fetching
    implementations.

    Attributes:
        fetcher_config (`open_ticket_ai.src.ce.core.config.config_models.ProvidableConfig`): Configuration instance for the fetcher.
        ticket_system (`TicketSystemAdapter`): Adapter for interacting with the ticket system.
    """

    def __init__(self, config: ProvidableConfig, ticket_system: TicketSystemAdapter):
        """Initializes the BasicTicketFetcher with configuration and ticket system adapter.

        Args:
            config (`open_ticket_ai.src.ce.core.config.config_models.ProvidableConfig`): The configuration instance for the fetcher.
            ticket_system (`TicketSystemAdapter`): The adapter for interacting with the ticket system.
        """
        super().__init__(config)
        self.fetcher_config = config
        self.ticket_system = ticket_system

    def process(self, context: PipelineContext) -> PipelineContext:
        """Fetch ticket data using configured filters and update the context.

        The fetcher reads optional `filters` from its configuration. Each filter
        contains an `attribute` and `value` entry. Attributes must map to
        fields supported by `TicketSearchCriteria`. Unsupported attributes
        result in a controlled pipeline stop.

        If no filters are provided, the `ticket_id` from the context is used as
        the search criterion. When no ticket is found, the pipeline is stopped.

        Args:
            context: The current `PipelineContext`.

        Returns:
            The updated context or the original context if the pipeline was
            stopped.
        """

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
