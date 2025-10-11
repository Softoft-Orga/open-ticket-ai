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
        """Bind context variables to the logger.
        
        Args:
            **kwargs: Key-value pairs to bind as context
            
        Returns:
            A new logger instance with bound context
        """
        return StructlogLogger(self._logger.bind(**kwargs))

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.error(message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.exception(message, **kwargs)


class StructlogLoggerFactory:
    """Factory for creating structlog logger instances."""

    def get_logger(self, name: str, **context: Any) -> AppLogger:
        """Create or retrieve a logger instance.
        
        Args:
            name: The name of the logger (typically module or class name)
            **context: Initial context to bind to the logger
            
        Returns:
            An AppLogger instance wrapping structlog
        """
        logger = structlog.get_logger(name)
        if context:
            logger = logger.bind(**context)
        return StructlogLogger(logger)


def configure_structlog(
    level: str = "INFO",
    use_console: bool = True,
    use_json: bool = False,
) -> None:
    """Configure structlog with standard settings.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        use_console: Whether to use console output
        use_json: Whether to use JSON formatting (vs. key-value)
    """
    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if use_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
