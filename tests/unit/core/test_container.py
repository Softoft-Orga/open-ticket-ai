from __future__ import annotations

import pytest

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig

pytestmark = [pytest.mark.unit]


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
