# Test Setup Notes

## Summary of Test Infrastructure Fixes

This document describes the changes made to fix the test infrastructure issues in the Open Ticket AI repository.

## Issues Fixed

### 1. Package Test Directories Had `__init__.py` Files
**Problem**: Test directories in workspace packages (`packages/*/tests/`) contained `__init__.py` files, which caused pytest to try importing them as Python packages, leading to `ModuleNotFoundError`.

**Solution**: Removed all `__init__.py` files from test directories:
- `packages/otai_hf_local/tests/__init__.py`
- `packages/otai_otobo_znuny/tests/__init__.py`

**Rationale**: According to AGENTS.md, test directories should NOT be Python packages.

### 2. Manual sys.path Manipulation
**Problem**: `tests/unit/core/conftest.py` manually modified `sys.path` to add the parent directory.

**Solution**: Removed all sys.path manipulation code from conftest files.

**Rationale**: The uv workspace configuration installs packages in editable mode, so manual path manipulation is unnecessary and violates AGENTS.md guidelines.

### 3. Contract Test Parametrize Issue
**Problem**: The `ids=lambda x: x[0]` parameter in contract tests caused a `TypeError: 'module' object is not subscriptable` error in Python 3.13.

**Solution**: Changed to use a list comprehension: `ids=[name for name, _, _ in discover_plugins()]`

**Rationale**: Python 3.13 has stricter type checking. The ids parameter should be a list of strings, not a lambda function.

### 4. Workspace Packages Not Installed
**Problem**: Workspace member packages (`otai-hf-local` and `otai-otobo-znuny`) were not installed in editable mode, causing import errors in their tests.

**Solution**: Use `uv sync --all-packages --all-extras` instead of just `uv sync`.

**Rationale**: The `--all-packages` flag ensures all workspace members are installed in editable mode.

### 5. Incorrect Import Path in CLI
**Problem**: The CLI code in `packages/otai_otobo_znuny/src/otai_otobo_znuny/cli.py` incorrectly imported from `otai_otobo_znuny.clients.otobo_client` instead of `otobo_znuny.clients.otobo_client`.

**Solution**: Fixed the import to use the correct external dependency package.

**Rationale**: The `OTOBOZnunyClient` is provided by the external `otobo-znuny` package, not the `otai_otobo_znuny` plugin package itself.

### 6. Plugins Missing API Contract Implementation
**Problem**: Both plugins (`otai_hf_local` and `otai_otobo_znuny`) were missing the required plugin API functions (`get_metadata()`, `register_pipes()`, `register_services()`).

**Solution**: Implemented all required functions in both plugin `__init__.py` files.

**Rationale**: The contract tests verify that all plugins implement the required plugin API. This is necessary for the plugin system to work correctly.

## CI/CD Configuration

### Required Command for CI

**IMPORTANT**: CI/CD pipelines MUST use the following command to install dependencies:

```bash
uv sync --all-packages --all-extras
```

Do NOT use just `uv sync` as this will not install workspace member packages.

### Test Execution

After syncing dependencies, run tests with:

```bash
uv run -m pytest
```

This will discover and run all tests according to the configuration in `pyproject.toml`.

## Test Results

After all fixes:
- ✅ **94 tests passing**
- ⏭️ **8 tests skipped** (expected - missing optional dependencies like SpaCy)
- ❌ **0 tests failing**

## Project Structure (Compliant with AGENTS.md)

```
open-ticket-ai/
├── packages/
│   ├── otai_hf_local/
│   │   ├── src/otai_hf_local/
│   │   └── tests/              # ✅ No __init__.py
│   └── otai_otobo_znuny/
│       ├── src/otai_otobo_znuny/
│       └── tests/              # ✅ No __init__.py
├── src/open_ticket_ai/
├── tests/                      # Root-level integration/e2e tests
│   ├── contract/
│   ├── e2e/
│   ├── integration/
│   └── unit/                   # Tests for root package
└── pyproject.toml
```

## Lessons Learned

1. **Never add `__init__.py` to test directories** - They should not be Python packages
2. **Don't manipulate sys.path** - Use proper package installation instead
3. **Use workspace-aware sync commands** - `uv sync --all-packages --all-extras`
4. **Implement plugin contracts** - All plugins must implement the required API
5. **Test early and often** - Run tests frequently during development to catch issues

## References

- [AGENTS.md](./AGENTS.md) - Authoritative guidelines for the project
- [pyproject.toml](./pyproject.toml) - Pytest configuration
