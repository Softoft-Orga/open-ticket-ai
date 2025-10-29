---
description: Step-by-step tutorial for creating your first ticket classification pipeline with Open Ticket AI using the current configuration schema (module-based plugins, service registry, and PipeConfig orchestrator).
---

# Creating Your First Pipeline

This guide walks through building a working ticket-classification pipeline on top of the latest Open Ticket AI configuration schema. You will learn how plugin modules are loaded, how services are registered by identifier, and how the orchestrator is composed entirely from nested `PipeConfig` definitions.

## Configuration building blocks

All configuration lives under the top-level `open_ticket_ai` key. Every object underneath is validated by Pydantic models before the orchestrator starts, so matching the schema is essential.

### Plugin modules (`open_ticket_ai.plugins`)

Plugins are enabled by module (entry point) name. List each plugin you want to load as a string. At minimum you need the core `otai-base` plugin to access the built-in runners, orchestrators, and utility pipes.

### Service registry (`open_ticket_ai.services`)

Services are defined in a dictionary keyed by their identifier. Each service describes the implementation to instantiate via `use`, optional constructor dependencies via `injects`, and configuration data via `params`. Services become injectable dependencies for pipes and other services. Open Ticket AI expects exactly one `TemplateRenderer` service; the example below registers the default Jinja renderer.

### Orchestrator (`open_ticket_ai.orchestrator`)

The orchestrator itself is a `PipeConfig`. You choose an orchestrator implementation via `use` (for example `base:SimpleSequentialOrchestrator`) and configure it via `params`. In the sequential orchestrator, `params.steps` is a list of nested `PipeConfig` objects. Each step can be any pipe—including runners such as `SimpleSequentialRunner`, other orchestrators, or concrete business logic pipes.

The following minimal configuration highlights the structure and validates against the current schema:

```yaml
open_ticket_ai:
  api_version: "1"
  plugins:
    - otai-base
  services:
    default_renderer:
      use: "base:JinjaRenderer"
  orchestrator:
    id: orchestrator
    use: "base:SimpleSequentialOrchestrator"
    params:
      steps: []
```

## Build a minimal ticket-routing pipeline

We will extend the skeleton above into a runnable pipeline that fetches tickets from OTOBO/Znuny, classifies the queue using a Hugging Face model, updates the ticket, and stores a note. Each section explains how the configuration maps to concrete classes in the codebase.

### Step 1: Declare plugin modules and template renderer

Add the plugins that provide the injectables we need:

- `otai-base` – core orchestrators (`SimpleSequentialOrchestrator`), runners (`SimpleSequentialRunner`), pipes (`CompositePipe`, `FetchTicketsPipe`, `UpdateTicketPipe`, `AddNotePipe`, `ExpressionPipe`), triggers (`IntervalTrigger`), and the default `JinjaRenderer`.
- `otai-otobo-znuny` – ticket system integration service (`OTOBOZnunyTicketSystemService`).
- `otai-hf-local` – on-device Hugging Face classification service (`HFClassificationService`).

Keep the `default_renderer` service registered so template rendering is available before any other service instantiates.

### Step 2: Connect external services

Define services keyed by ID:

- `default_renderer` instantiates `base:JinjaRenderer`, satisfying the requirement that exactly one `TemplateRenderer` exists.
- `otobo_znuny` points at `otobo-znuny:OTOBOZnunyTicketSystemService` and passes connection credentials inside `params`.
- `hf_classifier` resolves to `hf-local:HFClassificationService` with an optional API token.

These IDs (for example `otobo_znuny` and `hf_classifier`) will be referenced from pipe `injects` sections later.

### Step 3: Configure the orchestrator and runner

Use `base:SimpleSequentialOrchestrator` for a continuously running event loop. Its `params.orchestrator_sleep` controls the idle time between cycles. Inside `params.steps`, add a single `SimpleSequentialRunner`. This runner expects two nested `PipeConfig` definitions under `params`:

- `on` – a trigger pipe; we use `base:IntervalTrigger` with a `timedelta` interval (`PT60S` runs once per minute).
- `run` – the pipeline to execute when the trigger succeeds. Here we reference `base:CompositePipe`, which processes its own `params.steps` sequentially.

### Step 4: Define the composite pipeline steps

Inside the composite pipe, each element in `params.steps` is another `PipeConfig` that maps 1:1 to a pipe class:

1. **`fetch_open_tickets`** (`base:FetchTicketsPipe`) injects the ticket system service and loads incoming tickets via `ticket_search_criteria`.
2. **`ensure_tickets_found`** (`base:ExpressionPipe`) calls `fail()` if no tickets were fetched, stopping the runner gracefully.
3. **`queue_classifier`** (`base:ClassificationPipe`) injects the Hugging Face service and classifies the ticket text.
4. **`update_queue`** (`base:UpdateTicketPipe`) writes the new queue selection back to OTOBO/Znuny.
5. **`add_classification_note`** (`base:AddNotePipe`) records an audit trail of the automated classification.

All parameters reference earlier results using helper functions exposed by the Jinja renderer (`get_pipe_result`, `fail`, `get_env`, etc.).

### Complete configuration

Save the following validated configuration as `config.yml` in your working directory. It combines all steps described above and matches the current schema exactly.

```yaml
open_ticket_ai:
  api_version: "1"
  plugins:
    - otai-base
    - otai-otobo-znuny
    - otai-hf-local
  services:
    default_renderer:
      use: "base:JinjaRenderer"
    otobo_znuny:
      use: "otobo-znuny:OTOBOZnunyTicketSystemService"
      params:
        base_url: "https://helpdesk.example.com/otobo/nph-genericinterface.pl"
        username: "open_ticket_ai"
        password: "{{ get_env('OTOBO_API_TOKEN') }}"
    hf_classifier:
      use: "hf-local:HFClassificationService"
      params:
        api_token: "{{ get_env('HF_TOKEN') }}"
  orchestrator:
    id: ticket-automation
    use: "base:SimpleSequentialOrchestrator"
    params:
      orchestrator_sleep: "PT60S"
      steps:
        - id: ticket-routing-runner
          use: "base:SimpleSequentialRunner"
          params:
            on:
              id: every-minute
              use: "base:IntervalTrigger"
              params:
                interval: "PT60S"
            run:
              id: ticket-routing
              use: "base:CompositePipe"
              params:
                steps:
                  - id: fetch_open_tickets
                    use: "base:FetchTicketsPipe"
                    injects:
                      ticket_system: "otobo_znuny"
                    params:
                      ticket_search_criteria:
                        queue:
                          name: "OpenTicketAI::Incoming"
                        limit: 25
                  - id: ensure_tickets_found
                    use: "base:ExpressionPipe"
                    params:
                      expression: "{{ fail('No open tickets found') if (get_pipe_result('fetch_open_tickets','fetched_tickets') | length) == 0 else 'tickets ready' }}"
                  - id: queue_classifier
                    use: "base:ClassificationPipe"
                    injects:
                      classification_service: "hf_classifier"
                    params:
                      text: "{{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['subject'] }} {{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['body'] }}"
                      model_name: "softoft/otai-queue-de-bert-v1"
                  - id: update_queue
                    use: "base:UpdateTicketPipe"
                    injects:
                      ticket_system: "otobo_znuny"
                    params:
                      ticket_id: "{{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['id'] }}"
                      updated_ticket:
                        queue:
                          name: "{{ get_pipe_result('queue_classifier','label') }}"
                  - id: add_classification_note
                    use: "base:AddNotePipe"
                    injects:
                      ticket_system: "otobo_znuny"
                    params:
                      ticket_id: "{{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['id'] }}"
                      note:
                        subject: "Queue classification"
                        body: |
                          Auto-classified queue: {{ get_pipe_result('queue_classifier','label') }}
                          Confidence: {{ (get_pipe_result('queue_classifier','confidence') * 100) | round(1) }}%
```

## Running and verifying the pipeline

1. Install the required packages (core plus the plugins listed above).
2. Provide credentials through environment variables referenced in the configuration (for example `OTOBO_API_TOKEN`, `HF_TOKEN`).
3. Place the configuration file at `config.yml` in your working directory so `AppConfig` picks it up automatically.
4. Start the orchestrator:

   ```bash
   uv run python -m open_ticket_ai.main
   ```

`AppConfig` validates the YAML against the schema on startup. If a section is missing or a parameter name is wrong, the application exits with a descriptive validation error before any tickets are processed. Once running, the orchestrator executes the `SimpleSequentialRunner` every minute, applies the nested `CompositePipe` steps, and logs progress through the configured services.
