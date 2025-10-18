from __future__ import annotations

import logging
import sys
from typing import Any

from open_ticket_ai.core.logging.logging_iface import AppLogger, LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingConfig


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
    def create(self, *args: Any, **kwargs: Any) -> AppLogger:
        return StdlibLogger(*args, **kwargs)


def create_logger_factory(logging_config: LoggingConfig) -> LoggerFactory:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_config.level)
    root_logger.handlers.clear()

    formatter = logging.Formatter(
        fmt=logging_config.log_format,
        datefmt=logging_config.date_format,
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging_config.level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if logging_config.log_to_file and logging_config.log_file_path:
        file_handler = logging.FileHandler(logging_config.log_file_path)
        file_handler.setLevel(logging_config.level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return StdlibLoggerFactory()
