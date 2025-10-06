# Quick Start Guide for PyPI Publishing

This guide helps you get started with the automated PyPI publishing system.

## ⚡ Quick Setup (5 minutes)

### 1. Configure PyPI Tokens

Create three PyPI API tokens at https://pypi.org/manage/account/token/:

| Token Name | Scope | For Package |
|------------|-------|-------------|
| `open-ticket-ai-github-actions` | Project: open-ticket-ai | Core package |
| `open-ticket-ai-hf-local-github-actions` | Project: open-ticket-ai-hf-local | HF plugin |
| `open-ticket-ai-otobo-znuny-plugin-github-actions` | Project: open-ticket-ai-otobo-znuny-plugin | OTOBO plugin |

### 2. Add GitHub Secrets

Go to: **Repository Settings → Secrets and variables → Actions**

Add these secrets:
- `PYPI_API_TOKEN` → token for core package
- `PYPI_API_TOKEN_HF_LOCAL` → token for HF plugin
- `PYPI_API_TOKEN_OTOBO_ZNUNY` → token for OTOBO plugin

### 3. Test with Dry-Run

1. Go to **Actions** tab
2. Select "Publish open-ticket-ai to PyPI"
3. Click **Run workflow**
4. ✅ Check "Run in dry-run mode"
5. Click **Run workflow**
6. Wait for completion
7. Check build artifacts

Repeat for the other two packages.

### 4. First Real Release

Once dry-runs succeed:

```bash
# Update version in pyproject.toml (if needed)
git add pyproject.toml
git commit -m "Bump version to 1.0.0"
git push

# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Workflow automatically runs and publishes to PyPI
```

### 5. Verify on PyPI

Check your packages:
- https://pypi.org/project/open-ticket-ai/
- https://pypi.org/project/open-ticket-ai-hf-local/
- https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/

## 🚀 Release Methods

### Method 1: Tag (Automatic)
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

### Method 2: Manual (GitHub UI)
1. Actions → Select workflow → Run workflow

### Method 3: GitHub Release (Automatic)
Create release through GitHub UI

## 📦 Package-Specific Tags

Each package has its own tag patterns:

```bash
# Core package
git tag v1.0.0

# HF Local plugin
git tag hf-local-v1.0.0

# OTOBO/Znuny plugin
git tag otobo-znuny-v1.0.0
```

## 🔍 Troubleshooting

### Build fails?
- Check GitHub Actions logs
- Verify pyproject.toml syntax
- Test build locally: `python -m build`

### Publish fails?
- Verify secrets are set correctly
- Check if version already exists on PyPI
- Review PyPI token permissions

### Version conflict?
- Increment version in pyproject.toml
- Create new tag
- Re-run workflow

## 📚 Documentation

For detailed information, see:

- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Complete setup guide
- [pypi_release_process.md](pypi_release_process.md) - Release process
- [workflow_architecture.md](workflow_architecture.md) - Technical details
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What was built

## 🎯 Next Steps

After your first successful release:

1. ✅ Test installation: `pip install open-ticket-ai`
2. ✅ Verify package metadata on PyPI
3. ✅ Update project documentation
4. ✅ Announce the release

## ⚠️ Important Notes

- Each version can only be published **once** to PyPI
- Always test with **dry-run mode** first
- Keep PyPI tokens **secure** (never commit them)
- Update version in pyproject.toml **before** releasing
- Plugin packages depend on the core package (publish core first)

## 🆘 Support

Having issues?
1. Review the documentation in `docs/`
2. Check GitHub Actions logs for errors
3. Open an issue with details

---

**Ready to publish?** Start with a dry-run test! 🚀
