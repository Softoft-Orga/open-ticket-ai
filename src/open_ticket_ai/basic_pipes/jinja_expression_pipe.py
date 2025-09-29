from typing import Any

from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.pipeline.configurable_pipe_config import PipeConfig, RawPipeConfig, RenderedPipeConfig


class RawJinjaExpressionPipeConfig(RawPipeConfig):
    expression: str


class RenderedJinjaExpressionPipeConfig(RenderedPipeConfig):
    expression: Any


class JinjaExpressionPipeConfig(PipeConfig[RawJinjaExpressionPipeConfig, RenderedJinjaExpressionPipeConfig]):
    pass


class JinjaExpressionPipe(ConfigurablePipe[RawJinjaExpressionPipeConfig, RenderedJinjaExpressionPipeConfig]):

    async def _process(self) -> dict[str, Any]:
        return {"value": self.config.expression}
