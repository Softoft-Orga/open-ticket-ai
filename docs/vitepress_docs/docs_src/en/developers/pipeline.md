---
title: Pipeline Reference
description: Understand the YAML structure that drives OpenTicketAI's orchestrator, pipes, and reusable definitions.
---

# Pipeline Reference

OpenTicketAI is configured entirely through YAML. This reference explains how the root configuration is organised, how
reusable
anchors and definitions work, and how the orchestrator turns that configuration into `Pipe` instances and `PipeResult`
objects at
runtime.

## Root Layout

All settings live under the top-level `open_ticket_ai` key. The schema matches `RawOpenTicketAIConfig` and is split into
four
main sections:

- **`plugins`** – optional Python modules to import before instantiating any pipes.
- **`general_config`** – global settings such as logging and `pipe_classes` (a catalogue of reusable pipe templates
  stored under
  YAML anchors).
- **`defs`** – reusable definitions (services, composite pipe templates, parameter sets) that can be merged into
  scheduled pipes
  via `<<: *anchor`.
- **`orchestrator`** – an array of schedule entries. Each item declares `run_every_milli_seconds` and the `pipe` (
  usually a
  composite definition pulled from `defs`) that should execute on that cadence.

```yaml
open_ticket_ai:
  plugins: []
  general_config:
    pipe_classes:
      - &ticket_fetch_pipe
        use: "open_ticket_ai.base:FetchTicketsPipe"
  defs:
    - &default_ticket_fetcher
      <<: *ticket_fetch_pipe
      injects:
        ticket_system: "otobo_znuny"
  orchestrator:
    - run_every_milli_seconds: 10000
      pipe:
        <<: *default_ticket_fetcher
        ticket_search_criteria:
          state.name: "new"
```

## Reusable Definitions & Anchors

OpenTicketAI relies heavily on YAML anchors:

- Define a block once (e.g. `&ticket_classifier`) and merge it with `<<: *ticket_classifier` wherever needed.
- Anchors can be combined. Parent configuration is merged with child overrides via `PipeFactory.resolve_config`, so
  child entries
  only specify the differences.
- Definitions stored in `defs` can include nested `steps`, additional anchors, or injected dependencies. When referenced
  from the
  orchestrator they expand into a full pipe tree.

## Pipe Configuration Fields

Every pipe (including nested steps) is validated into a `RegisterableConfig`/`RenderedPipeConfig` instance. The most
common
fields are:

- `id` – unique identifier for the pipe. If omitted, a UUID is generated, but you should set it explicitly so templates
  can
  reference the result via `get_pipe_result('your_id', 'value')`.
- `use` – dotted import path (`module:ClassName`) resolved by the `PipeFactory`.
- `injects` – mapping of constructor arguments to IDs defined in `defs`. These references are resolved before
  instantiation.
- `steps` – for composite pipes, an ordered list of child pipe configurations that will be executed sequentially.
- `if` – optional Jinja2 expression rendered to a boolean. The result becomes `_if` on `RenderedPipeConfig`; if it
  evaluates to
  `False`, the pipe is skipped.
- `depends_on` – a string or list of pipe IDs that must have succeeded (`PipeResult.success == True`) before this pipe
  runs.
- `retries` – optional integer specifying how many times to retry on failure (default: 2, used by Prefect orchestration).
- `retry_delay_seconds` – optional integer specifying delay between retries in seconds (default: 30, used by Prefect orchestration).
- `config` / additional fields – arbitrary values that become attributes on the rendered config and can be consumed by
  the pipe.

## Execution Model

1. The orchestrator selects the next schedule entry whose `run_every_milli_seconds` interval has elapsed.
2. The associated `pipe` definition is rendered with a fresh `Context` (`context.config` contains the schedule entry;
   `context.pipes`
   starts empty).
3. For each pipe or step:
    - The `_if` expression is evaluated. If false, the pipe is skipped.
    - Dependencies listed in `depends_on` are checked against prior `PipeResult.success` values.
    - The `PipeFactory` locates the Python class referenced by `use`, injects any dependencies from `injects`, and calls
      the pipe's
      asynchronous `process()` method (which internally awaits `_process()`).
    - The return value is wrapped in a `PipeResult` (`success`, `failed`, `message`, `data`) and stored under
      `context.pipes[id]`.
4. Helper functions exposed to templates (`get_pipe_result`, `has_failed`, etc.) read from `context.pipes`, making
   previous
   results available to later steps.
5. When all steps complete, composite pipes merge their children's results with `PipeResult.union` so the composite
   exposes a
   single success/failure state alongside combined data.

## Working with `PipeResult`

Every saved state is a `PipeResult` (see `open_ticket_ai.core.pipeline.pipe_config`). Use these conventions when
implementing
custom pipes:

- Return a dictionary that `PipeResult.model_validate` can consume, or instantiate `PipeResult(...)` and call
  `.model_dump()`.
- Populate the `data` field with any payload you want downstream steps to reuse.
- Set `success`/`failed` and `message` appropriately so templates can make conditional decisions.

## Scheduling Tips

- Schedule entries in `orchestrator` are independent; each one receives a clean `Context` per run.
- You can define multiple entries that reuse the same composite definition but override configuration (e.g. different
  search
  criteria or thresholds).
- Because intervals are expressed in milliseconds, `run_every_milli_seconds: 60000` triggers a run roughly once per
  minute.

## Prefect Orchestration

OpenTicketAI supports **Prefect** as an alternative orchestrator with enhanced observability and retry capabilities.

### Task-per-Pipe Architecture

When using Prefect, each pipe runs as an individual Prefect task:

- **Atomic Pipes**: Each pipe's `_process()` method becomes a separate Prefect task named `pipe_{pipe_id}`
- **Composite Pipes**: When running in a Prefect context, `CompositePipe` automatically dispatches each step as its own task
- **Granular Control**: Each pipe can have its own retry configuration via `retries` and `retry_delay_seconds`

### Configuration

Add retry settings to any pipe:

```yaml
orchestrator:
  - run_every_milli_seconds: 300000
    pipe:
      id: ticket_processor
      use: ProcessTickets
      retries: 3  # Override default retry count
      retry_delay_seconds: 60  # Override default delay
      steps:
        - id: fetch
          use: FetchTickets
          retries: 5  # Critical step gets more retries
        - id: classify
          use: ClassifyTickets
```

### Benefits

- **Visibility**: Each pipe appears as a separate task in Prefect UI
- **Error Isolation**: Failures in one pipe don't block the entire pipeline
- **Granular Metrics**: Track duration and success rates per pipe
- **Retry Strategies**: Configure different retry behavior per pipe
- **Observability**: Centralized logging and monitoring through Prefect dashboard

See [PREFECT_SETUP.md](../../../PREFECT_SETUP.md) and [PREFECT_USAGE.md](../../../PREFECT_USAGE.md) for detailed setup and usage instructions.

Armed with this structure you can compose complex ticket-processing workflows without changing Python code—simply adjust
the YAML
and let the orchestrator rebuild the pipeline at runtime.
