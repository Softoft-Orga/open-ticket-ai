import logging
from typing import List

from .context import PipelineContext
from .pipe import Pipe
from .status import PipelineStatus  # Import the status enum
from open_ticket_ai.src.core.config.config_models import PipelineConfig

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, config: PipelineConfig, pipes: list[Pipe]):
        self.config: PipelineConfig = config
        self.pipes: List[Pipe] = pipes

    def execute(self, context: PipelineContext) -> PipelineContext:
        if context.status not in [PipelineStatus.RUNNING, PipelineStatus.SUCCESS]:
            logger.warning(
                f"Pipeline for ticket {context.ticket_id} started with non-runnable status: {context.status.name}",
            )
            return context

        context.status = PipelineStatus.RUNNING

        for pipe in self.pipes:
            try:
                context = pipe.process(context)

                if context.status == PipelineStatus.STOPPED:
                    logger.info(f"Pipeline stopped by '{pipe.__class__.__name__}' with context {context}.")
                    break

            except Exception as e:
                logger.error(
                    f"Pipeline failed at pipe '{pipe.__class__.__name__}' with contex {context.ticket_id}.",
                    exc_info=True,
                )
                context.meta_info.status = PipelineStatus.FAILED
                context.meta_info.error_message = str(e)
                context.meta_info.failed_pipe = pipe.__class__.__name__
                break

        if context.meta_info.status == PipelineStatus.RUNNING:
            context.meta_info.status = PipelineStatus.SUCCESS

        return context
