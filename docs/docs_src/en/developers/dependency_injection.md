---
description: Learn how Open Ticket AI uses dependency injection to manage services, resolve dependencies, and enable testability with loose coupling.
---

## TODO not much changed.

# Dependency Injection

Open Ticket AI uses dependency injection (DI) to manage services and their dependencies, promoting loose coupling and
testability.

## DI Container Overview

The DI container:

- Manages service lifecycle
- Resolves dependencies automatically
- Supports singleton and transient services
- Enables easy testing with mocks

## Service Registration and Resolution

Services are registered at application startup using the injector module. The DI container manages service instances and
resolves dependencies automatically when pipes request them.

## UnifiedRegistry Usage

The UnifiedRegistry is the central registry for:

- Services
- Pipes
- Plugins
- Configuration

## Injecting Services into Pipes

Pipes can request services via constructor injection using decorators. The DI container automatically provides the
required service instances when creating pipe instances.

## Service Scopes

### Singleton

- One instance for the entire application
- Used for stateless services
- Default scope for most services

### Transient

- New instance for each injection
- Used for stateful services
- Rarely needed in pipe architecture

## Testing with DI

DI makes testing easier by allowing you to inject mock services into pipes during testing. You can create mock
implementations of services and pass them directly to pipe constructors for unit testing.

## Related Documentation

- [Services](services.md)
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Plugin System](../plugins/plugin_system.md)
