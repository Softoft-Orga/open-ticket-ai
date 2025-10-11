# Open Ticket AI
AI enhancements for open source ticket systems

## Packages

This repository contains multiple Python packages that are published to PyPI:

- **[open-ticket-ai](https://pypi.org/project/open-ticket-ai/)** - Core package with AI-powered ticket classification and automation
- **[open-ticket-ai-hf-local](https://pypi.org/project/open-ticket-ai-hf-local/)** - HuggingFace local inference plugin
- **[open-ticket-ai-otobo-znuny-plugin](https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/)** - OTOBO/Znuny ticket system integration plugin
- **[open-ticket-ai-bundle](https://pypi.org/project/open-ticket-ai-bundle/)** - Meta-package with tested compatible versions (optional)

### Version Compatibility

The core package and plugins use independent versioning. Plugins declare compatibility with core versions:

| Core Version | Plugin API | HF Local | OTOBO/Znuny | Status |
|--------------|-----------|----------|-------------|--------|
| 1.0.0rc1     | 2.0       | 1.0.0rc1 | 1.0.0rc1    | Beta   |
| 1.x.x        | 2.0       | 1.x.x    | 1.x.x       | Compatible |

Plugins specify core compatibility via dependency ranges (e.g., `open-ticket-ai>=1.0.0,<2.0.0`) and must match the Plugin API version defined in the core contract tests.

## Installation

### Quick Start (Bundle)

Install everything with guaranteed compatibility:

```bash
pip install open-ticket-ai-bundle
```

### Core Package

```bash
pip install open-ticket-ai
```

### Plugins

Install plugins separately as needed:

```bash
# HuggingFace local inference
pip install open-ticket-ai-hf-local

# OTOBO/Znuny integration
pip install open-ticket-ai-otobo-znuny-plugin
```

## CLI Tool

Open Ticket AI includes a command-line interface (CLI) tool for easy management:

```bash
# Initialize a new config from template
otai init queue_classification

# Validate configuration
otai check-config config.yml

# Start the application
otai start --config config.yml

# Manage plugins
otai plugin list
otai plugin install open-ticket-ai-hf-local
otai plugin remove open-ticket-ai-hf-local

# Upgrade OTAI
otai upgrade
```

For detailed CLI usage, see the documentation at https://open-ticket-ai.com or run `otai --help`.

## Repository Structure

This repository uses a monorepo structure containing the core application and plugins:

- **`src/open_ticket_ai/`** - Core application package directory
  - `pyproject.toml` - Core package metadata and dependencies
  - `open_ticket_ai/` - Source code organized by domain (core, base, extras)
- **`src/open_ticket_ai_hf_local/`** - HuggingFace local inference plugin package
- **`src/open_ticket_ai_otobo_znuny_plugin/`** - OTOBO/Znuny integration plugin package
- **`tests/`** - Test suite (unit, e2e, integration tests)
- **`docs/`** - Documentation, diagrams, and configuration examples
- **`packages/`** - Standalone package builds

Configuration files:
- **`pyproject.toml`** - Project metadata, dependencies, and tool configuration
- **`uv.lock`** - Locked dependency versions for reproducible builds
- **Runtime config** - YAML files validated with Pydantic models

For detailed information, see [CONTRIBUTING.md](general/CONTRIBUTING.md).

## Workspace Architecture

This repository uses a **uv workspace** to manage multiple Python packages as a monorepo:

### Core vs Plugins

- **Core Package** (`open-ticket-ai`)
  - Located at `src/open_ticket_ai/` with its own `pyproject.toml`
  - Source code in `src/open_ticket_ai/open_ticket_ai/`
  - Provides the foundational AI pipeline framework, configuration system, and dependency injection
  - Includes base pipes for ticket operations and template rendering
  - Can be used standalone for custom implementations

- **Plugin Packages**
  - Each plugin is a separate workspace member with its own `pyproject.toml`
  - `open-ticket-ai-hf-local` - HuggingFace local inference for text classification
  - `open-ticket-ai-otobo-znuny-plugin` - OTOBO/Znuny ticket system integration
  - Plugins extend core functionality without modifying core code

### Plugin Discovery

Plugins are discovered and loaded through:

1. **Configuration-based registration** - Plugins define services in `config.yml`:
   ```yaml
   open_ticket_ai:
     defs:
       otobo_service:
         use: "otai_otobo_znuny.OTOBOZnunyTicketSystemService"
         # ... configuration
   ```

2. **Dependency injection** - Core uses the `UnifiedRegistry` to resolve plugin services by ID
3. **YAML references** - Pipeline steps inject plugin services via `injects` declarations
4. **Workspace dependencies** - The uv workspace ensures plugins can depend on the core package during development

### Development Workflow

The workspace configuration (in root `pyproject.toml`):
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

This allows:
- Installing all packages together with `uv sync`
- Cross-package imports during development
- Centralized tooling (ruff, mypy, pytest) configured at the root
- Independent versioning and publishing of each package

For plugin development details, see [Plugin Developer Guide](https://open-ticket-ai.com/developers/plugins.html).

## Release Automation

### PyPI Publishing Workflow

All packages are automatically built and published to PyPI using GitHub Actions. The repository uses a reusable workflow pattern for consistent publishing across packages.

### Triggering a Release

Releases can be triggered in multiple ways:

#### 1. Manual Trigger (Dry-Run for Testing)

You can test the build process without publishing:

1. Go to the Actions tab in GitHub
2. Select the workflow for the package you want to test:
   - "Publish open-ticket-ai to PyPI"
   - "Publish open-ticket-ai-hf-local to PyPI"
   - "Publish open-ticket-ai-otobo-znuny-plugin to PyPI"
3. Click "Run workflow"
4. Check "Run in dry-run mode" to build without publishing
5. Click "Run workflow"

#### 2. Tag-Based Release

Create and push a version tag to trigger automatic publishing:

```bash
# For core package
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# For HuggingFace plugin
git tag -a hf-local-v1.0.0 -m "Release HF Local plugin 1.0.0"
git push origin hf-local-v1.0.0

# For OTOBO/Znuny plugin
git tag -a otobo-znuny-v1.0.0 -m "Release OTOBO/Znuny plugin 1.0.0"
git push origin otobo-znuny-v1.0.0
```

#### 3. GitHub Release

Create a release through the GitHub UI, which will automatically trigger the publishing workflow.

### Required Secrets

The following secrets must be configured in the repository settings:

- `PYPI_API_TOKEN` - PyPI API token for the core package
- `PYPI_API_TOKEN_HF_LOCAL` - PyPI API token for the HuggingFace plugin
- `PYPI_API_TOKEN_OTOBO_ZNUNY` - PyPI API token for the OTOBO/Znuny plugin

To create PyPI API tokens:
1. Go to https://pypi.org/manage/account/token/
2. Create a token with scope limited to the specific project
3. Add the token to GitHub repository secrets

### Version Management

Before releasing, update the version in the appropriate `pyproject.toml`:

- Core package: `/pyproject.toml`
- HF Local plugin: `/src/open_ticket_ai_hf_local/pyproject.toml`
- OTOBO/Znuny plugin: `/src/open_ticket_ai_otobo_znuny_plugin/pyproject.toml`

For comprehensive release procedures, compatibility requirements, and versioning policies, see [RELEASE.md](RELEASE.md).

### Workspace and Dependency Locking

This repository uses `uv` for workspace management with locked dependencies for reproducible builds. The workspace includes the core package and all plugins, managed from `uv.lock`.

Lock dependencies after changes:
```bash
uv lock
```

CI uses locked versions to ensure reproducibility:
```bash
uv sync --locked
```

### Workflow Details

The publishing workflow:
1. Checks out the repository
2. Sets up Python 3.13
3. Installs build tools (`build` and `twine`)
4. Builds the package using `python -m build`
5. Validates the built package with `twine check`
6. Publishes to PyPI (or skips in dry-run mode)
7. Uploads build artifacts for inspection

## Development

### Getting Started

See [CONTRIBUTING.md](general/CONTRIBUTING.md) for comprehensive guidance on:
- Repository structure and organization
- Development setup and tooling
- Coding standards and best practices
- Testing and quality assurance
- Contribution workflow

### Reporting Issues and Requesting Features

Open Ticket AI provides structured issue templates to help you report bugs, request features, or suggest improvements:

- **Bug Report** - For unexpected behavior, errors, or crashes
- **Documentation Request** - For documentation improvements
- **Configuration Issue** - For YAML config, Jinja2, or DI problems
- **Pipe or Plugin Request** - For new pipes or plugin proposals
- **Feature Request (General)** - For general enhancements
- **CI/CD Issue** - For workflow, build, deployment, and automation changes

See [ISSUE_TEMPLATES.md](general/ISSUE_TEMPLATES.md) for detailed guidance on using these templates.

### Plugin API Compatibility

The core package defines a Plugin API version that ensures compatibility between the core and plugins.

**Current Plugin API Version: 2.0**

#### Compatibility Table

| Core Version | Plugin API Version | Compatible Plugins |
|--------------|-------------------|-------------------|
| 1.0.0rc1+    | 2.0               | open-ticket-ai-hf-local >= 1.0.0rc1<br>open-ticket-ai-otobo-znuny-plugin >= 1.0.0rc1 |

#### Plugin Development

Plugins must implement the following interface to be compatible:

```python
def get_metadata() -> dict:
    return {
        "name": "plugin-name",
        "version": "1.0.0",
        "core_api": "2.0"  # Must match core API version
    }

def register_services(binder) -> None:
    # Register DI services
    pass

def register_pipes(factory) -> None:
    # Register pipeline components
    pass
```

Plugins are discovered via entry points in the `open_ticket_ai.plugins` group. Add this to your plugin's `pyproject.toml`:

```toml
[project.entry-points."open_ticket_ai.plugins"]
your_plugin = "your_package:plugin_module"
```

For detailed plugin development guidance, see [docs/vitepress_docs/docs_src/en/developers/plugins.md](docs/vitepress_docs/docs_src/en/developers/plugins.md).
### Plugin Development

For plugin developers:
- **[PLUGIN_STANDARDS.md](../../PLUGIN_STANDARDS.md)** - Complete plugin packaging and metadata standards
- **[PLUGIN_QUICK_REFERENCE.md](general/PLUGIN_QUICK_REFERENCE.md)** - Quick reference guide
- **Plugin validation**: Run `python scripts/validate_plugins.py` to check compliance
### Testing

This repository uses a comprehensive testing strategy with different test types and CI stages:

#### Test Types

- **Unit Tests** (`@pytest.mark.unit`): Fast, isolated tests for individual components
- **Integration Tests** (`@pytest.mark.integration`): Test Core + Plugin interactions
- **Contract Tests** (`@pytest.mark.contract`): Validate plugin API compatibility
- **E2E Tests** (`@pytest.mark.e2e`): End-to-end workflow tests

#### Running Tests Locally

```bash
# Run all tests
pytest

# Run specific test types by directory
pytest src/open_ticket_ai/tests/  # Core unit tests
pytest tests/integration/       # Core integration tests
pytest tests/contract/          # Contract tests
pytest tests/e2e/              # E2E tests

# Run plugin tests
pytest src/otai_hf_local/tests/         # HF Local plugin
pytest src/otai_otobo_znuny/tests/  # OTOBO/Znuny plugin

# Run specific test types by marker
pytest -m unit          # Only tests marked with @pytest.mark.unit
pytest -m integration   # Only tests marked with @pytest.mark.integration
pytest -m contract      # Only tests marked with @pytest.mark.contract
pytest -m e2e          # Only tests marked with @pytest.mark.e2e

# Skip slow tests
pytest -m "not slow"
```

#### CI Test Stages

The CI pipeline runs different test stages:

1. **Core Tests** (on push/PR to main/dev):
   - Lint with ruff and mypy
   - Unit tests: All tests in `src/open_ticket_ai/tests/`
   - Integration tests: All tests in `tests/integration/`

2. **Plugin Tests** (on plugin changes):
   - HF Local: Unit tests in `src/open_ticket_ai_hf_local/tests/` + linting + type checking
   - OTOBO/Znuny: Unit tests in `src/open_ticket_ai_otobo_znuny_plugin/tests/` + linting + type checking

3. **Nightly Tests** (scheduled at 2 AM UTC or manual trigger):
   - Contract tests: All tests in `tests/contract/` - validates all installed plugins against core API
   - E2E tests: All tests in `tests/e2e/` - complete workflow testing

For detailed test structure and best practices, see:
- [Testing Guide](raw_en_docs/en/guides/testing.md) - Comprehensive testing guide with test structure, fixtures, and patterns
- [FIXTURES.md](../FIXTURES.md) - Complete fixture reference
- [FIXTURE_TEMPLATES.md](../FIXTURE_TEMPLATES.md) - Common fixture templates
- [AGENTS.md](../../AGENTS.md) - Authoritative test structure rules

#### CI Quality Assurance

The repository uses SonarCloud for continuous code quality monitoring. The QA workflow automatically generates and uploads:

- **Test Coverage Reports** (pytest with coverage.xml)
- **Linting Reports** (ruff in SARIF format)
- **Type Checking Reports** (mypy)

All reports are analyzed by SonarCloud and displayed in pull requests. For complete details on the QA workflow, report generation, and SonarCloud configuration, see [CI Quality Assurance](general/CI_QUALITY_ASSURANCE.md).

### Development Workflows

See [docs/developer_process.md](general/developer_process.md) for information about automated processes.

## License

LGPL-2.1-only

## Links

- Homepage: https://open-ticket-ai.com
- Documentation: [docs/](docs/)
