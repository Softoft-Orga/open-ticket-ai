from __future__ import annotations

import logging

from _pytest.logging import LogCaptureFixture

from open_ticket_ai.core.logging.stdlib_logging_adapter import StdlibLogger, StdlibLoggerFactory


def test_stdlib_logger_basic_logging(caplog: LogCaptureFixture) -> None:
    logger = StdlibLogger()
    with caplog.at_level(logging.INFO):
        logger.info("Info message")
        logger.error("Error message")
    assert "Info message" in caplog.text
    assert "Error message" in caplog.text


def test_stdlib_logger_factory_creates_logger() -> None:
    factory = StdlibLoggerFactory()
    logger = factory.create("test_factory")
    assert isinstance(logger, StdlibLogger)
