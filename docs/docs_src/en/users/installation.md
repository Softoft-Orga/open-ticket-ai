---
description: Easy installation guide for Open Ticket AI using Docker Compose - the recommended method for production deployment with all plugins included.
---

# Installation Guide

This guide will help you install Open Ticket AI on your server. We recommend using Docker Compose
for the easiest and most reliable installation.

## System Requirements

The hardware requirements depend on which AI models you want to run:

- **Minimum (no ML models)**: 512 MB RAM, 1 GB disk space
- **Recommended (with ML models)**: 4 GB RAM, 5 GB disk space
- **Operating System**: Linux, Windows, or macOS with Docker installed

## Docker Compose Installation (Recommended)

**Docker Compose is the recommended way to install Open Ticket AI.** It's the easiest method and
comes with all three currently available plugins pre-installed:

- **Base Plugin** (`otai-base`): Core functionality
- **OTOBO/Znuny Plugin** (`otai-otobo-znuny`): Ticket system integration
- **HuggingFace Local Plugin** (`otai-hf-local`): Local AI model support

### What is Docker and Docker Compose?

**Docker** is a tool that packages software and all its dependencies into a container, so it runs
the same way on any computer. Think of it like a self-contained box with everything the application
needs to run.

**Docker Compose** is a tool that makes it easy to run Docker applications with a simple
configuration file. Instead of typing long commands, you just create one file and run one command.

### Step 1: Install Docker

If you don't have Docker installed yet:

**Linux (Ubuntu/Debian):**

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose-plugin
```

**Windows/macOS:**
Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Step 2: Create Configuration Files

Create a new folder for Open Ticket AI and create two files inside it:

<InlineExample slug="basics-minimal" />

**1. Create `compose.yml`:**

```yaml
services:
  open-ticket-ai:
    image: openticketai/engine:latest
    restart: "unless-stopped"
    environment:
      OTAI_TS_PASSWORD: "${OTAI_TS_PASSWORD}"
    volumes:
      - ./config.yml:/app/config.yml:ro
```

**What does this mean?**

- `image: openticketai/engine:latest` - Uses our pre-built image with all plugins
- `restart: "unless-stopped"` - Automatically restarts if it crashes
- `environment` - Configuration via environment variables
- `volumes` - Links your configuration file into the container

**2. Create `config.yml`:**

```yaml
open_ticket_ai:
  api_version: ">=1.0.0"
  plugins:
    - otai-base
    - otai-otobo-znuny
    - otai-hf-local

  infrastructure:
    logging:
      level: INFO

  services:
    otobo_znuny:
      use: "otobo_znuny:OTOBOZnunyClient"
      params:
        base_url: "https://your-ticket-system.com"
        username: "your-username"
        password: "${OTAI_TS_PASSWORD}"

  orchestrator:
    id: "main_orchestrator"
    use: "core:someOrchestrator"
    params:
      pipes:
        - id: "fetch_tickets"
          use: "otobo_znuny:FetchTickets"
```

**Important:** Replace `https://your-ticket-system.com` and `your-username` with your actual ticket
system details.

### Step 3: Start Open Ticket AI

In the folder where you created the files, run:

```bash
docker-compose up -d
```

**What does this do?**

- Downloads the Open Ticket AI image (only needed the first time)
- Starts the application in the background
- All three plugins are automatically available

### Step 4: Verify Installation

Check if Open Ticket AI is running:

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f open-ticket-ai
```

You should see output indicating the application started successfully.

### Step 5: Stop or Update

**Stop the application:**

```bash
docker-compose down
```

**Update to the latest version:**

```bash
docker-compose pull
docker-compose up -d
```

## Configuration with Environment Variables

You can configure Open Ticket AI using environment variables in your `docker-compose.yml`:

```yaml
services:
  open-ticket-ai:
    image: openticketai/engine:latest
    restart: "unless-stopped"
    environment:
      # Ticket System Credentials
      - OTAI_OPEN_TICKET_AI__SERVICES__OTOBO_ZNUNY__PARAMS__BASE_URL=https://your-system.com
      - OTAI_OPEN_TICKET_AI__SERVICES__OTOBO_ZNUNY__PARAMS__USERNAME=admin
      - OTAI_OPEN_TICKET_AI__SERVICES__OTOBO_ZNUNY__PARAMS__PASSWORD=secret

      # Logging Level
      - OTAI_OPEN_TICKET_AI__INFRASTRUCTURE__LOGGING__LEVEL=INFO
    volumes:
      - ./config.yml:/app/config.yml:ro
```

Environment variables override settings in `config.yml`, which is useful for sensitive information
like passwords.

## Alternative: Python Installation (Advanced Users)

If you prefer to install without Docker or need a development setup:

### Using pip/uv

```bash
# Install with all plugins
pip install open-ticket-ai[all]

# Or install selectively
pip install open-ticket-ai
pip install otai-otobo-znuny
pip install otai-hf-local
```

**Requirements:**

- Python 3.13 or higher
- pip or uv package manager

### Using uv (Faster)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Open Ticket AI with all plugins
uv pip install open-ticket-ai[all]
```

## Troubleshooting

### Docker Issues

**Container won't start:**

```bash
# Check logs for errors
docker-compose logs open-ticket-ai

# Restart the container
docker-compose restart
```

**Port already in use:**
If you get a port conflict error, add a port mapping to your `docker-compose.yml`:

```yaml
services:
  open-ticket-ai:
    image: openticketai/engine:latest
    ports:
      - "8080:8080"  # Change 8080 to an available port
    # ...rest of config
```

**Configuration not loading:**
Make sure your `config.yml` file is in the same folder as `docker-compose.yml` and has correct YAML
syntax.

### Connection Issues

**Can't connect to ticket system:**

1. Verify the `base_url` in your config is correct
2. Check that your ticket system is accessible from the server
3. Verify username and password are correct
4. Check firewall settings

**Test connection:**

```bash
# Test if ticket system is reachable
curl https://your-ticket-system.com

# Check Open Ticket AI logs
docker-compose logs -f open-ticket-ai
```

### Getting Help

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify your configuration file syntax
3. Review the [Configuration Reference](../details/_config_reference.md)
4. Visit our [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
5. Join our community discussions

## Next Steps

After installation:

1. **Configure your first pipeline** - See [First Pipeline Guide](first_pipeline.md)
2. **Connect to your ticket system** - See [OTOBO/Znuny Integration](../users/ticket_systems.md)
3. **Set up AI classification** - See [ML Model Configuration](../users/ml_models.md)
4. **Review security settings** - See [Security Best Practices](../users/security.md)

## Related Documentation

- [Quick Start Guide](quick_start.md) - Get started quickly
- [First Pipeline](first_pipeline.md) - Create your first automation
- [Configuration Reference](../details/_config_reference.md) - Complete config documentation
- [Plugin System](../users/plugins.md) - Understanding plugins
