# Source Code Guidelines

This document provides Python-specific guidelines for all source code in the `src/` directory.

## Python Standards

All code follows Python 3.13 conventions with strict type checking enabled. See `.windsurf/rules/python.md` for detailed formatting and linting rules.

## Import Organization

- Use absolute imports as the default
- Group imports: standard library, third-party, first-party
- Keep imports alphabetically sorted within groups
- Avoid star imports (`from module import *`)

## Type Annotations

Every function, method, and variable that isn't trivially inferrable must have type annotations:

```python
def process_ticket(ticket_id: int, config: TicketConfig) -> ProcessingResult:
    result: ProcessingResult = ...
    return result
```

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

## Configuration

All configuration lives in `src/open_ticket_ai/core/config/` using pydantic models. When adding settings:

1. Add fields to appropriate config model
2. Update YAML schema documentation
3. Add validation logic if needed
4. Update VitePress docs with usage examples