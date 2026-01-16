# GitHub Copilot Instructions for Open Ticket AI

## ⚠️ Critical: Read AGENTS.md First

**BEFORE making any changes**, read the relevant AGENTS.md file(s):
- **Python changes**: `/AGENTS.md` (backend guidelines, test structure)
- **Website/docs changes**: `/docs/AGENTS.md` (Astro/Vue frontend guidelines)

These files are **authoritative** and contain repository structure, testing requirements, linting standards, and build processes.

## Repository Structure

Dual-stack project:
- **Python Backend**: uv workspace with packages in `packages/`, app code in `src/`, tests in `tests/`
- **Astro/Vue Frontend**: Website lives in `/docs` directory

## Quality Checks Before Committing

### Python Changes (outside `/docs`)

```bash
uv run ruff check .   # Lint (no warnings allowed)
uv run mypy .         # Type checking (strict)
uv run -m pytest      # Run tests
```

**Key rules**: Tests in `packages/<name>/tests/` or `tests/`, NEVER under `src/**/tests`

### Website/Docs Changes (in `/docs`)

```bash
cd /home/runner/work/open-ticket-ai/open-ticket-ai/docs
npm run format        # Format with Prettier (ALWAYS run)
npm run lint          # ESLint check
npm run test:site     # Site tests (if content/links changed)
```

**Key rules**: Always format after changes, update `COMPONENTS.md` for core Vue components

## Common Pitfalls

**Python**: ❌ Tests under `src/**/tests` ❌ Code comments ❌ Test `__init__.py` files  
**Docs**: ❌ Skip `npm run format` ❌ Custom CSS over Tailwind ❌ Outdated `COMPONENTS.md`

---

**Remember**: AGENTS.md files are your primary source of truth!
