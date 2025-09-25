# FILE_PATH: open_ticket_ai/src/ce/run/pipe_implementations/ticket_modifier.py
import logging

from open_ticket_ai.src.core.config.pipe_configs import (
    TicketModifierConfig,
    TicketModifierSetOperation,
)
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedTicket, UnifiedEntity


def operations_to_ticket_update(
    operations: list[TicketModifierSetOperation],
) -> UnifiedTicket:
    """
    Converts a list of 'Set' operations from the config into a TicketUpdate object.
    """
    ticket_update = UnifiedTicket()
    for op in operations:
        if op.ticket_field == "queue_name":
            ticket_update.queue = UnifiedEntity(name=op.value)
        elif op.ticket_field == "priority_name":
            ticket_update.priority = UnifiedEntity(name=op.value)

    return ticket_update


class TicketModifier(Pipe):
    def __init__(self, config: TicketModifierConfig, ticket_system: TicketSystemAdapter):
        super().__init__(config)
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(self.__class__.__name__)

    async def _process(self, context: PipelineContext, rendered_config: TicketModifierConfig) -> PipelineContext:
        if not rendered_config.ticket_id:
            self.logger.error(f"Could not find ticket ID in context using key: {rendered_config.ticket_id}")
            return context

        self.logger.info(f"Modifying ticket with ID: {rendered_config.ticket_id}")

        ticket_update = operations_to_ticket_update(rendered_config.update_operations)
        if ticket_update.queue or ticket_update.priority:
            await self.ticket_system.update_ticket(rendered_config.ticket_id, ticket_update)
            self.logger.info(
                f"Updated ticket {rendered_config.ticket_id} with: {ticket_update.model_dump_json(exclude_none=True)}")

        return context
