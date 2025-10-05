# Agent Guidelines for Open Ticket AI

This document outlines core principles and expectations for contributors working on Open Ticket AI. It serves as the foundation for all development work across the repository.

## Core Philosophy

Write code that speaks for itself. Favor clarity, simplicity, and explicitness over cleverness. The goal is maintainable software that can evolve without breaking.

## Design Principles

### Object-Oriented Design
- Use OOP where it provides clear structure and encapsulation
- Apply SOLID principles consistently
- Favor composition over inheritance
- Use well-established design patterns when they fit naturally

### Dependency Injection
- Leverage dependency injection for loose coupling
- Make dependencies explicit through constructor injection
- Use the injector framework already present in the codebase
- Avoid service locator patterns

### Type Safety
- All code must use explicit type annotations
- Leverage Python 3.13 features, especially new generic syntax (PEP 695)
- Use pydantic BaseModels for structured data validation
- Prefer type safety over dynamic approaches

### Minimal Magic
- Avoid monkey patching entirely
- Minimize use of complex reflection patterns
- Prefer direct attribute access over getattr/setattr unless absolutely required
- When dynamic access is necessary, use typing.cast for type safety
- Decorators are acceptable where they improve readability and reusability

## Code Quality Standards

### Comments and Documentation
- Comments should be minimal and only used when code cannot clearly express intent
- Do not add docstrings to source files
- Documentation belongs in VitePress markdown files, not in code
- Write self-explanatory code with clear naming instead of relying on comments

### Testing Philosophy
- Test core principles and behaviors, not implementation details
- Write tests that are robust against minor code changes
- Avoid brittle tests that break with every refactor
- Never use monkey patching in tests unless absolutely unavoidable
- Prefer testing contracts and interfaces over internal state

### Modern Python Features
- Target Python 3.13 exclusively
- Use new generic syntax: `type Point[T] = tuple[T, T]`
- Apply type parameter syntax for classes and functions
- Leverage pattern matching where it improves clarity
- Use structural pattern matching (match/case) for complex conditionals

## Repository Standards

Each subdirectory may have its own AGENTS.md with domain-specific guidance. Those files add detail without repeating what is stated here. Always consult both this root file and any subdirectory AGENTS.md when working in that area.

For Python-specific conventions (formatting, linting, imports), see `.windsurf/rules/python.md`.

For testing structure and standards, see `docs/raw_en_docs/CONTRIBUTING.md`.

For plugin development, see `PLUGIN_STANDARDS.md`.

## Expectations

- Read and understand existing code patterns before adding new code
- Keep changes minimal and focused
- Verify your code with ruff, mypy, and pytest before committing
- Update VitePress documentation when adding user-facing features
- Follow established module boundaries and architecture patterns
