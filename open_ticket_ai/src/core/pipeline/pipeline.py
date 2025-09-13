import logging
from typing import List

from .context import PipelineContext
from .pipe import Pipe
from .status import PipelineStatus  # Import the status enum
from open_ticket_ai.src.core.config.config_models import PipelineConfig

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, config: PipelineConfig, pipes: list[Pipe]):
        """Initializes the Pipeline with configuration and pipe sequence.

        Args:
            config: Configuration settings for the pipeline.
        """
        self.config: PipelineConfig = config
        self.pipes: List[Pipe] = pipes

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Executes all pipe_ids sequentially with error handling and status propagation.

        Processes each pipe in sequence while:
        - Validating input data using each pipe's input model
        - Handling STOPPED status requests from pipe_ids
        - Catching and logging exceptions during pipe execution
        - Updating context status appropriately (RUNNING, SUCCESS, FAILED, STOPPED)

        Args:
            context: The pipeline context containing execution state and data.

        Returns:
            Updated PipelineContext reflecting final execution state after processing.

        Notes:
            - Starts execution only if context status is RUNNING or SUCCESS
            - Sets context to RUNNING at start of execution
            - Breaks processing loop on STOPPED status or uncaught exception
            - Automatically sets status to SUCCESS if all pipe_ids complete without errors
        """
        # Ensure the context starts in a runnable state.
        if context.status not in [PipelineStatus.RUNNING, PipelineStatus.SUCCESS]:
            logger.warning(
                f"Pipeline for ticket {context.ticket_id} started with non-runnable status: {context.status.name}",
            )
            return context

        context.status = PipelineStatus.RUNNING

        for pipe in self.pipes:
            try:
                # Process the context with the current pipe
                context.data = pipe.InputDataType.model_validate(context)
                context = pipe.process(context)

                # After processing, check if the pipe requested a stop
                if context.status == PipelineStatus.STOPPED:
                    logger.info(f"Pipeline stopped by '{pipe.__class__.__name__}' for ticket {context.ticket_id}.")
                    break  # Exit the loop for a controlled stop

            except Exception as e:
                # An unexpected error occurred in the pipe
                logger.error(
                    f"Pipeline failed at pipe '{pipe.__class__.__name__}' for ticket {context.ticket_id}.",
                    exc_info=True,
                )
                context.status = PipelineStatus.FAILED
                context.error_message = str(e)
                context.failed_pipe = pipe.__class__.__name__
                break  # Exit the loop on failure

        # If the loop completed without being stopped or failing, mark it as successful
        if context.status == PipelineStatus.RUNNING:
            context.status = PipelineStatus.SUCCESS

        return context
