from __future__ import annotations

import logging
from logging.config import dictConfig
from typing import Any

from open_ticket_ai.core.config.logging_config import LoggingDictConfig
from open_ticket_ai.core.logging_iface import AppLogger, LoggerFactory


class StdlibLogger(AppLogger):
    def __init__(self, logger: logging.Logger, context: dict[str, Any] | None = None):
        self._logger = logger


    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(message, *args, **kwargs)

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.exception(message, *args, **kwargs)


class StdlibLoggerFactory(LoggerFactory):
    def create(self, name: str, **context: Any) -> AppLogger:
        logger = logging.getLogger(name)
        return StdlibLogger(logger, context)


def create_logger_factory(logging_config: LoggingDictConfig) -> LoggerFactory:
    dictConfig(logging_config.model_dump(by_alias=True, exclude_none=True))
    return StdlibLoggerFactory()
