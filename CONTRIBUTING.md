# Contributing to Open Ticket AI

Thank you for your interest in contributing to Open Ticket AI! This guide provides essential information for contributors and maintainers.

## Repository Overview

**Purpose:** Open Ticket AI provides automation components that enhance open-source ticket systems (primarily OTOBO/Znuny) with AI-driven workflows.

## Repository Structure

### Source Layout

- **Application code:** `src/open_ticket_ai/` organized by domain:
  - `core/` - Configuration models, dependency injection, pipeline engine, template rendering
  - `base/` - Reusable pipe implementations (ticket fetch/update, composite pipes)
  - `hf_local/` - HuggingFace transformers with optional local pipelines
  - `extras/` - Additional utilities and helpers
- **Configuration schemas and examples:** `src/open_ticket_ai/core/config/` and `docs/config_examples/`
- **Tests:** `tests/` and `classification_api_tests/`
- **Plugins:**
  - HuggingFace local: `src/open_ticket_ai_hf_local/`
  - OTOBO/Znuny integration: `src/open_ticket_ai_otobo_znuny_plugin/`
- **Documentation:** 
  - Developer notes and diagrams: `docs/`
  - VitePress documentation: `docs/vitepress_docs/`

### Package Structure

This repository contains multiple Python packages published to PyPI:

- **[open-ticket-ai](https://pypi.org/project/open-ticket-ai/)** - Core package with AI-powered ticket classification and automation
- **[open-ticket-ai-hf-local](https://pypi.org/project/open-ticket-ai-hf-local/)** - HuggingFace local inference plugin
- **[open-ticket-ai-otobo-znuny-plugin](https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/)** - OTOBO/Znuny ticket system integration plugin

## Development Environment Setup

### Prerequisites

- **Python 3.13+** required
- **[uv](https://github.com/astral-sh/uv)** for dependency management

### Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Softoft-Orga/open-ticket-ai.git
   cd open-ticket-ai
   ```

2. Install dependencies:
   ```bash
   uv sync --all-extras
   ```

## Tooling

### Dependency Management

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management. The lock file is `uv.lock`.

### Code Quality Tools

- **Formatting and Linting:** Ruff
  ```bash
  uv run ruff format .
  uv run ruff check .
  ```

- **Type Checking:** MyPy (strict mode) with `pydantic.mypy` plugin
  ```bash
  uv run mypy .
  ```

### Testing

Run the test suite using pytest:

```bash
# Main test suite
uv run pytest

# Classification API tests (if relevant)
uv run pytest classification_api_tests
```

Async tests rely on `pytest-asyncio`.

## Configuration

### Project Configuration

- **Project metadata and tool configuration:** Centralized in `pyproject.toml`
- **Runtime configuration:** Loaded from YAML (`src/config.yml` by default) and validated with Pydantic models

### AI Integrations

- **Hugging Face transformers:** Optional local pipelines in `src/open_ticket_ai/hf_local`
- **Ticket system integrations:** OTOBO/Znuny adapters in `src/open_ticket_ai/otobo_znuny_plugin`

## Development Workflow

### Making Changes

1. Create a feature branch from `dev`
2. Make your code changes following project conventions
3. Format and lint your code:
   ```bash
   uv run ruff format .
   uv run ruff check .
   ```
4. Type-check your code:
   ```bash
   uv run mypy .
   ```
5. Run tests:
   ```bash
   uv run pytest
   ```
6. Update documentation or configuration examples in `docs/` when behavior changes
7. Commit your changes with clear, descriptive messages

### Code Style Guidelines

- **Python 3.13 only**
- **No comments, no docstrings** - Write self-explanatory code
- **Prefer pure functions, clear names, small modules**
- **Documentation:** Put explanations in VitePress pages (Markdown), not in source files

### Pull Request Guidelines

1. Ensure all tests pass
2. Update relevant documentation
3. Add tests for new functionality
4. Follow existing code patterns and module boundaries
5. Keep configuration-driven behavior
6. Summarize changes in PR description, including commands run

## Extending Open Ticket AI

### Adding a Custom Pipe

1. **Define a configuration model** (optional) for your pipe parameters
2. **Subclass `Pipe`** and implement the asynchronous `_process()` method
3. **Return a dictionary** shaped like `PipeResult`
4. **Register** under `open_ticket_ai.defs` in the YAML configuration

See [Developer Information](docs/vitepress_docs/docs_src/en/developers/developer-information.md) for detailed examples.

### Creating a Plugin

To add support for another ticket system or AI service:

1. **Create unified models** to map entities into standard `UnifiedTicket`, `UnifiedNote`, etc.
2. **Implement a service class** that wraps the target API
3. **Expose configuration models** for credentials and endpoints
4. **Register the plugin** via YAML configuration under `open_ticket_ai.plugins`

See [Plugin Developer Guide](docs/vitepress_docs/docs_src/en/developers/plugins.md) for comprehensive documentation.

### Adding Template Extensions

Use decorators to extend Jinja2 templates:

```python
from open_ticket_ai.core.template_rendering import jinja_template_method, jinja_variable

@jinja_template_method("custom_formatter")
def format_data(data: str) -> str:
    return data.upper()

@jinja_variable("global_config")
def get_config() -> dict:
    return {"key": "value"}
```

See [Template Extensions Guide](docs/vitepress_docs/docs_src/en/developers/template-extensions.md) for more details.

## Documentation

### Where to Document

- **Code behavior and architecture:** VitePress docs in `docs/vitepress_docs/docs_src/en/`
- **API reference:** Auto-generated from code in `docs/vitepress_docs/docs_src/en/developers/api/`
- **Configuration examples:** `docs/config_examples/`
- **Developer processes:** `docs/developer_process.md`

### Documentation Standards

- Use Markdown for all documentation
- Keep documentation up-to-date with code changes
- Provide clear examples for new features
- Update configuration examples when adding new capabilities

## Best Practices

### When in Doubt

- Align new code with existing module boundaries
- Keep configuration-driven behavior
- Update docs/tests alongside code changes
- Follow the patterns established in existing code
- Consult [Architecture documentation](docs/vitepress_docs/docs_src/en/developers/architecture.md) for design decisions

### Configuration-Driven Design

Open Ticket AI emphasizes declarative configuration:

- Define behavior in YAML rather than hardcoding
- Use Jinja2 templates for dynamic values
- Leverage dependency injection for service wiring
- Keep pipes focused and composable

### Testing Strategy

- Write unit tests for new components
- Mock external dependencies (ticket systems, AI services)
- Test both success and failure paths
- Validate configuration parsing and validation
- Exercise critical pipelines end-to-end when possible

## Release Process

### Version Management

Before releasing, update the version in the appropriate `pyproject.toml`:

- Core package: `/pyproject.toml`
- HF Local plugin: `/src/open_ticket_ai_hf_local/pyproject.toml`
- OTOBO/Znuny plugin: `/src/open_ticket_ai_otobo_znuny_plugin/pyproject.toml`

### Publishing to PyPI

Packages are automatically published via GitHub Actions workflows. See [README.md](README.md#release-automation) for details on triggering releases.

## Getting Help

- **Documentation:** [docs/](docs/) and https://open-ticket-ai.com
- **Issues:** https://github.com/Softoft-Orga/open-ticket-ai/issues
- **Discussions:** Use GitHub Discussions for questions and ideas

## License

This project is licensed under LGPL-2.1-only. See [LICENSE](LICENSE) for details.

## Additional Resources

- [Quick Start Guide](QUICK_START.md)
- [Developer Information](docs/vitepress_docs/docs_src/en/developers/developer-information.md)
- [Pipeline Architecture](docs/vitepress_docs/docs_src/en/developers/pipeline.md)
- [Plugin Development](docs/vitepress_docs/docs_src/en/developers/plugins.md)
- [Configuration Examples](docs/config_examples/)
