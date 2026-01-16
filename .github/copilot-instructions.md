# GitHub Copilot Instructions for Open Ticket AI

## Overview

This repository contains a dual-stack project:
- **Python Backend**: AI-powered ticket processing and automation platform (uv workspace)
- **Astro/Vue Frontend**: Customer-facing documentation and website in `/docs`

## Critical: Always Read AGENTS.md First

**BEFORE making any changes**, you MUST read the relevant AGENTS.md file(s):

1. **Root AGENTS.md** (`/AGENTS.md`): Contains Python backend guidelines, test structure, and website/docs overview
2. **Docs AGENTS.md** (`/docs/AGENTS.md`): Contains Astro/Vue frontend-specific guidelines

These files are **authoritative** and contain essential rules about:
- Repository structure and conventions
- Testing requirements and layout
- Linting and formatting standards
- Build and deployment processes
- Component architecture and design patterns

## Repository Structure

```
open-ticket-ai/
├── packages/               # Python workspace packages
│   ├── otai_base/
│   ├── otai_hf_local/
│   ├── otai_otobo_znuny/
│   └── otai_zammad/
├── src/                    # Root Python application code
│   └── open_ticket_ai/
├── tests/                  # Workspace-level integration/e2e tests
├── docs/                   # Astro + Vue website/documentation
│   ├── src/
│   ├── public/
│   ├── stories/            # Storybook stories
│   └── package.json
├── pyproject.toml          # Root Python configuration
└── AGENTS.md               # Primary agent guidelines
```

## Python Backend: Linting, Formatting, and Testing

When working on Python code (anything outside `/docs`):

### Quality Checks (Required Before Committing)

```bash
# Lint code (no warnings allowed)
uv run ruff check .

# Type checking (strict)
uv run mypy .

# Run all tests
uv run -m pytest

# Run tests for a specific package
uv run -m pytest packages/<package-name>/tests
```

### Python-Specific Rules

- **Python version**: 3.13+ (uses modern typing PEP 695)
- **Test location**: 
  - Package unit tests: `packages/<name>/tests/`
  - Workspace integration/e2e: `tests/`
  - **NEVER** under `src/**/tests` (strictly forbidden)
- **No test `__init__.py` files**: Test directories are not Python packages
- **Check fixtures first**: Run `uv run -m pytest --fixtures` before creating new ones
- **No code comments**: Use clear, self-documenting code
- **Dependencies**: Use `uv add` to add new dependencies

## Docs/Website: Linting, Formatting, and Testing

When working in `/docs` (Astro/Vue website):

### Quality Checks (Required Before Committing)

**Navigate to `/docs` directory first:**

```bash
cd /home/runner/work/open-ticket-ai/open-ticket-ai/docs

# Format all files with Prettier (ALWAYS run after changes)
npm run format

# Verify formatting
npm run format:check

# Lint code (ESLint)
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Check for broken links
npm run lint:links

# Run site tests (broken links, localized links, locale markers)
npm run test:site

# Run Playwright crash-smoke tests
npm run test:playwright
```

### Docs-Specific Rules

- **Tech stack**: Astro 5 + Vue 3 + Tailwind CSS + Storybook
- **Components**: 
  - Core components: `docs/src/components/vue/core/**`
  - Domain components: `docs/src/components/vue/domain/**`
  - Astro components: `docs/src/components/astro/**`
- **Always format after changes**: Run `npm run format` before committing
- **Update documentation**:
  - Add/change core Vue components → Update `COMPONENTS.md` + create Storybook story
  - Modify content collections → Update `CONTENT_COLLECTIONS.md`
- **Prefer Tailwind utilities** over custom CSS
- **Image optimization**: Use `<Image>` component from `astro:assets`

## Workflow Guidelines

### Before Starting Work

1. **Read AGENTS.md** (root and/or docs, depending on your work area)
2. Check existing code patterns and conventions
3. Identify relevant lint/test commands for your work area

### During Development

1. Make minimal, focused changes
2. Run relevant linters frequently
3. Test your changes incrementally
4. For website changes: Check Storybook if modifying components

### Before Committing

#### For Python Changes:
```bash
uv run ruff check .
uv run mypy .
uv run -m pytest
```

#### For Docs/Website Changes:
```bash
cd /home/runner/work/open-ticket-ai/open-ticket-ai/docs
npm run format
npm run lint
npm run test:site  # If you modified content or links
```

## Common Pitfalls to Avoid

### Python
- ❌ Placing tests under `src/**/tests`
- ❌ Adding code comments (use self-documenting code)
- ❌ Creating `__init__.py` in test directories
- ❌ Not running `uv run ruff check .` before committing

### Docs/Website
- ❌ Forgetting to run `npm run format` after changes
- ❌ Not updating `COMPONENTS.md` when adding core Vue components
- ❌ Using custom CSS instead of Tailwind utilities
- ❌ Not checking Storybook after component changes

## Testing Philosophy

- **Python**: Unit tests in package `tests/`, integration/e2e in root `tests/`
- **Docs**: Broken link checking, locale validation, Playwright smoke tests
- **Always run tests** relevant to your changes before committing
- **No test files under `src/`** for Python code (enforced in CI)

## Getting Help

- Check `AGENTS.md` (root) for Python guidelines
- Check `docs/AGENTS.md` for website/docs guidelines  
- Check `docs/COMPONENTS.md` for component inventory
- Check `docs/CONTENT_COLLECTIONS.md` for content structure
- Review Storybook stories (`docs/stories/**/*.stories.ts`) for component usage

## CI/CD

- Python checks: ruff, mypy, pytest
- Docs checks: format (Prettier), lint (ESLint), site tests
- Copilot PR automation: Auto-retries on failure (see `.github/workflows/copilot-pr-retry.yml`)

---

**Remember**: The AGENTS.md files are your primary source of truth. Always read them before making changes!
