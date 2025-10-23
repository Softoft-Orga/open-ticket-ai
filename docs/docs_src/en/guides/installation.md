---
description: Detailed installation guide for Open Ticket AI with system requirements, Python setup, Docker deployment, and ML model configuration.
---

# TOODO DOcker Compose to install version with the 3 plugins installed. for not wanting all currently with pip uv nstallation.

but in the future. other docker images and beter installation scripts.
The hardware depends mostly on what AI you want to run. As such the OpenTicketAI can run on 512MB RAM systems if no ML
models are used.

# Installation Guide

Detailed installation instructions for Open Ticket AI and its components.

## System Requirements

### Minimum Requirements

- **Python**: 3.13 or higher
- **RAM**: 2 GB minimum, 4 GB recommended
- **Disk Space**: 500 MB for core, additional for models
- **OS**: Linux, macOS, or Windows

### Recommended for ML

- **RAM**: 8 GB or more
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **Disk Space**: 5 GB+ for model storage

## Core Package Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Open Ticket AI
uv pip install open-ticket-ai
```

### Using pip

```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install Open Ticket AI
pip install open-ticket-ai
```

### From Source

```bash
# Clone repository
git clone https://github.com/Softoft-Orga/open-ticket-ai.git
cd open-ticket-ai

# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Plugin Installation

### OTOBO/Znuny Plugin

```bash
# Install OTOBO/Znuny integration
uv pip install otai-otobo-znuny
```

Features:

- Ticket fetching and updating
- Custom field support
- API authentication

### HuggingFace Local Plugin

```bash
# Install HuggingFace plugin
uv pip install otai-hf-local
```

Features:

- Local ML model inference
- Support for classification models
- GPU acceleration

## Bundle Installation

Install everything at once:

```bash
# Install all plugins
uv pip install open-ticket-ai[all]

# Or specific combinations
uv pip install open-ticket-ai[otobo,ml]
```

Available bundles:

- `all`: All plugins
- `otobo`: OTOBO/Znuny integration
- `ml`: Machine learning plugins
- `dev`: Development dependencies

## Verification

Verify installation:

```bash
# Check version
open-ticket-ai --version

# List installed plugins
open-ticket-ai plugins list

# Show system info
open-ticket-ai info
```

Expected output:

```
Open Ticket AI version 2.0.0
Python 3.13.0

Installed plugins:
  - otobo_znuny (v1.5.0)
  - hf_local (v1.0.0)
```

## Development Setup

For contributing or customization:

### Clone Repository

```bash
git clone https://github.com/Softoft-Orga/open-ticket-ai.git
cd open-ticket-ai
```

### Install Dependencies

```bash
# Install with development dependencies
uv sync --all-extras

# Or specific groups
uv sync --group dev --group test
```

### Setup Pre-commit Hooks

```bash
# Install pre-commit
uv pip install pre-commit

# Install hooks
pre-commit install
```

### Run Tests

```bash
# Run all tests
uv run -m pytest

# Run with coverage
uv run -m pytest --cov=open_ticket_ai

# Run specific tests
uv run -m pytest tests/unit/
```

## Configuration

### Environment Setup

Create `.env` file:

```bash
# Ticket System
OTOBO_BASE_URL=https://your-ticket-system.com
OTOBO_API_TOKEN=your-api-token

# Application
LOG_LEVEL=INFO
ENVIRONMENT=production

# ML (optional)
HF_HOME=/path/to/model/cache
```

### Configuration File

Create `config.yml`:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"

infrastructure:
  log_level: "${LOG_LEVEL}"

orchestrator:
  pipelines:
    - name: main_pipeline
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
```

## GPU Support (Optional)

### Install CUDA

For NVIDIA GPU support:

```bash
# Check if CUDA is available
nvidia-smi

# Install PyTorch with CUDA support
uv pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Verify GPU

```python
import torch

print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0)}")
```

## Docker Installation

### Using Docker

```bash
# Pull image
docker pull softoft/open-ticket-ai:latest

# Run container
docker run -d \
  --name open-ticket-ai \
  -e OTOBO_BASE_URL="https://your-system.com" \
  -e OTOBO_API_TOKEN="your-token" \
  -v $(pwd)/config.yml:/app/config.yml \
  softoft/open-ticket-ai:latest
```

### Using Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  open-ticket-ai:
    image: softoft/open-ticket-ai:latest
    environment:
      - OTOBO_BASE_URL=${OTOBO_BASE_URL}
      - OTOBO_API_TOKEN=${OTOBO_API_TOKEN}
      - LOG_LEVEL=INFO
    volumes:
      - ./config.yml:/app/config.yml
      - ./models:/app/models
    restart: unless-stopped
```

Run:

```bash
docker-compose up -d
```

## Upgrading

### Upgrade Core Package

```bash
# Using uv
uv pip install --upgrade open-ticket-ai

# Using pip
pip install --upgrade open-ticket-ai
```

### Upgrade Plugins

```bash
# Upgrade all
uv pip install --upgrade otai-otobo-znuny otai-hf-local

# Or upgrade everything
uv pip install --upgrade open-ticket-ai[all]
```

### Check for Breaking Changes

```bash
# Review changelog
open-ticket-ai changelog

# Check plugin compatibility
open-ticket-ai plugins check-compatibility
```

## Uninstallation

### Remove Package

```bash
# Uninstall core
uv pip uninstall open-ticket-ai

# Uninstall plugins
uv pip uninstall otai-otobo-znuny otai-hf-local
```

### Clean Cache

```bash
# Remove model cache
rm -rf ~/.cache/huggingface

# Remove configuration
rm -rf ~/.config/open-ticket-ai
```

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python --version

# Install Python 3.13
# Ubuntu/Debian
sudo apt install python3.13

# macOS with Homebrew
brew install python@3.13
```

### Permission Errors

```bash
# Install in user directory
pip install --user open-ticket-ai

# Or use virtual environment
python -m venv venv
source venv/bin/activate
pip install open-ticket-ai
```

### Network Issues

```bash
# Use proxy
pip install --proxy http://proxy:port open-ticket-ai

# Or specify index
pip install --index-url https://pypi.org/simple open-ticket-ai
```

## Related Documentation

- [Quick Start](quick_start.md)
- [First Pipeline](first_pipeline.md)
- [Configuration Reference](../details/config_reference.md)
- [Troubleshooting](troubleshooting.md)
