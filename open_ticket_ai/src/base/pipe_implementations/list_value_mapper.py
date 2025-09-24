# FILE_PATH: open_ticket_ai/src/ce/run/pipe_implementations/list_value_mapper.py
import logging

from open_ticket_ai.src.base.pipe_implementations.context_helper import get_value_from_context
from open_ticket_ai.src.core.config.pipe_configs import ListValueMapperConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class ListValueMapper(Pipe):
    def __init__(self, config: ListValueMapperConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(self, context: PipelineContext[dict]) -> PipelineContext[dict]:
        # Safely get configuration parameters
        input_field = self.config.input_field
        output_field = self.config.output_field
        mapping_rules = self.config.mapping_rules

        if not all([input_field, output_field]):
            self.logger.error("Pipe is misconfigured. Missing 'input_field' or 'output_field'.")
            return context

        input_value = get_value_from_context(context.data, input_field)

        if input_value is None:
            self.logger.warning(f"Input field '{input_field}' not found in context. Passing context through.")
            return context

        # Default to the original value if no mapping is found
        mapped_value = input_value
        found_match = False

        for target_value, possible_values in mapping_rules.items():
            if input_value in possible_values:
                mapped_value = target_value
                found_match = True
                self.logger.info(f"Mapped input '{input_value}' to '{mapped_value}'.")
                break

        if not found_match:
            self.logger.info(f"No mapping found for input '{input_value}'. Using original value.")

        return PipelineContext(
            meta_info=context.meta_info,
            data=context.data | {output_field: mapped_value}
        )
