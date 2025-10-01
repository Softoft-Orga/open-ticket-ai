---
trigger: glob
description: Python coding conventions for Open Ticket AI.
globs: ["**/*.py"]
---

# Python Code Guidelines

- Target Python **3.13**.
- Keep string literals in **double quotes**.
- Follow `snake_case` for functions and variables, `UpperCamelCase` for classes.
- Typing:
  - Prefer standard builtins (`list`, `dict`, `set`, `tuple`).
  - Use unions with the `|` operator (`T | None`).
  - Apply `@typing.override` when overriding.
  - Lean on `TypedDict`, dataclasses, or `pydantic` models for structured data.
- Imports: prefer absolute over relative when reasonable.
- Paths and files: use `pathlib`.
- Dates: use timezone-aware `datetime` (e.g. `from datetime import UTC`).
- Errors: raise specific exceptions with actionable messages.
- Formatting & linting:
  - Use `uv run ruff format` (line length **120**).
  - Use `uv run ruff check` and `uv run mypy` (strict mode enabled via `pyproject.toml`).
- Structure: keep modules cohesive, favour small pure functions and early returns.
- Testing: write `pytest` tests under `tests/` using fixtures and parametrisation.
- Comments & docs: concise comments and module docstrings are fine when they add context.
- Configuration lives under `src/open_ticket_ai/core/config`; prefer updating models there when adding settings.
