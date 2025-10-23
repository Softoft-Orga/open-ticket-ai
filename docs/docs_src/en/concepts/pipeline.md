---
description: Learn how Open Ticket AI pipes process data through sequential execution, context sharing, dependencies, and conditional logic.
pageClass: full-page
aside: false
---

# Pipe System

Pipes are the fundamental processing units in Open Ticket AI. Each pipe performs a specific task, receives context from
previous pipes, executes its logic, and passes updated context forward.

## Basic Pipeline Flow

A pipeline is a sequence of pipes that execute one after another:

```mermaid
flowchart TD
    Start([Start]):::startNode
    Pipe1[Pipe 1 - Fetch Tickets]:::pipeNode
    Pipe2[Pipe 2 - Classify Tickets]:::pipeNode
    Pipe3[Pipe 3 - Update Tickets]:::pipeNode
    End([Complete]):::endNode
    Start --> Pipe1
    Pipe1 --> Pipe2
    Pipe2 --> Pipe3
    Pipe3 --> End
    classDef startNode fill: #2d6a4f, stroke: #1b4332, stroke-width: 3px, color: #fff, font-weight: bold
    classDef endNode fill: #2d6a4f, stroke: #1b4332, stroke-width: 3px, color: #fff, font-weight: bold
    classDef pipeNode fill: #2b2d42, stroke: #14213d, stroke-width: 2px, color: #e0e0e0
```

Each pipe:

1. Receives the `PipeContext` (containing results from previous pipes)
2. Executes its specific task
3. Creates a `PipeResult` with output data
4. Updates the context with its result
5. Passes the updated context to the next pipe

## What is a Pipe?

A **pipe** is a self-contained processing unit that:

- Implements specific business logic (fetch data, classify, update, etc.)
- Receives input via `PipeContext`
- Produces output as `PipeResult`
- Can depend on other pipes
- Can execute conditionally
- Can be composed into larger workflows

## Core Architecture

```mermaid
%%{init: {
  "classDiagram": { "layout": "elk", "useMaxWidth": false },
  "elk": { "spacing": { "nodeNode": 20, "nodeNodeBetweenLayers": 20, "componentComponent": 15 } }
}}%%
classDiagram
    direction TD

    class Pipe {
        +config: PipeConfig
        +process(ctx: PipeContext) PipeContext
        #_process()* PipeResult
    }

    class CompositePipe {
        +steps: list[PipeConfig]
        +_factory: RenderableFactory
        +_process_steps(ctx) list~PipeResult~
        +process(ctx) PipeContext
    }

    class PipeConfig {
        +id: str
        +use: str
        +params: BaseModel
        +if_: str | bool
        +depends_on: list[str]
        +steps: list[PipeConfig]
    }

    class PipeContext {
        +pipes: dict[str, PipeResult]
        +params: dict[str, Any]
        +parent: PipeContext | None
    }

    class PipeResult {
        +success: bool
        +message: str
        +data: BaseModel
    }

    CompositePipe --|> Pipe
    Pipe --> PipeConfig: configured by
    Pipe --> PipeContext: receives & updates
    Pipe --> PipeResult: produces
    PipeContext --> PipeResult: stores by pipe_id
    CompositePipe --> Pipe: contains
```

## Pipe Execution Lifecycle

How individual pipes execute their logic:

```mermaid
flowchart TB

%% ===================== PIPE ENTRY =====================
    subgraph ENTRY["📥 Pipe.process()"]
        direction TB
        Start([pipe.process]):::start
        CheckShould{"should_run?"}:::dec
        CheckDeps{"Dependencies met?"}:::dec
        Skip["⏭️ Skip execution"]:::skip
        Start --> CheckShould
        CheckShould -- ✓ True --> CheckDeps
        CheckShould -- ✗ False --> Skip
        CheckDeps -- ✗ Missing --> Skip
    end

%% ===================== EXECUTION =====================
    subgraph EXEC["⚙️ Execution"]
        direction TB
        ProcessAndSave["__process_and_save()"]:::proc
        TryCatch["try-catch wrapper"]:::proc
        RunProcess["await _process()<br/>(subclass implementation)"]:::proc
        CreateResult["Create PipeResult<br/>with data"]:::proc
        ProcessAndSave --> TryCatch --> RunProcess --> CreateResult
    end

%% ===================== ERROR HANDLING =====================
    subgraph ERROR["❌ Error Handling"]
        direction TB
        CatchEx["Catch Exception"]:::error
        LogError["Logger.error<br/>+ traceback"]:::log
        CreateFailed["Create failed<br/>PipeResult"]:::error
        CatchEx --> LogError --> CreateFailed
    end

%% ===================== PERSISTENCE =====================
    subgraph PERSIST["💾 Context Update"]
        direction TB
        SaveResult["context.pipes[pipe_id]<br/>= result"]:::ctx
        LogResult["Log result<br/>(info/warning)"]:::log
        Return["Return updated<br/>context"]:::ctx
        SaveResult --> LogResult --> Return
    end

%% ===================== CONNECTIONS =====================
    CheckDeps -- ✓ Met --> ProcessAndSave
    TryCatch --> CatchEx
    CreateResult --> SaveResult
    CreateFailed --> SaveResult
%% ===================== STYLES =====================
    classDef start fill: #2d6a4f, stroke: #1b4332, stroke-width: 3px, color: #fff, font-weight: bold
    classDef dec fill: #d97706, stroke: #b45309, stroke-width: 2px, color: #fff, font-weight: bold
    classDef skip fill: #374151, stroke: #1f2937, stroke-width: 2px, color: #9ca3af
    classDef proc fill: #2b2d42, stroke: #14213d, stroke-width: 2px, color: #e0e0e0
    classDef error fill: #dc2626, stroke: #991b1b, stroke-width: 2px, color: #fff
    classDef log fill: #0891b2, stroke: #0e7490, stroke-width: 2px, color: #fff
    classDef ctx fill: #165b33, stroke: #0d3b24, stroke-width: 2px, color: #e0e0e0
```

**Processing Steps:**

1. **Condition Check**: Evaluate `if_` field (defaults to `True`)
2. **Dependency Check**: Verify all `depends_on` pipes succeeded
3. **Skip Path**: If checks fail → return original context unchanged
4. **Execute Path**: If checks pass:
    - Wrap execution in try-catch
    - Call `_process()` (implemented by pipe subclass)
    - Create `PipeResult` from return value
    - On exception: create failed `PipeResult` with error message
5. **Persistence**: Save result to `context.pipes[pipe_id]`
6. **Return**: Return updated context to next pipe

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

**Example Implementation:**

```python
class FetchTicketsPipe(Pipe):
    def __init__(self, ticket_system: TicketSystemService, config: PipeConfig, logger_factory: LoggerFactory):
        super().__init__(config, logger_factory)
        self.ticket_system = ticket_system

    async def _process(self, context: PipeContext) -> FetchTicketsResult:
        criteria = self.config._config.search_criteria
        tickets = await self.ticket_system.find_tickets(criteria)
        return FetchTicketsResult(fetched_tickets=tickets)
```

### Composite Pipes

Orchestrators that contain and execute child pipes:

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
        text: "{{ pipe_result('fetch').data.fetched_tickets[0].subject }}"
      depends_on: [ fetch ]

    - id: update
      use: open_ticket_ai.base:UpdateTicketPipe
      injects: { ticket_system: "otobo_znuny" }
      params:
        ticket_id: "{{ pipe_result('fetch').data.fetched_tickets[0].id }}"
        updated_ticket:
          queue:
            name: "{{ pipe_result('classify').data.predicted_queue }}"
      depends_on: [ classify ]
```

**Characteristics:**

- Contains `steps` list of child pipe configs
- Uses `RenderableFactory` to build child pipes
- Executes children sequentially
- Merges results via `PipeResult.union()`
- Children can access parent params via `parent.params`

### Composite Pipe Execution

```mermaid
%%{init:{
  "flowchart":{"defaultRenderer":"elk","htmlLabels":true,"curve":"linear"},
  "themeVariables":{"fontSize":"14px","fontFamily":"system-ui","lineColor":"#718096"},
}}%%
flowchart TB

%% ===================== COMPOSITE START =====================
    subgraph START["🔀 CompositePipe.process()"]
        direction TB
        Entry([Composite pipe<br/>starts]):::start
        InitLoop["Initialize step<br/>iteration"]:::proc
        Entry --> InitLoop
    end

%% ===================== STEP PROCESSING =====================
    subgraph STEP_LOOP["🔁 For Each Step"]
        direction TB
        HasStep{"Has next<br/>step?"}:::dec
        MergeCtx["Merge parent +<br/>step params"]:::proc
        RenderStep["🎨 Render step config<br/>with Jinja"]:::render
        BuildChild["factory.create_pipe<br/>(step_config)"]:::factory
        RunChild["child.process<br/>(context)"]:::proc
        CollectResult["Collect result<br/>in context"]:::ctx
        HasStep -- Yes --> MergeCtx --> RenderStep --> BuildChild
        BuildChild --> RunChild --> CollectResult --> HasStep
    end

%% ===================== FINALIZATION =====================
    subgraph FINAL["✅ Finalization"]
        direction TB
        AllDone["All steps<br/>done"]:::proc
        UnionResults["PipeResult.union<br/>(all results)"]:::proc
        SaveComposite["Save composite<br/>result"]:::ctx
        Return["Return updated<br/>context"]:::ctx
        AllDone --> UnionResults --> SaveComposite --> Return
    end

%% ===================== CONNECTIONS =====================
    InitLoop --> HasStep
    HasStep -- No --> AllDone
%% ===================== STYLES =====================
    classDef start fill: #2d6a4f, stroke: #1b4332, stroke-width: 3px, color: #fff, font-weight: bold
    classDef dec fill: #d97706, stroke: #b45309, stroke-width: 2px, color: #fff, font-weight: bold
    classDef proc fill: #2b2d42, stroke: #14213d, stroke-width: 2px, color: #e0e0e0
    classDef render fill: #4338ca, stroke: #312e81, stroke-width: 2px, color: #e0e0e0
    classDef factory fill: #7c2d12, stroke: #5c1a0a, stroke-width: 2px, color: #e0e0e0
    classDef ctx fill: #165b33, stroke: #0d3b24, stroke-width: 2px, color: #e0e0e0
```

**Composite Execution:**

1. **Initialization**: Prepare to iterate through `steps` list
2. **For Each Step**:
    - **Merge**: Combine parent params with step params (step overrides)
    - **Render**: Apply Jinja2 template rendering to step config
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

**Dependency Rules:**

- Pipe executes only if `context.has_succeeded(dep_id)` returns `True` for all dependencies
- `has_succeeded()` checks: `pipes[dep_id].success == True` and `pipes[dep_id].failed == False`
- If any dependency fails → pipe is skipped → original context returned unchanged
- **Warning**: Circular dependencies are NOT detected and will cause execution failures

**Example with Dependencies:**

```yaml
steps:
  - id: fetch
    use: FetchTicketsPipe
    # No dependencies, executes first

  - id: validate
    use: ValidateTicketsPipe
    depends_on: [ fetch ]
    # Only runs if fetch succeeded

  - id: classify
    use: ClassifyPipe
    depends_on: [ fetch, validate ]
    # Only runs if both fetch and validate succeeded

  - id: update
    use: UpdateTicketPipe
    depends_on: [ classify ]
    # Only runs if classify succeeded
```

## Conditional Execution

The `if_` field enables runtime conditional logic:

```yaml
- id: high_confidence_update
  use: UpdateTicketPipe
  if_: "{{ pipe_result('classify').data.confidence > 0.8 }}"
  params:
    ticket_id: "{{ ticket.id }}"
    updated_ticket:
      queue:
        name: "{{ pipe_result('classify').data.predicted_queue }}"
```

**Condition Evaluation:**

- `if_` value rendered as Jinja2 template
- Result converted to Python truthy/falsy
- Can reference:
    - `params.*` - current pipe or parent params
    - `pipe_result(pipe_id)` - results from previous pipes
    - `env('VAR')` - environment variables
    - `has_succeeded(pipe_id)` - check if pipe succeeded
    - `has_failed(pipe_id)` - check if pipe failed
- Defaults to `True` if omitted

**Conditional Examples:**

```yaml
# Only run if previous pipe succeeded
- id: send_notification
  if_: "{{ has_succeeded('classify') }}"
  use: NotificationPipe

# Only run if confidence is high
- id: auto_update
  if_: "{{ pipe_result('classify').data.confidence > 0.9 }}"
  use: UpdateTicketPipe

# Only run if ticket priority is urgent
- id: escalate
  if_: "{{ pipe_result('fetch').data.fetched_tickets[0].priority.name == 'Urgent' }}"
  use: EscalationPipe

# Multiple conditions
- id: complex_condition
  if_: "{{ has_succeeded('fetch') and pipe_result('fetch').data.fetched_tickets | length > 0 }}"
  use: ProcessPipe
```

## PipeContext Structure

The `PipeContext` is the core data structure for data flow between pipes:

```python
class PipeContext(BaseModel):
    pipes: dict[str, PipeResult[Any]]  # All previous pipe results
    params: dict[str, Any]  # Current pipe parameters
    parent: PipeContext | None  # Parent context (for nested pipes)
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

This architecture enables building complex automation workflows from simple, testable, composable components.
