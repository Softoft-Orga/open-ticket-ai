from __future__ import annotations

import logging
from typing import Any

from open_ticket_ai.core.logging_iface import AppLogger


class StdlibLogger:
    """Adapter for Python's standard library logging."""

    def __init__(self, logger: logging.Logger, context: dict[str, Any] | None = None):
        self._logger = logger
        self._context = context or {}

    def bind(self, **kwargs: Any) -> AppLogger:
        """Bind context variables to the logger.
        
        Args:
            **kwargs: Key-value pairs to bind as context
            
        Returns:
            A new logger instance with merged context
        """
        new_context = {**self._context, **kwargs}
        return StdlibLogger(self._logger, new_context)

    def _format_message(self, message: str, **kwargs: Any) -> str:
        """Format message with context."""
        all_context = {**self._context, **kwargs}
        if all_context:
            context_str = " ".join(f"{k}={v}" for k, v in all_context.items())
            return f"{message} [{context_str}]"
        return message

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.debug(self._format_message(message, **kwargs))

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.info(self._format_message(message, **kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.warning(self._format_message(message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.error(self._format_message(message, **kwargs))

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        self._logger.exception(self._format_message(message, **kwargs))


class StdlibLoggerFactory:
    """Factory for creating stdlib logger instances."""

    def get_logger(self, name: str, **context: Any) -> AppLogger:
        """Create or retrieve a logger instance.
        
        Args:
            name: The name of the logger (typically module or class name)
            **context: Initial context to bind to the logger
            
        Returns:
            An AppLogger instance wrapping stdlib logger
        """
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
