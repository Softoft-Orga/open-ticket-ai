# Plugin Distribution Standards

This document defines the standards for Open Ticket AI plugin distributions to ensure consistency, maintainability, and interoperability.

## Directory Structure

Each plugin must follow one of these structures:

### Option 1: Flat Structure (simpler for small plugins)

```
src/open_ticket_ai_<plugin_name>/
├── pyproject.toml          # Package configuration
├── README.md               # Plugin documentation
├── LICENSE                 # LGPL-2.1-only license file
├── CHANGELOG.md            # Version history
├── __init__.py             # Plugin entry point with metadata
├── <module>.py             # Plugin modules
└── tests/                  # Plugin-specific unit tests
    └── ...
```

### Option 2: Nested Structure (recommended for complex plugins)

```
src/open_ticket_ai_<plugin_name>/
├── pyproject.toml          # Package configuration
├── README.md               # Plugin documentation
├── LICENSE                 # LGPL-2.1-only license file
├── CHANGELOG.md            # Version history
├── __init__.py             # Top-level re-export
├── open_ticket_ai_<plugin_name>/  # Plugin source code
│   ├── __init__.py         # Plugin entry point with metadata
│   └── ...                 # Plugin modules
└── tests/                  # Plugin-specific unit tests
    └── ...
```

## Naming Conventions

### Package Names
- PyPI distribution name: `open-ticket-ai-<plugin-name>` (with hyphens)
- Python import name: `open_ticket_ai_<plugin_name>` (with underscores)
- Plugin directory: `src/open_ticket_ai_<plugin_name>/` (with underscores)

Examples:
- `open-ticket-ai-hf-local` → `open_ticket_ai_hf_local`
- `open-ticket-ai-otobo-znuny-plugin` → `open_ticket_ai_otobo_znuny_plugin`

## Required Files

### pyproject.toml

Must include:

```toml
[project]
name = "open-ticket-ai-<plugin-name>"
version = "X.Y.Z"  # Semantic versioning
description = "Brief plugin description"
readme = "README.md"
requires-python = ">=3.13"
authors = [{ name = "Author Name", email = "email@example.com" }]
license = { text = "LGPL-2.1-only" }

keywords = ["open-ticket-ai", "plugin", "<relevant-keywords>"]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "open-ticket-ai>=1.0.0rc1",
    # Additional dependencies
]

[project.urls]
Homepage = "https://open-ticket-ai.com"
Repository = "https://github.com/Softoft-Orga/open-ticket-ai"
Documentation = "https://open-ticket-ai.com/en/guide/available-plugins.html"
Changelog = "https://github.com/Softoft-Orga/open-ticket-ai/blob/main/src/open_ticket_ai_<plugin_name>/CHANGELOG.md"

[project.entry-points."open_ticket_ai.plugins"]
<plugin_name> = "open_ticket_ai_<plugin_name>"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

### Package Configuration

For flat structure (Option 1):
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["open_ticket_ai_<plugin_name>*"]
```

For nested structure (Option 2):
```toml
[tool.setuptools]
packages = ["open_ticket_ai_<plugin_name>"]
```

Or with auto-discovery:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["open_ticket_ai_<plugin_name>"]
```

### README.md

Must include:
- Plugin name and brief description
- Installation instructions
- Requirements section
- Usage examples with YAML configuration
- Features list
- License information
- Links (Homepage, Repository, Documentation)

### LICENSE

Must contain the full LGPL-2.1-only license text.

### CHANGELOG.md

Must follow this format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD
### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes
```

## Plugin Interface

Each plugin must expose a standard interface in its `__init__.py`:

```python
from .<module> import <Classes>

__all__ = ["<Classes>"]

def get_metadata():
    return {
        "name": "<plugin-name>",
        "version": "X.Y.Z",
        "core_api": "2.0",
        "description": "Brief description",
    }

def register_pipes():
    return []

def register_services():
    return []
```

### Metadata Fields

- `name` (str, required): Plugin name matching package name
- `version` (str, required): Plugin version (semantic versioning)
- `core_api` (str, required): Compatible core API version (currently "2.0")
- `description` (str, required): Brief plugin description

### Hook Functions

- `register_pipes()`: Returns list of pipe class references
- `register_services()`: Returns list of service class references
- `register_cli_commands()`: (Optional) Returns list of Click command/group objects for CLI integration

## Versioning

### Semantic Versioning

Plugins must follow [Semantic Versioning 2.0.0](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

### Core API Compatibility

Plugins must declare compatible core API version via `core_api` in metadata.
Current core API version: **2.0**

Version compatibility matrix:
- Core API 2.0 → Plugin requires `core_api: "2.0"`
- Breaking changes in core → Increment core API version

## Dependencies

### Core Dependency

All plugins must depend on:
```toml
dependencies = [
    "open-ticket-ai>=1.0.0rc1",
]
```

### Additional Dependencies

- Pin major versions: `package~=X.Y.Z`
- Specify minimum versions where appropriate
- Document all external dependencies in README.md

## Testing

### Required Test Structure

```
tests/
├── test_<plugin_feature>.py
└── conftest.py  # Plugin-specific fixtures
```

### Test Markers

Use pytest markers:
- `@pytest.mark.unit`: Fast, isolated tests
- `@pytest.mark.integration`: Core + plugin interaction tests
- `@pytest.mark.slow`: Long-running tests

## Contract Compliance

All plugins must pass contract tests defined in `tests/contract/test_plugin_contract.py`:

1. Metadata validation
   - `get_metadata()` returns valid metadata dict
   - Required fields present: name, version, core_api, description
   - `core_api` matches current version

2. Hook validation
   - `register_pipes()` exists and returns list
   - `register_services()` exists and returns list

3. Entry point registration
   - Plugin registered in `open_ticket_ai.plugins` entry point group

### Validation Tools

Run the plugin validation script to check compliance:

```bash
python scripts/validate_plugins.py
```

See [scripts/README.md](scripts/README.md) for details.

## Documentation

### Plugin Documentation Location

Plugin documentation must be available at:
- Main docs: VitePress docs in `docs/vitepress_docs/docs_src/en/developers/plugins.md`
- Plugin-specific: README.md in plugin directory

### Required Documentation Sections

1. Overview
2. Installation
3. Requirements
4. Configuration
5. Usage Examples
6. API Reference (if applicable)
7. Development Guide

## Publishing

### Build Process

```bash
cd src/open_ticket_ai_<plugin_name>
python -m build
```

### PyPI Publishing

Plugins are published to PyPI as separate packages:
- Package name: `open-ticket-ai-<plugin-name>`
- Automated via GitHub Actions workflows

### Version Coordination

- Core version: Independent versioning
- Plugin versions: Independent but must specify core compatibility

## Migration Path

For existing plugins not following these standards:

1. Create CHANGELOG.md if missing
2. Add get_metadata() function to __init__.py
3. Add register_pipes() and register_services() hooks
4. Add entry points to pyproject.toml
5. Ensure README.md has all required sections
6. Verify LICENSE file present
7. Run contract tests to validate compliance

## Examples

### Complete Plugin Structure

See reference implementations:
- HuggingFace Plugin: `src/open_ticket_ai_hf_local/` (nested structure with advanced features)
- OTOBO/Znuny Plugin: `src/open_ticket_ai_otobo_znuny_plugin/` (flat structure for services)

### Minimal Plugin Template

Here's a minimal plugin implementation:

#### Directory Structure (Flat)

```
src/open_ticket_ai_minimal/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── __init__.py
├── minimal_pipe.py
└── tests/
    └── test_minimal_pipe.py
```

#### `__init__.py`

```python
from .minimal_pipe import MinimalPipe

__version__ = "1.0.0"

__all__ = ["MinimalPipe"]

def get_metadata():
    return {
        "name": "open-ticket-ai-minimal",
        "version": __version__,
        "core_api": "2.0",
        "description": "Minimal example plugin for Open Ticket AI",
    }

def register_pipes():
    return [MinimalPipe]

def register_services():
    return []

def register_cli_commands():
    from .cli import get_commands
    return get_commands()
```

#### `minimal_pipe.py`

```python
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.context import Context

class MinimalPipe(Pipe):
    def execute(self, context: Context):
        return {"message": "Hello from minimal plugin!"}
```

#### `pyproject.toml`

```toml
[project]
name = "open-ticket-ai-minimal"
version = "1.0.0"
description = "Minimal example plugin for Open Ticket AI"
readme = "README.md"
requires-python = ">=3.13"
authors = [{ name = "Your Name", email = "you@example.com" }]
license = { text = "LGPL-2.1-only" }

keywords = ["open-ticket-ai", "plugin", "example"]

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "open-ticket-ai>=1.0.0rc1",
]

[project.urls]
Homepage = "https://open-ticket-ai.com"
Repository = "https://github.com/Softoft-Orga/open-ticket-ai"

[project.entry-points."open_ticket_ai.plugins"]
minimal = "open_ticket_ai_minimal"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["open_ticket_ai_minimal*"]
```

## Questions and Support

For questions about plugin standards:
- Open an issue: https://github.com/Softoft-Orga/open-ticket-ai/issues
- Check documentation: https://open-ticket-ai.com
- Review examples in repository
