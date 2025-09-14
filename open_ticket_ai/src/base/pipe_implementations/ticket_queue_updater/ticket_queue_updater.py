"""Pipe implementation for updating a ticket's queue in the ticket system.

This pipe consumes the prediction of the preceding inference service and writes the
result back to the ticket system.  It needs to deal with a couple of edge cases:

* The prediction produced by the model might not use the same values as the ticket
  system.  A mapping between model predictions and ticket system values is therefore
  required.
* When the confidence of the prediction is below a configurable threshold the ticket
  should be routed to a *fallback* queue instead of the predicted one.
* The underlying ``TicketSystemAdapter`` exposes asynchronous methods.  The pipeline
  itself is synchronous though, therefore we have to run the coroutine explicitly.
"""

from __future__ import annotations

import asyncio

from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.models import (
    HFLocalAIInferenceServiceOutput,
)
from open_ticket_ai.src.base.pipe_implementations.empty_data_model import EmptyDataModel
from open_ticket_ai.src.base.pipe_implementations.ticket_queue_updater.models import (
    TicketQueueUpdaterConfig,
)
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import (
    TicketSystemAdapter,
)
from open_ticket_ai.src.core.ticket_system_integration.unified_models import (
    UnifiedQueue,
    UnifiedTicket,
)


class TicketQueueUpdater(
    Pipe[TicketQueueUpdaterConfig, HFLocalAIInferenceServiceOutput, EmptyDataModel]
):
    """Translate model predictions into ticket system queue updates."""

    def __init__(
        self, config: TicketQueueUpdaterConfig, ticket_system: TicketSystemAdapter
    ) -> None:
        super().__init__(config)
        # ``TicketQueueUpdaterConfig`` contains all knobs required to translate the
        # prediction into a value understood by the ticket system.
        self.modifier_config = config
        self.ticket_system = ticket_system

    # ------------------------------------------------------------------
    def _prediction_to_queue(self, prediction: str | int) -> str | int:
        """Map a model prediction to the ticket system queue value.

        ``TicketQueueUpdaterConfig.ticket_system_value2model_values`` stores the
        ticket system value as key and the corresponding model value as value.
        We therefore need to invert this mapping when looking up the queue name.
        If no mapping is found we simply fall back to the prediction itself.
        """

        for ticket_value, model_value in (
            self.modifier_config.ticket_system_value2model_values or {}
        ).items():
            if model_value == prediction:
                return ticket_value
        return prediction

    # ------------------------------------------------------------------
    def process(
        self, context: PipelineContext[HFLocalAIInferenceServiceOutput]
    ) -> PipelineContext[EmptyDataModel]:
        update_data = context.data
        if update_data:
            # Determine which queue should be used.  Low confidence predictions are
            # routed to the configured fallback queue.
            if (
                update_data.confidence
                < self.modifier_config.confidence_threshold
            ):
                queue_name = self.modifier_config.low_confidence_queue
            else:
                queue_name = self._prediction_to_queue(update_data.prediction)

            # ``update_ticket`` is async – run it explicitly.
            asyncio.run(
                self.ticket_system.update_ticket(
                    update_data.ticket.id,
                    UnifiedTicket(queue=UnifiedQueue(name=queue_name)),
                )
            )

        new_context = PipelineContext(
            meta_info=context.meta_info, data=EmptyDataModel()
        )
        return new_context
