# Examples

This directory contains example code demonstrating how to use Open Ticket AI features.

## Logging Example

**File:** `logging_example.py`

Demonstrates the abstract logging service implementation with both stdlib and structlog backends.

### Running the Example

```bash
uv run python examples/logging_example.py
```

### What It Shows

- How to use `LoggingModule` with dependency injection
- Injecting `LoggerFactory` into services
- Creating loggers with bound context
- Switching between stdlib and structlog implementations
- The difference in output format between the two backends

### Key Concepts

1. **LoggerFactory Injection**: Services receive a `LoggerFactory` via dependency injection
2. **Context Binding**: Attach metadata to loggers that automatically appears in all log messages
3. **Implementation Switching**: Change logging backend without modifying service code

### Example Output

**Stdlib logging:**
```
2025-10-11 00:21:14 - UserService - INFO - Creating user [service=user_service version=1.0 user_id=user_123 operation=create_user username=alice]
```

**Structlog:**
```
2025-10-11T00:21:36.765570Z [info] Creating user  operation=create_user service=user_service user_id=user_456 username=bob version=1.0
```

## More Examples

Additional examples will be added as new features are implemented.
