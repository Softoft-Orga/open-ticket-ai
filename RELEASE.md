# Release Workflow

This document describes the unified release workflow for Open Ticket AI.

## Overview

The release workflow publishes:
- **Core package**: `open-ticket-ai`
- **Plugins**: `otai-hf-local`, `otai-otobo-znuny`
- **Docker images**: 4 variants with different plugin combinations

All packages **always share the same version number** to ensure compatibility.

## Triggers

The workflow can be triggered in two ways:

1. **Manual trigger** (workflow_dispatch):
   - Go to Actions → Release → Run workflow
   - Uses the version from `pyproject.toml` files

2. **Tag push** (recommended):
   ```bash
   git tag v1.0.18
   git push origin v1.0.18
   ```
   - Tag must match pattern `v*.*.*` (e.g., `v1.0.18`)
   - Version in tag must match version in `pyproject.toml` files

## Version Management

### Setting a New Version

Use the provided script to update all packages at once:

```bash
python scripts/set_version.py 1.0.18
```

This updates:
- `pyproject.toml` (core)
- `packages/otai_hf_local/pyproject.toml`
- `packages/otai_otobo_znuny/pyproject.toml`

### Version Validation

The workflow automatically verifies:
1. All three packages have identical versions
2. If triggered by tag, the tag version matches package versions

If versions don't match, the workflow fails immediately.

## PyPI Publishing

### Trusted Publishing (OIDC)

The workflow uses **Trusted Publishers** for PyPI authentication:
- ✅ No API tokens needed
- ✅ More secure than token-based auth
- ✅ Automatic token generation per run

### Setup Requirements

Configure Trusted Publishers in PyPI for each package:

1. Go to pypi.org → Manage → Publishing
2. Add GitHub Actions as a trusted publisher:
   - **Owner**: `Softoft-Orga`
   - **Repository**: `open-ticket-ai`
   - **Workflow**: `release.yml`
   - **Environment**: `pypi`

Repeat for all three packages:
- `open-ticket-ai`
- `otai-hf-local`
- `otai-otobo-znuny`

## Docker Images

### Image Variants

Four variants are built and pushed to GitHub Container Registry:

| Variant | Tag Pattern | Includes |
|---------|-------------|----------|
| **core** | `{version}-core`, `core-latest` | Core package only |
| **hf_local** | `{version}-hf_local`, `hf_local-latest` | Core + HuggingFace plugin |
| **otobo_znuny** | `{version}-otobo_znuny`, `otobo_znuny-latest` | Core + OTOBO/Znuny plugin |
| **all** | `{version}-all`, `all-latest` | Core + all plugins |

### Image Building

Images are built from PyPI packages (not from repository code):

1. Uses the existing `/Dockerfile`
2. Installs packages via `uv add`
3. All packages installed at the same version
4. Multi-platform: `linux/amd64`, `linux/arm64`

### Using the Images

```bash
# Pull core-only image
docker pull ghcr.io/softoft-orga/open-ticket-ai:1.0.18-core

# Pull image with all plugins
docker pull ghcr.io/softoft-orga/open-ticket-ai:1.0.18-all

# Use latest
docker pull ghcr.io/softoft-orga/open-ticket-ai:all-latest
```

## Release Process

### Standard Release

1. **Update version** in all packages:
   ```bash
   python scripts/set_version.py 1.0.18
   git add .
   git commit -m "chore: bump version to 1.0.18"
   git push
   ```

2. **Create and push tag**:
   ```bash
   git tag v1.0.18
   git push origin v1.0.18
   ```

3. **Workflow executes automatically**:
   - Validates version consistency
   - Builds all packages
   - Publishes to PyPI via OIDC
   - Builds and pushes Docker images

### Emergency Manual Release

If you need to trigger manually without a tag:

1. Go to GitHub Actions → Release
2. Click "Run workflow"
3. Confirm the version in pyproject.toml is correct
4. Run

## Troubleshooting

### Version Mismatch Error

```
ERROR: All package versions must be identical!
```

**Solution**: Use `python scripts/set_version.py <version>` to sync all versions.

### Tag Version Mismatch

```
ERROR: Tag version (1.0.18) doesn't match package version (1.0.17)
```

**Solution**: Either:
- Update pyproject.toml versions to match the tag, OR
- Delete and recreate the tag with the correct version

### PyPI Publishing Fails

```
Error: Trusted publishing exchange failure
```

**Solution**: Verify Trusted Publisher configuration in PyPI:
- Check repository name is `open-ticket-ai`
- Check workflow name is `release.yml`
- Check environment is `pypi`

### Docker Build Fails

Check that packages were successfully published to PyPI before Docker builds start.

## Migration from Old Workflow

### Removed Components

- ❌ `scripts/publish-all.sh` (replaced by workflow)
- ❌ `deployment/Dockerfile` (moved to root)
- ❌ API token authentication (replaced by OIDC)
- ❌ `/publish-all` ChatOps command (use tags instead)

### What Stayed

- ✅ `Dockerfile` logic (now at root)
- ✅ Version enforcement (now stricter)
- ✅ Multi-platform builds
- ✅ GHCR publishing

## Security

### OIDC Benefits

- Tokens are short-lived (minutes)
- No long-term secrets stored
- Automatic rotation
- Per-run authentication

### Permissions

Workflow requires:
- `contents: write` - For creating releases/tags
- `packages: write` - For pushing Docker images
- `id-token: write` - For OIDC authentication

## References

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Docker metadata action](https://github.com/docker/metadata-action)
