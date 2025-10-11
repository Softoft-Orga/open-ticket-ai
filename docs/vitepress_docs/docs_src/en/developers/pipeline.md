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
- **`orchestrator`** – an array of runner entries. Each runner defines triggers (via `triggers`), the pipeline to execute (`pipe`), optional dependency injection (`injects`), and runtime settings (`settings`) for concurrency, retry, timeout, etc.

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
    runners:
      - id: ticket-processor
        triggers:
          - id: poll-interval
            use: apscheduler.triggers.interval:IntervalTrigger
            params:
              seconds: 10
        pipe:
          <<: *default_ticket_fetcher
          params:
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
- `config` / additional fields – arbitrary values that become attributes on the rendered config and can be consumed by
  the pipe.

## Execution Model

1. The orchestrator registers each runner's triggers with the APScheduler.
2. When a trigger fires, the associated `pipe` definition is rendered with a fresh `Context` (`context.params` contains the runner configuration; `context.pipes` starts empty).
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

## Runner Configuration

Each runner in the orchestrator defines how and when a pipeline should execute. Runner configuration includes:

### Required Fields

- `pipe` – The pipeline configuration to execute (typically a reference to a definition in `defs`)

### Optional Fields

- `id` – Unique identifier for the runner. If omitted, derived from the pipe ID
- `triggers` – List of trigger definitions that determine when the pipeline runs. Each trigger has:
  - `id` – Unique identifier for the trigger
  - `use` – Import path to the trigger class (e.g., `apscheduler.triggers.interval:IntervalTrigger`)
  - `params` – Parameters to pass to the trigger constructor
- `injects` – Dependency injection mappings for the runner
- `settings` – Runtime behavior settings:
  - `concurrency.max_workers` – Maximum concurrent executions (default: 1)
  - `concurrency.when_exhausted` – Action when max workers reached: `wait` or `enqueue`
  - `retry.attempts` – Number of retry attempts (default: 3)
  - `retry.delay` – Initial retry delay (e.g., `5s`)
  - `retry.backoff_factor` – Exponential backoff multiplier (default: 2.0)
  - `retry.max_delay` – Maximum retry delay (e.g., `30s`)
  - `retry.jitter` – Add random jitter to retry delays (default: true)
  - `timeout` – Maximum execution time (e.g., `1m`)
  - `retry_scope` – Retry at `pipeline` or `step` level (default: `pipeline`)
  - `priority` – Execution priority (default: 10)
  - `tags` – List of tags for categorization

### Example Runner Configuration

```yaml
orchestrator:
  runners:
    - id: fast-poller
      triggers:
        - id: poll-interval
          use: apscheduler.triggers.interval:IntervalTrigger
          params:
            seconds: 10
        - id: webhook-trigger
          use: apscheduler.triggers.webhook:WebhookTrigger
          params:
            path: "/hooks/queue-classify"
            method: POST
      injects:
        logging: default_logger
        template_renderer: jinja_renderer
      pipe:
        id: poll-and-process
        use: open_ticket_ai.base:CompositePipe
        steps:
          - id: fetch
            use: open_ticket_ai.base:FetchTicketsPipe
          - id: classify
            use: open_ticket_ai.base:ClassifyPipe
      settings:
        concurrency:
          max_workers: 4
          when_exhausted: enqueue
        retry:
          attempts: 3
          delay: "5s"
          backoff_factor: 2.0
          max_delay: "30s"
          jitter: true
        timeout: "1m"
        retry_scope: pipeline
        priority: 10
        tags: ["critical", "batch"]
```

### Legacy Format (Deprecated)

The old `run_every_milli_seconds` field is still supported for backward compatibility but will be removed in a future version:

```yaml
orchestrator:
  runners:
    - run_every_milli_seconds: 10000  # Deprecated, use 'triggers' instead
      pipe:
        id: legacy-pipe
```

This is automatically migrated to:

```yaml
orchestrator:
  runners:
    - triggers:
        - id: interval-trigger
          use: apscheduler.triggers.interval:IntervalTrigger
          params:
            seconds: 10
      pipe:
        id: legacy-pipe
```

## Scheduling Tips

- Runners in `orchestrator` are independent; each receives a clean `Context` per execution.
- You can define multiple runners that reuse the same composite definition but with different triggers or settings.
- Multiple triggers on a single runner allow the same pipeline to be executed by different events (e.g., both on schedule and via webhook).
- Use `settings.concurrency.max_workers` to control parallel execution of the same runner.

Armed with this structure you can compose complex ticket-processing workflows without changing Python code—simply adjust
the YAML
and let the orchestrator rebuild the pipeline at runtime.
