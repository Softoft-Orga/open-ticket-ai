---
description: Learn how Open Ticket AI's plugin system enables modular extensibility through custom services, pipes, and standardized package discovery.
---

# Plugin System

### TODO not much has changed here. Not regarding the concepts at least

###

The plugin system enables extending Open Ticket AI through standalone Python packages that provide custom services,
pipes, and configuration schemas.

## What is a Plugin?

A **plugin** is a Python package that extends capabilities by providing:

- **Custom Services**: Ticket systems, ML models, API clients
- **Custom Pipes**: Data fetching, processing, classification
- **Configuration Schemas**: Type-safe plugin settings

## How Plugins Work

### 1. Installation

```bash
# Install plugin via pip/uv
uv pip install otai-otobo-znuny
```

### Usage in Configuration

```yaml
# Use plugin service
services:
  - id: ticket_system
    use: "otobo_znuny:OtoboAdapter"
    params:
      base_url: "${OTOBO_URL}"

# Use plugin pipe
orchestrator:
  runners:
    - run:
        id: fetch
        use: "otobo_znuny:FetchTicketsPipe"
        injects:
          ticket_system: "ticket_system"
```

## API Compatibility

Plugins declare compatibility with core API versions:

```python
# In plugin __init__.py
__version__ = "1.0.0"
__core_api_version__ = "^2.0"  # Compatible with 2.x
```

Core validates compatibility at load time and fails gracefully if versions mismatch.

## Benefits

**For Users:**

- Install only needed functionality
- Mix plugins from different sources
- Upgrade plugins independently

**For Developers:**

- Extend without core access
- Distribute as standard packages
- Test in isolation

**For the Project:**

- Smaller core codebase
- Community ecosystem
- Faster innovation

## Available Plugins

### OTOBO/Znuny Plugin

```bash
uv add otai-otobo-znuny
```

Provides ticket system integration for OTOBO, Znuny, and OTRS.

### HuggingFace Local Plugin

```bash
uv add otai-hf-local
```

Enables local ML model inference with HuggingFace models.

## Creating a Plugin

See [Plugin Development Guide](../developers/plugin_development.md) for complete instructions.

**Basic Structure:**

```
my-plugin/
├── pyproject.toml          # Entry points defined here
├── src/
│   └── my_plugin/
│       ├── __init__.py
│       ├── plugin.py       # setup() function
│       ├── services/
│       └── pipes/
└── tests/
```

## Related Documentation

- [Plugin Development](../developers/plugin_development.md)
- [Dependency Injection](../developers/dependency_injection.md)
- [Pipe System](pipeline.md)
- [Configuration](../details/config_reference.md)
