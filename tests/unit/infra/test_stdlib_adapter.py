from __future__ import annotations

import logging

from open_ticket_ai.base.loggers.stdlib_logging_adapter import StdlibLogger, StdlibLoggerFactory


def test_stdlib_logger_basic_logging(caplog) -> None:
    logger_obj = logging.getLogger("test")
    logger = StdlibLogger(logger_obj)
    with caplog.at_level(logging.INFO):
        logger.info("Info message")
        logger.error("Error message")
    assert "Info message" in caplog.text
    assert "Error message" in caplog.text


def test_stdlib_logger_bind_context(caplog) -> None:
    logger_obj = logging.getLogger("test_bind")
    logger = StdlibLogger(logger_obj)
    bound_logger = logger.bind(user_id="123")
    with caplog.at_level(logging.INFO):
        bound_logger.info("Message with context")
    assert "user_id=123" in caplog.text


def test_stdlib_logger_factory_creates_logger() -> None:
    factory = StdlibLoggerFactory()
    logger = factory.create("test_factory")
    assert isinstance(logger, StdlibLogger)
