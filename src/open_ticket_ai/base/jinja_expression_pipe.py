from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class JinjaExpressionPipeConfig(BaseModel):
    expression: Any


class JinjaExpressionPipe(Pipe):
    def __init__(self, config_raw: dict[str, Any], *args, **kwargs) -> None:
        super().__init__(config_raw)
        self.expression = JinjaExpressionPipeConfig.model_validate(config_raw).expression

    async def _process(self) -> PipeResult:
        return PipeResult(success=True, failed=False, data={"value": self.expression})
