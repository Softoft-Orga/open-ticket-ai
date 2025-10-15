# Test Guidelines (AGENTS.md)

## Core

* Single source of truth for test practices in `/tests`.
* Principle: **test behavior/contracts, not implementation**.

## What to test

* Every **public** function/method gets tests.
* Count by complexity:

    * **Simple**: 1–2 tests
    * **Medium**: 2–3 tests
    * **Complex**: 3–5 tests
* Use `@pytest.mark.parametrize` to compress similar cases.
* Integration tests verify components working together; mark with `@pytest.mark.integration`.

## What **not** to test

* Files/classes ending with `*_model.py` and static `BaseModel`s (unless custom validators/logic).
* Private/protected members (`_name`, `__private`), trivial getters/setters, pass-throughs, over-asserting every field.

## Structure

```
tests/
  unit/
  integration/
  e2e/
  data/
  conftest.py
```

* Test files named `test_*.py` (not `*_test.py`).
* No `__init__.py` under `tests/`.
* No tests under `src/`.

## Patterns & guidelines

* Clear **Arrange–Act–Assert**; explicit error tests with `pytest.raises`.
* Prefer **fixtures** (shared in `conftest.py`) for DI/mocking; avoid ad-hoc `monkeypatch` unless needed.
* Fixture naming: `mock_*`, `sample_*`, `*_factory`, etc.
  List available fixtures: `uv run -m pytest --fixtures`.
* Keep tests **independent** and **deterministic** (seed/time control); avoid flaky/time-dependent checks.
* Consolidate edge cases via **parametrization**; avoid over-specific cases.

### Error & exception assertions

* Assert **exception type** (and stable code/enum if available), **not** exact messages.
* If a pattern is unavoidable, use a **coarse regex** (category words), never full sentences.

## Integration specifics

* Use real components where feasible (test env/data); assert meaningful outcomes.
* Mark with `@pytest.mark.integration`.

## Omission docs

* If skipping something (e.g., plain Pydantic `.dict()`), document why in comments/PR, referencing **AGENTS.md**.

## Commands

* Run all: `uv run -m pytest`
* Coverage: `uv run -m pytest --cov=open_ticket_ai --cov-report=html`
* Selective: files/tests/marks supported (`-m integration`, `-x`, `-v`, `-l`)

## Quality checklist (must pass)

* Public APIs covered; models/private not tested (unless custom logic).
* Fixtures over ad-hoc monkeypatch; parametrization used.
* No excessive assertions; tests independent and well-named.
* `uv run ruff check . --fix` passes
* `uv run mypy .` passes
* `uv run -m pytest` passes

---

## Fixture & Mock Location Policy

* Reusable fixtures and mocks **must** live centrally:

    * `tests/fixtures/` (group by domain, e.g. `fixtures/pipes.py`, `fixtures/io.py`)
    * Re-export in `tests/conftest.py` for global availability.
* Test files **may not** define `@pytest.fixture` unless it’s a true one-off used only in that file.
* Inline mocks allowed only if **single-use** and **≤5 lines**; otherwise create a shared Fake/Factory in
  `tests/fixtures/` and import it.
* Before adding anything new, **list existing fixtures** and reuse: `uv run -m pytest --fixtures`.
* Naming: `sample_*` (data), `fake_*` (Fakes), `mock_*` (thin mocks), `*_factory` (builders).
* PRs with duplicated fixtures/mocks in test files will be rejected; move them to `tests/fixtures/` and wire via
  `conftest.py`.

## Required workflow for new fixtures/mocks

1. Search existing fixtures (`uv run -m pytest --fixtures`) and the `tests/fixtures/` folder.
2. If reusable → add/update in `tests/fixtures/<area>.py`, import in `tests/conftest.py`.
3. Reference the centralized fixture in tests; remove duplicates.
4. Note additions in PR description under **“Shared fixtures updated”**.
