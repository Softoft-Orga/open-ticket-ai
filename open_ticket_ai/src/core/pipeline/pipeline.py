import logging

from .context import PipelineContext
from .meta_info import MetaInfo
from .pipe import Pipe
from .status import PipelineStatus
from ...base.pipe_implementations.empty_data_model import EmptyDataModel

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, pipes: list[Pipe]):
        self.pipes: list[Pipe] = pipes

    async def execute(self) -> PipelineContext:
        context: PipelineContext = PipelineContext(
            meta_info=MetaInfo(status=PipelineStatus.RUNNING),
            data=EmptyDataModel(),
        )

        for pipe in self.pipes:
            try:
                context = await pipe.process(context)
            except Exception as e:
                logger.error(
                    f"Pipeline failed at pipe '{pipe.__class__.__name__}' with contex {context}.",
                    exc_info=True,
                )
                context.meta_info.status = PipelineStatus.FAILED
                context.meta_info.error_message = str(e)
                context.meta_info.failed_pipe = pipe.__class__.__name__
                break
            if context.meta_info.status == PipelineStatus.STOPPED:
                logger.info(
                    f"Pipeline stopped by '{pipe.__class__.__name__}' "
                    f"with error message: {context.meta_info.error_message}"
                )
                break

        if context.meta_info.status == PipelineStatus.RUNNING:
            context.meta_info.status = PipelineStatus.SUCCESS
            logger.info(f"Pipeline completed successfully.")

        return context
