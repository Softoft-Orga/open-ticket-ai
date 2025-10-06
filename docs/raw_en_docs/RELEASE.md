# Release Process and Versioning

## Versioning Strategy

### Core Package (open-ticket-ai)

The core package follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible Plugin API changes
- **MINOR**: New functionality, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

#### Plugin API Version

The core package defines a Plugin API version tracked in `tests/contract/test_plugin_contract.py` as `REQUIRED_CORE_API`. This version uses a simplified `MAJOR.MINOR` format:

- **MAJOR**: Breaking changes to plugin contract (register_pipes, register_services, metadata)
- **MINOR**: New plugin capabilities, backward-compatible

**Critical Rule**: When the Plugin API MAJOR version changes, the Core package MUST bump its MAJOR version.

### Plugin Packages

Each plugin maintains independent Semantic Versioning:

- **MAJOR**: Breaking changes to plugin's public API
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, backward-compatible

Plugins declare Core compatibility in two ways:

1. **Dependency Range** in `pyproject.toml`: `open-ticket-ai>=X.Y.Z,<NEXT_MAJOR>`
2. **core_api** field in plugin metadata: Must match Core's `REQUIRED_CORE_API`

### Version Compatibility Matrix

| Core Version | Plugin API | HF Local | OTOBO/Znuny | Notes |
|--------------|-----------|----------|-------------|-------|
| 1.0.0rc1     | 2.0       | 1.0.0rc1 | 1.0.0rc1    | Initial release |
| 1.x.x        | 2.0       | 1.x.x    | 1.x.x       | Compatible within 1.x series |
| 2.0.0        | 3.0       | 2.0.0    | 2.0.0       | Breaking API change (hypothetical) |

## Deprecation Policy

### Deprecating Features in Core

When deprecating functionality:

1. **Announce**: Add deprecation warning to function/class with `warnings.warn()`
2. **Document**: Update docs and CHANGELOG with deprecation notice
3. **Retain**: Keep deprecated code for minimum 1-2 MINOR releases
4. **Remove**: Only remove in next MAJOR version

Example timeline:
- Version 1.1.0: Feature marked deprecated
- Version 1.2.0: Still available with warnings
- Version 1.3.0: Still available (optional)
- Version 2.0.0: Feature removed

### Shim Compatibility Layers

For breaking Plugin API changes:

1. Provide shim/adapter in Core for 1-2 minor releases
2. Log deprecation warnings when shim is used
3. Document migration path in upgrade guide
4. Remove shim in next MAJOR version

## Workspace Management with uv

### Locking Dependencies

Lock the entire workspace to ensure reproducible builds:

```bash
uv lock
```

This creates/updates `uv.lock` with exact dependency versions for all packages in the workspace.

### Installing Dependencies

Development setup:

```bash
uv sync
```

CI/Production (locked versions):

```bash
uv sync --locked
```

The `--locked` flag ensures the exact versions from `uv.lock` are used, failing if `pyproject.toml` has changed.

### Updating Dependencies

Update all dependencies:

```bash
uv lock --upgrade
```

Update specific dependency:

```bash
uv lock --upgrade-package package-name
```

## Publishing Packages

### Preparation

1. **Update Version Numbers**
   - Core: `/pyproject.toml`
   - HF Local: `/src/open_ticket_ai_hf_local/pyproject.toml`
   - OTOBO/Znuny: `/src/open_ticket_ai_otobo_znuny_plugin/pyproject.toml`

2. **Update CHANGELOG**
   - Document all changes since last release
   - Follow Keep a Changelog format

3. **Verify Plugin Compatibility**
   - Run contract tests: `uv run pytest -m contract`
   - Ensure plugins' `core_api` matches Core's `REQUIRED_CORE_API`

4. **Lock Dependencies**
   ```bash
   uv lock
   ```

5. **Test Build Locally**
   ```bash
   # Core
   cd /path/to/repo
   uv build
   
   # Plugins
   cd src/otai_hf_local
   uv build
   
   cd ../otai_otobo_znuny
   uv build
   ```

### Publishing with uv

Each package is published independently from its directory:

#### Core Package

```bash
cd /path/to/repo
uv build
uv publish
```

#### HF Local Plugin

```bash
cd src/otai_hf_local
uv build
uv publish
```

#### OTOBO/Znuny Plugin

```bash
cd src/otai_otobo_znuny
uv build
uv publish
```

### Publishing via GitHub Actions

The repository includes automated publishing workflows:

#### Method 1: Tag-Based Release

```bash
# Core package
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0

# HF Local plugin
git tag -a hf-local-v1.0.0 -m "Release HF Local 1.0.0"
git push origin hf-local-v1.0.0

# OTOBO/Znuny plugin
git tag -a otobo-znuny-v1.0.0 -m "Release OTOBO/Znuny 1.0.0"
git push origin otobo-znuny-v1.0.0
```

#### Method 2: Manual Trigger

1. Go to GitHub Actions tab
2. Select appropriate workflow:
   - "Publish open-ticket-ai to PyPI"
   - "Publish open-ticket-ai-hf-local to PyPI"
   - "Publish open-ticket-ai-otobo-znuny-plugin to PyPI"
3. Click "Run workflow"
4. Optionally check "dry-run mode" to test without publishing

### PyPI API Tokens

Required GitHub secrets:
- `PYPI_API_TOKEN` - Core package
- `PYPI_API_TOKEN_HF_LOCAL` - HF Local plugin
- `PYPI_API_TOKEN_OTOBO_ZNUNY` - OTOBO/Znuny plugin

Create tokens at https://pypi.org/manage/account/token/ with project-specific scope.

## Release Checklist

### Pre-Release

- [ ] Update version in appropriate `pyproject.toml`
- [ ] Update CHANGELOG with release notes
- [ ] Verify Plugin API compatibility (if releasing Core)
- [ ] Update plugin `core_api` version (if Plugin API changed)
- [ ] Update dependency ranges in plugins (if needed)
- [ ] Run full test suite: `uv run pytest`
- [ ] Run contract tests: `uv run pytest -m contract`
- [ ] Run linter: `uv run ruff check .`
- [ ] Run type checker: `uv run mypy src/`
- [ ] Lock dependencies: `uv lock`
- [ ] Test build locally: `uv build`
- [ ] Test installation in clean environment

### Release Order

**Important**: Always release packages in this order:

1. **Core** (`open-ticket-ai`)
2. **Plugins** (can be parallel)
   - `open-ticket-ai-hf-local`
   - `open-ticket-ai-otobo-znuny-plugin`

This ensures plugins can correctly specify their Core dependency.

### Post-Release

- [ ] Verify packages on PyPI
- [ ] Test installation: `pip install package-name`
- [ ] Test plugin installation with Core
- [ ] Update documentation if needed
- [ ] Create GitHub Release with release notes
- [ ] Announce release (if significant)
