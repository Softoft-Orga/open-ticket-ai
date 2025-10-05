# Core Application Guidelines

Guidelines specific to the `src/open_ticket_ai/` core application package.

## Architecture Overview

The core application is organized into distinct modules:

- `core/` - Core infrastructure (config, DI, pipeline, plugins)
- `base/` - Base components and reusable pipes
- `cli/` - Command-line interface
- `extras/` - Additional utilities and scripts

## Dependency Injection

The DI container (using `injector`) is the backbone of the application. Services are singletons registered at startup:

- Register services in `core/dependency_injection/create_registry.py`
- Use constructor injection to declare dependencies
- Services should be stateless or manage their own state safely
- Avoid circular dependencies between services

## Pipeline System

Pipes are the fundamental execution units:

- Pipes inherit from base classes in `base/`
- Each pipe should have a single, well-defined responsibility
- Pipes receive dependencies through DI
- Pipes can reference other services by ID from the registry

## Configuration Loading

Runtime configuration flows through pydantic models:

1. YAML is loaded from file or environment variable
2. Parsed into `RawOpenTicketAIConfig`
3. Validated through pydantic
4. Services and pipes instantiated from validated config

Keep configuration models in `core/config/` and ensure they match the YAML structure.

## Template Rendering

Template rendering lives in `core/template_rendering/`. When working with templates:

- Use Jinja2 for dynamic content
- Keep template logic minimal
- Pass structured data through clear context objects
- Templates should not contain business logic

## Ticket System Integration

Adapters for ticket systems live in `core/ticket_system_integration/`. When adding adapters:

- Implement the adapter interface completely
- Handle API errors gracefully with retries where appropriate
- Use async/await for I/O operations
- Log operations for debugging

## Plugin System

The plugin system in `core/plugins/` discovers and loads external plugins:

- Plugins register via entry points
- Use the plugin metadata interface for discoverability
- Plugins can contribute pipes and services
- Validate plugin compatibility at load time

## Testing Core Code

Tests for core code live in `tests/unit/open_ticket_ai/`. Focus on:

- Testing public interfaces and contracts
- Validating configuration parsing and validation
- Testing pipeline orchestration logic
- Verifying DI container setup
