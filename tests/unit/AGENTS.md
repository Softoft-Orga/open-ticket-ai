Core

Single source of truth for test practices in /tests.

Principle: test behavior/contracts, not implementation.

What to test

Every public function/method gets tests.

Count by complexity: simple 1–2; medium 2–3; complex 3–5.

Use @pytest.mark.parametrize to compress cases.

Integration tests verify components working together; mark with @pytest.mark.integration.

What not to test

Files/classes ending with *_model.py and static BaseModels (unless custom validators/logic).

Private/protected members (_name, __private), trivial getters/setters, pass-throughs, over-asserting every field.

Structure
tests/
unit/
integration/
e2e/
data/
conftest.py

Test files named test_*.py (not *_test.py), no __init__.py under tests, no tests under src/.

Patterns & guidelines

Clear Arrange–Act–Assert examples, explicit error tests with pytest.raises.

Prefer fixtures (shared in conftest.py) for DI/mocking; avoid ad-hoc monkeypatch unless needed.

Fixture naming: mock_*, sample_*, *_factory, etc. Check available fixtures with uv run -m pytest --fixtures.

Keep tests independent, deterministic (seed/time control), no flaky/time-dependent checks.

Consolidate edge cases via parametrization; avoid over-specific cases.

Integration specifics

Use real components where feasible (test env/data), assert meaningful outcomes, mark with @pytest.mark.integration.

Omission docs

If skipping something (e.g., plain Pydantic .dict()), document why in comments/PR, referencing AGENTS.md.

Commands

Run all: uv run -m pytest

Coverage: uv run -m pytest --cov=open_ticket_ai --cov-report=html

Selective: files/tests/marks supported (-m integration, -x, -v, -l).

Quality checklist (must pass)

Public APIs covered; models/private not tested (unless custom logic).

Fixtures over ad-hoc monkeypatch; parametrization used.

No excessive assertions; tests independent and well-named.

uv run ruff check . passes

uv run mypy . passes

uv run -m pytest passes