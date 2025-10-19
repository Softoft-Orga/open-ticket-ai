import pytest
from pydantic import ValidationError

from open_ticket_ai.base.pipes.expression_pipe import ExpressionParams, ExpressionPipe
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


@pytest.mark.parametrize("expression", ["foo", "bar", "Hello World!"])
async def test_expression_pipe_returns_value(logger_factory, expression):
    config = PipeConfig(
        id="test_expression_pipe",
        use="open_ticket_ai.base.pipes.expression_pipe.ExpressionPipe",
        params={"expression": expression},
    )

    pipe = ExpressionPipe(config=config, logger_factory=logger_factory)

    result = await pipe._process()

    assert result.succeeded is True
    assert result.data["value"] == expression


@pytest.mark.parametrize("invalid_value", [123, {"key": "value"}, [1, 2, 3]])
def test_expression_pipe_invalid_param(invalid_value):
    with pytest.raises(ValidationError):
        ExpressionParams(expression=invalid_value)
