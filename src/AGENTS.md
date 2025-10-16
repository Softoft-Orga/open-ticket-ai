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
- Prefer context managers for resource handling

## Logging

Never directly use the logging libary! Instead get the loggingfactory by gettin it injected throug the constructor of
your class.

## Error Handling

- Raise specific exception types with actionable messages
- Don't catch broad exceptions

## Documentation

- All documentation lives in `/docs` directory, not in code comments
- See [docs/AGENTS.md](../docs/AGENTS.md) for documentation structure