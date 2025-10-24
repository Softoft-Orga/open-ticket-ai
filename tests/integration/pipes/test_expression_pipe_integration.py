"""
Integration tests for ExpressionPipe with real dependencies.

Tests the ExpressionPipe with actual logger factory and Jinja2-rendered expressions,
verifying integration with PipeContext and template rendering results.
"""

import pytest
from otai_base.pipes.expression_pipe import ExpressionParams, ExpressionPipe
from otai_base.template_renderers.jinja_renderer_extras import FailMarker

from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


@pytest.fixture()
def expression_config_factory():
    """Factory for creating PipeConfig instances for ExpressionPipe in integration tests."""

    def create_expression_config(pipe_id: str, expression_params: ExpressionParams) -> PipeConfig:
        return PipeConfig(id=pipe_id, use="base:ExpressionPipe", params=expression_params.model_dump())

    return create_expression_config


@pytest.fixture()
def expression_pipe_factory(integration_logger_factory: LoggerFactory, expression_config_factory):
    """Factory for creating ExpressionPipe instances in integration tests."""

    def create_expression_pipe(pipe_id: str, expression_params: ExpressionParams) -> ExpressionPipe:
        expression_config = expression_config_factory(pipe_id=pipe_id, expression_params=expression_params)
        return ExpressionPipe(config=expression_config, logger_factory=integration_logger_factory)

    return create_expression_pipe


@pytest.mark.integration
async def test_expression_pipe_with_jinja_expressions(
    expression_pipe_factory, integration_empty_pipe_context: PipeContext
):
    """Test ExpressionPipe with various Jinja2 expression types."""
    # Given
    params = ExpressionParams(expression="{{ 5 + 10 }}")
    pipe = expression_pipe_factory("test_expression", params)

    # When
    result = await pipe.process(integration_empty_pipe_context)

    # Then
    assert result.succeeded is True
    assert result.has_succeeded()
    # Expression Pipe doesnt actually render the expression, it just returns it as is.
    # It is rendered through the PipeFactory's TemplateRenderer when creating the pipe.
    assert result.data["value"] == "{{ 5 + 10 }}"


@pytest.mark.integration
async def test_expression_pipe_with_fail_marker(expression_pipe_factory, integration_empty_pipe_context: PipeContext):
    """Test ExpressionPipe returns failure when expression is FailMarker."""
    # Given
    fail_marker = FailMarker()
    params = ExpressionParams(expression=fail_marker)
    pipe = expression_pipe_factory("test_fail_marker", params)

    # When
    result = await pipe.process(integration_empty_pipe_context)

    # Then
    assert result.succeeded is False
    assert result.has_failed()
    assert result.message == "Expression evaluated to FailMarker."
    assert result.was_skipped is False


@pytest.mark.integration
async def test_expression_pipe_with_pipe_factory_renders_expression(
    integration_empty_pipe_context: PipeContext,
    integration_pipe_factory: PipeFactory,
    expression_config_factory,
    integration_component_registry: ComponentRegistry,
):
    """Test ExpressionPipe with expression evaluated by PipeFactory's TemplateRenderer."""
    pipe_config = expression_config_factory(
        pipe_id="test_expression_eval", expression_params=ExpressionParams(expression="{{ 20 * 3 }}")
    )
    integration_component_registry.register(
        "base:ExpressionPipe",
        ExpressionPipe,
    )
    pipe = await integration_pipe_factory.create_pipe(pipe_config, integration_empty_pipe_context)

    assert isinstance(pipe, ExpressionPipe)

    pipe_result = await pipe.process(integration_empty_pipe_context)
    assert pipe_result.succeeded is True
    assert pipe_result.data["value"] == 60


@pytest.fixture
def make_expr_pipe(
    expression_config_factory, integration_component_registry: ComponentRegistry, integration_pipe_factory: PipeFactory
):
    async def _make(expr: str, ctx: PipeContext, pipe_id: str = "expr"):
        integration_component_registry.register("base:ExpressionPipe", ExpressionPipe)
        cfg = expression_config_factory(pipe_id=pipe_id, expression_params=ExpressionParams(expression=expr))
        return await integration_pipe_factory.create_pipe(cfg, ctx)

    return _make


@pytest.mark.integration
async def test_expression_pipe_with_make_fixture_evaluates_expression(
    integration_empty_pipe_context: PipeContext,
    make_expr_pipe,
):
    pipe = await make_expr_pipe("{{ 20 * 3 }}", integration_empty_pipe_context, pipe_id="test_expression_eval")
    assert isinstance(pipe, ExpressionPipe)
    res = await pipe.process(integration_empty_pipe_context)
    assert res.succeeded is True
    assert res.data["value"] == 60


@pytest.mark.integration
async def test_expression_pipe_reads_from_context_params(
    integration_empty_pipe_context: PipeContext,
    make_expr_pipe,
):
    ctx = integration_empty_pipe_context
    ctx.params["a"] = 7
    pipe = await make_expr_pipe("{{ params.a + 5 }}", ctx, pipe_id="read_from_params")
    assert isinstance(pipe, ExpressionPipe)
    res = await pipe.process(ctx)
    assert res.succeeded is True
    assert res.data["value"] == 12
