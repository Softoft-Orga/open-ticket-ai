import warnings

import pytest
from pydantic import BaseModel

from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.config.renderable_factory import render_params
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.pipeline.pipe_config import PipeConfig
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig


class SimpleParams(BaseModel):
    model: str
    confidence: float | None = None


class NestedOuter(BaseModel):
    inner: str
    static: str


class NestedParams(BaseModel):
    outer: NestedOuter


class ModelParams(BaseModel):
    model: str


@pytest.fixture
def renderer(logger_factory: LoggerFactory) -> JinjaRenderer:
    return JinjaRenderer(JinjaRendererConfig(), logger_factory)


@pytest.fixture
def context() -> PipeContext:
    return PipeContext(
        pipes={},
        params={"global_model": "my-global-model", "threshold": 0.7},
    )


def test_render_params_renders_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    params = {
        "model": "{{ params.global_model }}",
        "confidence": "{{ params.threshold }}",
    }
    config = PipeConfig(
        id="test",
        params=params,
    )

    rendered = render_params(config.params, context, renderer)

    assert isinstance(rendered, dict)
    assert rendered["model"] == "my-global-model"
    assert rendered["confidence"] == 0.7


def test_render_params_does_not_render_control_fields(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = PipeConfig(
        id="test",
        use="SomePipe",
        params={"model": "{{ params.global_model }}"},
    )

    rendered = render_params(config.params, context, renderer)

    assert isinstance(rendered, dict)
    assert rendered["model"] == "my-global-model"


def test_render_params_with_nested_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = PipeConfig(
        id="test",
        params={
            "outer": {
                "inner": "{{ params.global_model }}",
                "static": "value",
            }
        },
    )

    rendered = render_params(config.params, context, renderer)

    assert isinstance(rendered, dict)
    assert rendered["outer"]["inner"] == "my-global-model"
    assert rendered["outer"]["static"] == "value"


def test_render_params_empty_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config: PipeConfig = PipeConfig(id="test")

    rendered = render_params(config.params, context, renderer)

    assert isinstance(rendered, dict)
    assert rendered == {}


def test_render_params_with_params_template(renderer: JinjaRenderer, context: PipeContext) -> None:
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        config = PipeConfig(
            id="test",
            params={"model": "{{ params.global_model }}"},
        )

    rendered = render_params(config.params, context, renderer)

    assert isinstance(rendered, dict)
    assert rendered["model"] == "my-global-model"
