from __future__ import annotations

from injector import Injector
from open_ticket_ai.infra.structlog_adapter import StructlogLoggerFactory

from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule
from open_ticket_ai.core.logging_iface import LoggerFactory
from open_ticket_ai.infra.stdlib_logging_adapter import StdlibLoggerFactory


def test_logging_module_binds_stdlib_factory_by_default() -> None:
    """Test that LoggingModule binds stdlib factory by default."""
    injector = Injector([LoggingModule()])

    factory = injector.get(LoggerFactory)

    assert isinstance(factory, StdlibLoggerFactory)


def test_logging_module_binds_stdlib_factory_explicitly() -> None:
    """Test that LoggingModule binds stdlib factory when explicitly specified."""
    injector = Injector([LoggingModule(log_impl="stdlib")])

    factory = injector.get(LoggerFactory)

    assert isinstance(factory, StdlibLoggerFactory)


def test_logging_module_binds_structlog_factory() -> None:
    """Test that LoggingModule binds structlog factory when specified."""
    injector = Injector([LoggingModule(log_impl="structlog")])

    factory = injector.get(LoggerFactory)

    assert isinstance(factory, StructlogLoggerFactory)


def test_logging_module_respects_env_var_stdlib(monkeypatch) -> None:
    """Test that LoggingModule respects LOG_IMPL environment variable for stdlib."""
    monkeypatch.setenv("LOG_IMPL", "stdlib")

    injector = Injector([LoggingModule()])
    factory = injector.get(LoggerFactory)

    assert isinstance(factory, StdlibLoggerFactory)


def test_logging_module_respects_env_var_structlog(monkeypatch) -> None:
    """Test that LoggingModule respects LOG_IMPL environment variable for structlog."""
    monkeypatch.setenv("LOG_IMPL", "structlog")

    injector = Injector([LoggingModule()])
    factory = injector.get(LoggerFactory)

    assert isinstance(factory, StructlogLoggerFactory)


def test_logging_module_factory_creates_logger() -> None:
    """Test that factory can create loggers."""
    injector = Injector([LoggingModule()])

    factory = injector.get(LoggerFactory)
    logger = factory.get_logger("test_logger")

    assert logger is not None


def test_logging_module_factory_is_singleton() -> None:
    """Test that the logger factory is a singleton."""
    injector = Injector([LoggingModule()])

    factory1 = injector.get(LoggerFactory)
    factory2 = injector.get(LoggerFactory)

    assert factory1 is factory2


def test_logger_implements_protocol() -> None:
    """Test that created logger implements AppLogger protocol."""
    injector = Injector([LoggingModule()])
    factory = injector.get(LoggerFactory)

    logger = factory.get_logger("test")

    assert hasattr(logger, "bind")
    assert hasattr(logger, "debug")
    assert hasattr(logger, "info")
    assert hasattr(logger, "warning")
    assert hasattr(logger, "error")
    assert hasattr(logger, "exception")
