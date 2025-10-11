from __future__ import annotations

from typing import Any, Protocol


class AppLogger(Protocol):
    """Abstract logging interface for application-wide logging.
    
    This protocol defines the contract for logger implementations,
    allowing the application to depend on an abstraction rather than
    a specific logging library.
    """

    def bind(self, **kwargs: Any) -> AppLogger:
        """Bind context variables to the logger.
        
        Args:
            **kwargs: Key-value pairs to bind as context
            
        Returns:
            A new logger instance with bound context
        """
        ...

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        ...

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        ...

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        ...

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        ...

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback.
        
        Args:
            message: The message to log
            **kwargs: Additional context to include
        """
        ...


class LoggerFactory(Protocol):
    """Factory protocol for creating logger instances.
    
    This protocol defines the contract for logger factory implementations,
    enabling dependency injection of logger creation.
    """

    def get_logger(self, name: str, **context: Any) -> AppLogger:
        """Create or retrieve a logger instance.
        
        Args:
            name: The name of the logger (typically module or class name)
            **context: Initial context to bind to the logger
            
        Returns:
            An AppLogger instance
        """
        ...
