# Pipeline Execution Flow

```mermaid
flowchart TD
    Start([Start]) --> LoadConfig[Load open_ticket_ai config]
    LoadConfig --> ResolveAnchors[Resolve YAML anchors & merges]
    ResolveAnchors --> BuildContainer[Bootstrap Injector & TemplateRenderer]
    BuildContainer --> WarmDefs[Create reusable defs via PipeFactory]
    WarmDefs --> ScheduleLoop{Orchestrator schedule}

    ScheduleLoop -->|next due run| RenderPipe[Render pipeline entry with context]
    RenderPipe --> CheckCondition{`_if` expression true?}
    CheckCondition -->|No| SkipPipe[Skip pipe, keep context]
    CheckCondition -->|Yes| CheckDeps{Dependencies succeeded?}
    CheckDeps -->|No| SkipPipe
    CheckDeps -->|Yes| BuildPipe[Instantiate Pipe]

    BuildPipe --> ExecutePipe[Execute `_process` coroutine]
    ExecutePipe --> PipeResult[[PipeResult(success, failed, data)]]
    PipeResult --> Persist[Persist result into Context]
    Persist --> UpdateStatus[Update success/failure registries]
    UpdateStatus --> ScheduleLoop

    ScheduleLoop -->|no pending runs| End([End])
```

## Key Lifecycle Stages

- **Configuration loading** – `RawOpenTicketAIConfig` reads the YAML file under the `open_ticket_ai` root. The orchestrator works directly with this structure so the documented field names need to match the schema in `src/config.yml`.
- **Anchors and reusable snippets** – The YAML heavily uses anchors (`&ticket_fetch_pipe`) and merges (`<<: *ticket_fetch_pipe`). When the configuration is rendered, these anchors provide composable templates for `pipe_classes`, service definitions, and steps. The resolver expands them before any pipe is instantiated.
- **Dependency bootstrapping** – The Injector is initialised with the loaded config and the `TemplateRenderer`. Definitions from the `defs` array are created via the `PipeFactory`, cached in the `UnifiedRegistry`, and later injected into pipes by ID.
- **Scheduling** – The `orchestrator` section is an array of entries with `run_every_milli_seconds` and an associated `pipe` tree. The scheduler loops over these definitions, dispatching a run whenever its interval elapses. Each dispatch starts with a fresh `Context` instance seeded with `config` values from the scheduled entry.
- **Rendering & instantiation** – Before a pipe runs, its raw dictionary is rendered with the current scope (`config`, `pipes`, environment variables, helper filters, etc.). The `PipeFactory` resolves anchors, merges parent configuration into children, locates the class referenced by `use`, and injects dependencies declared through `injects`.

## Conditional Execution

- **`_if` flag** – Each pipe carries a rendered boolean `_if` attribute. The default is `True`, but any step can provide an `if:` expression in YAML. If the expression resolves to `False`, the pipe is skipped without changing the context.
- **`depends_on` chain** – Pipes can list one or more dependency IDs. Before a pipe executes, the orchestrator inspects the stored `PipeResult.success` flags for each dependency; if any dependency did not succeed, the pipe is skipped.
- **Composite steps** – `CompositePipe` instances execute their `steps` sequentially, collecting each child pipe’s `PipeResult`. Once all steps finish, their results are merged (using logical `and`) and stored under the composite pipe’s own ID. Any `_if` or `depends_on` rules on the composite apply before its children are processed.

## Execution Results & Context

- **Pipe output** – Concrete pipes implement the asynchronous `_process()` method and return a plain `dict`. The orchestrator wraps this output in a `PipeResult` object with `success`, `failed`, `message`, and `data` fields before storing it.
- **Context storage** – The shared `Context` model keeps two dictionaries: `pipes` (mapping pipe IDs to their `PipeResult`) and `config` (the rendered configuration for the current schedule entry). Helper template functions such as `get_pipe_result()` and `has_failed()` read from `context.pipes` to drive downstream logic.
- **Failure handling** – When `_process()` raises, the base class logs the exception, marks the `PipeResult` as failed, and keeps the previous context copy. Subsequent pipes can inspect `Context.has_failed(...)` to trigger fallback logic.

## Updated Configuration Concepts

- **No more `name`/`when`** – Pipes are addressed by their `id`. Any documentation or configuration should rely on `id` for referencing results. Conditional execution is expressed via `if:` in YAML, producing the `_if` flag in the rendered config; the legacy `when` property is no longer present.
- **Reusable defs** – Service constructors and composite pipe templates live under `open_ticket_ai.defs`. They can be merged into scheduled pipelines through YAML anchors, ensuring that a change to a shared definition updates every pipeline entry that references it.
- **PipeResult driven flow** – Because every stored state is a `PipeResult`, downstream pipes can compose both data (`result.data`) and meta-information (`result.success`, `result.failed`, `result.message`) when making decisions.

This flow matches the current implementation in `open_ticket_ai.core.pipeline` and should serve as the canonical reference for writing or updating pipelines.
