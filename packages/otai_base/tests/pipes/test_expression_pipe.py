import pytest
from open_ticket_ai.core.pipes.pipe_models import PipeConfig

from otai_base.pipes.expression_pipe import ExpressionPipe


@pytest.mark.parametrize("expression", ["foo", "bar", "Hello World!"])
async def test_expression_pipe_returns_value(logger_factory, expression):
    config = PipeConfig(
        id="test_expression_pipe",
        use="open_ticket_ai.otai_base.pipes.expression_pipe.ExpressionPipe",
        params={"expression": expression},
    )

    pipe = ExpressionPipe(config=config, logger_factory=logger_factory)

    result = await pipe._process()

    assert result.succeeded is True
    assert result.data["value"] == expression
