# Logging System

Open Ticket AI uses an abstract logging interface that allows developers to switch between different logging implementations without modifying application code.

## Overview

The logging system provides:
- **Abstract interfaces**: `AppLogger` and `LoggerFactory` protocols
- **Multiple implementations**: stdlib and structlog adapters
- **Dependency injection**: LoggingModule for automatic setup
- **Context binding**: Attach structured context to log messages
- **Environment-based selection**: Choose implementation via `LOG_IMPL` environment variable

## Quick Start

### Using with Dependency Injection

```python
from injector import Injector, inject
from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule
from open_ticket_ai.core.logging_iface import LoggerFactory

class MyService:
    @inject
    def __init__(self, logger_factory: LoggerFactory):
        self._logger = logger_factory.get_logger(
            self.__class__.__name__,
            service="my_service",
            version="1.0"
        )
    
    def do_something(self):
        logger = self._logger.bind(operation="do_something")
        logger.info("Starting operation")
        logger.debug("Processing data")
        logger.info("Operation complete")

# Create injector with logging module
injector = Injector([LoggingModule()])
service = injector.get(MyService)
service.do_something()
```

### Direct Usage (without DI)

```python
from open_ticket_ai.infra.stdlib_logging_adapter import (
    StdlibLoggerFactory,
    configure_stdlib_logging,
)

# Configure logging
configure_stdlib_logging(level="INFO")

# Create factory and logger
factory = StdlibLoggerFactory()
logger = factory.get_logger("my_module")

# Use logger
logger.info("Application started")
```

## Configuration

### Environment Variables

**LOG_IMPL**
- Controls which logging implementation to use
- Values: `stdlib` (default) or `structlog`
- Example: `export LOG_IMPL=structlog`

**LOG_LEVEL**
- Sets the logging level
- Values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- Default: `INFO`
- Example: `export LOG_LEVEL=DEBUG`

### Runtime Configuration

```python
from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule

# Use stdlib with DEBUG level
module = LoggingModule(log_impl="stdlib", log_level="DEBUG")

# Use structlog with INFO level
module = LoggingModule(log_impl="structlog", log_level="INFO")
```

## Logging Implementations

### Stdlib (Python Standard Library)

The stdlib adapter wraps Python's built-in `logging` module.

**Features:**
- Familiar API for Python developers
- Compatible with existing logging configurations
- Context is formatted as key-value pairs in log messages

**Example output:**
```
2025-10-11 00:21:14 - MyService - INFO - User created [user_id=123 operation=create]
```

**Configuration:**

```python
from open_ticket_ai.infra.stdlib_logging_adapter import configure_stdlib_logging

configure_stdlib_logging(
    level="INFO",
    format_string="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
```

### Structlog

The structlog adapter provides structured logging with rich formatting options.

**Features:**
- True structured logging with key-value pairs
- JSON output support
- Better for log aggregation systems (ELK, Splunk, etc.)
- Colored console output

**Example output (console):**
```
2025-10-11T00:21:36.765570Z [info] User created  operation=create user_id=123
```

**Example output (JSON):**
```json
{"event": "User created", "level": "info", "timestamp": "2025-10-11T00:21:36.765570Z", "user_id": "123", "operation": "create"}
```

**Configuration:**
```python
from open_ticket_ai.infra.structlog_adapter import configure_structlog

# Console output with colors
configure_structlog(level="INFO", use_console=True, use_json=False)

# JSON output for production
configure_structlog(level="INFO", use_console=False, use_json=True)
```

## Context Binding

Context binding allows you to attach structured data to log messages:

```python
# Create base logger with service context
logger = factory.get_logger(
    "OrderService",
    service="orders",
    version="2.0"
)

# Bind request-specific context
request_logger = logger.bind(
    request_id="req-123",
    user_id="user-456"
)

# All log messages will include the bound context
request_logger.info("Processing order", order_id="order-789")
# Output includes: service=orders version=2.0 request_id=req-123 user_id=user-456 order_id=order-789
```

## Logger Methods

The `AppLogger` protocol defines the following methods:

- **`bind(**kwargs)`**: Create a new logger with additional context
- **`debug(message, **kwargs)`**: Log debug information
- **`info(message, **kwargs)`**: Log informational messages
- **`warning(message, **kwargs)`**: Log warnings
- **`error(message, **kwargs)`**: Log errors
- **`exception(message, **kwargs)`**: Log exceptions with traceback

## Best Practices

### 1. Use Dependency Injection

Always inject the `LoggerFactory` rather than creating loggers directly:

```python
class MyService:
    @inject
    def __init__(self, logger_factory: LoggerFactory):
        self._logger = logger_factory.get_logger(self.__class__.__name__)
```

### 2. Bind Context Early

Create scoped loggers with bound context for better traceability:

```python
def process_ticket(self, ticket_id: str):
    logger = self._logger.bind(ticket_id=ticket_id, operation="process")
    logger.info("Starting ticket processing")
    # All subsequent logs will include ticket_id and operation
```

### 3. Use Appropriate Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **EXCEPTION**: Like ERROR but includes exception traceback

### 4. Include Relevant Context

Add context that helps with debugging and monitoring:

```python
logger.info(
    "Database query executed",
    query_time_ms=45,
    rows_affected=3,
    table="users"
)
```

### 5. Don't Log Sensitive Data

Never log passwords, tokens, or personal information:

```python
# Bad
logger.info("User logged in", password=user_password)

# Good
logger.info("User logged in", user_id=user_id)
```

## Testing with Logging

When writing tests, you can verify logging behavior:

```python
def test_service_logs_user_creation(caplog):
    factory = StdlibLoggerFactory()
    service = MyService(factory)
    
    service.create_user("user_123", "alice")
    
    assert "Creating user" in caplog.text
    assert "user_123" in caplog.text
```

## Migration Guide

### From Direct logging.getLogger()

**Before:**
```python
import logging

class MyService:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def process(self):
        self._logger.info("Processing")
```

**After:**
```python
from injector import inject
from open_ticket_ai.core.logging_iface import LoggerFactory

class MyService:
    @inject
    def __init__(self, logger_factory: LoggerFactory):
        self._logger = logger_factory.get_logger(self.__class__.__name__)
    
    def process(self):
        self._logger.info("Processing")
```

### From AppConfig.get_logger()

**Before:**
```python
class MyService:
    def __init__(self, app_config: AppConfig):
        self._logger = app_config.get_logger(self.__class__.__name__)
```

**After:**
```python
class MyService:
    @inject
    def __init__(self, logger_factory: LoggerFactory):
        self._logger = logger_factory.get_logger(self.__class__.__name__)
```

## Advanced Usage

### Custom Structlog Processors

You can customize structlog configuration:

```python
import structlog
from open_ticket_ai.infra.structlog_adapter import StructlogLoggerFactory

# Custom configuration
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

factory = StructlogLoggerFactory()
```

### Multiple Logger Instances

Different parts of your application can have different loggers:

```python
class TicketService:
    @inject
    def __init__(self, logger_factory: LoggerFactory):
        self._logger = logger_factory.get_logger(
            "TicketService",
            component="ticket_processing"
        )

class EmailService:
    @inject
    def __init__(self, logger_factory: LoggerFactory):
        self._logger = logger_factory.get_logger(
            "EmailService",
            component="notifications"
        )
```

## Related Documentation

- [Dependency Injection](dependency_injection.md)
- [Services](services.md)
- [Configuration](../configuration/config_structure.md)
