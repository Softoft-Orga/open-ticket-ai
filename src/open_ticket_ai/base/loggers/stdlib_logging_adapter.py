from __future__ import annotations

import logging
from logging.config import dictConfig
from typing import Any

from open_ticket_ai.core.config.logging_config import LoggingDictConfig
from open_ticket_ai.core.logging_iface import AppLogger, LoggerFactory


class StdlibLogger(AppLogger):
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

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        if args:
            self._logger.debug(message, *args)
        else:
            self._logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        if args:
            self._logger.info(message, *args)
        else:
            self._logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        if args:
            self._logger.warning(message, *args)
        else:
            self._logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        if args:
            self._logger.error(message, *args)
        else:
            self._logger.error(self._format_message(message, **kwargs))

    def exception(self, message: str, *args: Any, **kwargs: Any) -> None:
        if args:
            self._logger.exception(message, *args)
        else:
            self._logger.exception(self._format_message(message, **kwargs))


class StdlibLoggerFactory(LoggerFactory):
    def get_logger(self, name: str, **context: Any) -> AppLogger:
        logger = logging.getLogger(name)
        return StdlibLogger(logger, context)


def create_logger_factory(logging_config: LoggingDictConfig) -> LoggerFactory:
    print(logging_config.model_dump_json(indent=2, by_alias=True, exclude_none=True))
    dictConfig(logging_config.model_dump(by_alias=True, exclude_none=True))
    return StdlibLoggerFactory()
