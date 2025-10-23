---
description: Core services documentation for Open Ticket AI covering ticket system adapters, business logic encapsulation, and dependency injection.
---

### TODO Differentiate clearly between general Services and the Services you can configure. These are not singletons, you can have multiple tickesystemservices.

# Core Services

Services encapsulate business logic and provide reusable functionality to pipes. They are managed by the dependency
injection container.

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

## Service Lifecycle Management

Services are typically singletons:

- Created once at application startup
- Shared across all pipes
- Destroyed at application shutdown

## Creating Custom Services

1. Define service interface
2. Implement service
3. Register with DI container using the injector module
4. Inject into pipes using dependency injection

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
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Plugin Development](plugin_development.md)
