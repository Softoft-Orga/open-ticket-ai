import pytest

from open_ticket_ai.core.logging._stdlib_logging_adapter import StdlibLoggerFactory
from open_ticket_ai.core.logging.logging_iface import LoggerFactory


@pytest.fixture
def logger_factory() -> LoggerFactory:
    return StdlibLoggerFactory()
