import pytest

from open_ticket_ai.core.pipeline.pipe_config import RawPipeConfig, RenderedPipeConfig
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.pipeline.pipe_factory import render_base_model
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig


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
    config = RawPipeConfig(
        id="test",
        params={
            "model": "{{ params.global_model }}",
            "confidence": "{{ params.threshold }}",
        },
    )
    
    rendered = render_base_model(config, context, renderer)
    
    assert rendered["params"]["model"] == "my-global-model"
    assert rendered["params"]["confidence"] == 0.7


def test_render_base_model_does_not_render_control_fields(
    renderer: JinjaRenderer, context: PipeContext
) -> None:
    config = RawPipeConfig(
        id="test",
        use="SomePipe",
        params={"model": "{{ params.global_model }}"},
    )
    
    rendered = render_base_model(config, context, renderer)
    
    assert rendered["use"] == "SomePipe"
    assert rendered["params"]["model"] == "my-global-model"


def test_render_base_model_with_nested_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = RawPipeConfig(
        id="test",
        params={
            "outer": {
                "inner": "{{ params.global_model }}",
                "static": "value",
            },
        },
    )
    
    rendered = render_base_model(config, context, renderer)
    
    assert rendered["params"]["outer"]["inner"] == "my-global-model"
    assert rendered["params"]["outer"]["static"] == "value"


def test_render_base_model_empty_params(renderer: JinjaRenderer, context: PipeContext) -> None:
    config = RawPipeConfig(id="test")
    
    rendered = render_base_model(config, context, renderer)
    
    assert rendered["params"] == {}


def test_render_base_model_with_legacy_fields_migrated(
    renderer: JinjaRenderer, context: PipeContext
) -> None:
    import warnings
    
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        config = RawPipeConfig(
            id="test",
            model="{{ params.global_model }}",
        )
    
    rendered = render_base_model(config, context, renderer)
    
    assert rendered["params"]["model"] == "my-global-model"


def test_render_base_model_steps_not_rendered() -> None:
    renderer = JinjaRenderer(JinjaRendererConfig())
    context = PipeContext(pipes={}, config={})
    
    config = RawPipeConfig(
        id="test",
        steps=[
            RawPipeConfig(id="step1", params={"key": "value"}),
            RawPipeConfig(id="step2", params={"key": "value"}),
        ],
    )
    
    rendered = render_base_model(config, context, renderer)
    
    assert "steps" in rendered
    assert isinstance(rendered["steps"], list)
    assert len(rendered["steps"]) == 2


def test_render_base_model_params_with_template_expressions(
    renderer: JinjaRenderer, context: PipeContext
) -> None:
    config = RawPipeConfig(
        id="test",
        params={
            "combined": "Model: {{ params.global_model }}, Threshold: {{ params.threshold }}",
        },
    )
    
    rendered = render_base_model(config, context, renderer)
    
    assert rendered["params"]["combined"] == "Model: my-global-model, Threshold: 0.7"
