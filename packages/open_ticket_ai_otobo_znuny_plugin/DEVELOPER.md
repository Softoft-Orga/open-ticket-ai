# Developer Guide

This guide is for developers who want to contribute to the Open Ticket AI OTOBO/Znuny Plugin.

## Development Setup

1. Clone the main Open Ticket AI repository:
   ```bash
   git clone https://github.com/Softoft-Orga/open-ticket-ai.git
   cd open-ticket-ai
   ```

2. Navigate to the plugin package:
   ```bash
   cd packages/open_ticket_ai_otobo_znuny_plugin
   ```

3. Install dependencies (Python 3.13+ required):
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=open_ticket_ai_otobo_znuny_plugin tests/
```

## Code Quality

### Linting

```bash
ruff check src/ tests/
```

### Type Checking

```bash
mypy src/
```

### Auto-formatting

```bash
ruff format src/ tests/
```

## Building the Package

To build the distribution packages:

```bash
python -m build
```

This will create:
- `dist/*.tar.gz` - Source distribution
- `dist/*.whl` - Wheel distribution

## Testing Installation Locally

To test the package installation locally:

```bash
pip install dist/open_ticket_ai_otobo_znuny_plugin-*.whl
```

Or in editable mode for development:

```bash
pip install -e .
```

## Publishing to PyPI

### Prerequisites

1. Create accounts on:
   - [Test PyPI](https://test.pypi.org/) (for testing)
   - [PyPI](https://pypi.org/) (for production)

2. Generate API tokens for both platforms

3. Add tokens as GitHub secrets:
   - `TEST_PYPI_API_TOKEN`
   - `PYPI_API_TOKEN` (or use trusted publishing)

### Manual Publishing

For testing on Test PyPI:

```bash
python -m build
twine upload --repository testpypi dist/*
```

For production PyPI:

```bash
twine upload dist/*
```

### Automated Publishing via GitHub Actions

The package is automatically published when you:

1. **Create a release tag** matching `otobo-znuny-plugin-v*`:
   ```bash
   git tag -a otobo-znuny-plugin-v1.0.0 -m "Release version 1.0.0"
   git push origin otobo-znuny-plugin-v1.0.0
   ```

2. **Manually trigger** the workflow from GitHub Actions UI

The workflow will:
- Build the package
- Run package checks
- Publish to PyPI (on tag push) or Test PyPI (manual trigger)

## Release Checklist

Before releasing a new version:

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with changes
- [ ] Run all tests and ensure they pass
- [ ] Build the package locally and test installation
- [ ] Create and push a git tag
- [ ] Verify the GitHub Action completes successfully
- [ ] Check the package appears on PyPI
- [ ] Test installing from PyPI: `pip install open-ticket-ai-otobo-znuny-plugin`

## Project Structure

```
packages/open_ticket_ai_otobo_znuny_plugin/
├── src/
│   └── open_ticket_ai_otobo_znuny_plugin/
│       ├── __init__.py
│       ├── models.py
│       ├── otobo_znuny_ticket_system_service.py
│       └── otobo_znuny_ticket_system_service_config.py
├── tests/
│   ├── test_models.py
│   ├── test_otobo_znuny_ticket_system_service.py
│   └── test_otobo_znuny_ticket_system_service_config.py
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
└── MANIFEST.in
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and linting
6. Submit a pull request

## Support

For questions or issues:
- GitHub Issues: https://github.com/Softoft-Orga/open-ticket-ai/issues
- Documentation: https://open-ticket-ai.com
