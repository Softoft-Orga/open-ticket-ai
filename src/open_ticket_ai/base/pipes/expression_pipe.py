from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_models import PipeResult


class ExpressionParams(StrictBaseModel):
    expression: str = Field(
        description=(
            "Expression string to be evaluated or processed by the expression pipe for dynamic value computation."
        )
    )


class ExpressionPipe(Pipe[ExpressionParams]):
    @staticmethod
    def get_params_model() -> type[StrictBaseModel]:
        return ExpressionParams

    async def _process(self) -> PipeResult:
        return PipeResult(succeeded=True, data={"value": self._params.expression})
