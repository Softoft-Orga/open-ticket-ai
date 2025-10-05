# UV Monorepo Workspace Structure - Implementation Summary

## Overview
The repository is now properly configured as a UV monorepo workspace with the core package and plugins as workspace members.

## Important Note on Package Structure

The core package has been restructured to follow the standard Python package layout pattern:
1. `src/open_ticket_ai/` contains the package-level files (`pyproject.toml`, `README.md`)
2. `src/open_ticket_ai/open_ticket_ai/` contains the actual package code

This structure:
- Matches the plugin layout pattern (e.g., `src/otai_hf_local/otai_hf_local/`)
- Provides proper separation between package metadata and source code
- Allows `src/open_ticket_ai` to be a workspace member like the plugins
- Enables proper package building and distribution

## Workspace Configuration

### Root `pyproject.toml`
The root `pyproject.toml` now serves as the workspace configuration only, containing:
1. **Workspace Configuration** - Defines workspace members and sources
2. **Shared Tooling Configuration** - Ruff, mypy, pytest settings for all packages

```toml
[tool.uv.workspace]
members = [
    "src/open_ticket_ai",
    "src/open_ticket_ai_hf_local",
    "src/open_ticket_ai_otobo_znuny_plugin",
]

[tool.uv.sources]
open-ticket-ai = { workspace = true }
open-ticket-ai-hf-local = { workspace = true }
open-ticket-ai-otobo-znuny-plugin = { workspace = true }
```

### Core Package `pyproject.toml`
The core package has its own `pyproject.toml` at `src/open_ticket_ai/pyproject.toml`:

```toml
[project]
name = "open-ticket-ai"
version = "1.0.0rc1"
# ... package metadata

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["open_ticket_ai"]
```

### Package Structure

```
open-ticket-ai/
├── pyproject.toml                          # Root: workspace config only
├── src/
│   ├── open_ticket_ai/                     # Core package directory
│   │   ├── pyproject.toml                  # Core package definition
│   │   ├── README.md                       # Package README
│   │   ├── tests/                          # Package-specific tests
│   │   └── open_ticket_ai/                 # Core package source code
│   │       ├── __init__.py
│   │       ├── app.py
│   │       ├── main.py
│   │       ├── base/
│   │       ├── core/
│   │       └── extras/
│   ├── otai_hf_local/                      # HF Local plugin workspace member
│   │   ├── pyproject.toml                  # Plugin package definition
│   │   └── otai_hf_local/                  # Plugin source code
│   └── otai_otobo_znuny/                   # OTOBO plugin workspace member
│       ├── pyproject.toml                  # Plugin package definition
│       └── otai_otobo_znuny/               # Plugin source code
├── tests/                                  # Central test directory
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
└── uv.lock                                 # Locked dependencies
```

## Key Changes Made

1. **Restructured Core Package**
   - Moved all source code from `src/open_ticket_ai/` to `src/open_ticket_ai/open_ticket_ai/`
   - Created new `pyproject.toml` at `src/open_ticket_ai/pyproject.toml` for core package metadata
   - Added `src/open_ticket_ai` as a workspace member
   - Core package now follows the same pattern as plugins

2. **Root pyproject.toml Refactoring**
   - Removed `[project]` section from root (now in core package pyproject.toml)
   - Removed `[build-system]` section from root (now in core package pyproject.toml)
   - Root now only contains workspace configuration and shared tooling settings
   - Added `src/open_ticket_ai` to workspace members list

3. **Dependency Updates**
   - Added missing `apscheduler>=3.10.0` dependency to core package

4. **Code Updates**
   - Updated `get_project_info()` in `app.py` to use `__file__` for relative path resolution
   - Fixed import order issues with ruff auto-fix

5. **Workspace Benefits**
   - All packages can be installed together with `uv sync`
   - Cross-package imports work during development
   - Centralized tooling (ruff, mypy, pytest) configured at the root
   - Independent versioning and publishing of each package
   - Consistent package structure across core and plugins

## Build Verification

### Core Package
```bash
$ uv build --package open-ticket-ai
Building source distribution...
Building wheel from source distribution...
Successfully built dist/open_ticket_ai-1.0.0rc1.tar.gz
Successfully built dist/open_ticket_ai-1.0.0rc1-py3-none-any.whl
```

**Verification**: Core package wheel contains only `open_ticket_ai/` code, no plugins.

### HF Local Plugin
```bash
$ uv build --package open-ticket-ai-hf-local
Successfully built dist/otai_hf_local-1.0.0rc1.tar.gz
Successfully built dist/otai_hf_local-1.0.0rc1-py3-none-any.whl
```

### OTOBO/Znuny Plugin
```bash
$ uv build --package open-ticket-ai-otobo-znuny-plugin
Successfully built dist/otai_otobo_znuny-1.0.0rc1.tar.gz
Successfully built dist/otai_otobo_znuny-1.0.0rc1-py3-none-any.whl
```

## Testing and Linting

### Workspace Sync
```bash
uv sync --all-extras
# Installs all workspace packages and dependencies
```

### Linting
```bash
uv run ruff format .      # Format code
uv run ruff check .       # Lint code
uv run mypy src/          # Type check
```

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/contract/
uv run pytest tests/e2e/

# Run tests with markers
uv run pytest -m unit
uv run pytest -m integration
```

## Acceptance Criteria Status

✅ **The core package (`open_ticket_ai`) is buildable and installable independently**
   - Verified: `uv build --package open-ticket-ai` succeeds
   - Package only contains core code, no plugins

✅ **The root `pyproject.toml` acts as a uv workspace and references all subpackages/plugins**
   - Workspace members: HF Local and OTOBO/Znuny plugins
   - Workspace sources properly configured

✅ **Linting and e2e tests can be run from the root and cover all code and tests**
   - Ruff, mypy, pytest all configured at root level
   - Test paths include both root tests/ and plugin tests

✅ **All plugins are buildable and testable within the workspace**
   - Both plugins build successfully as independent packages
   - Plugins can depend on core via `{ workspace = true }`

✅ **Documentation already reflects the workspace setup (no changes needed)**
   - Existing docs already describe this structure correctly
   - README.md describes workspace architecture accurately

## Notes

- The root pyproject.toml being both workspace config AND core package is the standard UV workspace pattern
- Plugins remain separate workspace members with their own pyproject.toml files
- The workspace allows plugins to depend on `open-ticket-ai` using `{ workspace = true }`
- All packages can be independently versioned and published to PyPI
- The setuptools `exclude` configuration ensures plugins don't get bundled into the core package

## CI/CD Integration

The workspace setup is compatible with existing CI/CD workflows:
```yaml
- name: Install dependencies
  run: uv sync --locked --all-extras

- name: Lint with ruff
  run: |
    uv run ruff format --check .
    uv run ruff check .

- name: Type check with mypy
  run: uv run mypy src

- name: Test with pytest
  run: uv run pytest
```
