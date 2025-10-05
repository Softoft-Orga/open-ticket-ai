# Open Ticket AI

[![Python application](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/python-app.yml/badge.svg)](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/python-app.yml)
[![Publish open-ticket-ai](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/publish-open-ticket-ai.yml/badge.svg)](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/publish-open-ticket-ai.yml)
[![Publish HF Local](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/publish-hf-local.yml/badge.svg)](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/publish-hf-local.yml)
[![Publish OTOBO/Znuny Plugin](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/publish-otobo-znuny.yml/badge.svg)](https://github.com/Softoft-Orga/open-ticket-ai/actions/workflows/publish-otobo-znuny.yml)

AI enhancements for open source ticket systems

## Packages

This repository contains multiple Python packages that are published to PyPI:

- **[open-ticket-ai](https://pypi.org/project/open-ticket-ai/)** - Core package with AI-powered ticket classification and automation
- **[open-ticket-ai-hf-local](https://pypi.org/project/open-ticket-ai-hf-local/)** - HuggingFace local inference plugin
- **[open-ticket-ai-otobo-znuny-plugin](https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/)** - OTOBO/Znuny ticket system integration plugin

## Installation

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

## Repository Structure

This repository uses a monorepo structure containing the core application and plugins:

- **`src/open_ticket_ai/`** - Core application organized by domain (core, base, extras)
- **`src/open_ticket_ai_hf_local/`** - HuggingFace local inference plugin package
- **`src/open_ticket_ai_otobo_znuny_plugin/`** - OTOBO/Znuny integration plugin package
- **`tests/`** - Test suite (unit, e2e, integration tests)
- **`docs/`** - Documentation, diagrams, and configuration examples
- **`packages/`** - Standalone package builds

Configuration files:
- **`pyproject.toml`** - Project metadata, dependencies, and tool configuration
- **`uv.lock`** - Locked dependency versions for reproducible builds
- **Runtime config** - YAML files validated with Pydantic models

For detailed information, see [CONTRIBUTING.md](CONTRIBUTING.md).

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

See [CONTRIBUTING.md](CONTRIBUTING.md) for comprehensive guidance on:
- Repository structure and organization
- Development setup and tooling
- Coding standards and best practices
- Testing and quality assurance
- Contribution workflow

### Development Workflows

See [docs/developer_process.md](developer_process.md) for information about automated processes.

## License

LGPL-2.1-only

## Links

- Homepage: https://open-ticket-ai.com
- Documentation: [docs/](docs/)
