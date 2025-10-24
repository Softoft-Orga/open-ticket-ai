from __future__ import annotations

from typing import Any, ClassVar

from open_ticket_ai import Pipe, StrictBaseModel
from open_ticket_ai.core.pipes.pipe_models import PipeResult
from pydantic import Field

from otai_base.template_renderers.jinja_renderer_extras import FailMarker


class ExpressionParams(StrictBaseModel):
    expression: Any = Field(
        description=(
            "Expression string to be evaluated or processed by the expression pipe for dynamic value computation."
        )
    )


class ExpressionPipe(Pipe[ExpressionParams]):
    """
    Pipe that returns a value based on the provided expression. If the expression evaluates to a FailMarker,
    the pipe returns a failure result. Otherwise, it returns the expression value.
    """

    ParamsModel: ClassVar[type[StrictBaseModel]] = ExpressionParams

    async def _process(self, *_: Any, **__: Any) -> PipeResult:
        self._logger.debug("📐 Expression pipe returning value")
        if isinstance(self._params.expression, str):
            expr_preview = self._preview_expression(self._params.expression)
            self._logger.debug(f"Expression: {expr_preview}")

        if isinstance(self._params.expression, FailMarker):
            self._logger.debug("Expression evaluated to FailMarker, returning failure.")
            return PipeResult.failure("Expression evaluated to FailMarker.")
        return PipeResult(succeeded=True, data={"value": self._params.expression})

    def _preview_expression(self, expression: str) -> str:
        if len(expression) <= _EXPRESSION_PREVIEW_LIMIT:
            return expression
        return f"{expression[:_EXPRESSION_PREVIEW_LIMIT]}..."


_EXPRESSION_PREVIEW_LIMIT = 100
