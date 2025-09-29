from typing import Any

from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe
from open_ticket_ai.core.pipeline.configurable_pipe_config import RawPipeConfig, RenderedPipeConfig


class DefaultPipe(ConfigurablePipe[RawPipeConfig, RenderedPipeConfig]):
    async def _process(self) -> dict[str, Any]:
        return {}
