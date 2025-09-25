import logging

from .context import PipelineContext
from .meta_info import MetaInfo
from .pipe import Pipe
from .status import PipelineStatus



class Pipeline:
    def __init__(self, pipes: list[Pipe]):
        self.pipes: list[Pipe] = pipes
        self.logger = logging.getLogger(self.__class__.__name__)

    async def execute(self) -> PipelineContext:
        context: PipelineContext = PipelineContext(
            meta_info=MetaInfo(status=PipelineStatus.RUNNING),
            data={},
        )

        for pipe in self.pipes:
            try:
                self.logger.info(f"Executing pipe {pipe.__class__.__name__}")
                self.logger.debug(f"{context}")
                context = await pipe.process(context)
            except Exception as e:
                self.logger.error(
                    f"Pipeline failed at pipe '{pipe.__class__.__name__}' with contex {context}.",
                    exc_info=True,
                )
                context.meta_info.status = PipelineStatus.FAILED
                context.meta_info.error_message = str(e)
                context.meta_info.failed_pipe = pipe.__class__.__name__
            if context.meta_info.status == PipelineStatus.STOPPED:
                self.logger.info(
                    f"Pipeline stopped by '{pipe.__class__.__name__}' "
                    f"with error message: {context.meta_info.error_message}"
                )
                break

        if context.meta_info.status == PipelineStatus.RUNNING:
            context.meta_info.status = PipelineStatus.SUCCESS
            self.logger.info(f"Pipeline completed successfully.")

        return context
