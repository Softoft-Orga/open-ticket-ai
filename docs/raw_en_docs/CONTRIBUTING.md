# Contributing to Open Ticket AI

Thank you for your interest in contributing to Open Ticket AI! This guide will help you understand the repository structure, development workflow, and coding standards.

## Repository Purpose

Open Ticket AI provides automation components that enhance open-source ticket systems (primarily OTOBO/Znuny) with AI-driven workflows for intelligent ticket classification, routing, and processing.

## Repository Structure

### Source Layout

```
open-ticket-ai/
├── src/
│   ├── open_ticket_ai/           # Core application
│   │   ├── core/                 # Core functionality
│   │   │   ├── config/           # Configuration schemas and loaders
│   │   │   ├── pipeline/         # Pipeline orchestration
│   │   │   ├── template_rendering/
│   │   │   └── ticket_system_integration/
│   │   ├── base/                 # Base components and pipes
│   │   └── extras/               # Additional utilities
│   ├── open_ticket_ai_hf_local/  # HuggingFace local inference plugin
│   └── open_ticket_ai_otobo_znuny_plugin/  # OTOBO/Znuny integration
├── tests/
│   ├── unit/                     # Unit tests
│   ├── e2e/                      # End-to-end tests
│   └── classification_api_tests/ # API tests
├── docs/                         # Documentation
│   ├── config_examples/          # Configuration examples
│   ├── diagrams/                 # Architecture diagrams
│   └── vitepress_docs/           # VitePress documentation site
└── packages/                     # Standalone packages
```

### Configuration Files

- **Runtime configuration**: YAML files (default: `src/config.yml`) validated with Pydantic models
- **Project metadata**: `pyproject.toml` for dependencies, tool configuration, and package metadata
- **Config schemas**: Located in `src/open_ticket_ai/open_ticket_ai/core/config/`
- **Config examples**: Located in `docs/config_examples/`

## Development Setup

### Prerequisites

- Python 3.13 (required)
- [`uv`](https://github.com/astral-sh/uv) for dependency management

### Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Softoft-Orga/open-ticket-ai.git
   cd open-ticket-ai
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up your environment**:
   ```bash
   export OPEN_TICKET_AI_CONFIG=/path/to/your/config.yml
   ```

## Coding Standards

### Python Style

- **Python version**: 3.13 only
- **No comments or docstrings**: Write self-explanatory code with clear naming
- **Documentation**: Place explanations in VitePress documentation (Markdown), not in source files
- **Code style**: Pure functions, clear names, small modules

### Tools and Linting

- **Formatter**: Ruff (automatically formats code)
- **Linter**: Ruff (checks code quality)
- **Type checker**: MyPy (strict mode) with `pydantic.mypy` plugin

### Running Code Quality Tools

```bash
# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/

# Auto-fix linting issues
uv run ruff check --fix src/ tests/
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test directory
uv run pytest src/open_ticket_ai/tests/

# Run with coverage
uv run pytest --cov=open_ticket_ai tests/
```

### Test Organization

For detailed information about the test structure, markers, fixtures, and best practices, see [docs/TESTING.md](TESTING.md).

**Quick Overview**:
- **Unit tests**: `src/open_ticket_ai/tests/` (core) and `<plugin>/tests/` (plugins) - Test individual components
- **Integration tests**: `tests/integration/` - Test Core + Plugin interactions
- **Contract tests**: `tests/contract/` - Test Plugin API compliance
- **E2E tests**: `tests/e2e/` - Test complete workflows
- **Test data**: `tests/data/` - Shared test data files

**Test Markers**:
- `@pytest.mark.unit` - Fast, isolated tests
- `@pytest.mark.integration` - Core + plugin together
- `@pytest.mark.contract` - Plugin API contracts
- `@pytest.mark.e2e` - End-to-end flows
- `@pytest.mark.slow` - Long-running tests

**Run specific test types**:
```bash
pytest -m unit          # Only unit tests
pytest -m integration   # Only integration tests
pytest -m "not slow"    # Skip slow tests
```

### Writing Tests

- Place tests in appropriate directories (core tests in `src/open_ticket_ai/tests/`, integration in `tests/integration/`, e2e in `tests/e2e/`)
- Follow existing test patterns and naming conventions
- Ensure async tests are properly decorated
- Add tests for new functionality

## AI Integrations

### HuggingFace Integration

- Location: `src/open_ticket_ai_hf_local/`
- Purpose: Local transformer model inference
- Configuration: Loaded via YAML and Pydantic models

### Ticket System Integration

- Location: `src/open_ticket_ai_otobo_znuny_plugin/`
- Purpose: OTOBO/Znuny ticket system adapters
- Supports: Ticket fetching, classification, and updates

## Architecture Overview

### Pipeline Orchestration

The system uses a pipeline-based architecture where:

1. **Orchestrator** loads pipeline configuration and executes pipes
2. **Pipes** are reusable components that perform specific tasks (fetch, classify, update)
3. **Services** provide shared functionality (logging, HTTP clients, etc.)
4. **Adapters** integrate with external ticket systems

### Configuration-Driven Behavior

All runtime behavior is controlled via YAML configuration:

- Pipeline definitions (`orchestrator` section)
- Service configurations (`general_config` section)
- Plugin loading (`plugins` section)
- Pipe definitions (`defs` section)

## Contribution Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the coding standards
- Write self-explanatory code
- Add documentation to VitePress docs if needed
- Add tests for new functionality

### 3. Test Your Changes

```bash
# Run linting
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/

# Run tests
uv run pytest
```

### 4. Update Documentation

If your changes affect:
- **User-facing features**: Update VitePress docs in `docs/vitepress_docs/`
- **Configuration**: Add examples to `docs/config_examples/`
- **Architecture**: Update relevant diagrams in `docs/diagrams/`

### 5. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

Follow conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for test changes

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots for UI changes
- Test results

## Building and Publishing

### Package Structure

The repository contains three publishable packages:

1. **open-ticket-ai** (core) - Main application
2. **open-ticket-ai-hf-local** - HuggingFace plugin
3. **open-ticket-ai-otobo-znuny-plugin** - OTOBO/Znuny integration

### Local Development

```bash
# Install in development mode
pip install -e .

# Install with plugins
pip install -e ".[otobo-znuny]"
```

### Building Packages

```bash
# Build all packages
python -m build

# Build specific package
cd src/otai_hf_local
python -m build
```

See [QUICK_START.md](QUICK_START.md) for PyPI publishing workflow.

## Extending the System

### Adding New Pipes

1. Create pipe class in appropriate module under `src/open_ticket_ai/open_ticket_ai/`
2. Inherit from base pipe classes
3. Implement required methods
4. Add configuration schema if needed
5. Document in VitePress
6. Add tests

### Adding New Plugins

See [PLUGIN_STANDARDS.md](PLUGIN_STANDARDS.md) for complete plugin development standards.

1. Create plugin package under `src/open_ticket_ai_<plugin_name>/`
2. Follow standard directory structure and naming conventions
3. Implement required plugin interface (`get_metadata()`, `register_pipes()`, `register_services()`)
4. Add entry points in pyproject.toml
5. Include all required files (README.md, LICENSE, CHANGELOG.md, pyproject.toml)
6. Add plugin configuration schema
7. Add tests (unit tests in plugin directory, contract tests will auto-discover)
8. Document usage in VitePress docs

### Adding New Services

1. Create service in `src/open_ticket_ai/open_ticket_ai/core/`
2. Use dependency injection (via `injector`)
3. Add configuration model
4. Register in DI container
5. Add tests

## Versioning and Releases

This project follows [Semantic Versioning](https://semver.org/) with specific rules for Core and plugins:

- **Core**: MAJOR version bump required when Plugin API changes incompatibly
- **Plugins**: Independent versioning, must declare Core compatibility range
- **Deprecations**: Features deprecated for 1-2 MINOR versions before removal

See [RELEASE.md](RELEASE.md) for comprehensive release procedures and [DEPRECATION_POLICY.md](DEPRECATION_POLICY.md) for deprecation guidelines.

When contributing:
- Don't break existing APIs without discussion
- Announce deprecations early with warnings
- Update Plugin API version when making breaking changes
- Run contract tests to verify plugin compatibility

## Module Boundaries

When adding new code:

- **Core functionality**: `src/open_ticket_ai/open_ticket_ai/core/`
- **Base components**: `src/open_ticket_ai/open_ticket_ai/base/`
- **Plugins**: Separate packages with clear interfaces
- **Configuration**: Always use Pydantic models
- **Tests**: Mirror the source structure

## Common Tasks

### Running the Application

```bash
# Set configuration
export OPEN_TICKET_AI_CONFIG=/path/to/config.yml

# Run main application
python -m open_ticket_ai.main
```

### Updating Dependencies

```bash
# Add new dependency
uv add package-name

# Update all dependencies
uv lock --upgrade

# Sync dependencies
uv sync
```

### Generating Documentation

Documentation is built with VitePress:

```bash
cd docs/vitepress_docs
npm install
npm run docs:dev  # Development server
npm run docs:build  # Production build
```

## Getting Help

- **Issues**: https://github.com/Softoft-Orga/open-ticket-ai/issues
- **Documentation**: https://open-ticket-ai.com
- **Discussions**: GitHub Discussions (if enabled)

## Additional Resources

- [README.md](README.md) - Project overview and quick links
- [QUICK_START.md](QUICK_START.md) - PyPI publishing guide
- [docs/developer_process.md](developer_process.md) - Automated processes
- [docs/workflow_architecture.md](workflow_architecture.md) - Technical architecture
- [docs/pipeline_flow.md](pipeline_flow.md) - Pipeline execution details

## License

This project is licensed under LGPL-2.1-only. See [LICENSE](../../LICENSE) for details.

## Code of Conduct

Be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.
