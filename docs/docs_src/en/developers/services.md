---
description: Core services documentation for Open Ticket AI covering ticket system adapters, business logic encapsulation, and dependency injection.
---

# Core Services

Services encapsulate business logic and provide reusable functionality to pipes. They are managed by the dependency
injection container.

## Service Classes vs. Configuration Entries

Service *classes* are Python implementations that live in packages (for example `otai_base.ticket_system_integration.TicketSystemService` subclasses).
They become usable inside Open Ticket AI when you expose them through the plugin registry.

Service *configuration entries* live in `open_ticket_ai.services` inside your YAML configuration. Each entry binds a
service class to an identifier, optional constructor parameters, and a dependency-injection scope. Multiple entries can
reference the same class while providing different parameters.

### Example: Multiple Services Configured at Once

```yaml
open_ticket_ai:
  services:
    jinja_default:
      use: "base:JinjaRenderer"

    otobo_znuny:
      use: "otobo-znuny:OTOBOZnunyTicketSystemService"
      params:
        base_url: "http://example/otobo/nph-genericinterface.pl"
        password: "${OTOBO_PASSWORD}"

    hf_local:
      use: "hf-local:HFClassificationService"
      params:
        model_name: "softoft/otai-queue-de-bert-v1"
```

In this configuration three independent services become available for injection. Pipes select the instance they need by
referencing the entry identifier, for example:

```yaml
- id: fetch_otobo
  use: "base:FetchTicketsPipe"
  injects:
    ticket_system: "otobo_znuny"
```

## Core Service Types

### Ticket Services

- **TicketSystemAdapter**: Interface to ticket systems
- **TicketFetcher**: Retrieves tickets
- **TicketUpdater**: Updates ticket properties

### Classification Services

- **ClassificationService**: ML-based classification
- **QueueClassifier**: Queue assignment logic
- **PriorityClassifier**: Priority assignment logic

### Utility Services

- **TemplateRenderer**: Jinja2 template rendering (can be configured in `defs` for customization)
- **ConfigurationService**: Access to configuration
- **LoggerFactory**: Centralized logging with pluggable backends (stdlib/structlog)

## Service Lifecycle and Scopes

When the application loads configuration it converts each `open_ticket_ai.services` entry into an `InjectableConfig` and
registers it with the DI container. Every entry yields a distinct injectable instance. If you configure three ticket system
services, all three can be injected simultaneously under their identifiers.

Scopes control when those instances are created and reused. Open Ticket AI supports:

- **Singleton scope (default)** – the container creates one instance per configuration entry and reuses it across the
  application.
- **Transient scope** – a new instance is created each time the service is injected.

Choose the scope that matches the service’s statefulness. See the [Dependency Injection](dependency_injection.md) guide
for details about scopes and the [Configuration Reference](../../details/config_reference.md) for the `services`
structure.

## Creating Custom Services

1. Define service interface
2. Implement service
3. Register with DI container using the injector module
4. Add a configuration entry and inject it into pipes

## Service Best Practices

### Do:

- Keep services focused on single responsibility
- Use interfaces for service contracts
- Make services stateless when possible
- Inject dependencies, don't create them
- Write unit tests for services

### Don't:

- Store execution state in service instances
- Access configuration directly (inject ConfigurationService)
- Create circular dependencies
- Mix business logic with infrastructure concerns

## Testing Services

Services should be unit tested independently from the pipes that use them. Create test instances of services and verify
their behavior with test data.

## Related Documentation

- [Dependency Injection](dependency_injection.md)
- [Configuration Reference](../../details/config_reference.md)
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Plugin Development](plugin_development.md)
