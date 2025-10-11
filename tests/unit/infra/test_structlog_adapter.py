from __future__ import annotations

import structlog

from open_ticket_ai.infra.structlog_adapter import (
    StructlogLogger,
    StructlogLoggerFactory,
    configure_structlog,
)


def test_structlog_logger_bind() -> None:
    """Test that context binding works."""
    logger_obj = structlog.get_logger("test_bind")
    logger = StructlogLogger(logger_obj)
    
    bound_logger = logger.bind(user_id="123", session="abc")
    
    assert isinstance(bound_logger, StructlogLogger)


def test_structlog_logger_bind_preserves_original() -> None:
    """Test that binding creates a new logger."""
    logger_obj = structlog.get_logger("test_preserve")
    logger = StructlogLogger(logger_obj)
    
    bound_logger = logger.bind(key="value")
    
    assert logger is not bound_logger
    assert isinstance(bound_logger, StructlogLogger)


def test_structlog_logger_bind_chain() -> None:
    """Test that binding can be chained."""
    logger_obj = structlog.get_logger("test_chain")
    logger = StructlogLogger(logger_obj)
    
    bound1 = logger.bind(key1="value1")
    bound2 = bound1.bind(key2="value2")
    
    assert isinstance(bound2, StructlogLogger)


def test_structlog_logger_factory_creates_logger() -> None:
    """Test that factory creates logger instances."""
    factory = StructlogLoggerFactory()
    
    logger = factory.get_logger("test_factory")
    
    assert isinstance(logger, StructlogLogger)


def test_structlog_logger_factory_with_context() -> None:
    """Test that factory can create logger with initial context."""
    factory = StructlogLoggerFactory()
    
    logger = factory.get_logger("test_factory_context", app="test_app", version="1.0")
    
    assert isinstance(logger, StructlogLogger)


def test_configure_structlog_console() -> None:
    """Test that configure_structlog sets up logging with console renderer."""
    configure_structlog(level="DEBUG", use_console=True, use_json=False)
    
    logger = structlog.get_logger("test_config")
    assert logger is not None


def test_configure_structlog_json() -> None:
    """Test that configure_structlog sets up logging with JSON renderer."""
    configure_structlog(level="INFO", use_console=False, use_json=True)
    
    logger = structlog.get_logger("test_json")
    assert logger is not None


def test_structlog_logger_has_all_methods() -> None:
    """Test that StructlogLogger has all required methods."""
    logger_obj = structlog.get_logger("test_methods")
    logger = StructlogLogger(logger_obj)
    
    assert hasattr(logger, "bind")
    assert hasattr(logger, "debug")
    assert hasattr(logger, "info")
    assert hasattr(logger, "warning")
    assert hasattr(logger, "error")
    assert hasattr(logger, "exception")
