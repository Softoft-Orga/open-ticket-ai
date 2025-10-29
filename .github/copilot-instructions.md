# Agent Guidelines for Open Ticket AI

This document is **authoritative**. Follow these rules strictly when adding, moving, or generating files.

## Workspace & Repository Layout (uv)

The repo is a uv workspace with a root app and multiple packages.

```
open-ticket-ai/
├── packages/
│   ├── <package-a>/
│   │   ├── pyproject.toml
│   │   ├── src/<package_a>/...
│   │   └── tests/                 # package-local tests
│   └── <package-b>/
│       ├── pyproject.toml
│       ├── src/<package_b>/...
│       └── tests/
├── src/
│   └── open_ticket_ai/...         # root application code
├── tests/                         # workspace-level integration/e2e
├── pyproject.toml                 # root (workspace) config
```

### Absolute rules

- **Never** place tests under any `src/` path. Forbidden: `src/**/tests`, `src/**/test_*.py`.
- Unit tests live **with their package** under `packages/<name>/tests/`.
- Cross-package **integration/e2e** tests live in **root** `tests/`.
- Keep sample inputs/golden files under a sibling `data/` directory next to the tests that use them.
- Each package is an editable member of the uv workspace. Do not add ad‑hoc `PYTHONPATH` hacks.
- Python version: **3.13** only. Use modern typing (PEP 695). No inline code comments.

## Tests Layout (required)

For **each** package:

```
packages/<name>/
└── tests/
    ├── unit/            # fast, isolated
    ├── integration/     # touches I/O or package boundaries
    ├── data/            # fixtures/goldens
    └── conftest.py      # package-specific fixtures
```

At the repo root:

```
tests/
├── integration/         # spans multiple packages
├── e2e/                 # CLI/app-level
├── data/
└── conftest.py          # shared fixtures for the whole workspace
```

### Naming rules

- Test files: `test_*.py` only.
- Keep fixtures in `conftest.py` or `tests/**/fixtures_*.py` (no global helper modules under `src/`).
- **NO** `__init__.py` files in test directories. Test directories are not Python packages.

### Fixture guidelines

- Check existing fixtures before creating new ones: `uv run -m pytest --fixtures`
- Follow naming conventions: `mock_*`, `sample_*`, `tmp_*`, `empty_*`, `*_factory`
- Document fixtures with clear docstrings
- See [FIXTURE_TEMPLATES.md](./docs/FIXTURE_TEMPLATES.md) for common patterns

## Pytest configuration (root `pyproject.toml`)

```toml
[tool.pytest.ini_options]
python_files = "test_*.py"
testpaths = [
    "tests",
    "packages/*/tests"
]
addopts = ["-q"]
```

## How to run

- From repo root:
    - `uv sync`
    - `uv run -m pytest` (all tests)
    - `uv run -m pytest packages/<name>/tests` (single package)
- uv workspaces install members in editable mode; imports resolve without extra config.

## CI / Quality gates

- Lint: `uv run ruff check .` (no warnings allowed)
- Types: `uv run mypy .` (no ignores added without justification in PR)
- Tests: `uv run -m pytest`
- Test structure: `uv run python scripts/validate_test_structure.py`
- No test files under `src/**` will be accepted. PRs that create them must be changed.

## Architectural expectations (short)

- Prefer composition and DI (Injector) over inheritance.
- Pydantic v2 for data models; explicit type annotations everywhere.
- No monkey patching; avoid reflection “magic.”
- Documentation in Markdown (VitePress), not as docstrings or comments in code.

---

**Checklist for contributors (must pass):**

- [ ] New unit tests added under `packages/<name>/tests`
- [ ] No files under any `src/**/tests`
- [ ] Root-level integration/e2e tests only in `tests/`
- [ ] No `__init__.py` in any test directories
- [ ] Check existing fixtures before creating new ones
- [ ] `uv run ruff check .` clean
- [ ] `uv run mypy .` clean
- [ ] `uv run -m pytest` green
