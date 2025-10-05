# Quick Start Guide: First Release to PyPI

This is a quick reference for publishing the first release of `open-ticket-ai-otobo-znuny-plugin` to PyPI.

## Prerequisites Checklist

- [ ] PyPI account created at https://pypi.org/account/register/
- [ ] Two-factor authentication enabled on PyPI
- [ ] API token generated (or trusted publishing configured)
- [ ] GitHub secret `PYPI_API_TOKEN` added (if using API token)

## Release Steps

### 1. Pre-Release Validation

```bash
# Validate package can be built
cd packages/open_ticket_ai_otobo_znuny_plugin
python -m pip install build twine --quiet
python -m build

# Check package
twine check dist/*
```

### 2. Create Release

```bash
# From repository root
cd /path/to/open-ticket-ai

# Ensure you're on the correct branch
git checkout main  # or dev, depending on workflow

# Pull latest changes
git pull origin main

# Create and push tag
git tag -a otobo-znuny-plugin-v1.0.0 -m "Release version 1.0.0 - First PyPI release"
git push origin otobo-znuny-plugin-v1.0.0
```

### 3. Monitor GitHub Action

1. Go to: https://github.com/Softoft-Orga/open-ticket-ai/actions
2. Watch for "Build and Publish OTOBO/Znuny Plugin" workflow
3. Check that it completes successfully
4. Review the build log if any issues occur

### 4. Verify on PyPI

1. Visit: https://pypi.org/project/open-ticket-ai-otobo-znuny-plugin/
2. Confirm version 1.0.0 appears
3. Check that README renders correctly
4. Review package metadata

### 5. Test Installation

```bash
# Create a test virtual environment
python -m venv test-env
source test-env/bin/activate  # or test-env\Scripts\activate on Windows

# Install from PyPI
pip install open-ticket-ai-otobo-znuny-plugin

# Test import
python -c "from open_ticket_ai_otobo_znuny_plugin import OTOBOZnunyTicketSystemService; print('Success!')"

# Clean up
deactivate
rm -rf test-env
```

### 6. Create GitHub Release

1. Go to: https://github.com/Softoft-Orga/open-ticket-ai/releases/new
2. Select tag: `otobo-znuny-plugin-v1.0.0`
3. Title: `OTOBO/Znuny Plugin v1.0.0`
4. Description (example):

```markdown
## OTOBO/Znuny Plugin v1.0.0 - First PyPI Release

The OTOBO/Znuny ticket system integration plugin is now available as a standalone PyPI package! 🎉

### Installation

```bash
pip install open-ticket-ai-otobo-znuny-plugin
```

Or install with Open Ticket AI:

```bash
pip install open-ticket-ai[otobo-znuny]
```

### What's New

- First standalone release on PyPI
- Integration with OTOBO, Znuny, and OTRS ticket systems
- Support for ticket search, update, and note operations
- Comprehensive documentation and developer guides

### Documentation

- [README](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/packages/open_ticket_ai_otobo_znuny_plugin/README.md)
- [Developer Guide](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/packages/open_ticket_ai_otobo_znuny_plugin/DEVELOPER.md)
- [Full Documentation](https://open-ticket-ai.com/en/guide/available-plugins.html)

### Package Details

- Package name: `open-ticket-ai-otobo-znuny-plugin`
- Version: 1.0.0
- Python: >=3.13
- License: LGPL-2.1-only

**Full Changelog**: See [CHANGELOG.md](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/packages/open_ticket_ai_otobo_znuny_plugin/CHANGELOG.md)
```

5. Attach build artifacts (optional)
6. Click "Publish release"

## Troubleshooting

### Build Fails

**Check**:
- GitHub Actions has necessary permissions
- Secrets are properly configured
- pyproject.toml is valid

### Upload to PyPI Fails

**Common issues**:
- Package name already taken (unlikely for first release)
- API token invalid or expired
- Network/connectivity issues

**Solutions**:
- Verify token is correct in GitHub secrets
- Check PyPI status page
- Try manual upload: `cd packages/open_ticket_ai_otobo_znuny_plugin && twine upload dist/*`

### Installation from PyPI Fails

**Check**:
- Wait 1-2 minutes after publishing (PyPI CDN propagation)
- Use `pip install --no-cache-dir` to bypass cache
- Verify package name spelling

## Post-Release

- [ ] Announce on project website/blog
- [ ] Update main project documentation
- [ ] Share on relevant communities/forums
- [ ] Monitor GitHub issues for feedback
- [ ] Plan next release based on feedback

## Need Help?

- GitHub Issues: https://github.com/Softoft-Orga/open-ticket-ai/issues
- Documentation: https://open-ticket-ai.com
- Email: tab@softoft.de

---

**Note**: This is a one-time setup guide. For subsequent releases, you only need to:
1. Update version and CHANGELOG
2. Create and push new tag
3. GitHub Actions handles the rest automatically
