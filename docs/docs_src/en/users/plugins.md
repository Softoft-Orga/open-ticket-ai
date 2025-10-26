---
description: Learn how Open Ticket AI's plugin system enables modular extensibility through custom services, pipes, and standardized package discovery.
---

# Plugin System

Open Ticket AI's plugin system enables modular extensibility through standalone Python packages that
expose custom
injectables (services and pipes) and related configuration schemas.

## What is a Plugin?

A **plugin** is a Python package (published under the `otai-` prefix) that extends capabilities by
providing:

- **Custom Services**: Ticket systems, ML models, API clients
- **Custom Pipes**: Data fetching, processing, classification
- **Configuration Schemas**: Type-safe plugin settings

## How Plugins Work

### 1. Installation

```bash
# Install plugin via pip/uv
uv pip install otai-otobo-znuny
```

### 2. Discovery and Registration

Plugins are discovered via the `open_ticket_ai.plugins` entry-point group. Each entry point must
resolve to a *plugin
factory*—a callable that accepts the application configuration and returns an instance of a subclass
of
`open_ticket_ai.core.plugins.plugin.Plugin`. When Open Ticket AI boots, it calls each factory,
gathers the injectables
the plugin exposes, and registers them in the dependency-injection registry using the plugin's
identifier as a prefix.

The registry prefix is derived from the package name: the `otai-` prefix is removed and remaining
underscores are
converted to hyphens. For example, `otai_otobo_znuny` becomes `otobo-znuny`. Injectables are then
registered as
`<plugin-prefix>:<InjectableName>`.

### 3. Usage in Configuration

```yaml
# Use plugin service
services:
  - id: ticket_system
    use: "otobo-znuny:OTOBOZnunyTicketSystemService"
    params:
      base_url: "${OTOBO_URL}"

# Use plugin pipe
orchestrator:
  runners:
    - run:
        id: fetch
        use: "otobo-znuny:FetchTicketsPipe"
        injects:
          ticket_system: "ticket_system"
```

## Plugin Factory Lifecycle

1. **Entry Point Resolution** – During startup the plugin loader iterates over every entry point in
   `open_ticket_ai.plugins` and imports the referenced factory, such as
   `otai_base.base_plugin:create_base_plugin`.
2. **Factory Execution** – The loader calls the factory with the runtime `AppConfig`. Plugins can
   read global settings
   such as the registry separator (`:`) or the plugin prefix (`otai-`) from this object.
3. **Injectable Enumeration** – The returned `Plugin` subclass implements `_get_all_injectables()`
   to list every pipe or
   service it contributes. The base implementation automatically transforms each injectable into its
   registry name using
   the `<plugin-prefix>:<InjectableName>` pattern.
4. **Registration** – Each injectable is registered with the shared `ComponentRegistry`, making it
   available for use in
   configuration files and dependency injection.

## API Compatibility

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
otai-my-plugin/
├── pyproject.toml
├── src/
│   └── otai_my_plugin/
│       ├── __init__.py
│       ├── plugin.py
│       ├── services/
│       └── pipes/
└── tests/
```

## Related Documentation

- [Plugin Development](../developers/plugin_development.md)
- [Dependency Injection](../developers/dependency_injection.md)
- [Pipe System](pipeline.md)
- [Configuration](../details/_config_reference.md)
