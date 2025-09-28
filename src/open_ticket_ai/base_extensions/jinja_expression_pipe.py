from typing import Any

from open_ticket_ai.base_extensions.pipe_configs import (
    JinjaExpressionPipeConfig,
    JinjaExpressionPipeModel,
)
from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.pipeline.pipe import Pipe


class JinjaExpressionPipe(Pipe[JinjaExpressionPipeModel]):
    """
    A pipe implementation that processes Jinja expressions and modifies the pipeline context.
    This pipe can be used to transform data using Jinja templating.
    """

    def __init__(self, config: JinjaExpressionPipeConfig, *args: Any, **kwargs: Any):
        super().__init__(config, *args, **kwargs)

    async def _process(
        self, context: PipelineContext, config: JinjaExpressionPipeModel
    ) -> dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")
        # Base implementation does nothing and returns an empty dict
        # Subclasses can override this to implement specific Jinja expression processing
        return {}
