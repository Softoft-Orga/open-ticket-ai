---
trigger: glob
description: 
globs: **/*.py
---

# Python Codebase Rules

- Python: **3.13** target.
- Strings: **double quotes**.
- Naming: Classes UpperCamelCase, functions/vars snake_case.
- **No comments in code.**
- Typing (modern):
  - Use builtins: `list`, `dict`, `set`, `tuple` (not `List`, `Dict`, …).
  - Use unions: `T | None` (not `Optional[T]`).
  - Prefer `typing.Self`, `typing.Literal`, `typing.TypedDict | dataclass` where helpful.
  - Use `@typing.override` when overriding methods.
- Imports: absolute over relative where possible.
- I/O & paths: **pathlib** over `os.*` where possible.
- Time: timezone-aware `datetime` (`from datetime import UTC`; store in UTC).
- Errors: fail fast, raise specific exceptions; keep messages actionable.
- Structure:
  - Small pure functions; early returns > nested `if`.
  - Keep modules cohesive; avoid god-objects.
- Lint/format: Ruff (line length 100), `ruff format` for formatting.
- Type-check: MyPy (strict-ish): disallow untyped defs; no implicit optional.
- Testing: **pytest**
  - Put tests in `tests/`, named `test_*.py`.
  - Use fixtures, `pytest.mark.parametrize`, and tmp_path for FS.
  - Prefer assert style, no print.
  - Keep tests independent and fast.
- Packaging:
  - Use `pyproject.toml` for tool config.
  - Avoid runtime side-effects on import.
- Secrets/config: via env or `.env` loader; never hardcode.
- Concurrency: prefer `asyncio` for I/O-bound work; keep boundaries clear.
- Patterns: use structural pattern matching where it improves clarity.
