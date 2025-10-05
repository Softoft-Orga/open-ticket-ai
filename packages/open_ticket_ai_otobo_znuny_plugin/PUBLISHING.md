# Publishing the OTOBO/Znuny Plugin to PyPI

This document describes how to publish the `open-ticket-ai-otobo-znuny-plugin` package to PyPI.

## Prerequisites

### 1. PyPI Account Setup

1. Create an account on [PyPI](https://pypi.org/account/register/)
2. Enable 2FA (Two-Factor Authentication)
3. Create an API token:
   - Go to Account Settings → API tokens
   - Create a token with scope "Entire account" or project-specific
   - Save the token securely (starts with `pypi-`)

### 2. Test PyPI (Optional but Recommended)

1. Create an account on [Test PyPI](https://test.pypi.org/account/register/)
2. Create an API token for testing
3. Test deployments here before publishing to production PyPI

### 3. GitHub Secrets

Add the following secrets to the GitHub repository (Settings → Secrets → Actions):

- `PYPI_API_TOKEN` - Your PyPI API token (for production)
- `TEST_PYPI_API_TOKEN` - Your Test PyPI API token (for testing)

Alternatively, configure Trusted Publishing (see below).

## Publishing Methods

### Method 1: Automated via GitHub Actions (Recommended)

The repository includes a GitHub Actions workflow that automatically builds and publishes the package.

#### Publishing to Production PyPI

1. Update the version in `packages/open_ticket_ai_otobo_znuny_plugin/pyproject.toml`
2. Update `CHANGELOG.md` with release notes
3. Commit changes:
   ```bash
   git add packages/open_ticket_ai_otobo_znuny_plugin/pyproject.toml
   git add packages/open_ticket_ai_otobo_znuny_plugin/CHANGELOG.md
   git commit -m "Bump version to X.Y.Z"
   git push
   ```
4. Create and push a tag:
   ```bash
   git tag -a otobo-znuny-plugin-vX.Y.Z -m "Release version X.Y.Z"
   git push origin otobo-znuny-plugin-vX.Y.Z
   ```
5. The GitHub Action will automatically:
   - Build the package
   - Run checks
   - Publish to PyPI

#### Publishing to Test PyPI

Use the manual workflow dispatch:

1. Go to Actions → "Build and Publish OTOBO/Znuny Plugin"
2. Click "Run workflow"
3. Set "Publish to PyPI" to `false`
4. Click "Run workflow"

This will publish to Test PyPI for testing.

### Method 2: Manual Publishing

#### Build the Package

```bash
cd packages/open_ticket_ai_otobo_znuny_plugin

# Install build tools
pip install build twine

# Build the package
python -m build
```

This creates:
- `dist/open_ticket_ai_otobo_znuny_plugin-X.Y.Z.tar.gz` (source distribution)
- `dist/open_ticket_ai_otobo_znuny_plugin-X.Y.Z-py3-none-any.whl` (wheel)

#### Check the Package

```bash
twine check dist/*
```

#### Upload to Test PyPI (Testing)

```bash
twine upload --repository testpypi dist/*
```

Then test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ open-ticket-ai-otobo-znuny-plugin
```

#### Upload to Production PyPI

```bash
twine upload dist/*
```

When prompted, enter:
- Username: `__token__`
- Password: Your PyPI API token (including the `pypi-` prefix)

## Trusted Publishing (Recommended for Production)

Trusted Publishing eliminates the need for API tokens by using OpenID Connect (OIDC).

### Setup Steps

1. Go to [PyPI](https://pypi.org/) and sign in
2. Go to your project (or create it with the first manual upload)
3. Navigate to "Manage" → "Publishing"
4. Click "Add a new publisher"
5. Fill in the form:
   - **PyPI Project Name**: `open-ticket-ai-otobo-znuny-plugin`
   - **Owner**: `Softoft-Orga`
   - **Repository name**: `open-ticket-ai`
   - **Workflow name**: `publish-otobo-znuny-plugin.yml`
   - **Environment name**: (leave blank)

6. Save the publisher

Now the GitHub Action can publish without needing an API token!

## Version Management

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes (e.g., 2.0.0)
- **MINOR**: New functionality, backward compatible (e.g., 1.1.0)
- **PATCH**: Bug fixes, backward compatible (e.g., 1.0.1)

### Version Bumping

1. Update `version` in `pyproject.toml`
2. Update `CHANGELOG.md` with changes
3. Commit and create a git tag matching the version

## Release Checklist

- [ ] All tests pass locally
- [ ] Version updated in `pyproject.toml`
- [ ] `CHANGELOG.md` updated with changes
- [ ] Committed all changes
- [ ] Created and pushed git tag `otobo-znuny-plugin-vX.Y.Z`
- [ ] GitHub Action completed successfully
- [ ] Package appears on [PyPI](https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/)
- [ ] Test installation: `pip install open-ticket-ai-otobo-znuny-plugin==X.Y.Z`
- [ ] Documentation updated (if needed)
- [ ] Create GitHub Release with release notes

## Troubleshooting

### Build Failures

Check:
- Python version (must be 3.13+)
- All dependencies are properly specified in `pyproject.toml`
- `README.md` exists and is valid Markdown
- All source files have valid Python syntax

### Upload Failures

Check:
- API token is correct and has appropriate permissions
- Package name is not already taken (for first release)
- Version number hasn't been published before (PyPI doesn't allow re-uploading)
- Network connectivity to PyPI

### Import Errors After Installation

Check:
- Package structure matches setuptools expectations
- `__init__.py` files exist in all package directories
- Dependencies are installed: `pip install open-ticket-ai-otobo-znuny-plugin[dev]`

## Post-Release

After a successful release:

1. Announce the release in appropriate channels
2. Update main project documentation if needed
3. Monitor for issues and bug reports
4. Plan next release based on feedback

## Links

- [PyPI Project Page](https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/)
