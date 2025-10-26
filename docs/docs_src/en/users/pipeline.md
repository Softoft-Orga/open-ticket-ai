---
description: Learn how Open Ticket AI pipes process data through sequential execution, context sharing, dependencies, and conditional logic.
pageClass: full-page
aside: false
---

# Pipe System

Pipes are the fundamental processing units in Open Ticket AI. Each pipe performs a specific task,
receives context from
previous pipes, executes its logic, and passes updated context forward.

## Basic Pipeline Flow

A pipeline is a sequence of pipes that execute one after another:

```mermaid
flowchart TD
    Start([Start])
    Pipe1["Pipe 1 - Fetch Tickets"]
    Pipe2["Pipe 2 - Classify Tickets"]
    Pipe3["Pipe 3 - Update Tickets"]
    End([Complete])
    Start --> Pipe1
    Pipe1 --> Pipe2
    Pipe2 --> Pipe3
    Pipe3 --> End
```

Each pipe:

1. Receives the `PipeContext` (containing results from previous pipes)
2. Executes its specific task
3. Creates a `PipeResult` with output data

## What is a Pipe?

A **pipe** is a self-contained processing unit that:

- Implements specific business logic (fetch data, classify, update, etc.)
- Receives input via `PipeContext`
- Produces output as `PipeResult`

```mermaid
flowchart TB
    subgraph Rendering
        PipeContext["PipeContext"]
        Renderer["Jinja Renderer"]
        PipeParams["PipeParams"]
        PipeContext --> Renderer --> PipeParams
    end
    PIPE["Pipe"]
    PR["<strong>PipeResult</strong> <small><br/>succeeded <br/> was_skipped <br/> message <br/> data<br/> } </small>"]
    PipeParams --> PIPE --> PR

```

## Pipe Types

### Simple Pipes

Atomic processing units that implement specific business logic:

```yaml
- id: fetch_tickets
  use: open_ticket_ai.base:FetchTicketsPipe
  injects:
    ticket_system: "otobo_znuny"
  params:
    search_criteria:
      queue:
        name: "Support"
      limit: 10
```

**Characteristics:**

- Implements `_process()` method
- Returns single `PipeResult`
- No child pipes
- Accesses injected services via `self.<service_name>`

### Composite Pipes

Orchestrators that contain and execute child pipes:

```mermaid
flowchart TB
    subgraph CompositePipe
        A["Pipe #1"] --> B["Pipe #2"] --> C["Pipe #3"]
    end

    A --> U["Result #1"]
    B --> U["Result #2"]
    C --> U["Result #3"]
    U["union([Result #1, Result #2, Result #3])"]
    U --> CR["CompositeResult"]
```

:::details Composite Pipe Example

```yaml
- id: ticket_workflow
  use: open_ticket_ai.base:CompositePipe
  params:
    threshold: 0.8
  steps:
    - id: fetch
      use: open_ticket_ai.base:FetchTicketsPipe
      injects: { ticket_system: "otobo_znuny" }
      params:
        search_criteria:
          queue: { name: "Incoming" }
          limit: 10

    - id: classify
      use: otai_hf_local:HFLocalTextClassificationPipe
      params:
        model: "bert-base-german-cased"
        text: "{{ get_pipe_result('fetch').data.fetched_tickets[0].subject }}"
      depends_on: [ fetch ]

    - id: update
      use: open_ticket_ai.base:UpdateTicketPipe
      injects: { ticket_system: "otobo_znuny" }
      params:
        ticket_id: "{{ get_pipe_result('fetch').data.fetched_tickets[0].id }}"
        updated_ticket:
          queue:
            name: "{{ get_pipe_result('classify').data.predicted_queue }}"
      depends_on: [ classify ]
```

:::

**Characteristics:**

- Contains `steps` list of child pipe configs
- Uses `PipeFactory` to build child pipes
- Executes children sequentially
- Merges results via `PipeResult.union()`
- Children can access parent params via `parent.params`

### Composite Pipe Execution

```mermaid
flowchart TB

```

**Composite Execution:**

1. **Initialization**: Prepare to iterate through `steps` list
2. **For Each Step**:
    - **Merge**: Combine parent params with step params (step overrides)
    - **Build**: Use factory to create child pipe instance
    - **Execute**: Call `child.process(context)` → updates context
    - **Collect**: Child result stored in `context.pipes[child_id]`
    - **Loop**: Continue to next step
3. **Finalization**:
    - **Union**: Merge all child results using `PipeResult.union()`
    - **Save**: Store composite result in context
    - **Return**: Return final updated context

## Dependency Management

The `depends_on` field creates execution dependencies between pipes:

```yaml
- id: step_a
  use: PipeA
  # Executes first (no dependencies)

- id: step_b
  use: PipeB
  depends_on: [ step_a ]
  # Executes only if step_a succeeded

- id: step_c
  use: PipeC
  depends_on: [ step_a, step_b ]
  # Executes only if both step_a and step_b succeeded
```

**Field Details:**

- **`pipes`**: Contains results from all previously executed pipes, keyed by pipe ID
    - Accumulated as each pipe completes
    - In CompositePipe: merged results from all child steps
    - Access via `pipe_result('pipe_id')` in templates

- **`params`**: Current pipe's parameters
    - Set when the pipe is created
    - Accessible via `params.*` in templates
    - For nested pipes, can reference parent via `parent.params`

- **`parent`**: Reference to parent context (if inside a CompositePipe)
    - Allows access to parent scope variables
    - Creates hierarchical context chain
    - Can traverse multiple levels (`parent.parent...`)

**Accessing Context in Templates:**

```yaml
- id: child_pipe
  params:
    # Access previous pipe result
    tickets: "{{ pipe_result('fetch').data.fetched_tickets }}"

    # Access parent parameter
    threshold: "{{ parent.params.confidence_threshold }}"

    # Access own parameter
    limit: "{{ params.limit }}"

    # Check if pipe succeeded
    should_update: "{{ has_succeeded('classify') }}"
```

## PipeResult Structure

Each pipe produces a `PipeResult` containing execution outcome and data:

```python
class PipeResult[T]():
    success: bool  # True if execution succeeded
    failed: bool  # True if execution failed
    message: str  # Human-readable message
    data: T  # Pipe-specific result data (Pydantic model)
```

# Pipe Parameter Reference

## AddNotePipe – `AddNoteParams`

| Field     | Type        | Default | Required | Description                                                                                            |
|-----------|-------------|---------|----------|--------------------------------------------------------------------------------------------------------|
| ticket_id | str \| int  | —       | Yes      | Identifier of the ticket to which the note should be added, accepting either string or integer format. |
| note      | UnifiedNote | —       | Yes      | Note content including subject and body to be added to the specified ticket.                           |

## FetchTicketsPipe – `FetchTicketsParams`

| Field                  | Type                 | Default | Required | Description                                                                                     |
|------------------------|----------------------|---------|----------|-------------------------------------------------------------------------------------------------|
| ticket_search_criteria | TicketSearchCriteria | —       | Yes      | Search criteria including queue, limit, and offset for querying tickets from the ticket system. |

## UpdateTicketPipe – `UpdateTicketParams`

| Field          | Type          | Default | Required | Description                                                                           |
|----------------|---------------|---------|----------|---------------------------------------------------------------------------------------|
| ticket_id      | str \| int    | —       | Yes      | Unique identifier of the ticket to be updated in the ticket system.                   |
| updated_ticket | UnifiedTicket | —       | Yes      | Updated ticket data containing the fields and values to apply to the existing ticket. |

## ClassificationPipe – `ClassificationPipeParams`

| Field      | Type        | Default | Required | Description                                              |
|------------|-------------|---------|----------|----------------------------------------------------------|
| text       | str         | —       | Yes      | Text to classify.                                        |
| model_name | str         | —       | Yes      | Name of the model to use.                                |
| api_token  | str \| None | None    | No       | Optional API token passed to the classification service. |

## ExpressionPipe – `ExpressionParams`

| Field      | Type | Default | Required | Description                                                                                      |
|------------|------|---------|----------|--------------------------------------------------------------------------------------------------|
| expression | Any  | —       | Yes      | Expression string/value to be evaluated; if it becomes a `FailMarker`, the pipe returns failure. |

## IntervalTrigger – `IntervalTriggerParams`

| Field    | Type      | Default | Required | Description                               |
|----------|-----------|---------|----------|-------------------------------------------|
| interval | timedelta | —       | Yes      | Time interval between trigger executions. |

## CompositePipe – `CompositePipeParams`

| Field | Type             | Default | Required | Description                                                               |
|-------|------------------|---------|----------|---------------------------------------------------------------------------|
| steps | list[PipeConfig] | []      | No       | List of pipe configurations representing the steps in the composite pipe. |

## SimpleSequentialRunner – `SimpleSequentialRunnerParams`

| Field | Type       | Default | Required | Description                                                               |
|-------|------------|---------|----------|---------------------------------------------------------------------------|
| on    | PipeConfig | —       | Yes      | Trigger pipe that gates execution. Not rendered by the template renderer. |
| run   | PipeConfig | —       | Yes      | Pipe to run when triggered. Not rendered by the template renderer.        |

## SimpleSequentialOrchestrator – `SimpleSequentialOrchestratorParams`

| Field              | Type             | Default | Required | Description                                               |
|--------------------|------------------|---------|----------|-----------------------------------------------------------|
| orchestrator_sleep | timedelta        | 0.01s   | No       | Sleep time between orchestrator cycles.                   |
| exception_sleep    | timedelta        | 5s      | No       | Sleep time after exceptions when retrying.                |
| always_retry       | bool             | True    | No       | Whether to always retry failed steps.                     |
| steps              | list[PipeConfig] | []      | No       | Steps to execute (not rendered by the template renderer). |

## Best Practices

### Pipe Design

- Keep pipes focused on single responsibility
- Make pipes reusable across different workflows
- Use descriptive pipe IDs
- Document expected input and output
- Handle errors gracefully

### Configuration

- Use template variables for dynamic values
- Leverage `depends_on` for clear execution order
- Use `if_` conditions to skip unnecessary work
- Group related pipes in CompositePipe

### Performance

- Avoid blocking operations in `_process()`
- Use async/await for I/O operations
- Keep pipe execution time reasonable
- Consider batching for large datasets

### Testing

- Test pipes independently with mock services
- Test dependency chains
- Test conditional execution paths
- Test error scenarios

## Key Implementation Files

### Core Pipeline

- **`src/open_ticket_ai/core/pipeline/pipe.py`** - Base `Pipe` class
- **`src/open_ticket_ai/core/pipeline/pipe_config.py`** - `PipeConfig`, `PipeResult` models
- **`src/open_ticket_ai/core/pipeline/pipe_context.py`** - `PipeContext` model

### Base Pipes

- **`src/open_ticket_ai/base/pipes/composite_pipe.py`** - `CompositePipe` implementation
- **`src/open_ticket_ai/base/pipes/jinja_expression_pipe.py`** - Expression evaluation
- **`src/open_ticket_ai/base/pipes/ticket_system_pipes/`** - Ticket operations

### Configuration

- **`src/open_ticket_ai/core/config/renderable_factory.py`** - Pipe instantiation
- **`src/open_ticket_ai/core/config/renderable.py`** - `Renderable` interface

## Related Documentation

- **[Orchestrator System](orchestrator.md)** - How pipelines are scheduled and executed
- **[Configuration & Rendering](config_rendering.md)** - Template rendering and context
- **[First Pipeline Tutorial](../guides/first_pipeline.md)** - Step-by-step guide
- **[Plugin Development](../developers/plugin_development.md)** - Creating custom pipes
- **[Configuration Reference](../details/config_reference.md)** - YAML structure

## Summary

Pipes are the building blocks of Open Ticket AI workflows:

**Core Concepts:**

- Self-contained processing units
- Context-driven data flow
- Sequential execution with dependencies
- Conditional and composable

**Key Features:**

- Dependency management (`depends_on`)
- Conditional execution (`if_`)
- Nested composition (CompositePipe)
- Error isolation and handling
- Template-driven configuration

**Design Principles:**

- Single responsibility
- Reusability across workflows
- Type-safe results
- Graceful error handling

This architecture enables building complex automation workflows from simple, testable, composable
components.
