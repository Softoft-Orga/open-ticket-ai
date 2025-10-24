import pytest
from otai_base.pipes.expression_pipe import ExpressionParams, ExpressionPipe
from otai_base.pipes.pipe_runners.simple_sequential_runner import SimpleSequentialRunner, SimpleSequentialRunnerParams
from otai_base.template_renderers.jinja_renderer_extras import FailMarker

from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig


@pytest.fixture
def register_pipes(integration_component_registry: ComponentRegistry):
    integration_component_registry.register("base:ExpressionPipe", ExpressionPipe)
    return integration_component_registry


@pytest.fixture
def expr_cfg():
    def _make(pipe_id: str, expr: str | FailMarker) -> PipeConfig:
        return PipeConfig(
            id=pipe_id,
            use="base:ExpressionPipe",
            params=ExpressionParams(expression=expr).model_dump(),
        )

    return _make


@pytest.fixture
def make_runner(integration_pipe_factory: PipeFactory, register_pipes: ComponentRegistry, integration_logger_factory):
    _ = register_pipes

    def _make(on_cfg: PipeConfig, run_cfg: PipeConfig) -> SimpleSequentialRunner:
        return SimpleSequentialRunner(
            config=PipeConfig(
                id="runner",
                use="core:SimpleSequentialRunner",
                params=SimpleSequentialRunnerParams(on=on_cfg, run=run_cfg).model_dump(),
            ),
            logger_factory=integration_logger_factory,
            pipe_factory=integration_pipe_factory,
        )

    return _make


@pytest.mark.integration
async def test_runner_executes_run_when_on_succeeds(
    integration_empty_pipe_context: PipeContext,
    make_runner,
    expr_cfg,
):
    on = expr_cfg("on", "{{ 1 }}")
    run = expr_cfg("run", "{{ 40 + 2 }}")
    runner = make_runner(on, run)
    res = await runner.process(integration_empty_pipe_context)
    assert res.succeeded is True
    assert res.data["value"] == 42


@pytest.mark.integration
async def test_runner_skips_when_on_fails(
    integration_empty_pipe_context: PipeContext,
    make_runner,
    expr_cfg,
):
    on = expr_cfg("on", FailMarker())
    run = expr_cfg("run", "{{ 1 }}")
    runner = make_runner(on, run)
    res = await runner.process(integration_empty_pipe_context)
    assert res.succeeded is False
    assert res.was_skipped is True
    assert "did not succeed" in (res.message or "").lower()
