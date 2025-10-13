import warnings

import pytest
from pydantic import BaseModel

from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.config.renderable_factory import render_base_model
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
def renderer() -> JinjaRenderer:
    return JinjaRenderer(JinjaRendererConfig())


@pytest.fixture
def context() -> PipeContext:
    return PipeContext(
        pipes={},
        params={"global_model": "my-global-model", "threshold": 0.7},
    )


def test_render_base_model_renders_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = PipeConfig[SimpleParams](
        id="test",
        params=SimpleParams.model_construct(
            model="{{ params.global_model }}",
            confidence="{{ params.threshold }}",
        ),
    )

    rendered = render_base_model(config.params, context, renderer)

    assert rendered.model == "my-global-model"
    assert rendered.confidence == 0.7


def test_render_base_model_does_not_render_control_fields(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = PipeConfig[SimpleParams](
        id="test",
        use="SomePipe",
        params=SimpleParams.model_construct(model="{{ params.global_model }}"),
    )

    rendered = render_base_model(config.params, context, renderer)

    assert rendered.model == "my-global-model"


def test_render_base_model_with_nested_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = PipeConfig[NestedParams](
        id="test",
        params=NestedParams.model_construct(
            outer=NestedOuter.model_construct(
                inner="{{ params.global_model }}",
                static="value",
            ),
        ),
    )

    rendered = render_base_model(config.params, context, renderer)

    assert rendered.outer.inner == "my-global-model"
    assert rendered.outer.static == "value"


def test_render_base_model_empty_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = PipeConfig(id="test")

    rendered = render_base_model(config.params, context, renderer)

    assert rendered.model_dump() == {}


def test_render_base_model_with_legacy_fields_migrated(renderer: JinjaRenderer, context: PipeContext) -> None:
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        config = PipeConfig[ModelParams](
            id="test",
            model="{{ params.global_model }}",  # type: ignore
        )

    rendered = render_base_model(config.params, context, renderer)

    assert rendered.model == "my-global-model"
