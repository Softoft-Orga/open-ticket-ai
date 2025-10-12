from __future__ import annotations

import os

from injector import Binder, Module, provider, singleton

from open_ticket_ai.core.logging_iface import LoggerFactory


class LoggingModule(Module):

    def __init__(self, log_impl: str | None = None, log_level: str | None = None):
        self.log_impl = log_impl or os.getenv("LOG_IMPL", "stdlib").lower()
        self.log_level = log_level or os.getenv("LOG_LEVEL", "INFO").upper()

    def configure(self, binder: Binder) -> None:
        pass

    @provider
    @singleton
    def provide_logger_factory(self) -> LoggerFactory:
        if self.log_impl == "structlog":
            from open_ticket_ai.infra.structlog_adapter import (  # noqa: PLC0415
                StructlogLoggerFactory,
                configure_structlog,
            )

            configure_structlog(level=self.log_level)
            return StructlogLoggerFactory()
        else:
            from open_ticket_ai.base.loggers.stdlib_logging_adapter import (  # noqa: PLC0415
                StdlibLoggerFactory,
                configure_stdlib_logging,
            )

            configure_stdlib_logging(level=self.log_level)
            return StdlibLoggerFactory()
