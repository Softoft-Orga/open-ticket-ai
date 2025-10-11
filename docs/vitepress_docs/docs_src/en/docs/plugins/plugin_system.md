# Plugin System

Open Ticket AI's plugin system allows extending functionality through modular, reusable components.

## Plugin Architecture Overview

The plugin architecture provides:
- **Modular Design**: Self-contained functionality
- **Easy Distribution**: Plugins as Python packages
- **Entry Points**: Automatic plugin discovery
- **Versioning**: API compatibility tracking

## Plugin Discovery Mechanism

Plugins are discovered through Python entry points defined in `pyproject.toml`:

```toml
[project.entry-points."open_ticket_ai.plugins"]
my_plugin = "my_plugin.module:setup_plugin"
```

## Entry Points System

When Open Ticket AI starts:
1. Scans for registered entry points
2. Loads plugin modules
3. Calls setup functions
4. Registers services and pipes

## Plugin API Versioning

Plugins declare compatible API versions:

```python
PLUGIN_API_VERSION = "1.0"

def setup_plugin(registry):
    registry.register_pipe("my_pipe", MyPipe)
    registry.register_service(MyService, MyServiceImpl)
```

## Plugin Structure

A typical plugin contains:
- Service implementations
- Pipe implementations
- Configuration schemas
- Documentation
- Tests

## Available Plugins

- [HuggingFace Local](hf_local.md) - Local ML inference
- [OTOBO/Znuny](otobo_znuny.md) - Ticket system integration

## Related Documentation

- [Plugin Development](plugin_development.md)
- [API Compatibility](../integration/api_compatibility.md)
- [Creating Custom Adapters](../integration/custom_adapters.md)
