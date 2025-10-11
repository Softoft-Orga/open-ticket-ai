# Orchestrator

The Orchestrator is responsible for scheduling and supervising pipeline execution. It manages when pipelines run and handles errors during execution.

## Role and Responsibilities

- **Scheduling**: Runs pipelines at configured intervals
- **Supervision**: Monitors pipeline execution
- **Error Handling**: Manages failures and retries
- **Resource Management**: Ensures efficient resource usage

## Scheduling and Execution Model

The orchestrator uses a time-based scheduling model where each pipeline has a configured execution interval.

## Schedule Configuration

Configure pipeline execution frequency using `run_every_milli_seconds`:

```yaml
orchestrator:
  pipelines:
    - name: ticket_processor
      run_every_milli_seconds: 60000  # Run every 60 seconds
      pipes:
        - pipe_name: process_tickets
```

## Pipeline Supervision

The orchestrator monitors pipeline execution and:
- Logs execution status
- Captures errors
- Prevents overlapping executions
- Provides execution metrics

## Error Handling

When a pipeline fails:
1. Error is logged with full context
2. Pipeline execution stops
3. Next scheduled execution proceeds normally
4. Administrators are notified (if configured)

## Related Documentation

- [Pipeline System](pipeline.md)
- [Configuration Structure](../configuration/config_structure.md)
- [Troubleshooting](../guides/troubleshooting.md)
