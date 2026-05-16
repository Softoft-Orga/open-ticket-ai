# Source Code Guidelines

**Location:** `/src` directory in Open Ticket AI repository  
**Parent Guidelines:** [Root AGENTS.md](../AGENTS.md)  
**Last Updated:** 2026-04-15

This document provides Python-specific guidelines for all source code in the `src/` directory.

## Critical Test Placement Rules

**NEVER place tests under `src/`:**

- Forbidden: `src/**/tests/`, `src/**/test_*.py`
- Unit tests: `tests/unit/`
- Integration/e2e tests: `tests/integration/`, `tests/e2e/`

## Architecture

The runtime is a single `open_ticket_ai` package — no plugin registry, no DI
container, no separate installable sub-packages.

- **`settings.py`** — `pydantic-settings` based, env-var driven (`OTAI_` prefix)
- **`pipeline.py`** — constructs the pipe tree using direct Python imports (legacy CLI path)
- **`main.py`** — entry point, loads settings, starts FastAPI/uvicorn server
- **`workflow_manager.py`** — manages running workflow instances as background asyncio tasks

### API layer (`api/`)

The runtime exposes a FastAPI REST API for ticket system access and workflow management:

- **`api/app.py`** — FastAPI application factory (`create_app`)
- **`api/dependencies.py`** — shared state (`AppState`), template registry, service factories
- **`api/models.py`** — request/response Pydantic models
- **`api/routers/tickets.py`** — ticket CRUD endpoints (`/api/tickets/*`)
- **`api/routers/workflows.py`** — workflow start/stop/list endpoints (`/api/workflows/*`)

Workflows are started from predefined templates with user-supplied parameters.
No complex pipeline DSL — just template name + parameter overrides.

### Core modules

- `core/pipes/` — `Pipe` base class, `PipeResult`, `PipeContext`
- `core/ticket_system_integration/` — `TicketSystemService` ABC and unified models
- `core/ai_classification_services/` — `ClassificationService` ABC and models
- `core/logging/` — `LoggerFactory` / `AppLogger` interfaces (stdlib adapter)

### Pipe implementations (`pipes/`)

- `pipes/composite_pipe.py` — `CompositePipe`
- `pipes/classification_pipe.py` — `ClassificationPipe`
- `pipes/interval_trigger_pipe.py` — `IntervalTrigger`
- `pipes/context_resolver.py` — `ContextResolver` type alias and `resolve` helper
- `pipes/orchestrators/` — `SimpleSequentialOrchestrator`
- `pipes/pipe_runners/` — `SimpleSequentialRunner`
- `pipes/ticket_system_pipes/` — `FetchTicketsPipe`, `UpdateTicketPipe`, `AddNotePipe`
- `pipes/templates/` — `classify_and_route` template

### Ticket system connectors

- `otobo_znuny/` — OTOBO/Znuny ticket system service and models
- `zammad/` — Zammad ticket system service and models

### AI classification

- `hf_local/` — HuggingFace local classification service

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
