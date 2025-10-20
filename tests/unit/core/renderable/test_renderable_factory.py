from unittest.mock import MagicMock

import pytest

from open_ticket_ai.core.config.config_models import InfrastructureConfig, OpenTicketAIConfig
from open_ticket_ai.core.injectables.injectable_models import InjectableConfig
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext
from open_ticket_ai.core.pipes.pipe_factory import PipeFactory
from open_ticket_ai.core.pipes.pipe_models import PipeConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer
from tests.unit.conftest import SimplePipe


def test_render_pipe_creates_pipe_instance(
    mock_template_renderer: MagicMock,
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    mock_component_registry.get_pipe.return_value = SimplePipe
    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "test_value"},
    )
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.create_pipe(config, sample_pipe_context)

    assert isinstance(result, Pipe)
    mock_template_renderer.render.assert_called_once_with(config.params, sample_pipe_context.model_dump())


def test_render_pipe_passes_correct_params_to_instance(
    mock_template_renderer: MagicMock,
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    mock_component_registry.get_pipe.return_value = SimplePipe
    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "custom_value"},
    )
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.create_pipe(config, sample_pipe_context)

    assert result._params.value == "custom_value"


def test_render_pipe_applies_template_rendering_to_params(
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    mock_component_registry.get_pipe.return_value = SimplePipe
    mock_renderer = MagicMock(spec=TemplateRenderer)
    mock_renderer.render.return_value = {"value": "rendered_value"}

    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "{{ template }}"},
    )
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.create_pipe(config, sample_pipe_context)

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
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    params: dict,
    context_params: dict,
    expected_value: str,
) -> None:
    mock_component_registry.get_pipe.return_value = SimplePipe
    config = PipeConfig(
        id="test_pipe",
        use="tests.unit.conftest.SimplePipe",
        params=params,
    )
    context = PipeContext(pipe_results={}, params=context_params)
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    result = factory.create_pipe(config, context)

    assert result._params.value == expected_value


def test_render_pipe_with_inject_dependencies(
    mock_template_renderer: MagicMock,
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    mock_component_registry.get_pipe.return_value = SimplePipe
    mock_component_registry.get_injectable.return_value = SimplePipe
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
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=otai_config,
    )

    result = factory.create_pipe(config, sample_pipe_context)

    assert isinstance(result, Pipe)


def test_render_pipe_raises_type_error_for_non_pipe_class(
    mock_template_renderer: MagicMock,
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    from open_ticket_ai.core.config.errors import InjectableNotFoundError

    mock_component_registry.get_pipe.side_effect = InjectableNotFoundError("builtins.dict", mock_component_registry)
    config = PipeConfig(
        id="invalid_class",
        use="builtins.dict",
        params={},
    )
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    with pytest.raises(InjectableNotFoundError):
        factory.create_pipe(config, sample_pipe_context)


def test_render_pipe_raises_error_for_nonexistent_class(
    mock_template_renderer: MagicMock,
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    from open_ticket_ai.core.config.errors import InjectableNotFoundError

    mock_component_registry.get_pipe.side_effect = InjectableNotFoundError(
        "nonexistent.module.NonexistentClass", mock_component_registry
    )
    config = PipeConfig(
        id="nonexistent",
        use="nonexistent.module.NonexistentClass",
        params={},
    )
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    with pytest.raises(InjectableNotFoundError):
        factory.create_pipe(config, sample_pipe_context)


def test_render_pipe_raises_value_error_for_missing_inject_service(
    mock_template_renderer: MagicMock,
    mock_component_registry: MagicMock,
    logger_factory: MagicMock,
    mock_otai_config: MagicMock,
    sample_pipe_context: PipeContext,
) -> None:
    from open_ticket_ai.core.config.errors import NoServiceConfigurationFoundError

    mock_component_registry.get_pipe.return_value = SimplePipe
    config = PipeConfig(
        id="pipe_with_missing_dep",
        use="tests.unit.conftest.SimplePipe",
        params={"value": "test"},
        injects={"dependency": "nonexistent_service"},
    )
    factory = PipeFactory(
        component_registry=mock_component_registry,
        template_renderer=mock_template_renderer,
        logger_factory=logger_factory,
        otai_config=mock_otai_config,
    )

    with pytest.raises(NoServiceConfigurationFoundError, match="nonexistent_service"):
        factory.create_pipe(config, sample_pipe_context)
