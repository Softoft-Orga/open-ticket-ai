# Pipeline Execution Flow

```mermaid
flowchart TD
    Start([Start]) --> LoadConfig[Load config (config.yml)]
    LoadConfig --> InitContext[Initialise Context]
    InitContext --> BootInjector[Boot injector & PipeFactory]

    BootInjector --> PipelineLoop{Pipeline entries?}

    PipelineLoop --> Normalize[Normalise to RegisterableConfig]
    Normalize --> RenderConfig[Render with TemplateRenderer]
    RenderConfig --> CreatePipe[PipeFactory creates Pipe]
    CreatePipe --> CheckRunnable{`_if` ok & deps met?}

    CheckRunnable -->|No| SkipPipe[Skip pipe]
    CheckRunnable -->|Yes| Composite{Composite pipe?}

    Composite -->|Yes| StepLoop{For each rendered step}
    StepLoop --> BuildChild[PipeFactory builds child]
    BuildChild --> RunChild[child.process(context)]
    RunChild --> Collect[Collect PipeResult]
    Collect --> StepLoop
    StepLoop -->|Complete| Merge[Union child PipeResult]

    Composite -->|No| ExecutePipe[Execute pipe._process()]
    ExecutePipe --> WrapResult[Wrap output as PipeResult]

    Merge --> Persist[Persist PipeResult to context]
    WrapResult --> Persist
    SkipPipe --> Persist

    Persist --> Snapshot[Update context snapshot]
    Snapshot --> PipelineLoop

    PipelineLoop -->|No more| FinalState[Final Context]
    FinalState --> End([End])

    %% Styling
    classDef configClass fill:#e1f5fe
    classDef processClass fill:#f3e5f5
    classDef contextClass fill:#e8f5e8
    classDef decisionClass fill:#fff3e0

    class LoadConfig,RenderConfig,Normalize configClass
    class ExecutePipe,RunChild,Merge,WrapResult processClass
    class InitContext,Snapshot,FinalState contextClass
    class CheckRunnable,Composite,StepLoop,PipelineLoop decisionClass
```

The orchestrator drives execution by looping through each pipeline entry,
normalising it into a `RegisterableConfig`, rendering templates with the current
scope, and delegating instantiation to `PipeFactory`. Dependency gating via the
rendered `_if` flag and `depends_on` list decides whether the pipe should run. If
the config represents a `CompositePipe`, each rendered `step` is built through
`PipeFactory`, executed, and merged into a single `PipeResult`. Otherwise the
pipe’s `_process` implementation runs directly and its return payload is wrapped
as a `PipeResult`. In either case, the context stores the result under the pipe’s
identifier before moving to the next entry.

## Key Components

- **RegisterableConfig** – normalises every pipeline entry with consistent
  control fields (`uid`, `id`, `use`, `injects`) while preserving custom
  parameters for individual pipes.
- **RenderedPipeConfig** – the fully materialised configuration that results from
  rendering templates against the current execution scope.
- **PipeFactory** – central factory that renders configs, resolves `injects`, and
  instantiates both top-level pipes and nested step pipes.
- **Pipe & CompositePipe** – base execution units. `Pipe` implements dependency
  gating and `_process`, while `CompositePipe` orchestrates child pipes declared
  in its `steps` list.
- **PipeResult** – canonical result object persisted in the context after every
  pipe run, enabling downstream reuse and aggregation.
- **Context** – shared state that maps pipe identifiers to their `PipeResult`
  values alongside optional pipeline-wide configuration.

## Pipeline Architecture Concepts

### Configuration Layers

- **Root configuration**: `RawOpenTicketAIConfig` parses the YAML input into
  top-level groups such as `plugins`, `general_config`, reusable definition
  `defs`, and the `orchestrator` pipeline plan.
- **RegisterableConfig normalisation**: Each pipeline entry is wrapped in a
  `RegisterableConfig` so execution logic can rely on the presence of control
  fields while still honouring any additional user-defined keys.

### Pipe Construction

- **Template rendering**: The `TemplateRenderer` resolves environment variables,
  shared services, and previous pipe results when producing a
  `RenderedPipeConfig`. Rendering happens recursively for nested lists and
  dictionaries.
- **PipeFactory instantiation**: `PipeFactory` reuses the rendered config to
  create the requested Python class referenced in the `use` field, resolving any
  declared `injects` before the object is returned.

### Execution Flow

- **Dependency gating**: Each pipe evaluates its `_if` flag and `depends_on`
  requirements. Pipes that do not pass these checks are skipped without mutating
  the context.
- **Composite orchestration**: `CompositePipe` loops over rendered `steps`, builds
  child pipes through the shared factory, awaits their `process` calls, and
  merges the resulting `PipeResult` instances.
- **Atomic pipes**: Pipes that do not declare steps implement `_process` and have
  their raw output wrapped in a `PipeResult` for consistent storage.

### Context & Results

- **Shared context**: The `Context` model keeps a dictionary of `PipeResult`
  instances keyed by pipe identifier plus any global `config` state required by
  subsequent steps.
- **Result persistence**: After a pipe (or composite) finishes, the resulting
  `PipeResult` is written to `context.pipes[config.id]`, making it available to
  later templates or pipes within the same run.

### Dependency Integration

- **Injector bootstrapping**: Application start-up binds the raw configuration,
  `UnifiedRegistry`, and `PipeFactory` into the dependency-injection container so
  they can be reused throughout orchestration.
- **Service lookup**: Pipes resolve shared adapters from the `UnifiedRegistry`,
  ensuring integrations like ticket-system clients are created once and reused
  across multiple pipeline steps.
  =======
- **Config Normalization**: Each pipeline entry is wrapped in a `RegisterableConfig`, giving it a generated `id`, a
  display `name`, the Python class to `use`, a `when` flag, and nested `steps` to execute before the main pipe logic.
- **Rendered Pipe Config**: During execution the raw dictionaries are rendered into `RenderedPipeConfig` objects,
  computing boolean `when` conditions and optional `on_success`/`on_failure` policies before any code runs.
- **Jinja-Rendered Steps**: `ConfigurablePipe._build_pipe_from_step_config` runs each step configuration through the
  shared Jinja2 environment so that templates can reference context data or registered services when resolving the class
  in the `use` field.
- **Sequential Execution**: `_process_steps` walks the rendered list of step pipes and awaits their `process` methods,
  allowing complex behavior to be composed out of smaller reusable units before the main pipe executes.

### Context Handling

- **Execution Context**: The lightweight `Context` model carries a shared `pipes` dictionary for storing results and an
  optional `config` block for pipeline-wide settings.
- **State Propagation**: After `_process` finishes, `_save_pipe_result` stores the emitted `PipeResult` under the pipe's
  configured identifier so that later steps can read it via Jinja expressions like `{{ pipes.my_pipe.some_value }}`.
- **Conditional Execution**: Pipes whose rendered `when` evaluates to `False` are skipped with a log message, allowing
  declarative feature toggles without changing code.

### Error Strategy

- **Centralized Logging**: Exceptions raised inside `_process` are logged with the pipe name before being re-raised,
  ensuring orchestration layers can react while preserving tracebacks.
- **Default Behavior**: `DefaultPipe` provides a no-op implementation that simply returns an empty state, useful for
  scaffolding new pipeline entries while their real logic is under development.

### Context Flow

- **Initial State**: Empty context with `pipes={}` and `config={}`
- **State Accumulation**: Each pipe saves results to `context.pipes[pipe_id]`
- **Template Access**: Subsequent steps access previous results via `{{ pipes.* }}`

### Configuration Rendering

- **Pipeline Level**: Renders service instances and environment variables
- **Step Level**: Renders with current execution context and pipe results
- **Just-in-Time**: Pipes created dynamically from rendered configurations

### Execution Pattern

- **Conditional Processing**: `when` conditions control pipe execution
- **Nested Steps**: Pipes can contain multiple sub-steps
- **State Preservation**: Context carries state through entire pipeline execution

### Service Integration

- **Registry Pattern**: Services accessed via `{{ get_instance('service_id') }}`
- **Template Functions**: Jinja2 functions for dynamic service resolution
- **Stateless Pipes**: Pipes recreated for each execution with fresh context

## Dependency Injection Lifecycle

Open Ticket AI keeps object wiring out of the pipeline code by funnelling all
instantiation through a lightweight dependency injection (DI) layer.

### 1. Container bootstrapping

- The application entry point builds an `Injector` with `AppModule` and uses it
  to resolve the orchestrator, configuration, and instance factory during
  startup.
- `AppModule` reads the YAML configuration, exposes it as a singleton, and
  shares a process-wide `UnifiedRegistry` plus an `InstanceCreator` that knows
  how to populate that registry.

### 2. Registering configured services

- Configuration blocks placed under `open_ticket_ai.defs` are modelled by the
  `RawOpenTicketAIConfig` schema and describe reusable services with a `use`
  import path and arbitrary keyword arguments.
- During startup `InstanceCreator.create_instances()` walks over each `defs`
  entry, locates the referenced class, instantiates it with the configuration
  mapping, and registers the resulting object inside the shared registry so it
  can be reused later.
- The registry enforces singleton semantics by raising if the same identifier
  is registered twice and exposes `get_instance` to fetch stored services by
  their class name.

### 3. Consuming dependencies inside pipes

- Pipeline definitions reference registered services by identifier. For
  example, the bundled configuration creates an `otobo_znuny` ticket system
  service once and reuses its identifier within downstream pipe definitions to
  link to that adapter.
- When a configurable pipe is constructed, it resolves its dependencies through
  the registry. `FetchTicketsPipe`, `UpdateTicketsPipe`, and
  `AddNoteTicketsPipe` all take the configured ticket-system identifier and call
  `UnifiedRegistry.get_instance` to receive the shared service instance before
  performing their work.

This flow allows integrators to swap or extend services purely through YAML
configuration—new adapters only need to be registered in `defs`, and any pipe
that relies on them can look them up by identifier without importing concrete
classes.
