from typing import Any

from open_ticket_ai.core.pipeline.base_pipe import BasePipe
from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig, RenderedPipeConfig


class DefaultPipe(BasePipe[RawPipeConfig, RenderedPipeConfig]):
    async def _process(self) -> dict[str, Any]:
        return {}
