from __future__ import annotations

import logging
from typing import Any

from open_ticket_ai.core.logging_iface import AppLogger


class StdlibLogger:
    def __init__(self, logger: logging.Logger, context: dict[str, Any] | None = None):
        self._logger = logger
        self._context = context or {}

    def bind(self, **kwargs: Any) -> AppLogger:
        new_context = {**self._context, **kwargs}
        return StdlibLogger(self._logger, new_context)

    def _format_message(self, message: str, **kwargs: Any) -> str:
        all_context = {**self._context, **kwargs}
        if all_context:
            context_str = " ".join(f"{k}={v}" for k, v in all_context.items())
            return f"{message} [{context_str}]"
        return message

    def debug(self, message: str, **kwargs: Any) -> None:
        self._logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        self._logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        self._logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        self._logger.error(self._format_message(message, **kwargs))

    def exception(self, message: str, **kwargs: Any) -> None:
        self._logger.exception(self._format_message(message, **kwargs))


class StdlibLoggerFactory:
    def get_logger(self, name: str, **context: Any) -> AppLogger:
        logger = logging.getLogger(name)
        return StdlibLogger(logger, context)


def configure_stdlib_logging(
    level: str = "INFO",
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
) -> None:
    """Configure stdlib logging with standard settings.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Log format string
        datefmt: Date format string
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        datefmt=datefmt,
    )
