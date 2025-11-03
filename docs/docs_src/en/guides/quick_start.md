---
description: Get started with Open Ticket AI in 5 minutes. Quick setup guide for Python 3.13+ with OTOBO, Znuny, or OTRS ticket system integration.
---

# Quick Start Guide

Get started with Open Ticket AI in 5 minutes.

## Prerequisites

- Python 3.13+
- Access to an OTOBO, Znuny, or OTRS instance
- API token or credentials for your ticket system

## Installation

### Install Core Package

```bash
# Using uv (recommended)
uv pip install open-ticket-ai

# Or using pip
pip install open-ticket-ai
```

### Install Plugins

```bash
# Install OTOBO/Znuny plugin
uv pip install otai-otobo-znuny

# Install HuggingFace plugin (for ML)
uv pip install otai-hf-local

# Or install the complete bundle
uv pip install open-ticket-ai[all]
```

## First Configuration

### 1. Set Environment Variables

```bash
export OTOBO_BASE_URL="https://your-ticket-system.com"
export OTOBO_API_TOKEN="your-api-token"
```

### 2. Create Configuration File

Create `config.yml`:

```yaml
# Load plugins
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"

# Configure pipeline
orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000  # Run every 60 seconds
      pipes:
        # Fetch open tickets
        - pipe_name: fetch_tickets
          search:
            StateType: "Open"
            limit: 10

        # Log tickets (for testing)
        - pipe_name: log_tickets
```

## Running Your First Pipeline

```bash
# Run the pipeline
open-ticket-ai run --config config.yml

# Or with verbose logging
open-ticket-ai run --config config.yml --log-level DEBUG
```

You should see output like:

```
[INFO] Loading configuration from config.yml
[INFO] Initializing plugins...
[INFO] Starting orchestrator...
[INFO] Running pipeline: classify_tickets
[INFO] Fetched 10 tickets
[INFO] Pipeline completed successfully
```

## Next Steps

### Add Classification

Update your config to classify tickets:

```yaml
orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
          search:
            StateType: "Open"
            limit: 10

        # Add ML classification
        - pipe_name: classify_queue
          model_name: "bert-base-uncased"

        # Update tickets
        - pipe_name: update_ticket
          fields:
            QueueID: "{{ context.predicted_queue_id }}"
```

### Explore Examples

Check out complete examples:

```bash
# List available configExamples
ls docs/raw_en_docs/config_examples/

# Try the queue classification example
cp docs/raw_en_docs/config_examples/queue_classification.yml config.yml
open-ticket-ai run --config config.yml
```

### Learn More

- [Installation Guide](installation.md) - Detailed installation instructions
- [First Pipeline Tutorial](first_pipeline.md) - Step-by-step pipeline creation
- [Configuration Reference](../details/_config_reference.md) - Complete config docs
- [Available Plugins](../plugins/plugin_system.md) - Plugin documentation

## Common Issues

### Connection Error

```
Error: Failed to connect to ticket system
```

**Solution**: Verify `OTOBO_BASE_URL` is correct and accessible.

### Authentication Error

```
Error: 401 Unauthorized
```

**Solution**: Check that `OTOBO_API_TOKEN` is valid and has required permissions.

### Plugin Not Found

```
Error: Plugin 'otobo_znuny' not found
```

**Solution**: Install the plugin:

```bash
uv pip install otai-otobo-znuny
```

## Getting Help

- [Troubleshooting Guide](troubleshooting.md)
- [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- [Documentation](../README.md)

## What's Next?

Now that you have Open Ticket AI running:

1. **Customize Configuration**: Adapt to your workflow
2. **Add More Pipes**: Enhance functionality
3. **Monitor Performance**: Track classification accuracy
4. **Scale Up**: Process more tickets
5. **Contribute**: Share your experience and improvements
