from open_ticket_ai.src.core.config.config_models import ProvidableConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket
from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel


class GenericTicketUpdater(Pipe[UnifiedTicket, EmptyDataModel]):
    def __init__(self, config: ProvidableConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.modifier_config = config
        self.ticket_system = ticket_system

    def process(self, context: PipelineContext[UnifiedTicket]) -> PipelineContext[EmptyDataModel]:
        update_data: UnifiedTicket = context.data
        if update_data:
            self.ticket_system.update_ticket(context.ticket_id, update_data)
        return context
