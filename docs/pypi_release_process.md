# PyPI Package Release Process

This document describes how to release packages to PyPI.

## Overview

The repository contains three Python packages that are published to PyPI:

1. **open-ticket-ai** - Core package (published from repository root)
2. **open-ticket-ai-hf-local** - HuggingFace plugin (published from `src/open_ticket_ai_hf_local`)
3. **open-ticket-ai-otobo-znuny-plugin** - OTOBO/Znuny plugin (published from `src/open_ticket_ai_otobo_znuny_plugin`)

## Automated Release Workflow

All packages use GitHub Actions for automated building and publishing. The workflow:

1. Builds the package using `python -m build`
2. Validates the package with `twine check`
3. Publishes to PyPI using `twine upload`
4. Uploads build artifacts for inspection

## Prerequisites

Before releasing, ensure:

1. PyPI API tokens are configured as GitHub secrets:
   - `PYPI_API_TOKEN` for core package
   - `PYPI_API_TOKEN_HF_LOCAL` for HF Local plugin
   - `PYPI_API_TOKEN_OTOBO_ZNUNY` for OTOBO/Znuny plugin

2. Version numbers are updated in the appropriate `pyproject.toml` files

3. CHANGELOG is updated (if exists)

## Release Methods

### 1. Manual Trigger (Recommended for Testing)

Use the GitHub Actions UI to manually trigger a workflow:

1. Navigate to the Actions tab
2. Select the appropriate workflow
3. Click "Run workflow"
4. Check "Run in dry-run mode" for testing (builds but doesn't publish)
5. Review build artifacts if needed

### 2. Tag-Based Release

Create and push a version tag:

```bash
# Core package
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# HuggingFace plugin
git tag -a hf-local-v1.0.0 -m "Release HF Local plugin 1.0.0"
git push origin hf-local-v1.0.0

# OTOBO/Znuny plugin
git tag -a otobo-znuny-v1.0.0 -m "Release OTOBO/Znuny plugin 1.0.0"
git push origin otobo-znuny-v1.0.0
```

### 3. GitHub Release

Create a release through the GitHub UI, which automatically triggers publishing.

## Version Numbering

Follow semantic versioning:
- MAJOR.MINOR.PATCH for stable releases
- MAJOR.MINOR.PATCHrcN for release candidates
- MAJOR.MINOR.PATCHaN for alpha releases
- MAJOR.MINOR.PATCHbN for beta releases

## Local Testing

To test building a package locally:

```bash
# Install build tools
pip install build twine

# Build core package
cd /path/to/repo
python -m build

# Build plugin package
cd src/open_ticket_ai_hf_local
python -m build

# Check the built package
twine check dist/*
```

## Troubleshooting

### Build Failures

If a build fails:
1. Check the GitHub Actions logs
2. Verify `pyproject.toml` syntax
3. Ensure all required files are included
4. Test the build locally

### Publishing Failures

If publishing fails:
1. Verify PyPI API tokens are correctly configured
2. Check if the version already exists on PyPI
3. Ensure the package name is available

### Version Conflicts

Each package version can only be published once to PyPI. If you need to re-release:
1. Increment the version number
2. Create a new tag
3. Trigger the workflow again

## Package Structure

Each package follows this structure:

```
package_name/
├── pyproject.toml    # Package metadata and dependencies
├── README.md         # Package description for PyPI
├── __init__.py       # Package initialization
└── *.py             # Package modules
```

## Post-Release

After a successful release:

1. Verify the package appears on PyPI
2. Test installation: `pip install package-name`
3. Update documentation if needed
4. Announce the release to users

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
