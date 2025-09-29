from typing import Any

from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.pipeline.base_pipe_config import _BasePipeConfig, RenderedPipeConfig, RawPipeConfig, PipeConfig


class RawJinjaExpressionPipeConfig(RawPipeConfig, BaseJinjaExpressionPipeConfig):
    pass


class JinjaExpressionPipe(BasePipe[RawJinjaExpressionPipeConfig]):
    @staticmethod
    def get_raw_config_model_type() -> type[RawJinjaExpressionPipeConfig]:
        return RawJinjaExpressionPipeConfig

    def __init__(self, config: RawJinjaExpressionPipeConfig, *args: Any, **kwargs: Any):
        super().__init__(config, *args, **kwargs)

    async def _process(self) -> dict[str, Any]:
        return {}


class BaseJinjaExpressionPipeConfig(_BasePipeConfig):
    expression: str


class RenderedJinjaExpressionPipeConfig(RenderedPipeConfig, BaseJinjaExpressionPipeConfig):
    pass


class JinjaExpressionPipeConfig(PipeConfig[RawJinjaExpressionPipeConfig, RenderedJinjaExpressionPipeConfig]):
    pass
