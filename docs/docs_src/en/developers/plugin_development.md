---
description: Complete guide to developing custom plugins for Open Ticket AI including project structure, entry points, and best practices.
---

# Plugin Development Guide

Learn how to create custom plugins to extend Open Ticket AI functionality.

## Packaging & Naming Requirements

Open Ticket AI discovers plugins by their Python package name and project metadata.

- **Distribution/project name**: must start with `otai-`. This matches the `AppConfig.PLUGIN_NAME_PREFIX` (`otai-`) that the runtime uses when computing registry keys.
- **Python package name**: use the same words as the distribution name but with underscores (`otai_my_plugin`). The loader converts the top-level module name to kebab-case automatically, so `otai_my_plugin` becomes `otai-my-plugin` internally.
- **Registry prefix**: when a plugin registers injectables it strips the global prefix (`otai-`) and keeps the remainder (e.g. `otai-my-plugin` → `my-plugin`). That portion becomes the registry key prefix when combined with the injectable name, such as `my-plugin:MyPipe`.

## Recommended Project Layout

```
otai-my-plugin/
├── pyproject.toml
├── src/
│   └── otai_my_plugin/
│       ├── __init__.py
│       ├── pipes/
│       │   └── my_pipe.py
│       ├── services/
│       │   └── my_service.py
│       └── plugin_factory.py
└── tests/
    └── unit/
        └── test_my_plugin.py
```

## Entry Point Contract

Open Ticket AI loads plugins via the `open_ticket_ai.plugins` entry-point group. The entry point must resolve to a callable that accepts an `AppConfig` instance and returns a `Plugin`. Subclassing `Plugin` already satisfies that contract, so expose your subclass directly.

```toml
[project.entry-points."open_ticket_ai.plugins"]
my_plugin = "otai_my_plugin.plugin_factory:PluginFactory"
```

### Why reference the class?

- The loader invokes the target like a factory. Referencing the subclass keeps the wiring declarative—no wrapper function required.
- The class name clarifies that instantiating the plugin may involve dependency wiring (for example, constructor parameters beyond `AppConfig` can be injected by the IoC container).

## Implementing the PluginFactory Class

All plugins inherit from `open_ticket_ai.core.plugins.plugin.Plugin`. The base class:

1. Accepts `AppConfig` (injected by the loader) in its constructor.
2. Uses the top-level module name to infer the plugin name and registry prefix.
3. Calls `_get_all_injectables()` during `on_load` and registers each `Injectable` automatically with the `ComponentRegistry` using the pattern `<plugin-prefix>:<injectable-registry-name>`.

The separator between the prefix and the injectable name is `AppConfig.REGISTRY_IDENTIFIER_SEPERATOR`, which defaults to `:`.

Override `_get_all_injectables()` to return every injectable you want to expose. You should **not** call `registry.register(...)` yourself inside `on_load`; the base class does it for you.

```python
# src/otai_my_plugin/plugin_factory.py

from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.plugins.plugin import Plugin

from otai_my_plugin.pipes.my_pipe import MyPipe
from otai_my_plugin.services.my_service import MyService


class PluginFactory(Plugin):
    """Create the plugin instance and declare exported injectables."""

    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            MyPipe,
            MyService,
        ]
```

When the loader instantiates `PluginFactory`, the base implementation will:

1. Compute the registry prefix (`my-plugin` in this example).
2. Call `MyPipe.get_registry_name()` and `MyService.get_registry_name()`.
3. Register each injectable as `my-plugin:<registry-name>` with the shared `ComponentRegistry`.

### Returning Injectables vs Manual Registration

Prior implementations required a `setup(registry)` helper that performed manual registration. With the factory pattern above you simply return the list of injectables and let the base class handle the rest. This keeps registration consistent and ensures registry names follow the `prefix:Injectable` convention automatically.

If you do need to opt out of the automatic behaviour—for example, to register additional aliases—you can still access the registry inside `_get_all_injectables()` by overriding `on_load`. For typical use cases, returning the list is sufficient and preferred.

## pyproject.toml Essentials

Ensure the metadata aligns with the naming rules and entry-point contract:

```toml
[project]
name = "otai-my-plugin"
version = "0.1.0"
description = "Custom plugin for Open Ticket AI"
requires-python = ">=3.13"
dependencies = [
    "open-ticket-ai>=1.0.0,<2.0.0",
]

[project.entry-points."open_ticket_ai.plugins"]
my_plugin = "otai_my_plugin.plugin_factory:PluginFactory"
```

Use the distribution name (`otai-my-plugin`) to derive both the module prefix (`otai_my_plugin`) and registry prefix (`my-plugin`). Keeping these consistent ensures the loader resolves entry points correctly and produces predictable registry keys.

## Packaging, Distribution & Testing

```
uv build
uv publish
```

Install your plugin into an Open Ticket AI environment with:

```
uv pip install otai-my-plugin
```

Write unit tests alongside your plugin code under `tests/unit/` and run them with `uv run -m pytest`.

## Additional Resources

- [Plugin System](../plugins/plugin_system.md)
- [Dependency Injection](dependency_injection.md)
- [Services](services.md)
- [Pipeline Architecture](../concepts/pipeline-architecture.md)
- [Hugging Face Local plugin example](../plugins/hf_local.md)
