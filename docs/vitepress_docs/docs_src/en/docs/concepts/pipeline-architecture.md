# Pipeline Architecture

The pipeline system is the core execution model in Open Ticket AI. It orchestrates the flow of data through a series of processing steps (pipes) to accomplish tasks like ticket classification, enrichment, and routing.

## System Overview

Open Ticket AI uses a **pipeline-based architecture** where:
- **Pipelines** are sequences of processing steps
- **Pipes** are individual processing components
- **Orchestrator** manages pipeline scheduling and execution
- **Context** enables data sharing between pipes
- **Pipe Factory** handles pipe instantiation

## Pipeline Execution Model

### Core Concepts

A **pipeline** is a sequence of pipes that process data sequentially. Each pipe performs a specific task and can pass its results to the next pipe in the chain.

A **pipe** is a stateless component that:
- Receives input data from the execution context
- Performs a specific operation
- Returns a result
- Can access shared services via dependency injection

The **orchestrator** is responsible for:
- Scheduling pipeline execution at configured intervals
- Supervising pipeline runs
- Managing errors and failures
- Ensuring efficient resource usage

The **execution context** is a shared data structure that:
- Stores intermediate results
- Shares data between pipes
- Maintains execution metadata
- Provides access to services

### Pipeline Lifecycle

1. **Initialization**: Pipeline is configured from YAML
2. **Scheduling**: Orchestrator schedules pipeline execution based on configured intervals
3. **Context Creation**: A new execution context is created for each pipeline run
4. **Execution**: Pipes execute sequentially, reading from and writing to the context
5. **Result Handling**: Final results are collected and processed
6. **Cleanup**: Context is cleared after execution

### Pipe Execution Flow

Each pipe follows this execution pattern:

1. **Read from context**: Retrieve input data using context keys
2. **Process data**: Transform, enrich, or validate the data
3. **Write to context**: Store results using descriptive keys
4. **Return result**: Return a `PipeResult` indicating success or failure

### PipeResult Objects

Each pipe returns a `PipeResult` object containing:
- **Execution status**: Success or failure indicator
- **Output data**: The result of the pipe's processing
- **Error information**: Details if the pipe failed
- **Metadata**: Additional information about the execution

## Orchestrator Scheduling

### Scheduling Model

The orchestrator uses a **time-based scheduling model** where each pipeline has a configured execution interval specified in milliseconds.

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
- Captures errors with full context
- Prevents overlapping executions
- Provides execution metrics

### Error Handling

When a pipeline fails:
1. Error is logged with full context
2. Pipeline execution stops
3. Next scheduled execution proceeds normally
4. Administrators are notified (if configured)

## Pipe System

### Pipe Interface

All pipes must implement the base pipe interface with an `execute` method that takes a `PipelineContext` parameter and returns a `PipeResult`.

### Input/Output Handling

Pipes interact with the execution context:
- **Input**: Read data from context using `context.get(key, default)`
- **Processing**: Transform or enrich data
- **Output**: Write results using `context.set(key, value)`

### Stateless Design

Pipes are designed to be **stateless**:
- No instance variables should store execution state
- All data flows through the context
- Each execution is independent
- Configuration is injected via dependency injection

### Built-in Pipe Types

Open Ticket AI includes several built-in pipes:

**Data Fetching**
- `FetchTicketsPipe`: Retrieve tickets from ticket system
- `SearchTicketsPipe`: Search for specific tickets

**Processing**
- `ClassifyQueuePipe`: Classify tickets into queues
- `ClassifyPriorityPipe`: Assign priority levels
- `EnrichTicketPipe`: Add additional data to tickets

**Output**
- `UpdateTicketPipe`: Update ticket properties
- `AddNotePipe`: Add notes to tickets
- `SendNotificationPipe`: Send notifications

## Pipe Factory

### Pipe Instantiation

The Pipe Factory handles:
1. **Registration**: Pipes are registered with the factory
2. **Configuration**: YAML config specifies which pipes to use
3. **Creation**: Factory creates pipe instances
4. **Injection**: Dependencies are injected into pipes

### Pipe Registration

Pipes are registered through:
- Plugin entry points
- Explicit registration in code
- Auto-discovery from modules

### Custom Pipe Creation

To register a custom pipe, use the `@register_pipe` decorator on your pipe class. This makes the pipe available for use in YAML configuration files.

### Factory Pattern Benefits

The factory pattern provides:
- Decoupling pipe creation from pipeline logic
- Dynamic pipe selection based on configuration
- Easy testing with mock pipes
- Plugin extensibility

## Execution Context

### Context Concept

The execution context flows through the pipeline, allowing pipes to share data and maintain state during execution.

### Context Lifecycle

1. **Created**: Context is created before pipeline execution
2. **Populated**: Initial data is added to context
3. **Shared**: Pipes read and write during execution
4. **Cleaned**: Context is cleared after execution

### Sharing Data Between Pipes

Pipes can read and write to the context:
- **Read from context**: Use `context.get("key", default_value)` to retrieve data
- **Process data**: Transform or enrich the data as needed
- **Write to context**: Use `context.set("key", value)` to store results
- **Return result**: Return a `PipeResult` indicating success or failure

### Context API

The context provides methods for managing data:
- `get(key, default)`: Retrieve data with an optional default value
- `set(key, value)`: Store data in the context
- `has(key)`: Check if a key exists
- `remove(key)`: Remove a key from the context

### Best Practices for Context Usage

**Do:**
- Use descriptive keys for context data
- Document what data your pipe expects
- Clean up temporary data
- Use type hints for context data

**Don't:**
- Store large objects unnecessarily
- Modify context data in-place without documenting
- Rely on undocumented context keys
- Use context for pipe configuration (use DI instead)

## Pipeline Configuration

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

- [Dependency Injection](../code/dependency_injection.md) - Service management
- [Services](../code/services.md) - Core services and their roles
- [Template Rendering](../code/template_rendering.md) - Jinja2 template system
- [Configuration Structure](../configuration/config_structure.md) - YAML configuration
- [First Pipeline Tutorial](../guides/first_pipeline.md) - Step-by-step guide
- [Plugin Development](../plugins/plugin_development.md) - Creating custom pipes
