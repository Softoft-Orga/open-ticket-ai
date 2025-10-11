# PyPI Publishing Setup Instructions

This document provides step-by-step instructions for setting up automated PyPI publishing for the Open Ticket AI packages.

## Prerequisites

- Repository admin access to configure secrets
- PyPI account with permissions to create projects

## Step 1: Create PyPI API Tokens

For each package, you need to create a PyPI API token:

### 1.1 Core Package (open-ticket-ai)

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `open-ticket-ai-github-actions`
4. Scope: Select "Project" and choose `open-ticket-ai` (create the project first if it doesn't exist)
5. Click "Add token"
6. **IMPORTANT**: Copy the token immediately (it won't be shown again)

### 1.2 HuggingFace Plugin (open-ticket-ai-hf-local)

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `open-ticket-ai-hf-local-github-actions`
4. Scope: Select "Project" and choose `open-ticket-ai-hf-local`
5. Click "Add token"
6. Copy the token

### 1.3 OTOBO/Znuny Plugin (open-ticket-ai-otobo-znuny-plugin)

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `open-ticket-ai-otobo-znuny-plugin-github-actions`
4. Scope: Select "Project" and choose `open-ticket-ai-otobo-znuny-plugin`
5. Click "Add token"
6. Copy the token

## Step 2: Add Secrets to GitHub Repository

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add the following secrets:

### Secret 1: PYPI_API_TOKEN
- Name: `PYPI_API_TOKEN`
- Value: The token from Step 1.1 (core package)

### Secret 2: PYPI_API_TOKEN_HF_LOCAL
- Name: `PYPI_API_TOKEN_HF_LOCAL`
- Value: The token from Step 1.2 (HF Local plugin)

### Secret 3: PYPI_API_TOKEN_OTOBO_ZNUNY
- Name: `PYPI_API_TOKEN_OTOBO_ZNUNY`
- Value: The token from Step 1.3 (OTOBO/Znuny plugin)

## Step 3: Verify Workflow Configuration

The workflows are already configured in `.github/workflows/`:
- `publish-to-pypi.yml` - Reusable workflow for building and publishing
- `publish-open-ticket-ai.yml` - Triggers for core package
- `publish-hf-local.yml` - Triggers for HF Local plugin
- `publish-otobo-znuny.yml` - Triggers for OTOBO/Znuny plugin

## Step 4: Test with Dry-Run

Before publishing to PyPI, test the workflow:

1. Go to **Actions** tab in GitHub
2. Select one of the publish workflows (e.g., "Publish open-ticket-ai to PyPI")
3. Click **Run workflow**
4. Check the "Run in dry-run mode" option
5. Click **Run workflow**
6. Monitor the workflow execution
7. Review build artifacts to ensure packages are built correctly

## Step 5: First Release

### Option A: Manual Trigger (Recommended)

1. Update version in appropriate `pyproject.toml`
2. Commit and push changes
3. Go to **Actions** → Select workflow → **Run workflow**
4. Leave "dry-run mode" unchecked
5. Click **Run workflow**

### Option B: Tag-Based Release

1. Update version in `pyproject.toml`
2. Commit changes
3. Create and push a tag:
   ```bash
   git tag -a v1.0.0rc1 -m "Release v1.0.0rc1"
   git push origin v1.0.0rc1
   ```
4. Workflow automatically triggers

### Option C: GitHub Release

1. Create a new release through GitHub UI
2. Workflow automatically triggers on release publication

## Troubleshooting

### Token Authentication Errors

If you see authentication errors:
- Verify the token is correctly copied (no extra spaces)
- Check token hasn't expired
- Ensure token has correct project scope

### Package Already Exists

Each version can only be uploaded once. To resolve:
1. Increment version in `pyproject.toml`
2. Commit and retrigger workflow

### Build Failures

Common causes:
- Missing dependencies in `pyproject.toml`
- Syntax errors in `pyproject.toml`
- Missing required files (README.md, __init__.py)

Check the workflow logs for detailed error messages.

## Security Best Practices

1. **Never commit tokens** to the repository
2. **Use project-scoped tokens** instead of account-wide tokens
3. **Rotate tokens periodically** (e.g., annually)
4. **Monitor token usage** in PyPI account settings
5. **Revoke tokens** if compromised

## Maintenance

### Updating Versions

Before each release:
1. Update version in the appropriate `pyproject.toml` file
2. Update CHANGELOG (if exists)
3. Commit changes
4. Create tag or trigger workflow

### Revoking and Replacing Tokens

If a token needs to be replaced:
1. Create a new token on PyPI
2. Update the corresponding secret in GitHub
3. Revoke the old token on PyPI

## References

- [PyPI API Tokens](https://pypi.org/help/#apitoken)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Python Packaging Guide](https://packaging.python.org/)

## Support

For issues or questions:
1. Check workflow logs in GitHub Actions
2. Review [docs/pypi_release_process.md](pypi_release_process.md)
3. Open an issue in the repository
