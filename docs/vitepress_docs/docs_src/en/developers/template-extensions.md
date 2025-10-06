---
description: Learn how to extend Jinja2 templates with custom methods and variables using decorators
title: Template Extensions
---

# Template Extensions

Open Ticket AI uses Jinja2 for template rendering throughout the pipeline. The JinjaRenderer now supports extension via decorators, allowing you to add custom template methods and global variables without modifying the core renderer.

## Overview

The template extension system provides two decorators:
- `@jinja_template_method(method_name: str)` - Register functions as template methods/filters
- `@jinja_variable(variable_name: str)` - Register global variables accessible in templates

## Basic Usage

### Registering Template Methods

Template methods can be used as functions or filters in your templates:

```python
from open_ticket_ai.core import jinja_template_method


@jinja_template_method("my_upper")
def my_upper(text: str) -> str:
    return text.upper()
```

Now you can use this in any template:

```jinja2
{{ my_upper("hello world") }}
{# or as a filter #}
{{ "hello world" | my_upper }}
```

### Registering Global Variables

Global variables are evaluated once when the JinjaRenderer is initialized and made available to all templates:

```python
from open_ticket_ai.core import jinja_variable


@jinja_variable("app_config")
def get_app_config() -> dict[str, str]:
    return {
        "app_name": "Open Ticket AI",
        "version": "1.0.0"
    }
```

Use in templates:

```jinja2
{{ app_config.app_name }} v{{ app_config.version }}
```

## Advanced Examples

### Complex Data Processing

```python
from open_ticket_ai.core import jinja_template_method


@jinja_template_method("format_currency")
def format_currency(amount: float, currency: str = "USD") -> str:
    return f"{currency} {amount:,.2f}"


@jinja_template_method("truncate_text")
def truncate_text(text: str, max_length: int = 50) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."
```

Usage:

```jinja2
Price: {{ format_currency(1234.56) }}
Summary: {{ truncate_text(ticket.description, 100) }}
```

### Configuration and Context

```python
import os
from open_ticket_ai.core import jinja_variable


@jinja_variable("system_info")
def get_system_info() -> dict[str, str]:
    return {
        "hostname": os.getenv("HOSTNAME", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "development")
    }
```

## Plugin Integration

Plugins can register their own template extensions. Simply decorate your functions at module level, and they'll be available when the module is imported:

```python
from open_ticket_ai.core import jinja_template_method, jinja_variable


@jinja_template_method("my_plugin_filter")
def my_plugin_filter(value: str) -> str:
    return f"[PLUGIN] {value}"


@jinja_variable("plugin_config")
def get_plugin_config() -> dict[str, str]:
    return {"feature_enabled": "true"}
```

## Best Practices

1. **Keep functions pure**: Template methods should be deterministic and free of side effects
2. **Handle edge cases**: Add proper error handling and default values
3. **Document your extensions**: Add docstrings to help others understand usage
4. **Use meaningful names**: Choose clear, descriptive names for your methods and variables
5. **Consider performance**: Template methods are called during rendering, so avoid expensive operations

## Thread Safety

The decorator registry is thread-safe and uses locks to prevent race conditions. Multiple JinjaRenderer instances will share the same registry, ensuring consistent behavior across your application.

## Testing Your Extensions

When testing templates with custom extensions, make sure to clear the registry between tests:

```python
import pytest
from open_ticket_ai.core import clear_registry


@pytest.fixture(autouse=True)
def reset_registry():
    clear_registry()
    yield
    clear_registry()
```

## API Reference

### `@jinja_template_method(method_name: str)`

Decorator that registers a function as a Jinja2 template method.

**Parameters:**
- `method_name` (str): The name to use in templates

**Returns:** The original function (decorator doesn't modify it)

### `@jinja_variable(variable_name: str)`

Decorator that registers a function to provide a global template variable.

**Parameters:**
- `variable_name` (str): The variable name to use in templates

**Returns:** The original function (decorator doesn't modify it)

**Note:** The function is called once during JinjaRenderer initialization. The returned value becomes the global variable.

## Built-in Template Features

The JinjaRenderer still includes all its standard features:
- `env` - Filtered environment variables
- `env_get(key, default)` - Get specific environment variable
- `has_failed(pipe_id)` - Check if a pipe failed
- `pipe_result(pipe_id, data_key)` - Get result from a previous pipe
- `at_path` filter - Extract nested values from data structures
