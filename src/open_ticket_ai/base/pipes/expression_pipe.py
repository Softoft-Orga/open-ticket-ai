from typing import Any

from pydantic import BaseModel

from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig, PipeResult


class ExpressionParams(BaseModel):
    expression: str


class ExpressionPipeResultData(BaseModel):
    value: Any


class ExpressionPipeConfig(PipeConfig):
    params: ExpressionParams


class ExpressionPipe(Pipe):
    def __init__(
        self,
        config: ExpressionPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if logger_factory is None:
            raise ValueError("logger_factory is required")
        super().__init__(config, logger_factory=logger_factory)
        self.config = ExpressionPipeConfig.model_validate(config.model_dump())

    async def _process(self) -> PipeResult:
        return PipeResult(
            success=True, failed=False, data=ExpressionPipeResultData(value=self.config.params.expression)
        )
