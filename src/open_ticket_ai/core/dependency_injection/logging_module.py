from __future__ import annotations

import os

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.logging_iface import LoggerFactory


class LoggingModule(Module):
    """Dependency injection module for logging configuration.
    
    Selects the logging implementation based on the LOG_IMPL environment variable:
    - LOG_IMPL=structlog: Use structlog adapter
    - LOG_IMPL=stdlib (default): Use stdlib logging adapter
    """

    def __init__(self, log_impl: str | None = None, log_level: str | None = None):
        """Initialize LoggingModule.
        
        Args:
            log_impl: Override for LOG_IMPL env var (structlog or stdlib)
            log_level: Override for LOG_LEVEL env var (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_impl = log_impl or os.getenv("LOG_IMPL", "stdlib").lower()
        self.log_level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()

    def configure(self, binder: Binder) -> None:
        """Configure the dependency injection bindings for logging.
        
        Args:
            binder: The injector binder to configure
        """
        pass

    @provider
    @singleton
    def provide_logger_factory(self) -> LoggerFactory:
        """Provide a LoggerFactory instance based on configuration.
        
        Returns:
            A LoggerFactory implementation (structlog or stdlib)
        """
        if self.log_impl == "structlog":
            from open_ticket_ai.infra.structlog_adapter import (  # noqa: PLC0415
                StructlogLoggerFactory,
                configure_structlog,
            )

            configure_structlog(level=self.log_level)
            return StructlogLoggerFactory()
        else:
            from open_ticket_ai.infra.stdlib_adapter import (  # noqa: PLC0415
                StdlibLoggerFactory,
                configure_stdlib_logging,
            )

            configure_stdlib_logging(level=self.log_level)
            return StdlibLoggerFactory()
