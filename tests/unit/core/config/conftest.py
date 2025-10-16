import pytest

from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.logging.logging_iface import LoggerFactory


@pytest.fixture
def app_config() -> AppConfig:
    return AppConfig()


@pytest.fixture
def logger_factory() -> LoggerFactory:
    from open_ticket_ai.base.loggers.stdlib_logging_adapter import StdlibLoggerFactory

    return StdlibLoggerFactory()


@pytest.fixture
def config_loader(app_config: AppConfig, logger_factory: LoggerFactory) -> ConfigLoader:
    return ConfigLoader(app_config, logger_factory)
