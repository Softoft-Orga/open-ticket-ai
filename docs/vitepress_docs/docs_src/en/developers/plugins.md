---
description: Learn how Open Ticket AI plugins extend the pipeline via YAML configuration, dependency injection, and unified ticket system services.
title: Plugin Developer Guide
---

# Plugin Developer Guide

This guide explains how Open Ticket AI discovers, instantiates, and executes plug-ins. The focus is on ticket-system
adapters, but the same mechanics apply to any component that you register via configuration.

## Lifecycle Overview

1. **Configuration load** – `load_config` reads `config.yml` into `RawOpenTicketAIConfig`, exposing the `plugins`,
   `general_config`, reusable `defs`, and orchestrator pipeline nodes.【F:
   src/open_ticket_ai/core/config/config_models.py†L9-L18】【F:src/open_ticket_ai/core/config/config_models.py†L22-L25】
2. **Container bootstrap** – `AppModule` binds the parsed config, the singleton `UnifiedRegistry`, the
   `InstanceCreator`, and the `PipeFactory` into the Injector so that they can be reused across the process.【F:
   src/open_ticket_ai/core/dependency_injection/container.py†L4-L25】
3. **Service instantiation** – Before the orchestrator runs, the instance creator walks over every entry under
   `open_ticket_ai.defs`, resolves the configured `use` path, and registers the resulting object inside the
   `UnifiedRegistry`. Pipes can later look up those shared services by identifier.【F:src/config.yml†L20-L69】【F:
   src/open_ticket_ai/core/dependency_injection/unified_registry.py†L15-L35】
4. **Pipeline execution** – When a pipe runs, the `PipeFactory` renders its configuration, instantiates the required
   class, and injects registered services declared in the pipe's `injects` map. Each pipe saves its result into the
   shared `Context`, which templates can read via helper functions such as `get_pipe_result` and `has_failed`.【F:
   src/open_ticket_ai/core/pipeline/pipe_factory.py†L33-L84】【F:src/open_ticket_ai/core/pipeline/pipe.py†L17-L43】【F:
   src/open_ticket_ai/core/template_rendering/jinja_renderer.py†L28-L64】

## What Counts as a Plug-in?

A plug-in is any Python package that contributes new services, pipes, or helper classes which can be referenced in YAML.
The project ships with the `otobo_znuny_plugin`, which provides a `TicketSystemService` implementation for OTOBO/OTOBO
Znuny.【F:src/open_ticket_ai/otobo_znuny_plugin/__init__.py†L1-L1】【F:
src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L24-L74】

Plug-ins typically expose:

- **Service classes** that inherit from framework base classes. Ticket adapters implement the abstract
  `TicketSystemService` contract for finding, fetching, updating, and annotating tickets.【F:
  src/open_ticket_ai/core/ticket_system_integration/ticket_system_service.py†L1-L22】
- **Configuration models** that capture credentials or options. The OTOBO adapter uses Pydantic models to parse raw YAML
  values and turn them into the client-specific structures it needs.【F:
  src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service_config.py†L1-L40】
- **Conversion helpers** that translate between the remote API schema and Open Ticket AI's unified models.【F:
  src/open_ticket_ai/otobo_znuny_plugin/models.py†L1-L27】

## Plugin Standards and Metadata

All plugins must follow standardized packaging and metadata conventions defined in [PLUGIN_STANDARDS.md](../../../../raw_en_docs/PLUGIN_STANDARDS.md).

### Required Plugin Interface

Each plugin must expose three functions in its `__init__.py`:

```python
def get_metadata():
    return {
        "name": "open-ticket-ai-<plugin-name>",
        "version": "X.Y.Z",
        "core_api": "2.0",
        "description": "Plugin description",
    }

def register_pipes():
    return [PipeClass1, PipeClass2]

def register_services():
    return [ServiceClass1, ServiceClass2]
```

### Entry Points

Plugins register via setuptools entry points in `pyproject.toml`:

```toml
[project.entry-points."open_ticket_ai.plugins"]
<plugin_name> = "open_ticket_ai_<plugin_name>"
```

### Metadata Validation

Contract tests automatically validate that all installed plugins:
- Provide required metadata fields (name, version, core_api, description)
- Implement required hooks (register_pipes, register_services)
- Declare compatible core API version

## CLI Command Registration

Plugins can expose CLI commands that integrate with the main `otai` command-line interface. This is useful for setup wizards, configuration tools, or maintenance utilities.

### Implementing CLI Commands

1. Create a `cli.py` module in your plugin with Click commands or groups:

```python
import click

@click.group()
def my_plugin():
    """My plugin commands"""
    pass

@my_plugin.command()
@click.option('--option', help='An option')
def setup(option: str):
    """Setup command for my plugin"""
    click.echo(f"Setting up with option: {option}")

def get_commands():
    return [my_plugin]
```

2. Register the CLI commands in your plugin's `__init__.py`:

```python
def register_cli_commands():
    from .cli import get_commands
    return get_commands()
```

3. Commands are automatically discovered and added to the `otai` CLI when the plugin is installed.

### Example: OTOBO/Znuny Setup

The OTOBO/Znuny plugin provides an interactive setup command:

```bash
otai otobo-znuny setup --base-url "https://example.com" --output-config config.yml
```

This demonstrates how plugins can provide user-friendly setup wizards that generate configuration files, verify connections, and guide users through the integration process.

## Registering a Plug-in

After packaging your code, wire it into the runtime through YAML:

1. **List the module** in `open_ticket_ai.plugins` if it needs to be imported for side effects such as monkey-patching
   or global registration. Modules are specified by dotted import path strings.【F:
   src/open_ticket_ai/core/config/config_models.py†L9-L12】
2. **Define reusable services** under `open_ticket_ai.defs`. Each entry provides a unique `id`, the `use` path that
   points to your class, and any constructor arguments. The bundled configuration registers the OTOBO service once and
   stores credentials sourced from environment variables.【F:src/config.yml†L20-L34】
3. **Inject services into pipes** by referencing the definition `id` in a pipe's `injects` block. Composite
   definitions (via YAML anchors) let you reuse these bindings across multiple steps.【F:src/config.yml†L35-L69】【F:
   src/open_ticket_ai/core/pipeline/pipe_factory.py†L66-L84】

Once registered, any pipe can retrieve the shared instance by asking the `UnifiedRegistry` for the configured
identifier. This keeps heavy clients (HTTP sessions, SDKs) as singletons and avoids recreating them for each pipeline
run.【F:src/open_ticket_ai/core/dependency_injection/unified_registry.py†L19-L35】

## Using Plug-in Services in Pipes

The base ticket-system pipes demonstrate how downstream components interact with plug-ins:

- `FetchTicketsPipe` resolves the injected ticket-system service, optionally renders search criteria from the current
  context, and returns a list of unified tickets.【F:
  src/open_ticket_ai/base/ticket_system_pipes/fetch_tickets_pipe.py†L12-L31】
- `UpdateTicketPipe` and `AddNotePipe` pull the shared service from the registry and call its adapter methods to mutate
  the remote ticket.【F:src/open_ticket_ai/base/ticket_system_pipes/update_ticket_pipe.py†L12-L33】【F:
  src/open_ticket_ai/base/ticket_system_pipes/add_note_pipe.py†L12-L32】
- The composite classifier pipeline in `config.yml` injects the same ticket-system adapter into multiple steps,
  showcasing how a single plug-in can power different actions (fetching, updating, adding notes) within one orchestrated
  run.【F:src/config.yml†L52-L95】

Because every pipe result is written back to the shared context, later steps and templates can read plug-in output via
helper filters such as `at_path` or conditionally branch on failures with `has_failed`.【F:
src/open_ticket_ai/core/template_rendering/jinja_renderer.py†L36-L64】【F:
src/open_ticket_ai/base/composite_pipe.py†L8-L30】

## Building Your Own Ticket-System Plug-in

To add support for another help desk platform:

1. **Create unified models** (if needed) to map remote entities into the standard `UnifiedTicket`, `UnifiedNote`, and
   `TicketSearchCriteria` classes so downstream logic remains consistent.【F:
   src/open_ticket_ai/core/ticket_system_integration/unified_models.py†L1-L32】
2. **Implement a service class** that inherits `TicketSystemService` and wraps the target API. Your methods should
   convert between unified models and the provider's request/response payloads, similar to the OTOBO adapter's
   conversion helpers.【F:src/open_ticket_ai/otobo_znuny_plugin/models.py†L11-L27】【F:
   src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service.py†L37-L74】
3. **Expose configuration models** that parse credentials, tokens, or endpoints so they can be supplied via YAML and
   environment variables.【F:src/open_ticket_ai/otobo_znuny_plugin/otobo_znuny_ticket_system_service_config.py†L1-L40】
4. **Register the service in YAML** under `open_ticket_ai.defs`, provide any secrets via environment substitution, and
   reference the definition `id` in the relevant pipeline steps or reusable anchors.【F:src/config.yml†L20-L69】

After these steps, the orchestrator can call your adapter through the standard pipes without additional code changes.
Existing templates will continue to work because they consume the unified data structures rather than adapter-specific
responses.

## Testing and Validation

- Write unit tests for your adapter that mock the remote client and validate conversions to the unified models,
  following the pattern established in `tests/unit/open_ticket_ai/otobo_znuny_plugin`.
- Exercise critical pipelines end-to-end by running the orchestrator with a staging configuration. Since pipes rely on
  async methods, remember to await your adapter's coroutine implementations in tests.
- Confirm that secrets and endpoints render correctly by running the configuration through the
  `PipeFactory.render_recursive` logic with representative context data.

By keeping the plug-in contract narrow—configuration models, a registry-friendly service class, and optional helper
functions—you can extend Open Ticket AI to any ticketing platform while staying fully declarative from the
orchestrator's perspective.

## CLI Integration

Open Ticket AI provides a CLI for managing plugins and accessing plugin-specific functionality.

### Using the Plugin Management CLI

```bash
# List all installed plugins
otai plugin list

# Install a plugin from PyPI
otai plugin install open-ticket-ai-otobo-znuny-plugin

# Remove a plugin
otai plugin remove open-ticket-ai-otobo-znuny-plugin
```

### Exposing Plugin CLI Commands

Plugins can expose their own CLI commands by implementing the optional `register_cli_commands()` function:

```python
def register_cli_commands():
    import click
    
    @click.group()
    def my_plugin():
        """My plugin CLI commands."""
        pass
    
    @my_plugin.command()
    def setup():
        """Setup the plugin."""
        click.echo("Running setup...")
    
    return my_plugin
```

Once registered, the command becomes available:
```bash
otai my_plugin setup
```

For more details, see the [CLI Usage Guide](../../../../docs/CLI_USAGE.md).
