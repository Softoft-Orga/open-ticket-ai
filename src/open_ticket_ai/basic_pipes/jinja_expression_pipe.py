from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.configurable_pipe import ConfigurablePipe


class JinjaExpressionPipeConfig(BaseModel):
    expression: Any


class JinjaExpressionPipe(ConfigurablePipe):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        pipe_config = JinjaExpressionPipeConfig(**config)
        self.expression = pipe_config.expression

    async def _process(self) -> dict[str, Any]:
        return {"value": self.expression}
