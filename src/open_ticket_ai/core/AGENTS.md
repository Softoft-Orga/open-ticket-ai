# Core Infrastructure Guidelines

**Location:** `/src/open_ticket_ai/core/` directory  
**Parent Guidelines:** [Source AGENTS.md](../../AGENTS.md) | [Root AGENTS.md](../../../AGENTS.md)  
**Last Updated:** 2025-10-11

Guidelines for `src/open_ticket_ai/core/` - the foundational infrastructure of the application.

## Critical Test Placement Rules

⚠️ **NEVER place tests in this directory:**

- ❌ Forbidden: `src/open_ticket_ai/core/tests/`
- ✅ Tests for core components: `tests/unit/core/`

See [Root AGENTS.md](../../../AGENTS.md) for complete test structure rules.

## Core Responsibilities

The `core/` module provides essential infrastructure that the rest of the application depends on:

- `config/` - Configuration schemas and loaders
- `dependency_injection/` - DI container setup and registry
- `pipeline/` - Pipeline orchestration and execution
- `plugins/` - Plugin discovery and loading
- `template_rendering/` - Jinja2 template processing
- `ticket_system_integration/` - Adapter interfaces for ticket systems

## Configuration Module

All configuration lives in `config/`. When modifying:

- Use pydantic models for validation
- Keep models aligned with YAML structure
- Add validation logic for complex rules
- Provide sensible defaults where appropriate
- Document config options in VitePress, not in code

Configuration flows from YAML → RawOpenTicketAIConfig → validated models → runtime objects.

### Config Structure

- `plugins`: List of plugin names to load
- `infrastructure`: Core infrastructure config (logging, default_template_renderer)
- `services`: Registerable services (TemplateRenderer, TicketSystems, etc.)
- `orchestrator`: Pipeline and runner definitions

## Dependency Injection Module

The DI container in `dependency_injection/` manages object lifecycles:

- Services are registered as singletons by default
- Use `@inject` decorator for constructor injection
- Register services in `create_registry.py`
- Keep circular dependencies to zero
- Services should be stateless or thread-safe

The UnifiedRegistry ties together all registered services and makes them available to pipes.

## Pipeline Module

Pipeline orchestration in `pipeline/` controls execution flow:

- Orchestrator loads configuration and schedules pipes
- Pipes are executed according to defined intervals and dependencies
- Pipeline execution is async by default
- Handle errors at the orchestrator level
- Log execution metrics for monitoring

### Pipe Parameter Pattern

The `Pipe` base class supports runtime parameter validation:

**Key Implementation (pipe.py:27-30):**

```python
if isinstance(pipe_params._config, dict):
    self._config: ParamsT = self.params_class.model_validate(pipe_params._config)
else:
    self._config: ParamsT = pipe_params._config
```

**Flow:**

1. YAML config loaded as dict structure
2. Jinja2 templates rendered in dict form
3. Rendered dict passed to Pipe constructor
4. `model_validate()` converts dict → typed Pydantic model
5. Validated params available as `self.params`

**Benefits:**

- Template rendering happens before type validation
- YAML remains simple and flexible
- Full type safety after rendering
- Clear validation error messages
- Compatible with Copilot code generation

**When implementing pipes:**

- Always define `params_class` class attribute
- Let parent `__init__` handle param conversion
- Access validated params via `self.params`
- Don't manually validate in subclass `__init__`

## Plugin Module

Plugin loading in `plugins/` enables extensibility:

- Discovers plugins via entry points
- Validates plugin metadata and compatibility
- Calls plugin registration hooks
- Maintains plugin registry for runtime access
- Fails gracefully if plugin loading fails

## Template Rendering Module

Template system in `template_rendering/` processes dynamic content:

- TemplateRenderer is bootstrapped as a service before all other services
- Configure the default renderer in `infrastructure.default_template_renderer`
- Template renderer params are NEVER templated (raw config only)
- All other service/pipe configs are rendered using the TemplateRenderer
- Uses Jinja2 for templating by default
- Context objects passed to templates
- Templates should be data-driven, not logic-heavy
- Cache compiled templates for performance
- Handle missing variables gracefully

Example config:

```yaml
infrastructure:
  default_template_renderer: "jinja_default"
services:
  - id: "jinja_default"
    use: "open_ticket_ai.core.template_rendering:JinjaRenderer"
    params:
      env_config:
        prefix: "OTAI_"
      autoescape: false
```

## Ticket System Integration Module

Adapter interfaces in `ticket_system_integration/` abstract ticket systems:

- Define clear adapter contracts
- Support async operations
- Handle authentication and session management
- Implement retry logic for transient failures
- Log all ticket system interactions

## Testing Core Infrastructure

Core infrastructure tests focus on:

- Configuration parsing and validation
- DI container setup and resolution
- Pipeline execution and error handling
- Plugin discovery and loading
- Template rendering with various inputs
- Adapter contract compliance

**Test location:** All tests for core components are in `tests/unit/core/`

## Documentation

- Architecture concepts: `docs/vitepress_docs/docs_src/en/docs/concepts/`
- Code architecture details: `docs/vitepress_docs/docs_src/en/docs/code/`
- Configuration guides: `docs/vitepress_docs/docs_src/en/docs/configuration/`
- See [docs/AGENTS.md](../../../docs/AGENTS.md) for documentation structure
