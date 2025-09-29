from typing import Any

from open_ticket_ai.basic_pipes.pipe_configs import RawJinjaExpressionPipeConfig
from open_ticket_ai.core.pipeline.base_pipe import BasePipe


class JinjaExpressionPipe(BasePipe[RawJinjaExpressionPipeConfig]):
    @staticmethod
    def get_raw_config_model_type() -> type[RawJinjaExpressionPipeConfig]:
        return RawJinjaExpressionPipeConfig

    def __init__(self, config: RawJinjaExpressionPipeConfig, *args: Any, **kwargs: Any):
        super().__init__(config, *args, **kwargs)

    async def _process(self) -> dict[str, Any]:
        return {}
