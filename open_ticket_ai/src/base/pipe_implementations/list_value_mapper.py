# FILE_PATH: open_ticket_ai/src/ce/run/pipe_implementations/list_value_mapper.py
import logging

from open_ticket_ai.src.core.config.base_pipe_config import BasePipeConfig
from open_ticket_ai.src.core.config.pipe_configs import ListValueMapperConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class ListValueMapper(Pipe):
    def __init__(self, config: ListValueMapperConfig):
        super().__init__(config)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def _process(self, context: PipelineContext, rendered_config: ListValueMapperConfig) -> PipelineContext:
        mapped_value = rendered_config.input_value
        for target_value, possible_values in rendered_config.mapping_rules.items():
            if rendered_config.input_value in possible_values:
                mapped_value = target_value
                self.logger.info(f"Mapped input '{rendered_config.input_value}' to '{mapped_value}'.")
                break

        return PipelineContext(
            meta_info=context.meta_info,
            data=context.data | {rendered_config.output_field: mapped_value}
        )
