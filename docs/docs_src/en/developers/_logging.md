---
description: Open Ticket AI logging system documentation covering the abstract interfaces and current standard-library implementation.
---

# Logging System

Open Ticket AI uses an abstract logging interface that allows developers to configure logging
behaviour without
modifying
application code. The current implementation is built entirely on Python's standard-library
`logging` module.

## Overview

The logging system provides:

- **Abstract interfaces**: `AppLogger` and `LoggerFactory` protocols
- **Standard-library implementation**: `StdlibLoggerFactory`
- **Dependency injection**: `AppModule` provides `LoggerFactory` for automatic setup
- **Context binding**: Attach structured context to log messages using the logger API

## Quick Start

### Using with dependency injection

Services can inject the `LoggerFactory` and use it to create loggers with bound context. The factory
returns instances
of
`StdlibLogger`, which proxy to `logging.getLogger`.

### Direct usage (without DI)

The standard-library adapter can be configured and used directly without the dependency injection
container. Configure
the
logging system at application startup and create loggers as needed.

```python
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import (
    StdlibLoggerFactory,
    create_logger_factory,
)

config = LoggingConfig(level="INFO")
factory = create_logger_factory(config)

logger = factory.create("my_module")
logger.info("Application started")
```

## Configuration

### Runtime configuration

The logging system is configured through the application's YAML configuration file under the
`infrastructure.logging` section, which is loaded by the `AppModule` during dependency injection
setup.

### LoggingConfig fields

`LoggingConfig` defines the supported runtime configuration:

| Field                   | Type                                                               | Default                                                  | Description                                                                        |
|-------------------------|--------------------------------------------------------------------|----------------------------------------------------------|------------------------------------------------------------------------------------|
| `level`                 | Literal[`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`] | `"INFO"`                                                 | Minimum severity level captured by handlers.                                       |
| `log_to_file`           | `bool`                                                             | `False`                                                  | Enables writing log output to a file handler.                                      |
| `log_file_path`         | `str \| None`                                                      | `None`                                                   | Absolute or relative path for file logging. Required when `log_to_file` is `True`. |
| `format.message_format` | `str`                                                              | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` | Format string passed to `logging.Formatter`.                                       |
| `format.date_format`    | `str`                                                              | `"%Y-%m-%d %H:%M:%S"`                                    | Timestamp format used by the formatter.                                            |

## Logging implementation

### Stdlib (Python standard library)

The standard-library adapter wraps Python's built-in `logging` module.

**Features:**

- Familiar API for Python developers
- Compatible with existing logging configurations
- Respects the `LoggingConfig` options for format, level, and optional file output

**Example output:**

```
2025-10-11 00:21:14 - my_module - INFO - Application started
```

### Handler wiring

`create_logger_factory` prepares the global logging state:

1. Fetch the root logger and set its level from `LoggingConfig.level`.
2. Remove any previously registered handlers to avoid duplicate messages.
3. Build a `logging.Formatter` using `log_format` and `date_format`.
4. Attach a `StreamHandler` writing to `sys.stdout`, configured with the selected level and
   formatter.
5. Optionally attach a `FileHandler` when `log_to_file` is `True` and `log_file_path` is provided.
6. Return a `StdlibLoggerFactory`, which creates `StdlibLogger` instances bound to named loggers.

## Context binding

Context binding allows you to attach structured data to log messages. Create a base logger with
service context, then
bind request-specific context. All subsequent log messages from that logger will include the bound
context
automatically.

## Logger methods

The `AppLogger` protocol defines the following methods:

- **`bind(**kwargs)`**: Create a new logger with additional context
- **`debug(message, **kwargs)`**: Log debug information
- **`info(message, **kwargs)`**: Log informational messages
- **`warning(message, **kwargs)`**: Log warnings
- **`error(message, **kwargs)`**: Log errors
- **`exception(message, **kwargs)`**: Log exceptions with traceback

## Best practices

### 1. Use dependency injection

Always inject the `LoggerFactory` rather than creating loggers directly. This allows for easier
testing and
configuration
management.

### 2. Bind context early

Create scoped loggers with bound context for better traceability. Bind context data like request
IDs, user IDs, or
operation names early so all subsequent logs include this information.

### 3. Use appropriate log levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **EXCEPTION**: Like ERROR but includes exception traceback

### 4. Include relevant context

Add context that helps with debugging and monitoring, such as:

- Query execution time
- Number of rows affected
- Table or resource names
- Operation identifiers

### 5. Don't log sensitive data

Never log passwords, tokens, or personal information. Always log identifiers instead of sensitive
values.

## Testing with logging

When writing tests, you can verify logging behavior by capturing log output and asserting on the
messages and context
data.

## Migration guide

### From direct `logging.getLogger()`

Replace direct use of Python's logging module with dependency injection of the `LoggerFactory`. This
allows the logging
implementation to be swapped without code changes.

### From `AppConfig.get_logger()`

Replace usages of legacy factory helpers with dependency-injected instances of `LoggerFactory`
created by
`create_logger_factory`.

## Future roadmap

The logging abstraction allows for introducing alternative adapters (such as Structlog or
OpenTelemetry exporters) in
the
future. These integrations are currently under evaluation and not yet available. This page will be
updated when new
implementations are added so readers can adopt them confidently.
