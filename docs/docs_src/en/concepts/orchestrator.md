---
description: Learn how Open Ticket AI's orchestrator manages pipes scheduling, triggers, and execution lifecycle from bootstrap to runtime.
pageClass: full-page
aside: false
---

# Orchestrator System

Open Ticket AI treats the orchestrator itself as an injectable pipe. The orchestrator entry in your workspace configuration is a normal `PipeConfig` that is resolved through dependency injection, exactly like any other pipe in the system. The default implementation, `base:SimpleSequentialOrchestrator`, receives its configuration via `params` and builds the runtime loop from the nested pipe definitions you supply.

## SimpleSequentialOrchestrator lifecycle

`SimpleSequentialOrchestrator` is a `CompositePipe` that performs an endless cycle:

1. Each iteration it renders the configured `steps` list, which must contain `PipeConfig` objects.
2. For every step it resolves the referenced pipe (typically a runner) and awaits its execution.
3. After all steps complete it sleeps for `orchestrator_sleep` (defaults to 10 ms) before starting the next cycle.
4. Any exception inside a step is logged. When `always_retry` is `True` (the default) the orchestrator waits for `exception_sleep` and then restarts the cycle; otherwise the exception is propagated.

Because the orchestrator is just a pipe, you can replace it with any other implementation by changing the `use` target or inject additional collaborators through `params`.

## Runner pipes inside `steps`

The orchestrator’s `steps` array is where runner pipes live. Each entry is a fully qualified `PipeConfig` that will be instantiated inside the orchestrator’s execution context. Runners can inject services, render templates, and emit results the same way any other pipe does. You can mix different runner implementations within the same orchestrator loop by adding multiple step entries.

## SimpleSequentialRunner semantics

`SimpleSequentialRunner` is the default runner pipe. It accepts two nested `PipeConfig` values:

- `on`: A pipe that decides whether the runner should execute its workload. The pipe runs first on every orchestrator cycle. If it returns a successful `PipeResult`, the runner proceeds.
- `run`: The pipe that performs the actual work. It executes only when the `on` pipe succeeds. If the `on` pipe fails or is skipped, the runner skips execution and reports the reason in its result message.

Both nested configs are rendered within the runner’s context, so they have access to the parent orchestrator parameters and any templating variables produced earlier in the pipeline.

## Configuration example

The current end-to-end demo configuration shows how the orchestrator and runners are composed:

```yaml
open_ticket_ai:
  orchestrator:
    use: "base:SimpleSequentialOrchestrator"
    params:
      orchestrator_sleep: "PT0.01S"
      steps:
        - id: ticket-routing-runner
          use: "base:SimpleSequentialRunner"
          params:
            on:
              id: trigger_interval
              use: "base:IntervalTrigger"
              params:
                interval: "PT0.5S"
            run:
              id: ticket-routing
              use: "base:CompositePipe"
              params:
                steps:
                  - id: ticket_fetcher
                    use: "base:FetchTicketsPipe"
                    injects: { ticket_system: "otobo_znuny" }
                    params:
                      ticket_search_criteria:
                        queue:
                          name: "OpenTicketAI::Incoming"
                        limit: 1
                  - id: queue_classify
                    use: "base:ClassificationPipe"
                    injects: { classification_service: "hf_local" }
                    params:
                      text: "{{ get_pipe_result('ticket')['subject'] }} {{ get_pipe_result('ticket')['body'] }}"
                      model_name: "softoft/otai-queue-de-bert-v1"
                  # additional steps omitted for brevity
```

Key points illustrated above:

- The orchestrator itself is declared with `use` and `params`, just like any other pipe.
- Runner definitions reside inside the orchestrator’s `steps` list and can inject services.
- Runner `on` and `run` sections are full pipe configs whose templates are rendered within the orchestrator loop.
- The orchestrator continues looping, evaluating the `on` pipe each cycle and running the workload only when it succeeds.

## Related documentation

- [Pipe System](pipeline.md)
- [Configuration Reference](../details/config_reference.md)
- [First Pipeline Tutorial](../guides/first_pipeline.md)
