# PyPI Publishing Workflow Architecture

## Overview

This document describes the architecture of the automated PyPI publishing system for Open Ticket AI packages.

## Package Structure

```
open-ticket-ai/
├── pyproject.toml                           # Core package config
├── src/
│   ├── open_ticket_ai/                      # Core package
│   ├── open_ticket_ai_hf_local/            # HF Local plugin
│   │   ├── pyproject.toml                  # Plugin config
│   │   └── README.md                       # Plugin docs
│   └── open_ticket_ai_otobo_znuny_plugin/ # OTOBO plugin
│       ├── pyproject.toml                  # Plugin config
│       └── README.md                       # Plugin docs
└── .github/workflows/
    ├── publish-to-pypi.yml                 # Reusable workflow
    ├── publish-open-ticket-ai.yml          # Core trigger
    ├── publish-hf-local.yml                # HF trigger
    └── publish-otobo-znuny.yml            # OTOBO trigger
```

## Workflow Architecture

### Reusable Workflow (publish-to-pypi.yml)

This is the core workflow that handles building and publishing:

```
Input Parameters:
├── package-name (string)     - Name of the package
├── package-path (string)     - Path to package directory
└── dry-run (boolean)         - Whether to skip publishing

Secrets:
└── PYPI_API_TOKEN           - PyPI authentication token

Steps:
1. Checkout repository
2. Set up Python 3.13
3. Install build tools (build, twine)
4. Build package (python -m build)
5. Validate package (twine check)
6. Publish to PyPI (twine upload) OR show dry-run info
7. Upload build artifacts
```

### Package-Specific Workflows

Each package has its own trigger workflow that calls the reusable workflow:

#### 1. publish-open-ticket-ai.yml (Core Package)

```
Triggers:
├── release (published)
├── push (tags: v*, open-ticket-ai-v*)
└── workflow_dispatch (manual with dry-run option)

Parameters:
├── package-name: "open-ticket-ai"
├── package-path: "."
└── dry-run: false (true if manual dry-run)

Secret: PYPI_API_TOKEN
```

#### 2. publish-hf-local.yml (HuggingFace Plugin)

```
Triggers:
├── release (published)
├── push (tags: hf-local-v*, open-ticket-ai-hf-local-v*)
└── workflow_dispatch (manual with dry-run option)

Parameters:
├── package-name: "open-ticket-ai-hf-local"
├── package-path: "src/open_ticket_ai_hf_local"
└── dry-run: false (true if manual dry-run)

Secret: PYPI_API_TOKEN_HF_LOCAL
```

#### 3. publish-otobo-znuny.yml (OTOBO/Znuny Plugin)

```
Triggers:
├── release (published)
├── push (tags: otobo-znuny-v*, open-ticket-ai-otobo-znuny-v*)
└── workflow_dispatch (manual with dry-run option)

Parameters:
├── package-name: "open-ticket-ai-otobo-znuny-plugin"
├── package-path: "src/open_ticket_ai_otobo_znuny_plugin"
└── dry-run: false (true if manual dry-run)

Secret: PYPI_API_TOKEN_OTOBO_ZNUNY
```

## Trigger Flow Diagram

```
Tag Creation          Manual Trigger        GitHub Release
     |                     |                       |
     |                     |                       |
     v                     v                       v
┌─────────────────────────────────────────────────────┐
│        Package-Specific Workflow                    │
│  (publish-open-ticket-ai.yml, etc.)                 │
└─────────────────────────────────────────────────────┘
                        |
                        | calls with parameters
                        v
┌─────────────────────────────────────────────────────┐
│         Reusable Workflow                           │
│      (publish-to-pypi.yml)                          │
│                                                     │
│  Steps:                                             │
│  1. Setup Python                                    │
│  2. Install build tools                             │
│  3. Build package                                   │
│  4. Validate with twine                             │
│  5. Publish to PyPI (or dry-run)                    │
│  6. Upload artifacts                                │
└─────────────────────────────────────────────────────┘
                        |
                        v
                    PyPI.org
```

## Tag Naming Convention

Each package has its own tag prefix to trigger the appropriate workflow:

| Package | Tag Patterns | Examples |
|---------|-------------|----------|
| Core | `v*`, `open-ticket-ai-v*` | `v1.0.0`, `open-ticket-ai-v1.0.0` |
| HF Local | `hf-local-v*`, `open-ticket-ai-hf-local-v*` | `hf-local-v1.0.0` |
| OTOBO/Znuny | `otobo-znuny-v*`, `open-ticket-ai-otobo-znuny-v*` | `otobo-znuny-v1.0.0` |

## Security Model

```
GitHub Repository Secrets
├── PYPI_API_TOKEN              → open-ticket-ai package
├── PYPI_API_TOKEN_HF_LOCAL     → open-ticket-ai-hf-local package
└── PYPI_API_TOKEN_OTOBO_ZNUNY  → open-ticket-ai-otobo-znuny-plugin package

Each token is:
- Project-scoped (limited to one package)
- Encrypted in GitHub Secrets
- Only accessible to workflows
- Never exposed in logs
```

## Dependency Graph

```
open-ticket-ai (core)
        ↑
        ├──── open-ticket-ai-hf-local
        │     (depends on core + transformers)
        │
        └──── open-ticket-ai-otobo-znuny-plugin
              (depends on core + otobo-znuny)
```

**Note**: Plugin packages depend on the core package. Ensure the core package is published first or is already available on PyPI.

## Dry-Run Testing

Dry-run mode allows testing the build process without publishing:

```
Developer Action
    |
    v
GitHub Actions UI
    |
    | Select workflow
    | Check "dry-run mode"
    | Click "Run workflow"
    v
Workflow Executes
    |
    ├─ Builds package ✓
    ├─ Validates package ✓
    ├─ Shows what would be published ✓
    └─ Skips actual PyPI upload ✓
    |
    v
Review Build Artifacts
```

## Version Management

Each package maintains its own version in its `pyproject.toml`:

```
Core Package:          /pyproject.toml
HF Local Plugin:       /src/open_ticket_ai_hf_local/pyproject.toml
OTOBO/Znuny Plugin:    /src/open_ticket_ai_otobo_znuny_plugin/pyproject.toml
```

Versions can evolve independently, but plugins should specify compatible core versions.

## Build Artifacts

After each workflow run, the following artifacts are uploaded:

```
Artifacts (retained for 90 days)
├── open-ticket-ai-dist/
│   ├── open_ticket_ai-X.Y.Z.tar.gz      # Source distribution
│   └── open_ticket_ai-X.Y.Z-*.whl       # Wheel distribution
│
├── open-ticket-ai-hf-local-dist/
│   ├── open_ticket_ai_hf_local-X.Y.Z.tar.gz
│   └── open_ticket_ai_hf_local-X.Y.Z-*.whl
│
└── open-ticket-ai-otobo-znuny-plugin-dist/
    ├── open_ticket_ai_otobo_znuny_plugin-X.Y.Z.tar.gz
    └── open_ticket_ai_otobo_znuny_plugin-X.Y.Z-*.whl
```

## Monitoring and Debugging

### Workflow Status

Check workflow status at:
- GitHub Actions tab
- Status badges in README.md

### Build Logs

Access detailed logs:
1. GitHub Actions → Select workflow run
2. Click on job "build-and-publish"
3. Expand each step to view logs

### Package Verification

After publishing:
1. Check PyPI: https://pypi.org/project/{package-name}/
2. Test installation: `pip install {package-name}`
3. Verify version: `pip show {package-name}`

## Future Enhancements

Potential improvements:
- [ ] Automated version bumping
- [ ] CHANGELOG generation
- [ ] Pre-release testing on TestPyPI
- [ ] Automated documentation updates
- [ ] Release notes generation
- [ ] Multi-Python version testing
