# Pipeline System

The pipeline system is the core execution model in Open Ticket AI. It orchestrates the flow of data through a series of processing steps (pipes) to accomplish tasks like ticket classification, enrichment, and routing.

## Overview

A pipeline is a sequence of pipes that process data sequentially. Each pipe performs a specific task and can pass its results to the next pipe in the chain.

## Pipeline Lifecycle

1. **Initialization**: Pipeline is configured from YAML
2. **Scheduling**: Orchestrator schedules pipeline execution
3. **Execution**: Pipes execute sequentially
4. **Context Management**: Data flows through execution context
5. **Result Handling**: Final results are collected and processed

## Working with PipeResult Objects

Each pipe returns a `PipeResult` object containing:
- Execution status
- Output data
- Error information (if any)
- Metadata about the execution

## Configuration

Pipelines are defined in the `orchestrator.pipelines` section of your configuration:

```yaml
orchestrator:
  pipelines:
    - name: my_pipeline
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
        - pipe_name: classify_tickets
        - pipe_name: update_tickets
```

## Related Documentation

- [Orchestrator](orchestrator.md) - Pipeline scheduling and supervision
- [Pipes](pipe.md) - Individual pipeline components
- [Context](context.md) - Data sharing between pipes
- [First Pipeline Tutorial](../guides/first_pipeline.md)
