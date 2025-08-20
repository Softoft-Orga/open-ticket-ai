# FILE_PATH: open_ticket_ai\src\ce\run\pipe_implementations\generic_ticket_updater.py
from open_ticket_ai.src.core.config.config_models import ProvidableConfig

from open_ticket_ai.src.core.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.ticket_system_integration.ticket_system_adapter import (
    TicketSystemAdapter,
)
from open_ticket_ai.src.ticket_system_integration.unified_models import UnifiedTicket


class GenericTicketUpdater(Pipe[UnifiedTicket, EmptyDataModel]):
    """Updates tickets in external systems using pipeline-generated data.

    This component updates tickets in external ticket tracking systems (e.g., Jira, ServiceNow)
    using data generated during pipeline execution. It checks the pipeline context for update
    instructions and delegates the update operation to the configured ticket system adapter.

    `Attributes`:
        modifier_config: Configuration settings for the ticket updater.
        ticket_system: Adapter instance for interacting with the external ticket system.
    """

    def __init__(self, config: ProvidableConfig, ticket_system: TicketSystemAdapter):
        """Initializes the `GenericTicketUpdater` with configuration and ticket system adapter.

        `Args`:
            config: Configuration instance containing settings for the pipeline component.
            ticket_system: Adapter object that handles communication with the external ticket system.
        """
        super().__init__(config)
        self.modifier_config = config
        self.ticket_system = ticket_system

    def process(self, context: PipelineContext[UnifiedTicket]) -> PipelineContext[EmptyDataModel]:
        """Updates the ticket in the external system if update data exists.

        Retrieves update data from `context.data` (of type `UnifiedTicket`) and updates the ticket
        in the ticket system when update data is present. Returns the context unchanged after processing.

        `Args`:
            context: Pipeline context containing data and ticket information.

        `Returns`:
            The original pipeline context after processing (unchanged).

        `Example`:
            ```python
            context = PipelineContext(ticket_id="TICKET-123", data=update_data)
            updater.process(context)  # Updates ticket if update_data exists
            ```
        """
        update_data: UnifiedTicket = context.data
        if update_data:
            self.ticket_system.update_ticket(context.ticket_id, update_data)
        return context

    @staticmethod
    def get_description() -> str:
        """Provides a description of the pipe's purpose.

        `Returns`:
            A string describing the pipe's functionality.
        """
        return "Updates the ticket in the ticket system using data stored in the context."
