from __future__ import annotations

import logging
from typing import Any

import structlog

from open_ticket_ai.core.logging_iface import AppLogger


class StructlogLogger:
    """Adapter for structlog structured logging."""

    def __init__(self, logger: structlog.BoundLogger):
        self._logger = logger

    def bind(self, **kwargs: Any) -> AppLogger:
        return StructlogLogger(self._logger.bind(**kwargs))

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._logger.error(message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        self._logger.exception(message, **kwargs)


class StructlogLoggerFactory:
    def get_logger(self, name: str, **context: Any) -> AppLogger:
        logger = structlog.get_logger(name)
        if context:
            logger = logger.bind(**context)
        return StructlogLogger(logger)


def configure_structlog(
    level: str = "INFO",
    use_console: bool = True,
    use_json: bool = False,
) -> None:
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if use_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level.upper())),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
