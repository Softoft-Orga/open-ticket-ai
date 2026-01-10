# Agent Guidelines for Open Ticket AI

This repository hosts **two distinct projects**:

1. The **Open Ticket Automation Python workspace** (uv-based) that powers the back-end packages.
2. The **customer-facing marketing/docs website** implemented with Astro, Vue, and Storybook under
   `docs/`.

These projects share a repository but evolve independently. Understand which surface you are
changing before making edits and follow the rules for that surface specifically.

## Python Automation Platform (uv workspace)

### Development Standards & Layout
- **Workspace Layout**: The repo is a uv workspace with a root app and multiple packages under `packages/`.
- **Naming Rules**: Test files must be `test_*.py` only. Fixtures in `conftest.py` or `tests/**/fixtures_*.py`. **NO** `__init__.py` in test directories.
- **Python Version**: **3.13** only. Use modern typing (PEP 695).
- **Absolute Rules**: Never place tests under `src/`. No ad-hoc `PYTHONPATH` hacks. No inline code comments.
- **Architecture**: Prefer composition/DI (Injector) over inheritance. Pydantic v2 for data models. No monkey patching or reflection "magic." Documentation in Markdown (VitePress).

### Test Architecture
- **Tests Layout (required)**:
    - **Per Package**: `packages/<name>/tests/` (unit/, integration/, data/, conftest.py).
    - **Root Integration**: `tests/` (integration/, e2e/, data/, conftest.py) for cross-package tests.
- **Fixture Guidelines**: Check `uv run -m pytest --fixtures` before creating. Format: `mock_*`, `sample_*`, `tmp_*`, `empty_*`, `*_factory`.
- **Sample Data**: Keep inputs/goldens in `data/` sibling directories to tests.
- **Pytest Configuration**: Defined in root `pyproject.toml`.

### Quality & Workflow
- **CI / Quality Gates**:
    - Lint: `uv run ruff check .` (zero warnings).
    - Types: `uv run mypy .` (no justified ignores).
    - Structure: `uv run python scripts/validate_test_structure.py`.
- **How to Run**:
    - `uv sync`
    - `uv run -m pytest` (all tests)
    - `uv run -m pytest packages/<name>/tests` (single package)

### Contributor Checklist (Must Pass)
- [ ] New unit tests in `packages/<name>/tests`
- [ ] No files in `src/**/tests`
- [ ] Root-level integration/e2e only in `tests/`
- [ ] No `__init__.py` in test directories
- [ ] `uv run ruff check .` clean
- [ ] `uv run mypy .` clean
- [ ] `uv run -m pytest` green

## Docs Website Project (Astro)

### Tech Stack & Styling
- **Stack**: Astro + Vite with Vue 3 islands. Storybook (`docs/.storybook`) for components.
- **Styling**: Tailwind CSS (`docs/tailwind.config.cjs`).
- **Design System**: Use theme tokens (`primary`, `primary-dark`, etc.) and gradient utilities (`bg-cyber-gradient`). Avoid ad-hoc hex codes. Global typography in `docs/src/styles/global.css`.
- **Theme**: Deep purple/cyan glow, glassy surfaces, neon accents (mirrors `open-ticket-ai-platform-prototype`).

### Component Guidelines
- **Location**: Components in `docs/src/components/vue/**`. Stories in `docs/stories/**`.
- **Reusable First**: Always prefer existing components. Check `docs/storybook-static/index.json` before creating new ones.
- **Storybook**: Update stories when changing components.

### Development Workflow
- **Working Directory**: All commands run from `docs/`.
- **Scripts**:
    - `npm run docs:dev`: Local development.
    - `npm run docs:build`: Production build (run before handoff).
    - `npm run storybook`: Component development.
- **Accessing Storybook**:
    - Locally: Run `npm run storybook` and navigate to `http://localhost:6006`.
    - Online: [https://open-ticket-ai-storybook.netlify.app/](https://open-ticket-ai-storybook.netlify.app/)
- **Verification**: Use Playwright MCP for UI, Chrome DevTools for debugging.


### Tooling Usage (MCP)
- **context7**: API usage questions.
- **playwright**: verify UI/navigation/a11y in running app.
- **chrome_devtools**: performance/debug inspection.
- **serena**: large refactors/symbol edits.
- **github**: repo/PR/issue operations.

After completing a task, output all MCP Servers used;

### Updating AGENTS.md ans copilot-instructions.md
- When important changes have taken place or information in AGENTS.md files or copilot-instructions.md
  files is out of date, please update those files to reflect the current state of the repository.
- Keep the Files small and focused on the most important information for contributors and agents.
