from __future__ import annotations

import logging

from open_ticket_ai.base.loggers.stdlib_logging_adapter import (
    StdlibLogger,
    StdlibLoggerFactory,
    create_logger_factory,
)


def test_stdlib_logger_debug(caplog) -> None:
    """Test that debug logging works."""
    logger_obj = logging.getLogger("test_debug")
    logger = StdlibLogger(logger_obj)

    with caplog.at_level(logging.DEBUG):
        logger.debug("Debug message")

    assert "Debug message" in caplog.text


def test_stdlib_logger_info(caplog) -> None:
    """Test that info logging works."""
    logger_obj = logging.getLogger("test_info")
    logger = StdlibLogger(logger_obj)

    with caplog.at_level(logging.INFO):
        logger.info("Info message")

    assert "Info message" in caplog.text


def test_stdlib_logger_warning(caplog) -> None:
    """Test that warning logging works."""
    logger_obj = logging.getLogger("test_warning")
    logger = StdlibLogger(logger_obj)

    with caplog.at_level(logging.WARNING):
        logger.warning("Warning message")

    assert "Warning message" in caplog.text


def test_stdlib_logger_error(caplog) -> None:
    """Test that error logging works."""
    logger_obj = logging.getLogger("test_error")
    logger = StdlibLogger(logger_obj)

    with caplog.at_level(logging.ERROR):
        logger.error("Error message")

    assert "Error message" in caplog.text


def test_stdlib_logger_bind_context(caplog) -> None:
    """Test that context binding works."""
    logger_obj = logging.getLogger("test_bind")
    logger = StdlibLogger(logger_obj)

    bound_logger = logger.bind(user_id="123", session="abc")

    with caplog.at_level(logging.INFO):
        bound_logger.info("Message with context")

    assert "Message with context" in caplog.text
    assert "user_id=123" in caplog.text
    assert "session=abc" in caplog.text


def test_stdlib_logger_bind_preserves_original(caplog) -> None:
    """Test that binding creates a new logger and preserves original."""
    logger_obj = logging.getLogger("test_preserve")
    logger = StdlibLogger(logger_obj)

    bound_logger = logger.bind(key="value")

    with caplog.at_level(logging.INFO):
        logger.info("Original logger")
        bound_logger.info("Bound logger")

    records = caplog.records
    assert len(records) == 2
    assert "key=value" not in records[0].message
    assert "key=value" in records[1].message


def test_stdlib_logger_bind_chain(caplog) -> None:
    """Test that binding can be chained."""
    logger_obj = logging.getLogger("test_chain")
    logger = StdlibLogger(logger_obj)

    bound1 = logger.bind(key1="value1")
    bound2 = bound1.bind(key2="value2")

    with caplog.at_level(logging.INFO):
        bound2.info("Chained context")

    assert "key1=value1" in caplog.text
    assert "key2=value2" in caplog.text


def test_stdlib_logger_kwargs_in_log_call(caplog) -> None:
    """Test that additional kwargs in log call are included."""
    logger_obj = logging.getLogger("test_kwargs")
    logger = StdlibLogger(logger_obj)

    with caplog.at_level(logging.INFO):
        logger.info("Message", request_id="456")

    assert "request_id=456" in caplog.text


def test_stdlib_logger_factory_creates_logger() -> None:
    """Test that factory creates logger instances."""
    factory = StdlibLoggerFactory()

    logger = factory.get_logger("test_factory")

    assert isinstance(logger, StdlibLogger)


def test_stdlib_logger_factory_with_context(caplog) -> None:
    """Test that factory can create logger with initial context."""
    factory = StdlibLoggerFactory()

    logger = factory.get_logger("test_factory_context", app="test_app", version="1.0")

    with caplog.at_level(logging.INFO):
        logger.info("Factory message")

    assert "app=test_app" in caplog.text
    assert "version=1.0" in caplog.text


def test_stdlib_logger_exception(caplog) -> None:
    """Test that exception logging works."""
    logger_obj = logging.getLogger("test_exception")
    logger = StdlibLogger(logger_obj)

    def raise_error() -> None:
        raise ValueError("Test error")

    try:
        raise_error()
    except ValueError:
        with caplog.at_level(logging.ERROR):
            logger.exception("Exception occurred")

    assert "Exception occurred" in caplog.text
    assert "ValueError: Test error" in caplog.text


def test_configure_stdlib_logging() -> None:
    """Test that configure_stdlib_logging sets up logging."""
    create_logger_factory(level="DEBUG")

    logger = logging.getLogger("test_configure")
    logger.setLevel(logging.DEBUG)
    assert logger.level == logging.DEBUG
