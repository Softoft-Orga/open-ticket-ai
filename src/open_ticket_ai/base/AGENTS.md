# Base Components Guidelines

**Location:** `/src/open_ticket_ai/base/` directory  
**Parent Guidelines:** [Source AGENTS.md](../../AGENTS.md) | [Root AGENTS.md](../../../AGENTS.md)  
**Last Updated:** 2025-10-11

Guidelines for `src/open_ticket_ai/base/` - reusable pipes and foundational components.

## Critical Test Placement Rules

⚠️ **NEVER place tests in this directory:**

- ❌ Forbidden: `src/open_ticket_ai/base/tests/`
- ✅ Tests for base components: `tests/unit/base/`

See [Root AGENTS.md](../../../AGENTS.md) for complete test structure rules.

## Purpose of Base

The `base/` module provides abstract base classes and concrete implementations that can be reused across the application
and plugins. This is the foundation layer that other modules build upon.

## Base Pipe Classes

When creating or modifying base pipes:

- Define clear abstract interfaces with well-documented contracts
- Use ABC (Abstract Base Class) for interfaces that must be implemented
- Keep base classes focused and cohesive
- Avoid putting business logic in base classes

### Pipe Implementation Pattern

All pipes must follow this pattern for parameter handling:

**1. Define Params Model:**
```python
class MyPipeParams(BaseModel):
    field1: str
    field2: int = 10  # with default
```

**2. Define Pipe Class:**
```python
class MyPipe(Pipe[MyPipeParams]):
    params_class = MyPipeParams  # Required class attribute
    
    def __init__(
        self,
        pipe_config: PipeConfig[MyPipeParams],
        logger_factory: LoggerFactory,
        # Add injected dependencies here
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory)
        # self.params is now validated MyPipeParams instance
        # Use self.params.field1, self.params.field2, etc.
    
    async def _process(self) -> PipeResult[Any]:
        # Implementation using self.params
        pass
```

**Key Points:**
- `params_class` attribute is mandatory
- Parent `__init__` handles dict → Pydantic conversion
- Params can be dict (from YAML rendering) or typed model
- Access params via `self.params` (validated)
- Don't call `model_validate()` yourself

**Example with Dependency Injection:**
```python
class FetchTicketsPipe(Pipe[FetchTicketsParams]):
    params_class = FetchTicketsParams
    
    def __init__(
        self,
        ticket_system: TicketSystemService,  # Injected
        pipe_config: PipeConfig[FetchTicketsParams],
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory)
        self.ticket_system = ticket_system
```

**YAML Configuration (User View):**
```yaml
- id: my_pipe
  use: "mypackage:MyPipe"
  params:
    field1: "{{ env('MY_VALUE') }}"  # Template rendered as dict
    field2: 20
```

The template is rendered to a dict, then validated against `MyPipeParams`.

## Pipe Lifecycle

Base pipes define the lifecycle and execution model:

1. Initialization - constructed by DI container
2. Configuration - validated through pydantic models
3. Execution - `run()` or `execute()` methods called by orchestrator
4. Cleanup - resources released as needed

## Ticket System Pipes

The `ticket_system_pipes/` subdirectory contains reusable pipes for common ticket operations:

- Fetching tickets from systems
- Classifying and analyzing tickets
- Updating ticket properties
- Adding notes and comments

When adding new ticket system pipes:

- Inherit from appropriate base classes
- Make operations idempotent where possible
- Handle partial failures gracefully
- Support batch operations for efficiency

## Mixins and Composition

Use mixins to add orthogonal functionality:

- Keep mixins small and focused on a single concern
- Document mixin requirements clearly
- Use Protocol classes for structural typing where appropriate
- Prefer composition over deep inheritance hierarchies

## Extension Points

Base classes should provide clear extension points:

- Use template method pattern for common workflows
- Allow subclasses to override specific behaviors
- Provide hooks for pre/post processing
- Document which methods are intended for override

## Testing Base Components

Tests for base components should verify:

- Abstract contracts are properly defined
- Base implementations work correctly
- Subclasses can properly extend base behavior
- Mixins compose correctly without conflicts

**Test location:** All tests for base components are in `tests/unit/base/`

## Documentation

- Architecture concepts: `docs/vitepress_docs/docs_src/en/docs/concepts/`
- Code details: `docs/vitepress_docs/docs_src/en/docs/code/pipe.md`
- See [docs/AGENTS.md](../../../docs/AGENTS.md) for documentation structure