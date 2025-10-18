import pytest
from open_ticket_ai.core.logging.logging_iface import LoggerFactory
from open_ticket_ai.core.logging.stdlib_logging_adapter import StdlibLoggerFactory


@pytest.fixture
def logger_factory() -> LoggerFactory:
    return StdlibLoggerFactory()
