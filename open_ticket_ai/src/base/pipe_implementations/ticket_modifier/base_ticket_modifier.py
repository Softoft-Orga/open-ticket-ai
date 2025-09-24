import logging
from abc import ABC, abstractmethod

from injector import inject

from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import (
    HFLocalAIInferenceServiceOutput,
)
from open_ticket_ai.src.base.pipe_implementations.ticket_modifier.models import TicketUpdaterOutput
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.meta_info import MetaInfo
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.pipeline.status import PipelineStatus
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    UnifiedTicket, UnifiedNote,
)


class BaseTicketModifier(
    Pipe[HFLocalAIInferenceServiceOutput, TicketUpdaterOutput],
    ABC,
):
    @inject
    def __init__(self, config: OpenTicketAIConfig, ticket_system: TicketSystemAdapter):
        self.config = config
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def build_ticket_update(
        self,
        data: HFLocalAIInferenceServiceOutput,
        config: OpenTicketAIConfig,
    ) -> UnifiedTicket | None:
        pass

    def build_note(self, data: HFLocalAIInferenceServiceOutput,
                   config: OpenTicketAIConfig, ticket_update: UnifiedTicket) -> UnifiedNote | None:
        pass

    async def process(
        self, context: PipelineContext[HFLocalAIInferenceServiceOutput]
    ) -> PipelineContext[TicketUpdaterOutput]:
        data = context.data
        self.logger.info(f"Processing ticket {data.ticket.id if data and data.ticket else 'N/A'} in {self.__class__.__name__}")
        if data is None or data.ticket is None:
            return PipelineContext(
                meta_info=MetaInfo(
                    status=PipelineStatus.FAILED,
                    error_message="Missing ticket in context.",
                    failed_pipe=self.__class__.__name__,
                ),
                data=None,
            )

        ticket_update = self.build_ticket_update(data, self.config)
        self.logger.info(f"Built ticket update: {ticket_update}")
        if ticket_update is None:
            return PipelineContext(meta_info=context.meta_info, data=TicketUpdaterOutput(ticket=data.ticket))

        try:
            ok = await self.ticket_system.update_ticket(data.ticket.id, ticket_update)
            if not ok:
                raise RuntimeError("Adapter returned False")
        except Exception as e:
            return PipelineContext(
                meta_info=MetaInfo(
                    status=PipelineStatus.FAILED,
                    error_message=f"Ticket update failed: {e}",
                    failed_pipe=self.__class__.__name__,
                ),
                data=None,
            )
            raise e
        note = self.build_note(data, self.config, ticket_update)
        if note is not None:
            await self.ticket_system.add_note_to_ticket(ticket_update.id, note)

        return PipelineContext(meta_info=context.meta_info, data=TicketUpdaterOutput(ticket=data.ticket))
