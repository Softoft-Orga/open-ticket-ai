from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import HFLocalAIInferenceServiceOutput
from open_ticket_ai.src.base.pipe_implementations.ticket_modifier.base_ticket_modifier import BaseTicketModifier
from open_ticket_ai.src.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket, UnifiedQueue, UnifiedNote


class TicketQueueModifier(BaseTicketModifier):
    def build_ticket_update(
        self, data: HFLocalAIInferenceServiceOutput, config: OpenTicketAIConfig
    ) -> UnifiedTicket | None:
        new_queue = config.low_confidence_queue if data.confidence < config.queue_confidence_threshold else data.prediction
        return UnifiedTicket(id=data.ticket.id, queue=UnifiedQueue(name=new_queue))

    def build_note(self, data: HFLocalAIInferenceServiceOutput,
                   config: OpenTicketAIConfig, ticket_update: UnifiedTicket) -> UnifiedNote | None:
        note = UnifiedNote(
            subject="KI: Queue geändert",
            body=f"Ticket wurde per KI in die Queue „{ticket_update.queue}“ verschoben. Konfidenz: {data.confidence:.2f}.",
        )
        self.logger.info(f"Ticket {ticket_update.id} queue → {ticket_update.queue}")
        return note
