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

The logging system integrates with the dependency injection container. Inject the `LoggerFactory` into your services and use it to create loggers with appropriate context.

### Direct Usage (without DI)

You can also use the logging system directly by configuring the logging implementation and creating a logger factory.

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

The `LoggingModule` can be configured with specific log implementation and level settings at runtime.

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

## Context Binding

Context binding allows you to attach structured data to log messages. Create a base logger with service context, then bind request-specific or operation-specific context as needed. All log messages from the bound logger will include the bound context.

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

Always inject the `LoggerFactory` rather than creating loggers directly. This allows for better testability and configuration management.

### 2. Bind Context Early

Create scoped loggers with bound context for better traceability. Bind operation-specific or request-specific context at the start of processing.

### 3. Use Appropriate Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **EXCEPTION**: Like ERROR but includes exception traceback

### 4. Include Relevant Context

Add context that helps with debugging and monitoring, such as query times, affected rows, or resource identifiers.

### 5. Don't Log Sensitive Data

Never log passwords, tokens, or personal information. Log only identifiers that can be used to trace operations without exposing sensitive data.

## Testing with Logging

When writing tests, you can verify logging behavior using test fixtures and assertions.

## Integration with Open Ticket AI

The logging system is integrated throughout Open Ticket AI:
- **Pipeline execution**: Track pipeline and pipe execution
- **Service operations**: Log service method calls
- **Error handling**: Capture and log exceptions
- **Configuration**: Log configuration loading and validation

## Related Documentation

- [Dependency Injection](dependency_injection.md)
- [Services](services.md)
- [Configuration](../configuration/config_structure.md)
