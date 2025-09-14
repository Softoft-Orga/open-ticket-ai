from injector import inject

from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import HFLocalAIInferenceServiceOutput
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket, UnifiedQueue


class TicketQueueUpdater(Pipe[HFLocalAIInferenceServiceOutput, EmptyDataModel]):
    InputModel = HFLocalAIInferenceServiceOutput
    OutputModel = EmptyDataModel
    @inject
    def __init__(self, config: OpenTicketAIConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.modifier_config = config
        self.ticket_system = ticket_system

    async def process(self, context: PipelineContext[HFLocalAIInferenceServiceOutput]) -> PipelineContext[
        EmptyDataModel]:
        update_worked = await self.ticket_system.update_ticket(
            context.data.ticket.id,
            UnifiedTicket(queue=UnifiedQueue(name=context.data.prediction))
        )
        if not update_worked:
            raise RuntimeError("Failed to update ticket queue")
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=EmptyDataModel()
        )
        return new_context
