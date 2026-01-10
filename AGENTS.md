# Agent Guidelines for Open Ticket AI

This document is **authoritative**. Follow these rules strictly when adding, moving, or generating files.

> **Important:** The Astro/Vue website and all docs live under the `/docs` directory. Any instructions mentioning "website", "docs", Astro, or Vue components refer to files inside `docs/`.

The Astro Website is in the /docs directory!
So when I am refering to a website Astro or Vue Components to change or Pages to change.
I am speaking about the content in the /docs folder!

## Information on Python Open Ticket Automation Platform (NOT FOR WEBSITE)
### Workspace & Repository Layout (uv)

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

#### Absolute rules

- **Never** place tests under any `src/` path. Forbidden: `src/**/tests`, `src/**/test_*.py`.
- Unit tests of plugins live **with their package** under `packages/<name>/tests/` Unit Tests of the core in
  /tests/unit/.
- Cross-package **integration,e2e** tests live in **root** `tests/`.
- Keep sample inputs/golden files under a sibling `data/` directory next to the tests that use them.
- Each package is an editable member of the uv workspace. Do not add ad‑hoc `PYTHONPATH` hacks.
- Python version: **3.13** only. Use modern typing (PEP 695). No code comments.

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
    unit/
├── integration/         # spans multiple packages
├── e2e/                 # CLI/app-level
├── data/
└── conftest.py          # shared fixtures for the whole workspace
```

#### Naming rules

- Test files: `test_*.py` only.
- Keep fixtures in `conftest.py` or `tests/**/fixtures_*.py` (no global helper modules under `src/`).
- **NO** `__init__.py` files in test directories. Test directories are not Python packages.

#### Fixture guidelines

- Check existing fixtures before creating new ones: `uv run -m pytest --fixtures`
- Follow naming conventions: `mock_*`, `sample_*`, `tmp_*`, `empty_*`, `*_factory`

### Pytest configuration (root `pyproject.toml`)

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
- No test files under `src/**` will be accepted. PRs that create them must be changed.

#### Copilot PR Automation

The `.github/workflows/copilot-pr-retry.yml` workflow automatically handles PRs created by `github-copilot[bot]`. When checks fail, it labels the PR with `retry-needed` and `copilot-pr`, comments with failure details, and closes the PR to enable retry. This only affects Copilot bot PRs.

### Architectural expectations (short)

- Prefer composition and DI (Injector) over inheritance.
- Pydantic v2 for data models; explicit type annotations everywhere.
- No monkey patching; avoid reflection “magic.”
- Documentation in Markdown (VitePress), not as docstrings or comments in code.

### Documentation Structure

All documentation lives in `/docs` directory.

## Website/Docs Component System (Astro + Vue)

The customer-facing website lives in `/docs` and uses:
- **Astro** for static site generation
- **Vue 3** for interactive components
- **Storybook** for component development
- **Tailwind CSS** with custom design tokens

### Transition System

**Location**: `docs/src/components/vue/core/transitions/`

**When to Use**:
- Dialog/Modal, Menu, Popover, Dropdown, Toast, Slide-over panels (required)
- Accordion (optional; collapse is tricky, prefer no animation unless needed)

**Choosing Transitions**:
- **Default**: `UiTransitionFadeScale` with `strength='sm'` for panels/dialogs
- **Backdrops**: `UiTransitionFade`
- **Menus**: `UiTransitionSlide direction='down'`
- **Slide-overs**: `UiTransitionSlide direction='left'` or `'right'`
- **Toasts**: `UiTransitionSlide direction='up'`

**Usage Example**:
```vue
<TransitionRoot :show="isOpen" as="template">
  <UiTransitionFade>
    <div class="fixed inset-0 bg-black/80" />
  </UiTransitionFade>
  <UiTransitionFadeScale strength="sm">
    <DialogPanel>...</DialogPanel>
  </UiTransitionFadeScale>
</TransitionRoot>
```

**Rules**:
- All presets include `motion-reduce` support; never remove these classes
- Always reuse presets/wrappers; never hand-write transition strings
- For custom needs, import presets: `import { fadeScaleSm } from './presets'` and use with `v-bind`

---

## Checklist for contributors (must pass) (When making Python changes, NOT website changes)

- [ ] New unit tests added under `packages/<name>/tests` or `tests/unit/`
- [ ] No files under any `src/**/tests`
- [ ] Root-level integration/e2e tests only in `tests/`
- [ ] No `__init__.py` in any test directories
- [ ] Check existing fixtures before creating new ones
- [ ] `uv run ruff check .` clean
- [ ] `uv run mypy .` clean
- [ ] `uv run -m pytest` green
