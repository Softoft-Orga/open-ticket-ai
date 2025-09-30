---
description: |-
   One-shot hygiene workflow to make the repo pass formatting, linting, and type checks. Uses `uv` to run Ruff/MyPy,
   applies safe autofixes (`--fix`), then iterates on remaining issues with multi-file edits.
   Enforces project rules (Py 3.13, double quotes, modern typing).
---

# /fix-ruff-mypy

Refactor the repo to pass Ruff and MyPy.

1. List current lint and type errors:
    - Run: `uv run ruff format --check . && uv run ruff check .`
    - Run: `uv run mypy .`
2. Autofix what can be fixed safely:
    - Run: `uv run ruff format .`
    - Run: `uv run ruff check --fix .`
3. For EACH remaining error group, propose a patch and apply multi-file edits until the checks pass.
4. Keep string quotes consistent with the rules (py: double).
5. Re-run full suite:
    - Run: `uv run ruff format --check . && uv run ruff check . && uv run mypy .`
6. If types hinge on optional imports or stubs, add minimal `py.typed` or install `types-*` packages as needed and
   retry.
7. Summarize changes and remaining manual items.
