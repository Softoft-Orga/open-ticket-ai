import logging

from injector import inject

from open_ticket_ai.src.base.pipe_implementations.context_helper import get_value_from_context
from open_ticket_ai.src.core.config.pipe_configs import SubjectBodyPreparerConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class SubjectBodyPreparer(Pipe):
    @inject
    def __init__(self, config: SubjectBodyPreparerConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(self, context: PipelineContext[dict]) -> PipelineContext[dict]:
        self.logger.info(f"Preparing subject and body.")

        # Correctly access the keys from the config dictionary
        subject_field_key = self.config.subject_field
        body_field_key = self.config.body_field
        output_field_key = self.config.output_field

        # Use the keys to get the values from the context dictionary
        subject = get_value_from_context(context.data, subject_field_key) or ""
        body = get_value_from_context(context.data, body_field_key) or ""

        # Add a newline for better separation between subject and body
        prepared_text = f"{subject}\n{body}"

        self.logger.debug(f"Writing combined text to field '{output_field_key}'")
        new_context = PipelineContext(
            meta_info=context.meta_info,
            data=context.data | {output_field_key: prepared_text}
        )
        return new_context
