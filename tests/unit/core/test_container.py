from __future__ import annotations

import pytest

from open_ticket_ai.core.config.config_models import OpenTicketAIConfig
from open_ticket_ai.core.dependency_injection.container import AppModule
from open_ticket_ai.core.logging.logging_iface import LoggerFactory

pytestmark = [pytest.mark.unit]


def test_provide_logger_factory(valid_raw_config: OpenTicketAIConfig) -> None:
    module = AppModule()
    factory = module.provide_logger_factory(valid_raw_config)
    assert isinstance(factory, LoggerFactory)
