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
- **Documentation**: 
  - Quick reference: `docs/COMPONENTS.md` lists all components with brief descriptions
  - Detailed usage: Storybook stories in `docs/stories/**/*.stories.ts`
- **Reusable First**: Always prefer existing components. Check `docs/COMPONENTS.md` or Storybook before creating new ones.
- **Storybook**: Update stories when changing components.
- **Design-system tokens**: Use shared types from `docs/src/components/vue/core/design-system/tokens.ts`:
  - `Variant`, `Size`, `Tone` types for consistent component props
  - Export arrays (`VARIANTS`, `SIZES`, `TONES`) for Storybook controls
  - Badge uses combined types: `'primary' | 'secondary' | Tone`

### Transitions (Animation System)
- **Location**: `docs/src/components/vue/core/transitions/`
- **When to Use Transitions**:
  - **Required for**: Dialog/Modal, Menu, Popover, Dropdown, Toast, Slide-over panels
  - **Optional for**: Accordion (collapse is tricky; prefer no animation unless needed)
- **Choosing the Right Transition**:
  - **Default choice**: `UiTransitionFadeScale` with `strength='sm'` for panels/dialogs
  - **Backdrops/overlays**: `UiTransitionFade`
  - **Dropdown menus**: `UiTransitionSlide` with `direction='down'`
  - **Slide-over panels**: `UiTransitionSlide` with `direction='left'` or `'right'`
  - **Toasts/notifications**: `UiTransitionSlide` with `direction='up'`
- **Usage with Headless UI**:
  ```vue
  <TransitionRoot :show="isOpen" as="template">
    <!-- Backdrop -->
    <UiTransitionFade>
      <div class="fixed inset-0 bg-black/80" />
    </UiTransitionFade>
    
    <!-- Panel -->
    <UiTransitionFadeScale strength="sm">
      <DialogPanel>...</DialogPanel>
    </UiTransitionFadeScale>
  </TransitionRoot>
  ```
- **Reduced Motion**: All presets include `motion-reduce` support. Never remove these classes.
- **Direct Preset Usage**: Import presets from `presets.ts` and use with `v-bind` for custom needs:
  ```vue
  <TransitionChild v-bind="fadeScaleSm" as="template">
  ```
- **Do NOT Duplicate**: Always reuse presets/wrappers. Never hand-write transition class strings in components.

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

### Content Collections (Astro 5)
- **Definition**: All collections defined in `docs/src/content/config.ts`
- **Documentation**: See `docs/CONTENT_COLLECTIONS.md` for complete reference
- **Collections**:
  - `docs` - Documentation pages (MD/MDX in `docs/src/content/docs/`)
  - `blog` - Blog articles (MD/MDX in `docs/src/content/blog/`)
  - `products` - Product listings (YAML in `docs/src/content/products.yaml`)
  - `services` - Service offerings (YAML in `docs/src/content/services.yaml`)
- **Usage**: Pages use `getCollection('name')` to fetch entries
- **Routing**: 
  - Docs: `docs/src/pages/docs/[...slug].astro`
  - Blog: `docs/src/pages/blog/[...slug].astro`
  - Products: `docs/src/pages/products.astro`
  - Services: `docs/src/pages/services.astro`


### Tooling Usage (MCP)
- **context7**: API usage questions.
- **playwright**: verify UI/navigation/a11y in running app.
- **chrome_devtools**: performance/debug inspection.
- **serena**: large refactors/symbol edits.
- **github**: repo/PR/issue operations.

After completing a task, output all MCP Servers used;

### Documentation Update Rules

**ALWAYS** update documentation when making these changes:

#### When changing Vue components (`docs/src/components/vue/**`)
- [ ] Update `docs/COMPONENTS.md` with new component entry (name, description, props, slots)
- [ ] Create or update Storybook story in `docs/stories/**/*.stories.ts`
- [ ] Follow naming convention: `{ComponentName}.stories.ts`
- [ ] Verify component renders correctly in Storybook

#### When changing content collections (`docs/src/content/**` or `docs/src/content/config.ts`)
- [ ] Update `docs/CONTENT_COLLECTIONS.md` if schemas, fields, or conventions change
- [ ] Document all required frontmatter fields
- [ ] Test pages using `getCollection()` still work
- [ ] Run `npm run docs:build` to verify no errors

#### Quick validation checklist
Before finalizing changes:
- Components: `COMPONENTS.md` updated + Storybook story exists + renders correctly
- Collections: `CONTENT_COLLECTIONS.md` accurate + schema valid + pages render
- Build: `npm run docs:build` succeeds without errors

### Updating AGENTS.md and copilot-instructions.md
- When important changes have taken place or information in AGENTS.md files or copilot-instructions.md
  files is out of date, please update those files to reflect the current state of the repository.
- Keep the Files small and focused on the most important information for contributors and agents.
