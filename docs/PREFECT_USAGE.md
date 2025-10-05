# Prefect Integration Usage Guide

## Overview

Open-Ticket-AI now integrates with **Prefect 3.4.20** for advanced workflow orchestration, monitoring, and scheduling
capabilities. This guide shows you how to use the Prefect integration with your pipelines.

## Quick Start

### 1. Start Prefect Server

```powershell
# Start the Prefect server (runs on http://127.0.0.1:4200)
uv run prefect server start
```

Access the Prefect UI at: **http://127.0.0.1:4200**

### 2. Basic Usage with PrefectOrchestrator

The `PrefectOrchestrator` is a drop-in replacement for the APScheduler-based `Orchestrator`:

```python
from open_ticket_ai.core.pipeline import PrefectOrchestrator
from injector import Injector

# Get orchestrator via dependency injection
orchestrator = injector.get(PrefectOrchestrator)

# Start serving all scheduled deployments (blocks until shutdown)
await orchestrator.run()
```

### 3. Configuration

Use the same configuration format as the regular orchestrator in your `config.yml`:

```yaml
orchestrator:
  runners:
    - pipe_id: ticket_processor
      pipe:
        use: ProcessTickets
        queue: "my-queue"
        # ... other pipe config
      interval_seconds: 300  # Run every 5 minutes

    - pipe_id: escalation_checker
      pipe:
        use: CheckEscalations
      interval_seconds: 600  # Run every 10 minutes
```

## Key Features

### ✨ Retry Logic

Tasks automatically retry on failure:

```python
@task(name="execute_pipe", retries=2, retry_delay_seconds=30)
async def execute_pipe_task(...):
    # Your pipe execution logic
    pass
```

### 📊 Web UI

Monitor all your pipeline executions in real-time:

- **Flow runs**: See current and past executions
- **Logs**: Centralized logging for debugging
- **Task status**: Track individual task completion
- **Metrics**: Execution duration, success rates, etc.

### 🔄 Flexible Scheduling

Prefect 3.x supports multiple scheduling options:

```python
# Interval-based (current implementation)
deployment_params["interval"] = timedelta(seconds=300)

# Cron-based (can be added)
from prefect.client.schemas.schedules import CronSchedule
deployment_params["schedule"] = CronSchedule(cron="0 */6 * * *")  # Every 6 hours
```

### 🎯 One-Time Execution

Execute a specific pipe once without scheduling:

```python
result = await orchestrator.run_once("ticket_processor")
print(f"Result: {result}")
```

## API Reference

### PrefectOrchestrator

**Methods:**

- **`async start()`** - Initialize and register all deployments
- **`async stop()`** - Gracefully shutdown the orchestrator
- **`async run()`** - Start serving deployments (blocks until shutdown)
- **`async run_once(pipe_id: str)`** - Execute a specific pipe once

**Example:**

```python
orchestrator = PrefectOrchestrator(pipe_factory, app_config)

# Start and serve all deployments
await orchestrator.run()

# Or run a specific pipe once
result = await orchestrator.run_once("my_pipe")
```

### Prefect Flows

**`execute_scheduled_pipe_flow(pipe_factory, definition)`**

- Wraps pipe execution in a Prefect flow
- Provides observability and retry logic
- Returns final context data after execution

**`execute_pipe_task(pipe_factory, pipe_config, context_data, pipe_id)`**

- Executes a single pipe as a Prefect task
- Configured with 2 retries and 30-second delay
- Returns updated context data

## Advanced Usage

### Custom Deployments

You can create custom deployments programmatically:

```python
from open_ticket_ai.core.pipeline.prefect_flows import execute_scheduled_pipe_flow
from datetime import timedelta

# Create a custom deployment
deployment = execute_scheduled_pipe_flow.to_deployment(
    name="custom_processor",
    parameters={
        "pipe_factory": my_pipe_factory,
        "definition": my_runner_definition,
    },
    interval=timedelta(minutes=15),
    tags=["custom", "high-priority"],
)

# Serve it
await serve(deployment)
```

### Integration with Existing Code

The Prefect integration works alongside your existing APScheduler-based orchestrator:

```python
# Use APScheduler for local development
from open_ticket_ai.core.pipeline import Orchestrator
orchestrator = injector.get(Orchestrator)

# Use Prefect for production with monitoring
from open_ticket_ai.core.pipeline import PrefectOrchestrator
orchestrator = injector.get(PrefectOrchestrator)
```

## Monitoring & Observability

### View Flow Runs

```powershell
# List all flow runs
uv run prefect flow-run ls

# View details of a specific run
uv run prefect flow-run inspect <flow-run-id>
```

### View Logs

All logs are automatically captured and available in the Prefect UI under each flow run.

### Alerts & Notifications

Configure Prefect to send notifications on failures:

```python
# In your flow definition
@flow(
    name="execute_scheduled_pipe",
    log_prints=True,
    on_failure=[send_notification],  # Custom failure handler
)
async def execute_scheduled_pipe_flow(...):
    pass
```

## Comparison: APScheduler vs Prefect

| Feature       | APScheduler (Orchestrator) | Prefect (PrefectOrchestrator) |
|---------------|----------------------------|-------------------------------|
| Scheduling    | ✅ Interval-based           | ✅ Interval, Cron, Event-based |
| Web UI        | ❌ None                     | ✅ Full-featured dashboard     |
| Retry Logic   | ⚠️ Manual                  | ✅ Built-in with backoff       |
| Logging       | ⚠️ Local files             | ✅ Centralized in UI           |
| Observability | ❌ Limited                  | ✅ Comprehensive               |
| Dependencies  | Minimal                    | Requires Prefect server       |
| Complexity    | Simple                     | More features, more complex   |

## Troubleshooting

### Prefect Server Won't Start

```powershell
# Reset Prefect database
uv run prefect server database reset -y

# Restart server
uv run prefect server start
```

### Deployment Not Appearing in UI

1. Check that `interval_seconds > 0` in your config
2. Verify the orchestrator is running: `await orchestrator.run()`
3. Refresh the Prefect UI

### Task Failures

- Check logs in the Prefect UI under the failed flow run
- Verify your pipe configuration is valid
- Ensure all required services are available

### Docker Compose: Worker Connection Errors

If you see `httpcore.ConnectError: All connection attempts failed` in Docker Compose:

**Problem**: Worker tries to connect before server is ready or work pool doesn't exist.

**Solution**: The updated `compose.yml` includes:

1. **Health check on prefect-server** - Ensures server is ready before worker starts
2. **prefect-init service** - Creates the default work pool automatically
3. **Proper dependencies** - Worker waits for both server health and init completion

See [DOCKER_COMPOSE_SETUP.md](./DOCKER_COMPOSE_SETUP.md) for detailed Docker deployment guide.

**Quick fix for existing deployments**:

```bash
# Recreate services with updated compose file
docker compose down
docker compose up -d

# Or manually create work pool if needed
docker compose exec prefect-server prefect work-pool create default --type process
```

## Best Practices

1. **Use Prefect for Production** - The monitoring and retry capabilities are valuable in production
2. **Use APScheduler for Development** - Simpler setup for local development
3. **Configure Retries** - Adjust retry counts based on your use case
4. **Monitor the UI** - Regularly check the Prefect UI for failures
5. **Tag Your Deployments** - Use tags for easy filtering and organization

## Next Steps

- Explore [Prefect Cloud](https://www.prefect.io/cloud/) for enterprise features
- Set up [Prefect Blocks](https://docs.prefect.io/concepts/blocks/) for configuration management
- Configure [Notifications](https://docs.prefect.io/concepts/notifications/) for alerts
- Use [Work Pools](https://docs.prefect.io/concepts/work-pools/) for distributed execution

## Resources

- **Prefect Documentation**: https://docs.prefect.io/
- **Prefect 3.x Migration Guide**: https://docs.prefect.io/v3/migration-guide/
- **Prefect Community**: https://prefect.io/slack
