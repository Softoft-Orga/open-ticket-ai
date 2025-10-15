from __future__ import annotations

import logging
from logging.config import dictConfig
from typing import Any

from open_ticket_ai.core.logging.logging_iface import AppLogger, LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingDictConfig


class StdlibLogger(AppLogger):
    def __init__(self, *args: Any, **kwargs: Any):
        self._logger = logging.getLogger(*args, **kwargs)

    def debug(self, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(*args, **kwargs)

    def info(self, *args: Any, **kwargs: Any) -> None:
        self._logger.info(*args, **kwargs)

    def warning(self, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(*args, **kwargs)

    def error(self, *args: Any, **kwargs: Any) -> None:
        self._logger.error(*args, **kwargs)

    def exception(self, *args: Any, **kwargs: Any) -> None:
        self._logger.exception(*args, **kwargs)


class StdlibLoggerFactory(LoggerFactory):
    def create(self, name: str, *args: Any, **kwargs: Any) -> AppLogger:
        return StdlibLogger(name)


def create_logger_factory(logging_config: LoggingDictConfig) -> LoggerFactory:
    dictConfig(logging_config.model_dump(by_alias=True, exclude_none=True))
    return StdlibLoggerFactory()
