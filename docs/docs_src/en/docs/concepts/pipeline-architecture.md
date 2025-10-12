# Pipeline Architecture

Open Ticket AI is built on a pipeline architecture where data flows through a series of processing steps called "pipes". This document provides a comprehensive overview of the pipeline system, its components, and how they work together.

## System Overview

The pipeline architecture consists of several key components:

- **Pipeline**: A sequence of pipes that process data sequentially
- **Pipes**: Individual processing components that perform specific tasks
- **Orchestrator**: Schedules and supervises pipeline execution
- **Context**: Shared data structure that flows through the pipeline
- **Pipe Factory**: Instantiates and registers pipes

## Pipeline System

The pipeline system is the core execution model in Open Ticket AI. It orchestrates the flow of data through a series of processing steps to accomplish tasks like ticket classification, enrichment, and routing.

### Pipeline Overview

A pipeline is a sequence of pipes that process data sequentially. Each pipe performs a specific task and can pass its results to the next pipe in the chain.

### Pipeline Lifecycle

1. **Initialization**: Pipeline is configured from YAML
2. **Scheduling**: Orchestrator schedules pipeline execution
3. **Execution**: Pipes execute sequentially
4. **Context Management**: Data flows through execution context
5. **Result Handling**: Final results are collected and processed

### Working with PipeResult Objects

Each pipe returns a `PipeResult` object containing:
- Execution status
- Output data
- Error information (if any)
- Metadata about the execution

### Pipeline Configuration

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

## Pipe System

Pipes are the individual processing components in a pipeline. Each pipe performs a specific task and follows a consistent interface for input/output handling.

### What is a Pipe?

A pipe is a stateless component that:
- Receives input data
- Performs a specific operation
- Returns a result
- Can access shared services via dependency injection

### Pipe Interface and Contract

All pipes must implement a base pipe interface with an `execute` method that:
- Accepts a `PipelineContext` parameter
- Returns a `PipeResult` object
- Performs the pipe's specific processing logic

### Input/Output Handling

Pipes interact with the execution context:
- **Input**: Read data from context
- **Processing**: Transform or enrich data
- **Output**: Write results back to context

### Stateless Execution Model

Pipes are designed to be stateless:
- No instance variables should store execution state
- All data flows through the context
- Each execution is independent

### Built-in Pipe Types

Open Ticket AI includes several built-in pipes:

#### Data Fetching
- `FetchTicketsPipe`: Retrieve tickets from ticket system
- `SearchTicketsPipe`: Search for specific tickets

#### Processing
- `ClassifyQueuePipe`: Classify tickets into queues
- `ClassifyPriorityPipe`: Assign priority levels
- `EnrichTicketPipe`: Add additional data to tickets

#### Output
- `UpdateTicketPipe`: Update ticket properties
- `AddNotePipe`: Add notes to tickets
- `SendNotificationPipe`: Send notifications

### Custom Pipes

See [Creating Custom Pipes](../plugins/plugin_development.md) for information on building your own pipes.

## Orchestrator

The Orchestrator is responsible for scheduling and supervising pipeline execution. It manages when pipelines run and handles errors during execution.

### Role and Responsibilities

- **Scheduling**: Runs pipelines at configured intervals
- **Supervision**: Monitors pipeline execution
- **Error Handling**: Manages failures and retries
- **Resource Management**: Ensures efficient resource usage

### Scheduling and Execution Model

The orchestrator uses a time-based scheduling model where each pipeline has a configured execution interval.

### Schedule Configuration

Configure pipeline execution frequency using `run_every_milli_seconds`:

```yaml
orchestrator:
  pipelines:
    - name: ticket_processor
      run_every_milli_seconds: 60000  # Run every 60 seconds
      pipes:
        - pipe_name: process_tickets
```

### Pipeline Supervision

The orchestrator monitors pipeline execution and:
- Logs execution status
- Captures errors
- Prevents overlapping executions
- Provides execution metrics

### Error Handling

When a pipeline fails:
1. Error is logged with full context
2. Pipeline execution stops
3. Next scheduled execution proceeds normally
4. Administrators are notified (if configured)

## Pipeline Execution Context

The execution context is a shared data structure that flows through the pipeline, allowing pipes to share data and maintain state during execution.

### Execution Context Concept

The context object:
- Stores intermediate results
- Shares data between pipes
- Maintains execution metadata
- Provides access to services

### Sharing Data Between Pipes

Pipes can read and write to the context to share data between processing steps. Each pipe can access data stored by previous pipes and add its own results for downstream pipes to use.

### Context Lifecycle

1. **Created**: Context is created before pipeline execution
2. **Populated**: Initial data is added to context
3. **Shared**: Pipes read and write during execution
4. **Cleaned**: Context is cleared after execution

### Best Practices for Context Usage

#### Do:
- Use descriptive keys for context data
- Document what data your pipe expects
- Clean up temporary data
- Use type hints for context data

#### Don't:
- Store large objects unnecessarily
- Modify context data in-place without documenting
- Rely on undocumented context keys
- Use context for pipe configuration (use DI instead)

### Context API

The context provides methods for:
- Getting data with defaults
- Setting data
- Checking if keys exist
- Removing keys

## Pipe Factory

The Pipe Factory is responsible for instantiating and registering pipes. It uses the factory pattern to create pipe instances based on configuration.

### Pipe Instantiation Process

1. **Registration**: Pipes are registered with the factory
2. **Configuration**: YAML config specifies which pipes to use
3. **Creation**: Factory creates pipe instances
4. **Injection**: Dependencies are injected into pipes

### Pipe Registration and Discovery

Pipes are registered through:
- Plugin entry points
- Explicit registration in code
- Auto-discovery from modules

### Factory Pattern Implementation

The factory pattern allows:
- Decoupling pipe creation from pipeline logic
- Dynamic pipe selection based on configuration
- Easy testing with mock pipes
- Plugin extensibility

### Custom Pipe Creation

Custom pipes can be registered with the factory and used in pipelines just like built-in pipes. See the [Plugin Development](../plugins/plugin_development.md) guide for details on creating and registering custom pipes.

## Best Practices

### Pipeline Design

- Keep pipelines focused on a single purpose
- Use descriptive names for pipelines and pipes
- Configure appropriate execution intervals
- Monitor pipeline performance

### Pipe Development

- Make pipes stateless and reusable
- Use dependency injection for services
- Document expected inputs and outputs
- Handle errors gracefully

### Context Management

- Use clear, descriptive keys
- Document data contracts between pipes
- Clean up temporary data
- Avoid storing large objects

### Error Handling

- Log errors with sufficient context
- Fail fast when appropriate
- Provide meaningful error messages
- Consider retry strategies

## Related Documentation

- [Configuration Structure](../configuration/config_structure.md)
- [Plugin Development](../plugins/plugin_development.md)
- [Dependency Injection](../code/dependency_injection.md)
- [Services](../code/services.md)
- [First Pipeline Tutorial](../guides/first_pipeline.md)
- [Troubleshooting](../guides/troubleshooting.md)
