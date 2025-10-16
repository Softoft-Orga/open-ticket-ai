from unittest.mock import MagicMock

import pytest

from open_ticket_ai.core.pipeline.pipe_context_model import PipeContext
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from tests.unit.core.renderable.conftest import SimpleRenderable


def test_render_creates_renderable_instance(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_renderable_config: RenderableConfig,
    sample_pipe_context: PipeContext,
) -> None:
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    result = factory.render(sample_renderable_config, sample_pipe_context)

    assert isinstance(result, SimpleRenderable)
    mock_template_renderer.render.assert_called_once_with(
        sample_renderable_config.params, sample_pipe_context.model_dump()
    )


def test_render_passes_correct_params_to_instance(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = RenderableConfig(
        id="test_renderable",
        use="tests.unit.core.renderable.conftest.SimpleRenderable",
        params={"value": "custom_value"},
    )
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    result = factory.render(config, sample_pipe_context)

    assert result._params.value == "custom_value"


def test_render_applies_template_rendering_to_params(
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    mock_renderer = MagicMock(spec=TemplateRenderer)
    mock_renderer.render.return_value = {"value": "rendered_value"}

    config = RenderableConfig(
        id="test_renderable",
        use="tests.unit.core.renderable.conftest.SimpleRenderable",
        params={"value": "{{ template }}"},
    )
    factory = RenderableFactory(
        template_renderer=mock_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    result = factory.render(config, sample_pipe_context)

    assert result._params.value == "rendered_value"
    mock_renderer.render.assert_called_once_with({"value": "{{ template }}"}, sample_pipe_context.model_dump())


@pytest.mark.parametrize(
    "params,context_params,expected_value",
    [
        ({"value": "static"}, {}, "static"),
        ({"value": "test"}, {"key": "val"}, "test"),
        ({"value": ""}, {}, ""),
    ],
)
def test_render_with_various_params_and_contexts(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    params: dict,
    context_params: dict,
    expected_value: str,
) -> None:
    config = RenderableConfig(
        id="test_renderable",
        use="tests.unit.core.renderable.conftest.SimpleRenderable",
        params=params,
    )
    context = PipeContext(pipe_results={}, params=context_params)
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    result = factory.render(config, context)

    assert result._params.value == expected_value


def test_render_with_inject_dependencies(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_registerable_configs: list[RenderableConfig],
    sample_pipe_context: PipeContext,
) -> None:
    config = RenderableConfig(
        id="main_service",
        use="tests.unit.core.renderable.conftest.SimpleRenderable",
        params={"value": "main"},
        injects={"dependency": "service1"},
    )
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=sample_registerable_configs,
        logger_factory=mock_logger_factory,
    )

    result = factory.render(config, sample_pipe_context)

    assert isinstance(result, SimpleRenderable)


def test_render_raises_type_error_for_non_renderable_class(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = RenderableConfig(
        id="invalid_class",
        use="builtins.dict",
        params={},
    )
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    with pytest.raises(TypeError, match="is not a"):
        factory.render(config, sample_pipe_context)


def test_render_raises_error_for_nonexistent_class(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = RenderableConfig(
        id="nonexistent",
        use="nonexistent.module.NonexistentClass",
        params={},
    )
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    with pytest.raises(TypeError):
        factory.render(config, sample_pipe_context)


def test_render_raises_key_error_for_missing_inject_service(
    mock_template_renderer: MagicMock,
    mock_app_config: MagicMock,
    mock_logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = RenderableConfig(
        id="service_with_missing_dep",
        use="tests.unit.core.renderable.conftest.SimpleRenderable",
        params={"value": "test"},
        injects={"dependency": "nonexistent_service"},
    )
    factory = RenderableFactory(
        template_renderer=mock_template_renderer,
        app_config=mock_app_config,
        registerable_configs=[],
        logger_factory=mock_logger_factory,
    )

    with pytest.raises(KeyError, match="nonexistent_service"):
        factory.render(config, sample_pipe_context)
