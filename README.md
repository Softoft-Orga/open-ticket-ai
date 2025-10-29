# Open Ticket AI

Open Ticket AI is an intelligent ticket classification and routing system that uses machine learning to automatically
categorize and prioritize support tickets.

- User documentation main page: https://open-ticket-ai.com
- User installation guide: https://open-ticket-ai.com/users/installation
- Developer documentation: https://open-ticket-ai.com/developers/

## CI/CD Automation

The repository includes automated workflows for handling Copilot-generated Pull Requests. When GitHub Copilot creates a
PR that fails CI checks, the workflow automatically labels it with `retry-needed` and `copilot-pr`, posts a comment
explaining the failures, and closes the PR to allow Copilot to retry with fixes. This automation only affects PRs
created by `github-copilot[bot]` and has no impact on manually created PRs.

## Quick Start

```bash
# Install core package
pip install open-ticket-ai

# Install with plugins
pip install open-ticket-ai otai-hf-local otai-otobo-znuny
```

## Docker

```bash
docker pull openticketai/engine:latest
```

### Docker Compose

```yaml
services:
  open-ticket-ai:
    image: openticketai/engine:latest
    ports:
      - "8080:8080"
    environment:
      OT_AI_CONFIG: /app/config.yml
    volumes:
      - ./config.yml:/app/config.yml:ro
```

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

### Create Release

```bash
./scripts/bump_version
git push origin <your-branch>
```

Open a pull request targeting the `main` branch after pushing your changes. The release workflow runs once the pull
request is merged.

## Documentation

Full documentation: https://open-ticket-ai.com

## Contributing

The easiest way to extend Open Ticket AI is by creating a plugin. Explore the developer documentation to learn how to
build and integrate new capabilities.

## License

LGPL-2.1-only
