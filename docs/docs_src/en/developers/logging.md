---
description: Open Ticket AI logging system documentation covering abstract interfaces, stdlib and structlog implementations, and structured logging patterns.
---

#### TODO there is only standardlogger implementation currently.

# Logging System

Open Ticket AI uses an abstract logging interface that allows developers to switch between different logging
implementations without modifying application code.

## Overview

The logging system provides:

- **Abstract interfaces**: `AppLogger` and `LoggerFactory` protocols
- **Multiple implementations**: stdlib and structlog adapters
- **Dependency injection**: AppModule provides LoggerFactory for automatic setup
- **Context binding**: Attach structured context to log messages
- **Environment-based selection**: Choose implementation via `LOG_IMPL` environment variable

## Quick Start

### Using with Dependency Injection

Services can inject the `LoggerFactory` and use it to create loggers with bound context. The logger factory creates
logger instances with optional initial context data.

### Direct Usage (without DI)

The logging adapters can be configured and used directly without the dependency injection container. Configure the
logging system at application startup and create loggers as needed.

```python
from open_ticket_ai.core.logging.stdlib_logging_adapter import (
    StdlibLoggerFactory,
    create_logger_factory,
)

# Configure logging
create_logger_factory(level="INFO")

# Create factory and logger
factory = StdlibLoggerFactory()
logger = factory.create("my_module")

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

The logging system is configured through the application's YAML configuration file under the `infrastructure.logging`
section, which is loaded by the AppModule during dependency injection setup.

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

The stdlib logging can be configured with custom format strings and date formats.

```python
from open_ticket_ai.core.logging.stdlib_logging_adapter import create_logger_factory

create_logger_factory(
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
{
  "event": "User created",
  "level": "info",
  "timestamp": "2025-10-11T00:21:36.765570Z",
  "user_id": "123",
  "operation": "create"
}
```

**Configuration:**

Structlog can be configured for console output with colors or JSON output for production environments.

## Context Binding

Context binding allows you to attach structured data to log messages. Create a base logger with service context, then
bind request-specific context. All subsequent log messages from that logger will include the bound context
automatically.

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

Always inject the `LoggerFactory` rather than creating loggers directly. This allows for easier testing and
configuration management.

### 2. Bind Context Early

Create scoped loggers with bound context for better traceability. Bind context data like request IDs, user IDs, or
operation names early so all subsequent logs include this information.

### 3. Use Appropriate Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **EXCEPTION**: Like ERROR but includes exception traceback

### 4. Include Relevant Context

Add context that helps with debugging and monitoring, such as:

- Query execution time
- Number of rows affected
- Table or resource names
- Operation identifiers

### 5. Don't Log Sensitive Data

Never log passwords, tokens, or personal information. Always log identifiers instead of sensitive values.

## Testing with Logging

When writing tests, you can verify logging behavior by capturing log output and asserting on the messages and context
data.

## Migration Guide

### From Direct logging.getLogger()

Replace direct use of Python's logging module with dependency injection of the LoggerFactory. This allows the logging
implementation to be swapped without code changes.

### From AppConfig.get_logger()

Replace AppConfig-based logger creation with LoggerFactory injection. This decouples logging from the global
configuration object.

## Advanced Usage

### Custom Structlog Processors

Structlog configuration can be customized with custom processors for specialized formatting or filtering needs.

### Multiple Logger Instances

Different parts of your application can have different loggers with different bound context to help distinguish log
sources.

## Related Documentation

- [Dependency Injection](dependency_injection.md)
- [Services](services.md)
- [Configuration](../../details/configuration/config_structure.md)
