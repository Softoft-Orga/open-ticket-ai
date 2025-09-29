from typing import Any

from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig


class DefaultPipe(BasePipe[RawPipeConfig]):
    @staticmethod
    def get_raw_config_model_type() -> type[RawPipeConfig]:
        return RawPipeConfig

    def __init__(self, config: RawPipeConfig, *args: Any, **kwargs: Any):
        super().__init__(config, *args, **kwargs)

    async def _process(self) -> dict[str, Any]:
        return {}
