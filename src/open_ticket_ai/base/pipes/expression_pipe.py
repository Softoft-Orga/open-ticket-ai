from typing import Any

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

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        self._logger.debug("📐 Expression pipe returning value")
        expr_preview = (
            self._params.expression[:100] + "..." if len(self._params.expression) > 100 else self._params.expression
        )
        self._logger.debug(f"Expression: {expr_preview}")

        return PipeResult(succeeded=True, data={"value": self._params.expression})
