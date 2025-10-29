---
description: Learn how Open Ticket AI uses dependency injection to manage services, resolve dependencies, and enable testability with loose coupling.
---

# Dependency Injection

Open Ticket AI uses dependency injection (DI) to manage services, pipes, and shared infrastructure.
The container is responsible for building core singletons, loading plugins, and providing factories
that resolve dependencies at runtime.

## Component registry fundamentals

`ComponentRegistry` tracks every injectable that the runtime can construct. Pipes and services are
stored in separate dictionaries so the registry can enforce clearer error messages and type
expectations during lookup.【F:
src/open_ticket_ai/core/dependency_injection/component_registry.py†L12-L41】

- `register()` inspects the class that is being registered. Pipes (subclasses of `Pipe`) are stored
  in `_pipes`, while other subclasses of `Injectable` are stored in `_services`.
- When a lookup fails, `InjectableNotFoundError` includes the identifiers that are currently loaded
  to make configuration issues easier to diagnose.【F:
  src/open_ticket_ai/core/dependency_injection/component_registry.py†L23-L40】【F:
  src/open_ticket_ai/core/config/errors.py†L26-L34】
- `find_by_type()` performs a filtered search across both collections. The TemplateRenderer
  bootstrap (described below) relies on this to find services that implement a specific
  interface.【F:src/open_ticket_ai/core/dependency_injection/component_registry.py†L42-L48】

### How plugins populate the registry

Each plugin implements `Plugin._get_all_injectables()` and returns every service and pipe class that
should be discoverable. During application startup the `PluginLoader` locates entry points in the
`open_ticket_ai.plugins` group, instantiates the plugin, and calls `on_load()` with the shared
registry.【F:src/open_ticket_ai/core/plugins/plugin_loader.py†L19-L51】

`Plugin.on_load()` builds a registry identifier for each injectable. The prefix is derived from the
plugin module name (with the global `otai-` plugin prefix removed) and combined with the
injectable’s own `get_registry_name()` using `:` as the separator. This ensures registry IDs remain
globally unique while still being readable (for example `base:MyService`).【F:
src/open_ticket_ai/core/plugins/plugin.py†L13-L44】【F:
src/open_ticket_ai/core/config/app_config.py†L13-L23】

## Container bootstrap sequence

`AppModule` is the Injector module that wires together the runtime. Its constructor eagerly creates
several singletons:

1. `AppConfig` loads environment, `.env`, and `config.yml` settings and exposes the workspace
   configuration model.【F:src/open_ticket_ai/core/dependency_injection/container.py†L22-L25】【F:
   src/open_ticket_ai/core/config/app_config.py†L5-L37】
2. `ComponentRegistry` is instantiated and injected into the module, plugin loader, pipe factory,
   and tests.【F:src/open_ticket_ai/core/dependency_injection/container.py†L25-L28】
3. `LoggerFactory` is produced by `create_logger_factory()` so that every injectable can obtain
   structured loggers.【F:src/open_ticket_ai/core/dependency_injection/container.py†L26-L28】【F:
   src/open_ticket_ai/core/logging/stdlib_logging_adapter.py†L1-L45】
4. `PluginLoader` receives the registry, logger factory, and configuration. `load_plugins()` runs
   immediately so that pipes and services from plugins are available before the Injector resolves
   other bindings.【F:src/open_ticket_ai/core/dependency_injection/container.py†L27-L34】

During `configure()`, `AppModule` binds these instances as singletons and registers the
`PipeFactory` type itself as a singleton so other components can request it later.【F:
src/open_ticket_ai/core/dependency_injection/container.py†L36-L42】

### TemplateRenderer selection and safeguards

Template rendering is a required service. The provider method `create_renderer_from_service()`
inspects the configured services, filters the entries that implement `TemplateRenderer`, and
enforces that exactly one configuration exists.【F:
src/open_ticket_ai/core/dependency_injection/container.py†L44-L73】【F:
src/open_ticket_ai/core/dependency_injection/service_registry_util.py†L1-L17】

- If more than one TemplateRenderer service is present,
  `MultipleConfigurationsForSingletonServiceError` stops the bootstrap. This prevents ambiguity
  about which renderer should be used for templating.【F:
  src/open_ticket_ai/core/dependency_injection/container.py†L63-L66】【F:
  src/open_ticket_ai/core/config/errors.py†L52-L64】
- If none are found, `MissingConfigurationForRequiredServiceError` is raised, signalling that the
  configuration is incomplete and template rendering cannot proceed.【F:
  src/open_ticket_ai/core/dependency_injection/container.py†L68-L71】【F:
  src/open_ticket_ai/core/config/errors.py†L41-L50】

After validation, the registry is asked for the concrete renderer class, which is instantiated with
its rendered parameters and returned as the singleton TemplateRenderer for the application.【F:
src/open_ticket_ai/core/dependency_injection/container.py†L72-L78】【F:
src/open_ticket_ai/core/template_rendering/template_renderer.py†L1-L52】

## Injecting dependencies into pipes and services

Runtime dependency resolution is orchestrated by `PipeFactory`:

- When a pipe is created, the factory resolves every `injects` entry in the pipe configuration. Each
  mapping associates a constructor argument (such as `ticket_client`) with the identifier of a
  configured service. The factory fetches the service configuration, renders its parameters,
  instantiates the service, and passes it to the pipe constructor.【F:
  src/open_ticket_ai/core/pipes/pipe_factory.py†L19-L74】
- Services and pipes must accept `logger_factory` in their constructors (supplied by
  `Injectable.__init__`) so they can emit namespaced logs without reconfiguring logging backends.【F:
  src/open_ticket_ai/core/injectables/injectable.py†L11-L24】【F:
  src/open_ticket_ai/core/logging/logging_iface.py†L7-L23】
- Use the registry naming scheme produced by `Plugin._get_registry_name()` when declaring `use`
  targets in configuration. This ensures the factory can look up the correct class (e.g.
  `base:HttpTicketPipe`).【F:src/open_ticket_ai/core/plugins/plugin.py†L25-L44】

Pipes receive their parameters through templating before instantiation. `PipeFactory` renders the
`params` block using the active `TemplateRenderer`, then constructs the pipe with the rendered
`PipeConfig`, the `PipeContext`, references to itself (for creating nested pipes), and any injected
services.【F:src/open_ticket_ai/core/pipes/pipe_factory.py†L31-L61】

Services follow the same pattern: once selected, the factory renders the service configuration
against an empty scope and builds the injectable. Because every service derives from `Injectable`,
they automatically parse typed parameters via their `ParamsModel` and get a logger named after their
configuration ID.【F:src/open_ticket_ai/core/pipes/pipe_factory.py†L62-L74】【F:
src/open_ticket_ai/core/injectables/injectable.py†L11-L24】

### Practical tips

- Define a descriptive `ParamsModel` on your pipe or service subclass so configuration gets
  validated automatically during construction.【F:
  src/open_ticket_ai/core/injectables/injectable.py†L9-L24】
- Keep inject IDs consistent across configuration and runtime by reusing the registry prefix
  described above.
- When creating new plugins, return all injectable classes from `_get_all_injectables()` so they
  register automatically during bootstrap.【F:src/open_ticket_ai/core/plugins/plugin.py†L37-L44】
- If a pipe requires another pipe, inject `PipeFactory` and call
  `await pipe_factory.create_pipe(...)` rather than instantiating it directly. The factory will
  handle templating, logging, and dependency resolution for nested pipes.【F:
  src/open_ticket_ai/core/pipes/pipe_factory.py†L19-L61】

## Related documentation

- [Services](services.md)
