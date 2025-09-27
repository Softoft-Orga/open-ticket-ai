import logging
from typing import Any, Dict, List

from .context import MetaInfo, PipelineContext
from .pipe import Pipe


class Pipeline:
    def __init__(self, pipes: List[Pipe], config: Dict[str, Any] = None):
        self.pipes = pipes
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    async def execute(self, context: PipelineContext = None) -> PipelineContext:
        if context is None:
            context = PipelineContext(
                data={},
                meta_info=MetaInfo(),
                current_state={},
                pipeline_config=self.config,
            )

        for pipe in self.pipes:
            self.logger.info(f"Executing pipe {pipe.__class__.__name__}")
            context = await pipe.process(context)
        self.logger.info("Pipeline completed successfully.")
        return context
