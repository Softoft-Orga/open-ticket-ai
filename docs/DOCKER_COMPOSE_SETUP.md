# Docker Compose Setup for Prefect

This guide explains how to deploy Open Ticket AI with Prefect using Docker Compose.

## Overview

The Docker Compose setup includes:

- **postgres**: Database for Prefect metadata
- **redis**: Message broker for Prefect services
- **prefect-server**: Prefect API server with web UI
- **prefect-services**: Background services for Prefect
- **prefect-init**: One-time initialization service that creates the default work pool
- **prefect-worker**: Worker process that executes flows
- **open-ticket-ai**: The main application

## Quick Start

1. Navigate to the docs directory:
```bash
cd docs
```

2. Start all services:
```bash
docker compose up -d
```

3. Access the Prefect UI at http://localhost:4200

4. Check service status:
```bash
docker compose ps
```

## Service Details

### prefect-server
- Runs the Prefect API server
- Exposes port 4200 for the web UI
- Includes health check to ensure it's ready before worker starts
- Depends on postgres and redis being healthy

### prefect-init
- One-time initialization service
- Creates the default work pool if it doesn't exist
- Runs once and exits (restart: "no")
- Worker waits for this to complete successfully

### prefect-worker
- Connects to prefect-server via http://prefect-server:4200/api
- Waits for both prefect-server to be healthy AND prefect-init to complete
- Starts pulling work from the "default" work pool

## Troubleshooting

### Worker fails to connect

If you see connection errors like `httpcore.ConnectError`, check:

1. **Server health**: Ensure prefect-server is healthy
```bash
docker compose ps prefect-server
```

2. **Init completion**: Verify prefect-init completed successfully
```bash
docker compose ps prefect-init
```

3. **Work pool exists**: Connect to prefect-server and check
```bash
docker compose exec prefect-server prefect work-pool ls
```

### Starting over

To completely reset the environment:

```bash
docker compose down -v
docker compose up -d
```

The `-v` flag removes volumes, including the postgres database.

### View logs

Check logs for specific services:

```bash
# All services
docker compose logs

# Specific service
docker compose logs prefect-worker
docker compose logs prefect-server

# Follow logs in real-time
docker compose logs -f prefect-worker
```

## Architecture

The service startup order ensures proper initialization:

1. **postgres** and **redis** start first
2. **prefect-server** waits for postgres and redis to be healthy
3. **prefect-init** waits for prefect-server to be healthy, then creates work pool
4. **prefect-worker** waits for both prefect-server health AND prefect-init completion
5. **prefect-services** runs alongside the server

This prevents the worker from trying to connect before:
- The server is ready to accept connections
- The work pool exists

## Configuration

### Changing the work pool type

By default, the work pool type is "process". To use a different type:

1. Edit `compose.yml`:
```yaml
prefect-init:
  command: >
    sh -c "
    prefect work-pool create default --type docker || echo 'Work pool already exists';
    "
```

2. Update the worker if needed (e.g., for Docker, mount docker.sock):
```yaml
prefect-worker:
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```

### Custom environment variables

Add environment variables to the open-ticket-ai service:

```yaml
open-ticket-ai:
  environment:
    PREFECT_API_URL: http://prefect-server:4200/api
    # Add other variables as needed
```

## Production Considerations

For production deployments:

1. **Use specific image tags** instead of `:3-latest`
2. **Set resource limits** for each service
3. **Use secrets** for sensitive data (postgres password, API keys)
4. **Enable SSL/TLS** for prefect-server
5. **Configure backup** for postgres volumes
6. **Set up monitoring** for service health
7. **Use external postgres** for better reliability

Example resource limits:

```yaml
prefect-server:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '0.5'
        memory: 512M
```

## Related Documentation

- [PREFECT_SETUP.md](./PREFECT_SETUP.md) - Integration setup and components
- [PREFECT_USAGE.md](./PREFECT_USAGE.md) - Usage guide and API reference
- [Official Prefect Docker docs](https://docs.prefect.io/latest/guides/deployment/docker/)
