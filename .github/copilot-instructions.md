# Agent Guidelines for Open Ticket AI

This repository hosts **two distinct projects**:

1. The **Open Ticket Automation Python workspace** (uv-based) that powers the back-end packages.
2. The **customer-facing marketing/docs website** implemented with Astro, Vue, and Storybook under `docs/`.

These projects share a repository but evolve independently. Understand which surface you are changing before making edits and follow the rules for that surface specifically.

## Python Automation Platform (uv workspace)

### Workspace & Repository Layout

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

### Tests Layout (required)

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

### Pytest configuration (root `pyproject.toml`)

```toml
[tool.pytest.ini_options]
python_files = "test_*.py"
testpaths = [
    "tests",
    "packages/*/tests"
]
addopts = ["-q"]
```

### How to run

- From repo root:
    - `uv sync`
    - `uv run -m pytest` (all tests)
    - `uv run -m pytest packages/<name>/tests` (single package)
- uv workspaces install members in editable mode; imports resolve without extra config.

### CI / Quality gates

- Lint: `uv run ruff check .` (no warnings allowed)
- Types: `uv run mypy .` (no ignores added without justification in PR)
- Tests: `uv run -m pytest`
- Test structure: `uv run python scripts/validate_test_structure.py`
- No test files under `src/**` will be accepted. PRs that create them must be changed.

### Architectural expectations (short)

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

## Docs Website Project (Astro)

- Full marketing/docs site lives in `docs/`.
- Stack: Astro + Vite with Vue 3 islands and Storybook (`docs/.storybook`) for component review; Tailwind configured via `docs/tailwind.config.cjs`.
- Styling: use the shared tokens (`primary`, `primary-dark`, `primary-light`, `background-dark`, `surface-dark`, `surface-lighter`, `border-dark`, `text-dim`, `cyan-glow`) and gradient utilities (`bg-cyber-gradient`, `bg-glow-radial`); avoid ad-hoc hex codes. Global typography/theme is defined in `docs/src/styles/global.css` (Inter/system stack, dark background).
- Components live under `docs/src/components/vue/**` with matching stories in `docs/stories/**`. When changing components, update the Storybook stories accordingly.
- Design language mirrors `open-ticket-ai-platform-prototype`: deep purple/cyan glow, glassy layered surfaces, generous spacing, pill badges, and neon accents. Don’t copy layouts verbatim—match structure and tone.
- Workflow: run scripts from `docs/` (`npm run docs:dev`, `docs:build`, `docs:preview`, `storybook`, `build-storybook`). Use Playwright MCP to verify UI (Astro on :4321, Storybook on :6006) and prefer Storybook screenshots for regressions. Always run `npm run docs:build` before handing off.
- Prefer Tailwind utility classes over custom CSS, keep fonts consistent with global styles, and avoid merge conflicts.

### Testing Contract (Playwright)

- Avoid brittle selectors (IDs, classes, or throwaway `data-*` hooks). Use roles, accessible names, and semantic HTML.
- Keep CTA accessible names stable: "Get Demo" and "Contact Sales".
- Navbar links must expose "Home", "Products", "Services", and "Docs" accessible names.
- Ensure components use proper roles/labels so tests can rely on visible text.
- When UI copy intentionally changes, update Playwright tests and snapshots in the same PR.
- Never merge changes that break `npm run test:e2e` (run inside `docs/`).

## MCP tool usage
- context7: use for "latest / correct API usage" questions (framework/library docs).
- playwright: use to verify UI behavior in running app/storybook (navigation, forms, a11y tree checks).
- chrome_devtools: use for performance/debug inspection (network, console, layout investigation).
- serena: use for large refactors / symbol-level edits across the codebase.
- github: use only for repo/PR/issues/actions operations.
