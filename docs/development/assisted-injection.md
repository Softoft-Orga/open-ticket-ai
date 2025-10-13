# Assisted Injection with Explicit Inject Precedence

## Overview

This document explains the refactored `RenderableFactory` implementation that uses assisted injection with explicit inject precedence to properly handle dependency injection in Open Ticket AI.

## Problem Statement

Previously, `RenderableFactory.__create_renderable_instance` manually constructed kwargs and passed dependencies. This approach had several issues:

1. **Tight coupling**: Dependencies were hard-coded in the factory
2. **No precedence handling**: When multiple implementations of the same service existed (e.g., `OTOBOTicketSystemService` vs `ZnunyTicketSystemService`), there was no way to explicitly choose which one a pipe should receive
3. **Limited extensibility**: Adding new dependencies required modifying the factory code

## Solution

The refactored implementation uses the injector library's child injector pattern to implement explicit inject precedence:

### Key Components

1. **Child Injector Creation**: When explicit injects are specified in config, a child injector is created with those bindings
2. **Precedence**: Explicit injects in the child injector shadow parent injector bindings
3. **Type-Based Resolution**: Dependencies are resolved using `typing.get_type_hints()` to handle forward references
4. **Backward Compatibility**: The refactoring maintains the same external API

### How It Works

```python
# 1. Explicit injects are resolved from registerable_configs
resolved_injects = self.__resolve_injects(config.injects, scope)

# 2. If explicit injects exist, create a child injector with those bindings
if resolved_injects:
    child_injector = self.__create_child_injector_with_explicit_bindings(cls, resolved_injects)
    return self.__instantiate_with_injector(cls, config, child_injector)
else:
    # 3. Otherwise, use the parent injector
    return self.__instantiate_with_injector(cls, config, self._injector)
```

## Usage Example

### Configuration

```yaml
services:
  - id: otobo_service
    use: OTOBOTicketSystemService
    params:
      base_url: "https://otobo.example.com"
  
  - id: znuny_service
    use: ZnunyTicketSystemService
    params:
      base_url: "https://znuny.example.com"

orchestrator:
  runners:
    - run:
        use: FetchTicketsPipe
        injects:
          ticket_system: 'otobo_service'  # Explicitly use OTOBO
```

### What Happens

1. The parent injector might have a default `TicketSystemService` binding
2. The pipe's `injects` config specifies `ticket_system: 'otobo_service'`
3. A child injector is created with `TicketSystemService` bound to the OTOBO instance
4. The pipe receives the OTOBO service, overriding any parent default

## Technical Details

### Child Injector Binding

The child injector is created with explicit bindings based on the parameter types:

```python
def __create_child_injector_with_explicit_bindings(
    self, cls: type, explicit_deps: dict[str, Any]
) -> Injector:
    type_hints = get_type_hints(cls.__init__)
    
    def configure_explicit_bindings(binder: Any) -> None:
        for param_name, instance in explicit_deps.items():
            if param_name in type_hints:
                param_type = type_hints[param_name]
                binder.bind(param_type, to=instance)  # Shadows parent binding
    
    return self._injector.create_child_injector([configure_explicit_bindings])
```

### Dependency Resolution

Dependencies are resolved in this order:

1. **Explicit injects** (highest precedence) - from `config.injects`
2. **Injector bindings** - from parent or child injector
3. **Standard dependencies** - factory, app_config, logger_factory, pipe_config
4. **Config parameters** - params, config (for triggers)

### Handling **kwargs

The implementation detects when a class accepts `**kwargs` and provides standard dependencies:

```python
has_var_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())

if 'logger_factory' in sig.parameters or has_var_kwargs:
    kwargs["logger_factory"] = self._logger_factory
```

This ensures backward compatibility with classes that use `**kwargs` to accept dependencies.

## Testing

Two key tests verify the implementation:

### Test 1: Explicit Inject Precedence

```python
def test_explicit_inject_precedence_over_container_defaults():
    # Container has default SystemA binding
    injector.bind(TicketSystemService, to=SystemA())
    
    # Pipe explicitly requests SystemB
    pipe_config = TestPipeConfig(
        injects={"ticket_system": "system_b"}
    )
    
    # Pipe receives SystemB (explicit inject wins)
    assert pipe.ticket_system.name == "SystemB"
```

### Test 2: Container Defaults

```python
def test_no_explicit_inject_uses_container_defaults():
    # Container has default SystemA binding
    injector.bind(TicketSystemService, to=SystemA())
    
    # Pipe has no explicit injects
    pipe_config = TestPipeConfig()
    
    # Pipe receives SystemA (container default)
    assert pipe.ticket_system.name == "SystemA"
```

## Migration Guide

### For Existing Code

No changes needed! The refactoring is backward compatible. All existing pipes and services continue to work.

### For New Code

To leverage explicit inject precedence:

1. Define multiple service implementations in your config
2. Use the `injects` field in pipe configs to explicitly choose which service to use
3. The injector will automatically resolve the correct instance

## Benefits

1. **Explicit Control**: Pipes can explicitly choose which service implementation to use
2. **Multiple Implementations**: Support multiple implementations of the same interface
3. **Better Testing**: Easier to mock dependencies by using explicit injects
4. **Loose Coupling**: Services are injected, not manually constructed
5. **Type Safety**: Using `get_type_hints()` ensures proper type resolution

## Future Enhancements

Potential improvements:

1. Support for provider patterns for complex object graphs
2. Scope management for different lifecycle requirements
3. Lazy initialization of expensive dependencies
4. Circular dependency detection and resolution

## References

- [Injector Documentation](https://injector.readthedocs.io/en/latest/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Dependency Injection Patterns](https://martinfowler.com/articles/injection.html)
