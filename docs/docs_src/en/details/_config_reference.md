# Configuration Reference

Open Ticket AI loads its YAML configuration into the `OpenTicketAIConfig` model. The schema is built around a single
`open_ticket_ai` object that contains API/version metadata, infrastructure settings, dependency-injected services, and
the pipeline orchestrator definition. 【F:src/open_ticket_ai/core/config/config_models.py†L17-L37】

## Root configuration shape

| Field            | Type                                             | Description                                                                                                                                                                 |
|------------------|--------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `api_version`    | `str`                                            | Optional version string that defaults to `"1"`. 【F:src/open_ticket_ai/core/config/config_models.py†L18-L21】                                                                 |
| `plugins`        | `list[str]`                                      | Python modules that expose plugin entry points. Each plugin contributes additional injectables to the registry. 【F:src/open_ticket_ai/core/config/config_models.py†L22-L25】 |
| `infrastructure` | [`InfrastructureConfig`](#infrastructure-config) | Logging and other host-level concerns. 【F:src/open_ticket_ai/core/config/config_models.py†L26-L29】                                                                          |
| `services`       | `dict[str, InjectableConfigBase]`                | Map of injectable service definitions keyed by the identifier you will reference in pipelines. 【F:src/open_ticket_ai/core/config/config_models.py†L30-L33】                  |
| `orchestrator`   | [`PipeConfig`](#orchestrator-and-pipeconfig)     | Top-level pipe (typically an orchestrator) executed by the runtime. 【F:src/open_ticket_ai/core/config/config_models.py†L34-L36】                                             |

### Infrastructure config

`InfrastructureConfig` currently exposes logging configuration and defaults to the built-in logging schema. 【F:
src/open_ticket_ai/core/config/config_models.py†L10-L14】

## Services dictionary (`open_ticket_ai.services`)

All services share the same base schema because they are instances of `InjectableConfigBase`. Each entry lives under the
`services` dictionary and uses the dictionary key as its identifier. 【F:
src/open_ticket_ai/core/config/config_models.py†L30-L43】

| Field     | Type             | Description                                                                                                                                                                                             |
|-----------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `use`     | `str`            | Registry identifier of the injectable implementation to instantiate. Defaults to `"otai_base:CompositePipe"`. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L9-L15】                       |
| `injects` | `dict[str, str]` | Optional mapping from constructor parameter names to other service identifiers. This is how you connect one injectable to another. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L16-L20】 |
| `params`  | `dict[str, Any]` | Arbitrary configuration passed as keyword arguments to the injectable’s parameter model. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L21-L25】                                           |

When the runtime materialises services it merges the dictionary key into the model, making the identifier available to
dependency injection consumers. 【F:src/open_ticket_ai/core/config/config_models.py†L39-L43】

### How registry identifiers are built

Plugins derive registry identifiers from their module name. Every plugin starts with the prefix `otai-`; the runtime
strips that prefix and concatenates the remainder with the injectable class name using `:`. For example, the `otai_base`
plugin contributes identifiers such as `base:CompositePipe`. 【F:src/open_ticket_ai/core/config/app_config.py†L16-L21】【F:
src/open_ticket_ai/core/plugins/plugin.py†L18-L46】

## Orchestrator and `PipeConfig`

Pipelines are described with `PipeConfig`, which extends the same base injectable schema with an `id` field, forbids
extra keys, and keeps all values immutable for consistent hashing. 【F:
src/open_ticket_ai/core/pipes/pipe_models.py†L9-L15】 Each pipe returns a `PipeResult` indicating success, skip, failure,
and any structured data produced for downstream steps. 【F:src/open_ticket_ai/core/pipes/pipe_models.py†L17-L68】

## Updated configuration example

The snippet below mirrors the current `OpenTicketAIConfig` structure: services are keyed by identifier, and the
orchestrator is a `PipeConfig` that renders nested pipes and triggers.

```yaml
open_ticket_ai:
  api_version: "1"
  plugins:
    - otai_base
    - otai_hf_local
    - otai_otobo_znuny

  infrastructure:
    logging:
      version: 1
      root:
        level: INFO

  services:
    ticketing:
      use: "otobo-znuny:OTOBOZnunyTicketSystemService"
      params:
        base_url: "${OTOBO_BASE_URL}"
        username: "${OTOBO_USERNAME}"
        password: "${OTOBO_PASSWORD}"
    classifier:
      use: "hf-local:HFClassificationService"
      params:
        api_token: "${HF_TOKEN}"
    renderer:
      use: "base:JinjaRenderer"

  orchestrator:
    id: support-orchestrator
    use: "base:SimpleSequentialOrchestrator"
    params:
      orchestrator_sleep: "0:00:05"
      exception_sleep: "0:01:00"
      steps:
        - id: ticket-runner
          use: "base:SimpleSequentialRunner"
          params:
            on:
              id: every-minute
              use: "base:IntervalTrigger"
              params:
                interval: "0:01:00"
            run:
              id: ticket-flow
              use: "base:CompositePipe"
              params:
                steps:
                  - id: fetch
                    use: "base:FetchTicketsPipe"
                    injects:
                      ticket_system: ticketing
                    params:
                      ticket_search_criteria:
                        queue:
                          id: Raw
                          name: Raw
                        limit: 1
                  - id: classify
                    use: "base:ClassificationPipe"
                    injects:
                      classification_service: classifier
                    params:
                      text: "{{ get_pipe_result('fetch').data.fetched_tickets[0].body }}"
                      model_name: "distilbert-base-uncased"
                  - id: respond
                    use: "base:AddNotePipe"
                    injects:
                      ticket_system: ticketing
                    params:
                      ticket_id: "{{ get_pipe_result('fetch').data.fetched_tickets[0].id }}"
                      note:
                        subject: "Classification result"
                        body: "{{ get_pipe_result('classify').data.label }}"
```

## Core injectables

The table summarises the core injectables shipped with the default plugins. Follow the links for parameter and output
details.

| Identifier                                  | Plugin             | Kind              | Summary                                                                                                       |
|---------------------------------------------|--------------------|-------------------|---------------------------------------------------------------------------------------------------------------|
| `base:JinjaRenderer`                        | `otai_base`        | Template renderer | Async Jinja renderer with helpers for accessing pipe output. [Details](#basejinjarenderer)                    |
| `base:SimpleSequentialOrchestrator`         | `otai_base`        | Orchestrator pipe | Loops through child pipes on a schedule, retrying on failure. [Details](#basesimplesequentialorchestrator)    |
| `base:SimpleSequentialRunner`               | `otai_base`        | Runner pipe       | Executes a `run` pipe when the `on` trigger succeeds. [Details](#basesimplesequentialrunner)                  |
| `base:CompositePipe`                        | `otai_base`        | Composite pipe    | Evaluates nested pipes in sequence and merges their results. [Details](#basecompositepipe)                    |
| `base:ExpressionPipe`                       | `otai_base`        | Utility pipe      | Returns literal values or fails when a `FailMarker` is produced. [Details](#baseexpressionpipe)               |
| `base:ClassificationPipe`                   | `otai_base`        | AI pipe           | Delegates to a `ClassificationService` and returns the model output. [Details](#baseclassificationpipe)       |
| `base:IntervalTrigger`                      | `otai_base`        | Trigger pipe      | Emits success when the configured interval elapses. [Details](#baseintervaltrigger)                           |
| `base:FetchTicketsPipe`                     | `otai_base`        | Ticket pipe       | Loads tickets via an injected `TicketSystemService`. [Details](#basefetchticketspipe)                         |
| `base:UpdateTicketPipe`                     | `otai_base`        | Ticket pipe       | Applies updates to a ticket through the injected ticket service. [Details](#baseupdateticketpipe)             |
| `base:AddNotePipe`                          | `otai_base`        | Ticket pipe       | Appends a note to a ticket using the ticket service. [Details](#baseaddnotepipe)                              |
| `hf-local:HFClassificationService`          | `otai_hf_local`    | Service           | Hugging Face text-classification client with optional auth token. [Details](#hf-localhfclassificationservice) |
| `otobo-znuny:OTOBOZnunyTicketSystemService` | `otai_otobo_znuny` | Service           | Async ticket service backed by the OTOBO/Znuny API. [Details](#otobo-znunyotoboznuny-ticketsystemservice)     |

### `base:JinjaRenderer`

* **Use**: `base:JinjaRenderer`
* **Params**: none (defaults to an empty `StrictBaseModel`). 【F:
  packages/otai_base/src/otai_base/template_renderers/jinja_renderer.py†L21-L38】
* **Behaviour**: Renders strings, lists, and dicts asynchronously with helper globals such as `get_pipe_result` and
  `fail`. 【F:packages/otai_base/src/otai_base/template_renderers/jinja_renderer.py†L29-L38】

### `base:SimpleSequentialOrchestrator`

* **Use**: `base:SimpleSequentialOrchestrator`
* **Params**:
    * `orchestrator_sleep` (`timedelta`) – wait time between cycles. 【F:
      packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
    * `exception_sleep` (`timedelta`) – delay before retrying after an error. 【F:
      packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
    * `always_retry` (`bool`) – rethrow on failure when `false`. 【F:
      packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
    * `steps` (`list[PipeConfig]`) – nested steps rendered with full template support. 【F:
      packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L27】
* **Output**: Runs indefinitely, returning the aggregate `PipeResult` of all steps each cycle. Failures respect
  `always_retry`. 【F:packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L24-L40】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L36-L52】

### `base:SimpleSequentialRunner`

* **Use**: `base:SimpleSequentialRunner`
* **Params**:
    * `on` (`PipeConfig`) – trigger pipe; the runner skips execution when it fails. 【F:
      packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L12-L36】
    * `run` (`PipeConfig`) – pipe to execute when the trigger succeeds. 【F:
      packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L12-L36】
* **Output**: Returns the downstream pipe result or a skipped `PipeResult` with a diagnostic message. 【F:
  packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L26-L36】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L17-L64】

### `base:CompositePipe`

* **Use**: `base:CompositePipe`
* **Params**: `steps` – ordered list of `PipeConfig` definitions. Extra keys are allowed to support custom composite
  implementations. 【F:packages/otai_base/src/otai_base/pipes/composite_pipe.py†L11-L33】
* **Output**: Executes each step in order, stops on the first failure, and merges data from all successful steps with
  `PipeResult.union`. 【F:packages/otai_base/src/otai_base/pipes/composite_pipe.py†L29-L47】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L36-L52】

### `base:ExpressionPipe`

* **Use**: `base:ExpressionPipe`
* **Params**: `expression` – literal value or rendered expression result. 【F:
  packages/otai_base/src/otai_base/pipes/expression_pipe.py†L13-L18】
* **Output**: Returns `PipeResult.success` with `{"value": expression}` unless the expression evaluates to a
  `FailMarker`, in which case it fails. 【F:packages/otai_base/src/otai_base/pipes/expression_pipe.py†L21-L38】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L59-L68】

### `base:ClassificationPipe`

* **Use**: `base:ClassificationPipe`
* **Injects**: `classification_service` must point to a `ClassificationService` implementation.
* **Params**:
    * `text` (`str`) – content to classify.
    * `model_name` (`str`) – identifier forwarded to the service.
    * `api_token` (`str | None`) – optional token overriding the service default. 【F:
      packages/otai_base/src/otai_base/pipes/classification_pipe.py†L19-L52】
* **Output**: Successful results include the full `ClassificationResult` payload (label, confidence, optional scores).
  【F:packages/otai_base/src/otai_base/pipes/classification_pipe.py†L54-L63】

### `base:IntervalTrigger`

* **Use**: `base:IntervalTrigger`
* **Params**: `interval` (`timedelta`) – required elapsed time between successes. 【F:
  packages/otai_base/src/otai_base/pipes/interval_trigger_pipe.py†L11-L28】
* **Output**: Returns success once the interval has elapsed since the previous run; otherwise returns a failure result
  so downstream runners can skip work. 【F:packages/otai_base/src/otai_base/pipes/interval_trigger_pipe.py†L21-L30】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L17-L64】

### `base:FetchTicketsPipe`

* **Use**: `base:FetchTicketsPipe`
* **Injects**: `ticket_system` must resolve to a `TicketSystemService` implementation. 【F:
  packages/otai_base/src/otai_base/ticket_system_integration/ticket_system_service.py†L1-L27】
* **Params**: `ticket_search_criteria` describing queue, limit, and other filters. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/fetch_tickets_pipe.py†L11-L26】
* **Output**: Success result with `data.fetched_tickets` set to a list of `UnifiedTicket` records. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/fetch_tickets_pipe.py†L20-L26】

### `base:UpdateTicketPipe`

* **Use**: `base:UpdateTicketPipe`
* **Injects**: `ticket_system` (same as above).
* **Params**:
    * `ticket_id` (`str | int`) – target ticket identifier.
    * `updated_ticket` (`UnifiedTicket`) – fields to update. 【F:
      packages/otai_base/src/otai_base/pipes/ticket_system_pipes/update_ticket_pipe.py†L11-L28】
* **Output**: Returns success when the ticket service confirms the update. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/update_ticket_pipe.py†L21-L31】

### `base:AddNotePipe`

* **Use**: `base:AddNotePipe`
* **Injects**: `ticket_system`.
* **Params**:
    * `ticket_id` (`str | int`) – ticket receiving the note.
    * `note` (`UnifiedNote`) – subject/body payload. 【F:
      packages/otai_base/src/otai_base/pipes/ticket_system_pipes/add_note_pipe.py†L13-L40】
* **Output**: Returns success after delegating to the ticket service to append the note. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/add_note_pipe.py†L27-L40】

### `hf-local:HFClassificationService`

* **Use**: `hf-local:HFClassificationService`
* **Params**: `api_token` (`str | None`) – default Hugging Face token used when requests omit a token. 【F:
  packages/otai_hf_local/src/otai_hf_local/hf_classification_service.py†L105-L158】
* **Behaviour**: Lazily loads and caches a Hugging Face transformers pipeline, logs in when a token is provided, and
  exposes synchronous/asynchronous classification helpers. 【F:
  packages/otai_hf_local/src/otai_hf_local/hf_classification_service.py†L34-L163】

### `otobo-znuny:OTOBOZnunyTicketSystemService`

* **Use**: `otobo-znuny:OTOBOZnunyTicketSystemService`
* **Params** (`RenderedOTOBOZnunyTSServiceParams`):
    * `base_url` – OTOBO/Znuny endpoint base URL.
    * `username` / `password` – credentials for the configured web service.
    * `webservice_name` – optional service name override (defaults to `OpenTicketAI`).
    * `operation_urls` – mapping of ticket operations to relative API paths. 【F:
      packages/otai_otobo_znuny/src/otai_otobo_znuny/models.py†L44-L76】
* **Behaviour**: Creates and logs in an `OTOBOZnunyClient`, then implements the `TicketSystemService` interface for
  searching, retrieving, updating, and annotating tickets. 【F:
  packages/otai_otobo_znuny/src/otai_otobo_znuny/oto_znuny_ts_service.py†L21-L135】
