# Source Code Guidelines

**Location:** `/src` directory in Open Ticket AI repository  
**Parent Guidelines:** [Root AGENTS.md](../AGENTS.md)  
**Last Updated:** 2025-10-11

This document provides Python-specific guidelines for all source code in the `src/` directory.

## Critical Test Placement Rules

⚠️ **NEVER place tests under `src/`:**

- ❌ Forbidden: `src/**/tests/`, `src/**/test_*.py`
- ✅ Unit tests for root package: `tests/unit/`
- ✅ Package-specific tests: `packages/<name>/tests/`
- ✅ Integration/e2e tests: `tests/integration/`, `tests/e2e/`

See [Root AGENTS.md](../AGENTS.md) for complete test structure rules.

## Python Standards

All code follows Python 3.13 conventions with strict type checking enabled.

## Import Organization

- Use absolute imports as the default
- Group imports: standard library, third-party, first-party
- Keep imports alphabetically sorted within groups
- Avoid star imports (`from module import *`)

## Type Annotations

Every function, method, and variable that isn't trivially inferrable must have type annotations:

Use pydantic models for complex data structures rather than TypedDict or plain dicts.

## Module Structure

- Keep modules focused on a single responsibility
- Prefer small, pure functions with clear inputs and outputs
- Use early returns to reduce nesting
- Extract complex logic into separate functions

## Pathlib and Modern APIs

- Use `pathlib.Path` for all file system operations
- Use timezone-aware datetime with `datetime.UTC`
- Prefer context managers for resource handling

## Error Handling

- Raise specific exception types with actionable messages
- Don't catch broad exceptions unless absolutely necessary
- Provide context in exception messages to aid debugging
- Let exceptions propagate when you can't handle them meaningfully

## Pipe Implementation Pattern

When implementing custom pipes, follow this pattern for parameters:

**Pipe Class Signature:**
```python
class MyPipe(Pipe[MyParams]):
    params_class = MyParams  # Required class attribute
```

**Parameter Handling:**
- Pipes accept params as `dict[str, Any]` or typed `ParamsModel` in `__init__`
- Runtime validation converts `dict` → `ParamsModel` using `params_class.model_validate()`
- This enables Jinja2 template rendering of YAML configs before validation
- The base `Pipe` class handles conversion automatically (lines 27-30 in pipe.py)

**Example:**
```python
class MyParams(BaseModel):
    threshold: float
    model: str

class MyPipe(Pipe[MyParams]):
    params_class = MyParams
    
    def __init__(
        self,
        pipe_config: PipeConfig[MyParams],
        logger_factory: LoggerFactory,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(pipe_config, logger_factory)
        # self.params is now validated MyParams instance
```

**Why This Pattern:**
1. **Jinja2 Rendering**: YAML configs are rendered as dicts before validation
2. **YAML Flexibility**: Users write simple YAML that gets validated at runtime
3. **Type Safety**: Full Pydantic validation after template rendering
4. **Copilot Compatible**: Clear pattern for generating new pipes

## Documentation

- All documentation lives in `/docs` directory, not in code comments
- See [docs/AGENTS.md](../docs/AGENTS.md) for documentation structure
- Use VitePress documentation for user-facing content: `docs/vitepress_docs/docs_src/en/`
- Architecture diagrams go in `docs/diagrams/`