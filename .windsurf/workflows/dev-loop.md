---
description: >-
  Quick checklist for making code changes: environment setup, linting, typing, and tests using uv.
---

# /dev-loop

1. Ensure dependencies are installed: `uv sync --all-extras` (runs in the project root).
2. Make your code changes following `.windsurf/rules/` guidance.
3. Format and lint:
   - `uv run ruff format .`
   - `uv run ruff check .`
4. Type-check the project: `uv run mypy .`
5. Run the tests:
   - Main suite: `uv run pytest`
   - Classification API tests (if relevant): `uv run pytest classification_api_tests`
6. Update docs or configuration examples in `docs/` when behaviour changes.
7. Summarise results in the PR message, including commands run.
