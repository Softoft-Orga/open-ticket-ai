import logging
from typing import List, TYPE_CHECKING, Any

from .context import PipelineContext
from .status import PipelineStatus
from open_ticket_ai.src.core.config.config_models import PipelineConfig

if TYPE_CHECKING:  # pragma: no cover - used only for type checking
    from .pipe import Pipe

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, config: PipelineConfig, pipes: list['Pipe'] | List[Any]):
        self.config: PipelineConfig = config
        self.pipes: List[Any] = pipes

    def execute(self, context: PipelineContext) -> PipelineContext:
        """Run the configured pipes sequentially.

        The :class:`PipelineContext` carries a :class:`MetaInfo` instance which
        tracks the execution status of the pipeline.  The original implementation
        attempted to access attributes like ``status`` or ``error_message``
        directly on the context object which results in ``AttributeError`` at
        runtime.  Additionally, pipe input validation was performed on the whole
        ``context`` instead of on ``context.data``.  Both issues prevented the
        pipeline from functioning correctly.  The logic below interacts with the
        ``MetaInfo`` object and validates the data portion only.
        """

        if context.meta_info.status not in [PipelineStatus.RUNNING, PipelineStatus.SUCCESS]:
            logger.warning(
                "Pipeline started with non-runnable status: %s",
                context.meta_info.status.name,
            )
            return context

        # Ensure a running status before executing the pipes
        context.meta_info.status = PipelineStatus.RUNNING

        for pipe in self.pipes:
            try:
                # Validate and coerce the data for the next pipe
                context.data = pipe.InputDataType.model_validate(context.data)
                context = pipe.process(context)

                if context.meta_info.status == PipelineStatus.STOPPED:
                    logger.info("Pipeline stopped by '%s'.", pipe.__class__.__name__)
                    break

            except Exception as e:
                logger.error(
                    "Pipeline failed at pipe '%s'.",
                    pipe.__class__.__name__,
                    exc_info=True,
                )
                context.meta_info.status = PipelineStatus.FAILED
                context.meta_info.error_message = str(e)
                context.meta_info.failed_pipe = pipe.__class__.__name__
                break

        if context.meta_info.status == PipelineStatus.RUNNING:
            context.meta_info.status = PipelineStatus.SUCCESS

        return context

    def process(self, context: PipelineContext) -> PipelineContext:
        """Alias to :meth:`execute` for compatibility with the Pipe interface."""
        return self.execute(context)
