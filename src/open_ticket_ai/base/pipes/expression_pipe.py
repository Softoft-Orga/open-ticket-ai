from pydantic import BaseModel

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class ExpressionParams(BaseModel):
    expression: str


class ExpressionPipe(Pipe):
    @staticmethod
    def get_params_model() -> type[BaseModel]:
        return ExpressionParams

    async def _process(self) -> PipeResult:
        return PipeResult(success=True, data={"value": self._params.expression})
