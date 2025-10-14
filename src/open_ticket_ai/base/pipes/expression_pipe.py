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
    pass


class ExpressionPipe(Pipe):
    def __init__(
        self,
        pipe_config: ExpressionPipeConfig,
        logger_factory: LoggerFactory | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if logger_factory is None:
            raise ValueError("logger_factory is required")
        super().__init__(pipe_config, logger_factory=logger_factory)
        self.pipe_config = ExpressionPipeConfig.model_validate(pipe_config.model_dump())
        # Validate params at runtime
        self.validated_params = ExpressionParams.model_validate(self.params)
        self.expression = self.validated_params.expression

    async def _process(self) -> PipeResult:
        return PipeResult(
            success=True, failed=False, data=ExpressionPipeResultData(value=self.expression)
        )
