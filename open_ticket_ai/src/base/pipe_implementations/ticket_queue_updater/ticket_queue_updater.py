import logging

from injector import inject

from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import HFLocalAIInferenceServiceOutput
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket, UnifiedQueue, UnifiedNote


class TicketQueueUpdater(Pipe[HFLocalAIInferenceServiceOutput, EmptyDataModel]):
    InputModel = HFLocalAIInferenceServiceOutput
    OutputModel = EmptyDataModel

    @inject
    def __init__(self, config: OpenTicketAIConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.config = config
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(__name__)

    async def process(self, context: PipelineContext[HFLocalAIInferenceServiceOutput]) -> PipelineContext[
        EmptyDataModel]:
        if context.data.confidence < self.config.confidence_threshold:
            new_queue = self.config.low_confidence_queue
            self.logger.info(f"Low confidence {context.data.confidence}, moving to queue {new_queue}")
        else:
            new_queue = context.data.prediction
        self.logger.info(f"Trying to update ticket {context.data.ticket.id} to queue {new_queue}")

        try:
            update_worked = await self.ticket_system.update_ticket(
                context.data.ticket.id,
                UnifiedTicket(queue=UnifiedQueue(name=new_queue))
            )
        except Exception as e:
            return PipelineContext(
                meta_info=MetaInfo(
                    status=MetaInfo.Status.FAILED,
                    error_message=f"Updating Ticket failed: {e}",
                    failed_pipe=self.__class__.__name__
                ),
                data=None
            )
        if not update_worked:
            return PipelineContext(
                meta_info=MetaInfo(
                    status=MetaInfo.Status.FAILED,
                    error_message=f"Updating Ticket failed: Unknown error",
                    failed_pipe=self.__class__.__name__
                ),
                data=None
            )
        note = UnifiedNote(
            subject="Ticket wurde von KI verschoben",
            body=f"""
            Ticket wurde von KI in die Queue: {new_queue} verschoben! Konfidenz =  {context.data.confidence:.2f}.
            """
        )
        await (self.ticket_system.add_note_to_ticket(context.data.ticket.id, note))
        self.logger.info(f"Ticket {context.data.ticket.id} updated to queue {new_queue}")
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=EmptyDataModel()
        )
        return new_context
