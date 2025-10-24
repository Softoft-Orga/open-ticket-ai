from typing import Any

import pytest
from otai_base.pipes.composite_pipe import CompositePipe, CompositePipeParams
from otai_base.pipes.expression_pipe import ExpressionParams, ExpressionPipe
from otai_base.template_renderers.jinja_renderer_extras import FailMarker
from pydantic import BaseModel

from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig, PipeResult
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderError

COUNTER: list[str] = []


class CounterParams(BaseModel):
    tag: str


class CounterPipe(Pipe[CounterParams]):
    ParamsModel = CounterParams

    async def _process(self, _context: PipeContext) -> PipeResult:
        COUNTER.append(self._params.tag)
        return PipeResult.success(data={"value": self._params.tag})


@pytest.fixture(autouse=True, scope="function")
def register_pipes(integration_component_registry: ComponentRegistry):
    integration_component_registry.register("base:ExpressionPipe", ExpressionPipe)
    integration_component_registry.register("core:CompositePipe", CompositePipe)
    integration_component_registry.register("tests:CounterPipe", CounterPipe)
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
def counter_cfg():
    def _make(pipe_id: str, tag: str) -> PipeConfig:
        return PipeConfig(
            id=pipe_id,
            use="tests:CounterPipe",
            params=CounterParams(tag=tag).model_dump(),
        )

    return _make


@pytest.fixture
def make_composite(
    register_pipes: ComponentRegistry, integration_logger_factory: LoggerFactory, integration_pipe_factory: PipeFactory
):
    _ = register_pipes

    def _make(steps: list[PipeConfig], extra_composite_params: dict[str, Any] | None = None) -> CompositePipe:
        return CompositePipe(
            config=PipeConfig(
                id="composite",
                use="core:CompositePipe",
                params=CompositePipeParams(steps=steps).model_dump() | (extra_composite_params or {}),
            ),
            logger_factory=integration_logger_factory,
            pipe_factory=integration_pipe_factory,
        )

    return _make


@pytest.fixture(autouse=True)
def reset_counter():
    COUNTER.clear()


@pytest.mark.integration
async def test_composite_runs_steps_and_aggregates(
    integration_empty_pipe_context: PipeContext,
    make_composite,
    expr_cfg,
):
    s1 = expr_cfg("s1", "{{ 2 }}")
    s2 = expr_cfg("s2", "{{ get_pipe_result('s1','value') + 3 }}")
    pipe = make_composite([s1, s2])
    res = await pipe.process(integration_empty_pipe_context)
    assert res.succeeded is True
    assert res.data["value"] == 5


@pytest.mark.integration
async def test_composite_stops_after_failure_and_skips_remaining(
    integration_empty_pipe_context: PipeContext,
    make_composite,
    expr_cfg,
    counter_cfg,
):
    s1 = expr_cfg("s1", "{{ 1 }}")
    s2 = expr_cfg("s2", FailMarker())
    s3 = counter_cfg("s3", "should_not_run")
    pipe = make_composite([s1, s2, s3])
    res = await pipe.process(integration_empty_pipe_context)
    assert res.succeeded is True
    assert "should_not_run" not in COUNTER


@pytest.mark.integration
async def test_composite_passes_pipe_results_through_context(
    integration_empty_pipe_context: PipeContext,
    make_composite,
    expr_cfg,
):
    ctx = integration_empty_pipe_context
    ctx.params["x"] = 5
    s1 = expr_cfg("s1", "{{ params.x * 2 }}")
    s2 = expr_cfg("s2", "{{ get_pipe_result('s1') + 5 }}")
    pipe = make_composite([s1, s2])
    res = await pipe.process(ctx)
    assert res.succeeded is True
    assert res.data["value"] == 15


@pytest.mark.integration
async def test_composite_parent_is_not_previous_pipe(
    integration_empty_pipe_context: PipeContext,
    make_composite,
    expr_cfg,
):
    """A Pipes Parent is the Composite, not the previous Pipe."""
    ctx = integration_empty_pipe_context
    ctx.params["x"] = 5
    s1 = expr_cfg("s1", "{{ params.x * 2 }}")
    s2 = expr_cfg("s2", "{{ get_parent_param('expression') +  get_pipe_result('s1') }}")
    pipe = make_composite([s1, s2])
    with pytest.raises(TemplateRenderError):
        await pipe.process(ctx)


@pytest.mark.integration
async def test_get_parents_param_returns_correct_value(
    integration_empty_pipe_context: PipeContext,
    make_composite,
    expr_cfg,
):
    """A Pipes Parent is the Composite, not the previous Pipe."""
    ctx = integration_empty_pipe_context
    ctx.params["x"] = 5
    s1 = expr_cfg("s1", "{{ params.x * 2 }}")
    s2 = expr_cfg("s2", "{{ get_parent_param('my_parents_param') + get_pipe_result('s1') }}")
    pipe = make_composite([s1, s2], extra_composite_params={"my_parents_param": 10})
    res = await pipe.process(ctx)
    assert res.succeeded is True
    assert res.data["value"] == 20


@pytest.mark.integration
async def test_composite_with_no_steps_succeeds(
    integration_empty_pipe_context: PipeContext,
    make_composite,
):
    pipe = make_composite([])
    res = await pipe.process(integration_empty_pipe_context)
    assert res.succeeded is True
