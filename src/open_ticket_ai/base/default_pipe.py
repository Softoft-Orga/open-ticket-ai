from typing import Any

from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe


class DefaultPipe(ConfigurablePipe):
    async def _process(self) -> dict[str, Any]:
        return {}
