from __future__ import annotations

import pytest

from open_ticket_ai.core.config.config_models import InfrastructureConfig, RawOpenTicketAIConfig
from open_ticket_ai.core.config.logging_config import LoggingDictConfig
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer

pytestmark = [pytest.mark.unit]


@pytest.fixture
def valid_raw_config() -> RawOpenTicketAIConfig:
    return RawOpenTicketAIConfig(
        infrastructure=InfrastructureConfig(
            logging=LoggingDictConfig(), default_template_renderer="jinja_renderer"
        ),
        services=[
            RenderableConfig(
                id="jinja_renderer",
                use="open_ticket_ai.base.template_renderers.jinja_renderer.JinjaRenderer",
                params={"type": "jinja"},
            )
        ],
        orchestrator=OrchestratorConfig(),
    )


@pytest.fixture
def invalid_raw_config() -> RawOpenTicketAIConfig:
    return RawOpenTicketAIConfig(
        infrastructure=InfrastructureConfig(
            logging=LoggingDictConfig(), default_template_renderer="nonexistent_renderer"
        ),
        services=[],
        orchestrator=OrchestratorConfig(),
    )


def test_create_renderer_from_service_success(valid_raw_config: RawOpenTicketAIConfig) -> None:
    module = AppModule()
    logger_factory = module.provide_logger_factory(valid_raw_config)
    renderer = module._create_renderer_from_service(valid_raw_config, logger_factory)
    assert isinstance(renderer, TemplateRenderer)


def test_create_renderer_from_service_missing_service(invalid_raw_config: RawOpenTicketAIConfig) -> None:
    module = AppModule()
    logger_factory = module.provide_logger_factory(invalid_raw_config)
    with pytest.raises(ValueError):
        module._create_renderer_from_service(invalid_raw_config, logger_factory)


def test_provide_logger_factory(valid_raw_config: RawOpenTicketAIConfig) -> None:
    module = AppModule()
    factory = module.provide_logger_factory(valid_raw_config)
    assert isinstance(factory, LoggerFactory)


def test_provide_orchestrator_config(valid_raw_config: RawOpenTicketAIConfig) -> None:
    module = AppModule()
    config = module.provide_orchestrator_config(valid_raw_config)
    assert isinstance(config, OrchestratorConfig)


def test_provide_registerable_configs(valid_raw_config: RawOpenTicketAIConfig) -> None:
    module = AppModule()
    configs = module.provide_registerable_configs(valid_raw_config)
    assert isinstance(configs, list)
    assert all(isinstance(c, RenderableConfig) for c in configs)
