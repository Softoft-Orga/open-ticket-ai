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

## Key Components

- **RegisterableConfig** – normalises every pipeline entry with consistent control
  fields (`uid`, `id`, `use`, `injects`) while preserving custom parameters for
  individual pipes.
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
