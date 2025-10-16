# Test Guidelines (AGENTS.md)

## Core

* Single source of truth for test practices in `/tests`.
* Principle: **test behavior/contracts, not implementation**.

## ⚠️ FIXTURE LOCATION POLICY — READ FIRST ⚠️

**Fixtures belong in central locations for reuse. Creating fixtures in test files is FORBIDDEN except in rare cases.**

### Mandatory rules

* **ALL** fixtures **MUST** live in one of these locations:
    * `tests/fixtures/<domain>.py` (e.g., `fixtures/pipes.py`, `fixtures/io.py`, `fixtures/models.py`)
    * `tests/conftest.py` (for workspace-wide fixtures)
    * `packages/<name>/tests/conftest.py` (for package-specific fixtures)

* **Test files (`test_*.py`) MAY NOT define `@pytest.fixture`** except:
    * True one-off fixture used **only once** in that single test file **AND**
    * Cannot reasonably be generalized **AND**
    * Must be documented with a comment explaining why it cannot be centralized

* **BEFORE creating ANY fixture:**
    1. **Check existing fixtures**: `uv run -m pytest --fixtures`
    2. **Search** `tests/fixtures/` directory
    3. **Reuse or extend** existing fixtures
    4. **Only then** consider creating a new centralized fixture

### Inline mocks vs. fixtures

* Inline mocks allowed **ONLY IF**:
    * Single-use **AND**
    * ≤5 lines **AND**
    * Genuinely test-specific (e.g., `Mock(return_value=42)`)

* Otherwise → create a shared Fake/Factory in `tests/fixtures/<domain>.py`

### Naming conventions (strictly enforced)

* `sample_*` — sample data/inputs
* `fake_*` — Fake implementations (test doubles)
* `mock_*` — Mock objects (thin wrappers)
* `*_factory` — Factory functions/classes for building test objects
* `tmp_*` — temporary resources (files, dirs)
* `empty_*` — empty/minimal instances

### Code review enforcement

* **PRs with fixtures in test files will be REJECTED** unless exceptional justification is provided
* **PRs with duplicate fixtures will be REJECTED** — must consolidate to `tests/fixtures/`
* All new fixtures must be documented with clear docstrings

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
* **Fixtures centralized in `tests/fixtures/` or `conftest.py` — NOT in test files**
* Fixtures over ad-hoc monkeypatch; parametrization used.
* No excessive assertions; tests independent and well-named.
* `uv run ruff check . --fix` passes
* `uv run mypy .` passes
* `uv run -m pytest` passes

---

## Workflow for creating/using fixtures

### Every time you need test data or mocks:

1. **STOP** — Do NOT create a fixture in your test file
2. **CHECK** existing fixtures: `uv run -m pytest --fixtures`
3. **SEARCH** `tests/fixtures/` directory for similar fixtures
4. **REUSE** if one exists, or **EXTEND** it if close enough
5. **CREATE centrally** if truly new:

- Add to `tests/fixtures/<domain>.py` (choose appropriate domain)
- Import and re-export in `tests/conftest.py` if workspace-wide
- Or add to `packages/<name>/tests/conftest.py` if package-specific

6. **DOCUMENT** with clear docstring explaining purpose and usage
7. **IMPORT** and use in your test file

### When you can define a fixture in a test file (RARE):

- The fixture is **genuinely one-off** (used once, in one test, in one file)
- It **cannot be generalized** (highly test-specific logic)
- You **must document** with a comment: `# One-off fixture: <reason it cannot be centralized>`
- Expect scrutiny in code review

### Red flags (will fail review):

❌ Multiple test files using similar fixtures  
❌ Fixtures defined in `test_*.py` files without justification  
❌ Copy-pasted fixture code across tests  
❌ Fixtures that could be generalized but aren't  
❌ No docstrings on centralized fixtures  
❌ Not checking existing fixtures before creating new ones
