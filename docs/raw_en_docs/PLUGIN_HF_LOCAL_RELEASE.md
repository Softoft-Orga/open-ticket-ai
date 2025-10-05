# Release Instructions for open-ticket-ai-hf-local

This document describes how to release the `open-ticket-ai-hf-local` package to PyPI.

## Prerequisites

1. PyPI account with appropriate permissions
2. PyPI API token set as `PYPI_TOKEN_HF_LOCAL` in GitHub repository secrets

## Release Process

### Automated Release (Recommended)

1. Update the version number in `pyproject.toml`
2. Update `CHANGELOG.md` with the new version and changes
3. Commit the changes to the main branch
4. Create and push a git tag with the format `hf-local-vX.Y.Z`:
   ```bash
   git tag hf-local-v1.0.0
   git push origin hf-local-v1.0.0
   ```
5. The GitHub Actions workflow will automatically:
   - Build the package
   - Run twine check
   - Publish to PyPI

### Manual Release

If you need to release manually:

1. Navigate to the package directory:
   ```bash
   cd src/open_ticket_ai_hf_local
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Check the package:
   ```bash
   twine check dist/*
   ```

4. Upload to PyPI:
   ```bash
   twine upload dist/*
   ```

   You will be prompted for your PyPI credentials or can set them as environment variables:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=your-pypi-token
   twine upload dist/*
   ```

## Testing Before Release

Before releasing, test the package locally:

1. Build the package:
   ```bash
   cd src/open_ticket_ai_hf_local
   python -m build --no-isolation
   ```

2. Install in a test environment:
   ```bash
   pip install dist/open_ticket_ai_hf_local-*.whl
   ```

3. Run the tests:
   ```bash
   pytest tests/
   ```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward-compatible manner
- PATCH version for backward-compatible bug fixes

## After Release

1. Verify the package appears on PyPI: https://pypi.org/project/open-ticket-ai-hf-local/
2. Test installation from PyPI:
   ```bash
   pip install open-ticket-ai-hf-local
   ```
3. Update documentation if needed
4. Announce the release (optional)
