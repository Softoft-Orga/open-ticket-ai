from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_models import PipeResult


class ExpressionParams(StrictBaseModel):
    expression: str


class ExpressionPipe(Pipe[ExpressionParams]):
    @staticmethod
    def get_params_model() -> type[StrictBaseModel]:
        return ExpressionParams

    async def _process(self) -> PipeResult:
        return PipeResult(succeeded=True, data={"value": self._params.expression})
