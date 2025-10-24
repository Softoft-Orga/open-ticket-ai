import pytest
from open_ticket_ai import LoggerFactory, StdlibLoggerFactory


@pytest.fixture
def logger_factory() -> LoggerFactory:
    return StdlibLoggerFactory()
