# FILE_PATH: open_ticket_ai/src/ce/run/pipe_implementations/ticket_modifier.py
import logging

from open_ticket_ai.src.base.pipe_implementations.context_helper import get_value_from_context
from open_ticket_ai.src.core.config.pipe_configs import (
    TicketModifierAddNoteOperation,
    TicketModifierConfig,
    TicketModifierOperation,
    TicketModifierSetOperation,
)
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe
from open_ticket_ai.src.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.src.core.ticket_system_integration.unified_models import UnifiedNote, UnifiedQueue, \
    UnifiedPriority, UnifiedTicket


def operations_to_ticket_update(
    operations: list[TicketModifierOperation],
    context_data: dict,
) -> UnifiedTicket:
    """
    Converts a list of 'Set' operations from the config into a TicketUpdate object.
    """
    ticket_update = UnifiedTicket()
    for op in operations:
        if isinstance(op, TicketModifierSetOperation):
            value = get_value_from_context(context_data, op.value)

            if op.ticket_field == "queue_name" and value is not None:
                ticket_update.queue = UnifiedQueue(name=value)
            elif op.ticket_field == "priority_name" and value is not None:
                ticket_update.priority = UnifiedPriority(name=value)

    return ticket_update


class TicketModifier(Pipe):
    def __init__(self, config: TicketModifierConfig, ticket_system: TicketSystemAdapter):
        self.config = config
        self.ticket_system = ticket_system
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(self, context: PipelineContext[dict]) -> PipelineContext[dict]:
        ticket_id_field = self.config.ticket_id_field
        ticket_id = get_value_from_context(context.data, ticket_id_field)

        if not ticket_id:
            self.logger.error(f"Could not find ticket ID in context using key: {ticket_id_field}")
            # Decide if you want to stop the pipeline or just log an error
            return context

        self.logger.info(f"Modifying ticket with ID: {ticket_id}")

        operations = self.config.update_operations

        # Handle 'Set' operations
        ticket_update = operations_to_ticket_update(operations, context.data)
        if ticket_update.queue or ticket_update.priority:
            await self.ticket_system.update_ticket(ticket_id, ticket_update)
            self.logger.info(f"Updated ticket {ticket_id} with: {ticket_update.model_dump_json(exclude_none=True)}")

        # Handle 'AddNote' operations
        for op in operations:
            if isinstance(op, TicketModifierAddNoteOperation):
                subject = op.subject.format(**context.data)
                body = op.body.format(**context.data)
                note = UnifiedNote(subject=subject, body=body)
                await self.ticket_system.add_note_to_ticket(ticket_id, note)
                self.logger.info(f"Added note to ticket {ticket_id}: {subject}")

        return context
