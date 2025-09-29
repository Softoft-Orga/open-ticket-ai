import asyncio
import pytest

from open_ticket_ai.base_extensions.jinja_expression_pipe import JinjaExpressionPipe
from open_ticket_ai.base_extensions.pipe_configs import RawJinjaExpressionPipeConfig
from open_ticket_ai.core.pipeline.context import PipelineContext


@pytest.fixture
def raw_config() -> RawJinjaExpressionPipeConfig:
    """Provide a baseline raw configuration for the pipe."""
    return RawJinjaExpressionPipeConfig(
        name="jinja_expression",
        use="\"open_ticket_ai.base_extensions.jinja_expression_pipe.JinjaExpressionPipe\"",
        expression="{{ 1 + 1 }}",
    )


def test_get_raw_config_model_type() -> None:
    """The pipe should expose the expected raw configuration model."""
    assert JinjaExpressionPipe.get_raw_config_model_type() is RawJinjaExpressionPipeConfig


def test_config_model_alias() -> None:
    """The ConfigModel attribute should alias the raw configuration type."""
    assert JinjaExpressionPipe.ConfigModel is RawJinjaExpressionPipeConfig


def test_process_returns_empty_state(raw_config: RawJinjaExpressionPipeConfig) -> None:
    """The pipe does not produce any data when processing."""
    pipe = JinjaExpressionPipe(raw_config)
    result = asyncio.run(pipe._process())
    assert result == {}


def test_config_expression_renders_with_context() -> None:
    """The expression string should render against the pipeline context."""
    config = RawJinjaExpressionPipeConfig(
        name="jinja_expression",
        use="\"open_ticket_ai.base_extensions.jinja_expression_pipe.JinjaExpressionPipe\"",
        expression="{{ pipes.previous.value + config.offset }}",
    )
    pipe = JinjaExpressionPipe(config)
    pipe._current_context = PipelineContext(
        pipes={"previous": {"value": 5}},
        config={"offset": 3},
    )

    rendered_config = pipe.config
    assert rendered_config["expression"] == 8
