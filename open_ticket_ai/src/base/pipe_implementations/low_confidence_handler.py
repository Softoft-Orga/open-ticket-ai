# FILE_PATH: open_ticket_ai/src/ce/run/pipe_implementations/low_confidence_handler.py
import logging

from open_ticket_ai.src.base.pipe_implementations.context_helper import get_value_from_context
from open_ticket_ai.src.core.config.pipe_configs import LowConfidenceHandlerConfig
from open_ticket_ai.src.core.pipeline.context import PipelineContext
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class LowConfidenceHandler(Pipe):
    def __init__(self, config: LowConfidenceHandlerConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process(self, context: PipelineContext[dict]) -> PipelineContext[dict]:
        # Safely get all configuration parameters
        label_field = self.config.label_field
        confidence_field = self.config.confidence_field
        output_field = self.config.output_field
        threshold = self.config.threshold
        low_confidence_value = self.config.low_confidence_value

        if not all([label_field, confidence_field, output_field, threshold, low_confidence_value]):
            self.logger.error("Pipe is misconfigured. Missing one or more required fields.")
            # Pass the context through without modification
            return context

        # Get the actual values from the context dictionary
        label = get_value_from_context(context.data, label_field)
        confidence = get_value_from_context(context.data, confidence_field)

        if label is None or confidence is None:
            self.logger.warning(
                f"Missing label or confidence in context. "
                f"Cannot process low confidence logic for label '{label_field}' and confidence '{confidence_field}'."
            )
            # Pass the context through, but add the original label to the output field
            # to ensure the next pipe doesn't fail.
            return PipelineContext(
                meta_info=context.meta_info,
                data=context.data | {output_field: label}
            )

        final_value = label
        if float(confidence) < threshold:
            final_value = low_confidence_value
            self.logger.info(
                f"Confidence {confidence:.2f} is below threshold {threshold}. "
                f"Replacing label '{label}' with '{final_value}'."
            )
        else:
            self.logger.info(
                f"Confidence {confidence:.2f} is above or equal to threshold {threshold}. Keeping label '{label}'.")

        return PipelineContext(
            meta_info=context.meta_info,
            data=context.data | {output_field: final_value}
        )
