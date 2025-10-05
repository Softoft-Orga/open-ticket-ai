# UV Monorepo Workspace Structure - Implementation Summary

## Overview
The repository is now properly configured as a UV monorepo workspace with the core package and plugins as workspace members.

## Important Note on Package Structure

The issue originally requested "a dedicated `pyproject.toml` inside `src/open_ticket_ai/`". However, after careful analysis, we determined that the proper UV workspace pattern is to have the root `pyproject.toml` serve as both:
1. The workspace configuration
2. The core package definition

This is because:
- `src/open_ticket_ai/` IS the package itself (contains `__init__.py` and package code)
- A `pyproject.toml` inside the package directory would not work with setuptools
- The UV workspace standard pattern allows the root to be both a workspace AND a package
- This matches the existing documentation which states: "Core Package (`open-ticket-ai`) - Located in root `pyproject.toml` with source code in `src/open_ticket_ai/`"

## Workspace Configuration

### Root `pyproject.toml`
The root `pyproject.toml` serves dual purposes:
1. **Workspace Configuration** - Defines workspace members and sources
2. **Core Package Definition** - Contains the `open-ticket-ai` package metadata

```toml
[tool.uv.workspace]
members = [
    "src/open_ticket_ai_hf_local",
    "src/open_ticket_ai_otobo_znuny_plugin",
]

[tool.uv.sources]
open-ticket-ai = { workspace = true }
open-ticket-ai-hf-local = { workspace = true }
open-ticket-ai-otobo-znuny-plugin = { workspace = true }

[project]
name = "open-ticket-ai"
version = "1.0.0rc1"
# ... core package metadata

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
include = ["open_ticket_ai", "open_ticket_ai.*"]
exclude = ["open_ticket_ai.tests*", "open_ticket_ai_hf_local*", "open_ticket_ai_otobo_znuny_plugin*"]
```

### Package Structure

```
open-ticket-ai/
├── pyproject.toml                          # Root: workspace config + core package
├── src/
│   ├── open_ticket_ai/                     # Core package source code
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── main.py
│   │   ├── base/
│   │   ├── core/
│   │   └── extras/
│   ├── open_ticket_ai_hf_local/            # HF Local plugin workspace member
│   │   ├── pyproject.toml                  # Plugin package definition
│   │   └── open_ticket_ai_hf_local/        # Plugin source code
│   └── open_ticket_ai_otobo_znuny_plugin/  # OTOBO plugin workspace member
│       ├── pyproject.toml                  # Plugin package definition
│       └── *.py                            # Plugin source code
├── tests/                                  # Central test directory
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
└── uv.lock                                 # Locked dependencies
```

## Key Changes Made

1. **Fixed Duplicate Sections**
   - Removed duplicate `[tool.uv.workspace]` and `[tool.uv.sources]` sections from root pyproject.toml
   - Removed duplicate `dependencies`, `[project.urls]`, and `[project.entry-points]` from plugin files

2. **Package Exclusions**
   - Updated `[tool.setuptools.packages.find]` in root to explicitly exclude plugin packages
   - Core package build now only includes `open_ticket_ai` code, not plugin code
   - Properly excludes tests from the core package

3. **Plugin pyproject.toml Cleanup**
   - Fixed duplicate readme field in HF Local plugin
   - Fixed duplicate entry points in OTOBO/Znuny plugin
   - Removed conflicting dependencies sections

4. **Workspace Benefits**
   - All packages can be installed together with `uv sync`
   - Cross-package imports work during development
   - Centralized tooling (ruff, mypy, pytest) configured at the root
   - Independent versioning and publishing of each package

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
