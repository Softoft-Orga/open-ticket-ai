from unittest.mock import MagicMock

import pytest
from open_ticket_ai.core.pipes.pipe import Pipe

from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer


def test_render_pipe_creates_pipe_instance(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "test_value"},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.render_pipe(config, sample_pipe_context)

    assert isinstance(result, Pipe)
    mock_template_renderer.render.assert_called_once_with(config.params, sample_pipe_context.model_dump())


def test_render_pipe_passes_correct_params_to_instance(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "custom_value"},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.render_pipe(config, sample_pipe_context)

    assert result._params.value == "custom_value"


def test_render_pipe_applies_template_rendering_to_params(
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    mock_renderer = MagicMock(spec=TemplateRenderer)
    mock_renderer.render.return_value = {"value": "rendered_value"}

    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "{{ template }}"},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.render_pipe(config, sample_pipe_context)

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
def test_render_pipe_with_various_params_and_contexts(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    params: dict,
    context_params: dict,
    expected_value: str,
) -> None:
    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params=params,
    )
    context = PipeContext(pipe_results={}, params=context_params)
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.render_pipe(config, context)

    assert result._params.value == expected_value


def test_render_pipe_with_inject_dependencies(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    service_config = InjectableConfig(
        id="service1",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "service1_value"},
    )
    otai_config = OpenTicketAIConfig(
        infrastructure=InfrastructureConfig(logging=LoggingConfig()),
        services={"service1": service_config},
        orchestrator=PipeConfig(),
    )
    config = PipeConfig(
        id="main_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "main"},
        injects={"dependency": "service1"},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=otai_config,
    )

    result = factory.render_pipe(config, sample_pipe_context)

    assert isinstance(result, Pipe)


def test_render_pipe_raises_type_error_for_non_pipe_class(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = PipeConfig(
        id="invalid_class",
        use="builtins.dict",
        params={},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    with pytest.raises(TypeError, match=f".*{config.use}'.*Pipe.*"):
        factory.render_pipe(config, sample_pipe_context)


def test_render_pipe_raises_error_for_nonexistent_class(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = PipeConfig(
        id="nonexistent",
        use="nonexistent.module.NonexistentClass",
        params={},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    with pytest.raises(TypeError):
        factory.render_pipe(config, sample_pipe_context)


def test_render_pipe_raises_value_error_for_missing_inject_service(
    mock_template_renderer: MagicMock,
    mock_injector: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    config = PipeConfig(
        id="pipe_with_missing_dep",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "test"},
        injects={"dependency": "nonexistent_service"},
    )
    factory = PipeFactory(
        injector=mock_injector,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    with pytest.raises(ValueError, match="nonexistent_service"):
        factory.render_pipe(config, sample_pipe_context)
