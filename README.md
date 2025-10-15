# Open Ticket AI

AI-powered ticket processing and automation system.

## Quick Start

```bash
# Install core package
pip install open-ticket-ai

# Install with plugins
pip install open-ticket-ai otai-hf-local otai-otobo-znuny
```

## Docker

```bash
# Core only
docker pull ghcr.io/softoft-orga/open-ticket-ai:core-latest

# With all plugins
docker pull ghcr.io/softoft-orga/open-ticket-ai:all-latest
```

Available variants: `core`, `hf_local`, `otobo_znuny`, `all`

## Development

```bash
# Clone and setup
git clone https://github.com/Softoft-Orga/open-ticket-ai.git
cd open-ticket-ai
uv sync

# Run tests
uv run -m pytest
```

## Releasing

### Update Version

```bash
# Set version across all packages
python scripts/set_version.py 1.0.18
git add .
git commit -m "chore: bump version to 1.0.18"
git push
```

### Create Release

```bash
# Tag and push (triggers automatic release)
git tag v1.0.18
git push origin v1.0.18
```

The workflow automatically:
- Sets all package versions to match
- Builds and publishes to PyPI via OIDC
- Builds 4 Docker image variants (multi-platform)

### PyPI Setup (one-time)

Configure [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) for each package:
- Publisher: GitHub
- Owner: `Softoft-Orga`
- Repository: `open-ticket-ai`
- Workflow: `release.yml`

Required for: `open-ticket-ai`, `otai-hf-local`, `otai-otobo-znuny`

## Documentation

Full documentation: https://open-ticket-ai.com

## License

LGPL-2.1-only
