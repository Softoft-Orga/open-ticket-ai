# Source Code Guidelines

This document provides Python-specific guidelines for all source code in the `src/` directory.

## Critical Rules

- **NEVER** place tests under `src/` - this is strictly forbidden by [root AGENTS.md](../AGENTS.md)
- Tests for core modules live in `/tests/unit/` at the repository root
- See [root AGENTS.md](../AGENTS.md) for complete test structure rules

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

## Documentation

- All user-facing documentation lives in `docs/vitepress_docs/docs_src/en/` (VitePress)
- See [docs/AGENTS.md](../docs/AGENTS.md) for documentation structure and guidelines
- Do NOT write documentation as code comments or docstrings
- Code should be self-documenting through clear naming and structure