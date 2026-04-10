# Source Code Guidelines

**Location:** `/src` directory in Open Ticket AI repository  
**Parent Guidelines:** [Root AGENTS.md](../AGENTS.md)  
**Last Updated:** 2026-04-10

This document provides Python-specific guidelines for all source code in the `src/` directory.

## Critical Test Placement Rules

**NEVER place tests under `src/`:**

- Forbidden: `src/**/tests/`, `src/**/test_*.py`
- Unit tests for root package: `tests/unit/`
- Package-specific tests: `packages/<name>/tests/`
- Integration/e2e tests: `tests/integration/`, `tests/e2e/`

## Architecture (Post-Simplification)

The runtime uses direct Python construction — no YAML pipeline DSL, no plugin
registry, no DI container, no Jinja template rendering.

- **`settings.py`** — `pydantic-settings` based, env-var driven (`OTAI_` prefix)
- **`pipeline.py`** — constructs the pipe tree using direct Python imports
- **`main.py`** — entry point, loads settings, creates pipeline, runs app
- **`app.py`** — `OpenTicketAIApp` wraps the orchestrator pipe

### Core modules

- `core/pipes/` — `Pipe` base class, `PipeResult`, `PipeContext`
- `core/ticket_system_integration/` — `TicketSystemService` ABC and unified models
- `core/ai_classification_services/` — `ClassificationService` ABC and models
- `core/logging/` — `LoggerFactory` / `AppLogger` interfaces (stdlib adapter)

### Package modules (under `packages/`)

- `otai_base` — Pipe implementations: `CompositePipe`, `FetchTicketsPipe`,
  `ClassificationPipe`, `UpdateTicketPipe`, `AddNotePipe`,
  `SimpleSequentialOrchestrator`, `SimpleSequentialRunner`, `IntervalTrigger`
- `otai_otobo_znuny` — OTOBO/Znuny ticket system service
- `otai_hf_local` — HuggingFace local classification service
- `otai_zammad` — Zammad ticket system service

## Python Standards

All code follows Python 3.14 conventions with strict type checking enabled.

## Import Organization

- Use absolute imports as the default
- Group imports: standard library, third-party, first-party
- Keep imports alphabetically sorted within groups

## Logging

Use `logging.getLogger(__name__)` or `logging.getLogger(self.__class__.__name__)`.
The custom `LoggerFactory` / `AppLogger` interfaces in `core/logging/` are kept for
backward compatibility but stdlib logging is preferred for new code.

## Error Handling

- Raise specific exception types with actionable messages
- Don't catch broad exceptions
