from __future__ import annotations

import logging
import sys
from typing import Any

from open_ticket_ai.core.logging.logging_iface import AppLogger, LoggerFactory
from open_ticket_ai.core.logging.logging_models import LoggingConfig, LoggingFormatConfig

PIPE_FMT_DEFAULT = "%(asctime)s - %(levelname)s - %(name)s: %(pipe_name)s - %(message)s"

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def level_no(level: str) -> int:
    return LOG_LEVELS[level]


def build_formatter(logging_format_config: LoggingFormatConfig) -> logging.Formatter:
    return logging.Formatter(fmt=logging_format_config.message_format, datefmt=logging_format_config.date_format)


class StdlibLogger(AppLogger):
    def __init__(self, inner: logging.Logger | logging.LoggerAdapter | None = None):
        self._logger = inner or logging.getLogger()

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


class _PipeNameDefaultFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "pipe_name"):
            record.pipe_name = "-"
        return True


class StdlibLoggerFactory(LoggerFactory):
    def __init__(self, cfg: LoggingConfig | None = None):
        self._cfg = cfg or LoggingConfig()

    def create(
        self,
        name: str,
        format_config: LoggingFormatConfig | None = None,
        extras: dict[str, Any] | None = None,
        *_: Any,
        **__: Any,
    ) -> AppLogger:
        # PAD Name to 30 chars for alignment
        padded_name = name.ljust(30)
        logger = logging.getLogger(padded_name)
        if format_config:
            logger.handlers.clear()
            logger.propagate = False
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level_no(self._cfg.level))
            handler.setFormatter(build_formatter(format_config))
            logger.addHandler(handler)
            if self._cfg.log_to_file and self._cfg.log_file_path:
                fh = logging.FileHandler(self._cfg.log_file_path)
                fh.setLevel(level_no(self._cfg.level))
                fh.setFormatter(build_formatter(format_config))
                logger.addHandler(fh)
            adapter = logging.LoggerAdapter(logger, extras or {})
            return StdlibLogger(adapter)
        return StdlibLogger(logger)


def create_logger_factory(logging_config: LoggingConfig) -> LoggerFactory:
    root_logger = logging.getLogger()
    root_logger.setLevel(level_no(logging_config.level))
    root_logger.handlers.clear()

    formatter = build_formatter(logging_config.format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level_no(logging_config.level))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if logging_config.log_to_file and logging_config.log_file_path:
        file_handler = logging.FileHandler(logging_config.log_file_path)
        file_handler.setLevel(level_no(logging_config.level))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    return StdlibLoggerFactory(logging_config)
