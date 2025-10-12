from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult


class JinjaExpressionParams(BaseModel):
    expression: Any


class JinjaExpressionPipeResultData(BaseModel):
    value: Any


class JinjaExpressionPipeConfig(PipeConfig[JinjaExpressionParams]):
    pass


class JinjaExpressionPipe(Pipe[JinjaExpressionParams]):
    def __init__(
        self, pipe_config: JinjaExpressionPipeConfig, logger_factory: LoggerFactory | None = None, *args, **kwargs
    ) -> None:
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.expression = pipe_config.params.expression

    async def _process(self) -> PipeResult[JinjaExpressionPipeResultData]:
        return PipeResult[JinjaExpressionPipeResultData](
            success=True, failed=False, data=JinjaExpressionPipeResultData(value=self.expression)
        )
