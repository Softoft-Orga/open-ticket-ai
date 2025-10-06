# GitHub Copilot Instructions for Open Ticket AI

This document provides guidance for GitHub Copilot when working with the Open Ticket AI repository.

## Repository Overview

Open Ticket AI is a Python 3.13 ticket automation system using:
- **uv** for workspace and dependency management
- **Pydantic v2** for configuration and data validation
- **Dependency Injection** for component wiring
- **VitePress** for documentation

## Critical Rules

### Test File Placement (MANDATORY)

**NEVER** place test files under any `src/` path. This is strictly forbidden:
- ❌ `src/**/tests/`
- ❌ `src/**/test_*.py`

**Correct test locations:**
- ✅ Unit tests: `packages/<name>/tests/unit/`
- ✅ Integration tests: `packages/<name>/tests/integration/`
- ✅ E2E tests: `tests/e2e/`
- ✅ Cross-package integration: `tests/integration/`

### Python Standards

- **Version**: Python 3.13 only
- **Typing**: Use modern type annotations (PEP 695); all functions must be typed
- **Comments**: No inline code comments (document in Markdown instead)
- **Imports**: Absolute imports, alphabetically sorted within groups
- **Models**: Pydantic v2 for all data structures

## Workspace Structure

This is a uv workspace with multiple packages:

```
open-ticket-ai/
├── src/
│   └── open_ticket_ai/        # Root application
│       ├── core/              # Infrastructure (config, DI, pipeline)
│       ├── base/              # Reusable pipes and base classes
│       └── extras/            # Additional components
├── packages/
│   ├── <package-name>/        # Independent packages
│   │   ├── pyproject.toml
│   │   ├── src/<package>/
│   │   └── tests/             # Package-specific tests
├── tests/                     # Workspace-level integration/e2e
├── docs/                      # Documentation
└── pyproject.toml             # Workspace configuration
```

## Development Commands

From repository root:
```bash
# Install dependencies
uv sync

# Run all tests
uv run -m pytest

# Run specific package tests
uv run -m pytest packages/<name>/tests

# Lint
uv run ruff check .

# Type check
uv run mypy .
```

## Quality Gates (Must Pass)

All PRs must pass:
- ✅ `uv run ruff check .` - No warnings allowed
- ✅ `uv run mypy .` - No type errors (no ignores without justification)
- ✅ `uv run -m pytest` - All tests passing
- ✅ No test files under `src/**`

## Code Organization

### Core Module (`src/open_ticket_ai/core/`)

Infrastructure components:
- `config/` - Configuration schemas using Pydantic
- `dependency_injection/` - DI container and registry
- `pipeline/` - Pipeline orchestration
- `plugins/` - Plugin system
- `template_rendering/` - Jinja2 templates
- `ticket_system_integration/` - Ticket system adapters

### Base Module (`src/open_ticket_ai/base/`)

Reusable components:
- Abstract base classes for pipes
- Common ticket system operations
- Mixins for orthogonal functionality

### Configuration

- All configuration in YAML, validated by Pydantic models
- Flow: YAML → `RawOpenTicketAIConfig` → validated models → runtime
- Document config options in VitePress docs, not code comments

### Dependency Injection

- Use `@inject` decorator for constructor injection
- Services registered as singletons
- Services must be stateless or thread-safe
- Register in `create_registry.py`

## Architectural Patterns

- **Composition over inheritance**: Prefer DI and composition
- **No monkey patching**: Avoid runtime modifications
- **No reflection magic**: Explicit over implicit
- **Early returns**: Reduce nesting in functions
- **Specific exceptions**: Raise actionable errors with context

## Testing Patterns

### Unit Tests
- Fast, isolated, no I/O
- Location: `packages/<name>/tests/unit/`
- Mock external dependencies

### Integration Tests
- Test package boundaries and I/O
- Location: `packages/<name>/tests/integration/` or `tests/integration/`
- May use test databases or APIs

### E2E Tests
- Full application workflows
- Location: `tests/e2e/`
- Test CLI and orchestrator

### Test Data
- Keep fixtures and golden files in `tests/data/` or `packages/<name>/tests/data/`
- Use `conftest.py` for shared fixtures

## Documentation

- **User docs**: `/docs/raw_en_docs/` (English source)
- **VitePress site**: `/docs/vitepress_docs/` (DO NOT modify during general doc work)
- **Diagrams**: `/docs/diagrams/` (PlantUML and Markdown)
- **Config examples**: `/docs/raw_en_docs/config_examples/`
- **Naming**: UPPERCASE for major docs (README.md), lowercase_underscore for guides

## Context-Specific Instructions

For detailed guidelines in specific areas, refer to:
- General source code: `src/AGENTS.md`
- Core infrastructure: `src/open_ticket_ai/core/AGENTS.md`
- Base components: `src/open_ticket_ai/base/AGENTS.md`
- Config examples: `docs/raw_en_docs/config_examples/AGENTS.md`

## Common Pitfalls to Avoid

1. ❌ Adding tests under `src/**` directories
2. ❌ Using `PYTHONPATH` hacks instead of uv workspace
3. ❌ Adding inline code comments instead of Markdown docs
4. ❌ Using Python < 3.13 or old-style type hints
5. ❌ Catching broad exceptions without re-raising
6. ❌ Creating deep inheritance hierarchies
7. ❌ Ignoring mypy/ruff errors without justification

## Contribution Checklist

Before submitting:
- [ ] New unit tests added under `packages/<name>/tests`
- [ ] No files under any `src/**/tests`
- [ ] Root-level integration/e2e tests only in `tests/`
- [ ] `uv run ruff check .` clean
- [ ] `uv run mypy .` clean
- [ ] `uv run -m pytest` green
- [ ] Documentation updated if needed

## Plugin Development

Plugins are separate packages that extend functionality:
- Follow same workspace rules
- Register via entry points
- Implement required interfaces
- See Plugin Developer Guide in VitePress docs

## CI/CD

GitHub Actions workflows in `.github/workflows/`:
- `python-app.yml` - Main CI (lint, type check, test)
- `qa-tests.yml` - Quality assurance
- `nightly-tests.yml` - Contract and E2E tests
- `publish-*.yml` - PyPI publishing

## Getting Help

- Architecture docs: `docs/vitepress_docs/docs_src/en/developers/architecture.md`
- Contributing guide: `docs/raw_en_docs/general/CONTRIBUTING.md`
- Testing guide: `docs/raw_en_docs/general/TESTING.md`
- Main AGENTS.md: Root `AGENTS.md` (authoritative for test placement)
