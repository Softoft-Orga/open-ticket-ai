from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult


class ExpressionParams(BaseModel):
    expression: str


class ExpressionPipeResultData(BaseModel):
    value: Any


class ExpressionPipeConfig(PipeConfig[ExpressionParams]):
    pass


class ExpressionPipe(Pipe[ExpressionParams]):
    params_class = ExpressionParams

    def __init__(
        self,
        pipe_config: ExpressionPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.pipe_config = ExpressionPipeConfig.model_validate(pipe_config.model_dump())
        self.expression = self.params.expression

    async def _process(self) -> PipeResult[ExpressionPipeResultData]:
        return PipeResult[ExpressionPipeResultData](
            success=True, failed=False, data=ExpressionPipeResultData(value=self.expression)
        )
