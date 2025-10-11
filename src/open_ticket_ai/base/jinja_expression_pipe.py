from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.config.registerable import Renderable
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class JinjaExpressionParams(BaseModel):
    expression: Any


class JinjaExpressionPipeConfig(Renderable[JinjaExpressionParams]):
    pass


class JinjaExpressionPipe(Pipe):
    def __init__(self, pipe_params: JinjaExpressionPipeConfig, *args: Any, **kwargs: Any) -> None:
        super().__init__(pipe_params)
        if isinstance(pipe_params, dict):
            self.config = JinjaExpressionPipeConfig.model_validate(pipe_params)
        elif isinstance(pipe_params, JinjaExpressionPipeConfig):
            self.config = pipe_params
        else:
            self.config = JinjaExpressionPipeConfig.model_validate(pipe_params.model_dump())

    async def _process(self) -> PipeResult:
        return PipeResult(success=True, failed=False, data={"value": self.config.params.expression})
