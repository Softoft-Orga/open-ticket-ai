# Prefect Integration Setup

## ✅ Status: FULLY OPERATIONAL

Prefect **3.4.20** is successfully installed and integrated with open-ticket-ai!

### What Was Resolved

The initial dependency conflict between `otobo-znuny` and `prefect` (typer version mismatch) has been **resolved**:

- Updated `otobo-znuny` to use compatible typer version
- Upgraded to **Prefect 3.4.20** (fully compatible with Pydantic 2.11.x)
- All tests passing ✅

## Integration Components

The following Prefect integration components are **ready to use**:

1. **`src/open_ticket_ai/core/pipeline/prefect_flows.py`**
    - `execute_pipe_task()` - Prefect task wrapper for pipe execution with retry logic
    - `execute_scheduled_pipe_flow()` - Prefect flow for scheduled pipes
    - Includes automatic retries and error handling

2. **`src/open_ticket_ai/core/pipeline/prefect_orchestrator.py`**
    - `PrefectOrchestrator` class - Alternative to `Orchestrator` (APScheduler-based)
    - Manages Prefect deployments for scheduled pipeline execution
    - Methods: `start()`, `stop()`, `run()`, `run_once(pipe_id)`

3. **Example Scripts**
    - `examples/prefect_example.py` - Basic Prefect flow/task demo
    - `examples/prefect_working_example.py` - Working integration example

## Quick Start

### 1. Start Prefect Server

```powershell
uv run prefect server start
```

Access the UI at: **http://127.0.0.1:4200**

### 2. Use PrefectOrchestrator

```python
from open_ticket_ai.core.pipeline import PrefectOrchestrator

# Via dependency injection
orchestrator = injector.get(PrefectOrchestrator)

# Run all scheduled pipes
await orchestrator.run()

# Or run a specific pipe once
result = await orchestrator.run_once("my_pipe_id")
```

### 3. Configuration

The `PrefectOrchestrator` uses the same configuration as `Orchestrator`:

```yaml
orchestrator:
  runners:
    - pipe_id: ticket_processor
      pipe:
        use: ProcessTickets
        queue: "my-queue"
      interval_seconds: 300  # Run every 5 minutes
```

## Features & Benefits

### ✨ What Prefect Provides

- **🖥️ Web UI**: Visual monitoring and management at http://127.0.0.1:4200
- **🔄 Retry Logic**: Automatic retries with exponential backoff (2 retries, 30s delay)
- **📊 Logging**: Centralized logs for all flow runs in the UI
- **⏰ Scheduling**: Advanced scheduling options (interval, cron, event-based)
- **👀 Observability**: Track execution history, durations, failures, success rates
- **🔗 Orchestration**: Build complex workflows with dependencies
- **☁️ Cloud Option**: Deploy to Prefect Cloud for enterprise features

### 🆚 Comparison with APScheduler

| Feature              | APScheduler    | Prefect          |
|----------------------|----------------|------------------|
| **Web UI**           | ❌ None         | ✅ Full dashboard |
| **Retry Logic**      | ⚠️ Manual      | ✅ Built-in       |
| **Logging**          | ⚠️ Local files | ✅ Centralized UI |
| **Observability**    | ❌ Limited      | ✅ Comprehensive  |
| **Setup Complexity** | Simple         | Medium           |
| **Dependencies**     | Minimal        | Requires server  |

## Detailed Documentation

See **[PREFECT_USAGE.md](./PREFECT_USAGE.md)** for comprehensive documentation including:

- API reference
- Advanced usage patterns
- Monitoring & observability
- Troubleshooting
- Best practices

See **[DOCKER_COMPOSE_SETUP.md](./DOCKER_COMPOSE_SETUP.md)** for Docker Compose deployment:

- Complete setup guide for running Prefect with Docker Compose
- Service architecture and startup order
- Troubleshooting connection issues
- Production deployment considerations

## Testing

Run the example to verify installation:

```powershell
uv run python examples/prefect_example.py
```

Expected output:

```
INFO | prefect - Starting temporary server...
INFO | Flow run 'acoustic-aardwolf' - Beginning flow run...
INFO | Task run 'simple_task-855' - Finished in state Completed()
...
```

## Recommendation

**Choose based on your needs:**

- **Development/Simple Use Cases**: Use `Orchestrator` (APScheduler)
    - Simpler, fewer dependencies
    - No server required

- **Production/Complex Workflows**: Use `PrefectOrchestrator`
    - Better monitoring and observability
    - Automatic retries and error handling
    - Web UI for operations team

Both orchestrators are fully supported and can be used interchangeably! 🚀

## Version Information

- **Prefect**: 3.4.20
- **Pydantic**: 2.11.9
- **Python**: 3.13+
- **Typer**: 0.17.5 (compatible with both prefect and otobo-znuny)
