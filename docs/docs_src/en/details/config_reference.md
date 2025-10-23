###

TODO this is absoltely outdated.
but the good thing about how I setup the config. Almost everything is an InjectableConfig having same atributes.
Then for each Pipe, Service there are special params. There are about 10 Injectables. Create an overview table for them
and
then below that the details. what they do and what exactly arguments they get + for the Pipes the Result they produce
and examples if needed.

# Configuration Reference

Complete reference for Open Ticket AI configuration schema.

## Overview

This reference provides the complete schema for Open Ticket AI configuration files, auto-generated from the Python
Pydantic models. For practical examples and usage patterns, see the [Configuration Examples](configuration/examples.md).

## Quick Start

Minimal configuration structure:

```yaml
open_ticket_ai:
  plugins: [ ]
  infrastructure:
    logging:
      version: 1
  services: [ ]
  orchestrator:
    runners:
      - on:
          - id: my_trigger
            use: "open_ticket_ai.triggers.IntervalTrigger"
            params:
              interval: "60s"
        run:
          id: my_pipeline
          use: "open_ticket_ai.base.CompositePipe"
          steps: [ ]
```

## Root Configuration

| Field            | Type                                            | Required | Default | Description |
|------------------|-------------------------------------------------|----------|---------|-------------|
| `open_ticket_ai` | [RawOpenTicketAIConfig](#rawopenticketaiconfig) | ✓        |         |             |

## Type Definitions

### RawOpenTicketAIConfig

The main configuration object containing all application settings.

| Field            | Type                                          | Required | Default | Description                                           |
|------------------|-----------------------------------------------|----------|---------|-------------------------------------------------------|
| `plugins`        | array                                         |          |         | Plugin configurations                                 |
| `infrastructure` | [InfrastructureConfig](#infrastructureconfig) |          |         | Infrastructure settings (logging, template rendering) |
| `services`       | array                                         |          |         | Service definitions for dependency injection          |
| `orchestrator`   | [OrchestratorConfig](#orchestratorconfig)     |          |         | Pipeline and runner definitions                       |

**Example:**

```yaml
open_ticket_ai:
  plugins:
    - name: otobo_znuny
      config:
        base_url: "${OTOBO_BASE_URL}"
        api_token: "${OTOBO_API_TOKEN}"

  infrastructure:
    logging:
      version: 1
      root:
        level: INFO

  services:
    - id: ticket_classifier
      use: "my_plugin.TicketClassifier"
      params:
        model_name: "bert-base-classifier"

  orchestrator:
    runners:
      - on:
          - id: interval_trigger
            use: "open_ticket_ai.triggers.IntervalTrigger"
            params:
              interval: "60s"
        run:
          id: classify_pipeline
          steps:
            - id: fetch
              use: "otobo_znuny.pipes.FetchTickets"
            - id: classify
              use: "my_plugin.ClassifyPipe"
```

### OrchestratorConfig

Defines pipeline runners and default settings.

| Field      | Type           | Required | Default | Description                        |
|------------|----------------|----------|---------|------------------------------------|
| `defaults` | object or null |          | None    | Default parameters for all runners |
| `runners`  | array          |          |         | List of runner definitions         |

**Example:**

```yaml
orchestrator:
  defaults:
    timeout: "5m"
    retry:
      attempts: 3
      delay: "5s"
  runners:
    - on:
        - id: every_minute
          use: "open_ticket_ai.triggers.IntervalTrigger"
          params:
            interval: "60s"
      run:
        id: my_pipeline
        steps: [ ]
```

### RunnerDefinition

Defines a pipeline runner with its trigger and execution configuration.

| Field    | Type                          | Required | Default | Description                              |
|----------|-------------------------------|----------|---------|------------------------------------------|
| `id`     | string or null                |          | None    | Optional identifier for the runner       |
| `on`     | array                         |          |         | List of trigger definitions              |
| `run`    | [PipeConfig](#pipeconfig)     | ✓        |         | Pipeline to execute                      |
| `params` | [RunnerParams](#runnerparams) |          |         | Runner parameters (retry, timeout, etc.) |

**Example:**

```yaml
- id: classification_runner
  on:
    - id: interval_trigger
      use: "open_ticket_ai.triggers.IntervalTrigger"
      params:
        interval: "60s"
  run:
    id: classify_tickets
    steps:
      - id: fetch
        use: "otobo_znuny.pipes.FetchTickets"
  params:
    concurrency:
      max_workers: 4
    retry:
      attempts: 5
```

### RunnerParams

Parameters controlling runner behavior.

| Field         | Type                                                | Required | Default      | Description                                |
|---------------|-----------------------------------------------------|----------|--------------|--------------------------------------------|
| `concurrency` | [ConcurrencySettings](#concurrencysettings) or null |          | None         | Concurrency configuration                  |
| `retry`       | [RetrySettings](#retrysettings) or null             |          | None         | Retry configuration                        |
| `timeout`     | string or null                                      |          | None         | Maximum execution time (e.g., "5m", "30s") |
| `retry_scope` | string                                              |          | `"pipeline"` | Scope of retry logic                       |
| `priority`    | integer                                             |          | `10`         | Execution priority                         |

### TriggerDefinition

Defines when a pipeline should be executed.

| Field     | Type           | Required | Default                               | Description                                                 |
|-----------|----------------|----------|---------------------------------------|-------------------------------------------------------------|
| `uid`     | string         |          |                                       | Auto-generated unique identifier                            |
| `id`      | string or null |          | None                                  | User-defined identifier (auto-set to `uid` if not provided) |
| `use`     | string         |          | `"open_ticket_ai.base.CompositePipe"` | Fully qualified class name                                  |
| `injects` | object         |          |                                       | Dependencies to inject                                      |
| `params`  | any            |          |                                       | Trigger-specific parameters                                 |

**Note:** When `id` is not explicitly set, it automatically defaults to the `uid` value. This ensures all triggers have
a valid identifier for the orchestrator registry, preventing collisions and enabling trigger reuse across multiple
runners.

**Common Triggers:**

- `open_ticket_ai.triggers.IntervalTrigger` - Execute at regular intervals
- `open_ticket_ai.triggers.CronTrigger` - Execute on cron schedule
- `open_ticket_ai.triggers.ManualTrigger` - Execute manually

### PipeConfig

Configuration for a pipeline or pipe.

| Field        | Type              | Required | Default                               | Description                                                 |
|--------------|-------------------|----------|---------------------------------------|-------------------------------------------------------------|
| `uid`        | string            |          |                                       | Auto-generated unique identifier                            |
| `id`         | string or null    |          | None                                  | User-defined identifier (auto-set to `uid` if not provided) |
| `use`        | string            |          | `"open_ticket_ai.base.CompositePipe"` | Fully qualified class name                                  |
| `injects`    | object            |          |                                       | Dependencies to inject                                      |
| `params`     | any               |          |                                       | Pipe-specific parameters                                    |
| `if`         | string or boolean |          | `"True"`                              | Conditional execution (template expression)                 |
| `depends_on` | string or array   |          | []                                    | Dependencies on other pipes (by id)                         |
| `steps`      | array or null     |          | None                                  | Sub-steps for composite pipes                               |

**Example:**

<div v-pre>

```yaml
# Simple pipe
- id: fetch_tickets
  use: "otobo_znuny.pipes.FetchTickets"
  params:
    search:
      StateType: "Open"
      limit: 100

# Conditional pipe
- id: send_notification
  use: "my_plugin.NotifyPipe"
  if: "{{ context.pipes.classify.confidence > 0.8 }}"
  depends_on: classify

# Composite pipe with steps
- id: full_workflow
  use: "open_ticket_ai.base.CompositePipe"
  steps:
    - id: step1
      use: "my_plugin.Pipe1"
    - id: step2
      use: "my_plugin.Pipe2"
      depends_on: step1
```

</div>

### RenderableConfig

Base configuration for renderable components.

| Field     | Type           | Required | Default                               | Description                                                 |
|-----------|----------------|----------|---------------------------------------|-------------------------------------------------------------|
| `uid`     | string         |          |                                       | Auto-generated unique identifier                            |
| `id`      | string or null |          | None                                  | User-defined identifier (auto-set to `uid` if not provided) |
| `use`     | string         |          | `"open_ticket_ai.base.CompositePipe"` | Fully qualified class name                                  |
| `injects` | object         |          |                                       | Dependencies to inject                                      |
| `params`  | any            |          |                                       | Component-specific parameters                               |

**Note:** When `id` is not explicitly set, it automatically defaults to the `uid` value. This ensures all components
have a valid identifier.

### InfrastructureConfig

Infrastructure and system-level configuration.

| Field                      | Type                                              | Required | Default | Description                           |
|----------------------------|---------------------------------------------------|----------|---------|---------------------------------------|
| `logging`                  | [LoggingDictConfig](#loggingdictconfig)           |          |         | Python logging configuration          |
| `template_renderer_config` | [TemplateRendererConfig](#templaterendererconfig) |          |         | (Deprecated) Template renderer config |

**Example:**

```yaml
infrastructure:
  logging:
    version: 1
    formatters:
      simple:
        format: '%(levelname)s - %(message)s'
    handlers:
      console:
        class: logging.StreamHandler
        formatter: simple
    root:
      level: INFO
      handlers: [ console ]

  template_renderer_config:
    type: "jinja"
    env_config:
      prefix: "OTAI_"
      allowlist: [ "OTAI_*" ]
```

### LoggingDictConfig

Python dictConfig-compatible logging configuration.

| Field                      | Type                              | Required | Default | Description                 |
|----------------------------|-----------------------------------|----------|---------|-----------------------------|
| `version`                  | integer                           |          | `1`     | Config version (always 1)   |
| `disable_existing_loggers` | boolean or null                   |          | None    | Disable existing loggers    |
| `incremental`              | boolean or null                   |          | None    | Incremental configuration   |
| `root`                     | [RootConfig](#rootconfig) or null |          | None    | Root logger configuration   |
| `loggers`                  | object                            |          |         | Named logger configurations |
| `handlers`                 | object                            |          |         | Handler definitions         |
| `formatters`               | object                            |          |         | Formatter definitions       |
| `filters`                  | object                            |          |         | Filter definitions          |

See [Python logging.config documentation](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)
for complete reference.

### RootConfig

Root logger configuration.

| Field      | Type           | Required | Default | Description                                           |
|------------|----------------|----------|---------|-------------------------------------------------------|
| `level`    | string or null |          | None    | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `handlers` | array or null  |          | None    | Handler names to use                                  |
| `filters`  | array or null  |          | None    | Filter names to apply                                 |

### LoggerConfig

Named logger configuration.

| Field       | Type            | Required | Default | Description                |
|-------------|-----------------|----------|---------|----------------------------|
| `level`     | string or null  |          | None    | Logging level              |
| `handlers`  | array or null   |          | None    | Handler names              |
| `propagate` | boolean or null |          | None    | Propagate to parent logger |
| `filters`   | array or null   |          | None    | Filter names               |

### HandlerConfig

Logging handler configuration.

| Field       | Type           | Required | Default | Description                                   |
|-------------|----------------|----------|---------|-----------------------------------------------|
| `class`     | string         | ✓        |         | Handler class (e.g., `logging.StreamHandler`) |
| `level`     | string or null |          | None    | Minimum level to handle                       |
| `formatter` | string or null |          | None    | Formatter name                                |
| `filters`   | array or null  |          | None    | Filter names                                  |
| `()`        | string or null |          | None    | Alternative class specification               |

### FormatterConfig

Logging formatter configuration.

| Field     | Type           | Required | Default | Description                     |
|-----------|----------------|----------|---------|---------------------------------|
| `class`   | string or null |          | None    | Formatter class                 |
| `format`  | string or null |          | None    | Log message format              |
| `datefmt` | string or null |          | None    | Date format                     |
| `style`   | string or null |          | None    | Format style (%, {, $)          |
| `()`      | string or null |          | None    | Alternative class specification |

### FilterConfig

Logging filter configuration.

| Field   | Type           | Required | Default | Description                     |
|---------|----------------|----------|---------|---------------------------------|
| `class` | string or null |          | None    | Filter class                    |
| `name`  | string or null |          | None    | Filter name                     |
| `()`    | string or null |          | None    | Alternative class specification |

### TemplateRendererConfig

Template rendering configuration (deprecated - use services instead).

| Field        | Type                                                    | Required | Default | Description                        |
|--------------|---------------------------------------------------------|----------|---------|------------------------------------|
| `type`       | string                                                  | ✓        |         | Type of template renderer          |
| `env_config` | [TemplateRendererEnvConfig](#templaterendererenvconfig) |          |         | Environment variable configuration |

### TemplateRendererEnvConfig

Environment variable handling for template renderer.

| Field       | Type           | Required | Default   | Description                         |
|-------------|----------------|----------|-----------|-------------------------------------|
| `prefix`    | string or null |          | `"OTAI_"` | Primary environment variable prefix |
| `allowlist` | array or null  |          | None      | Allowed environment variable names  |
| `denylist`  | array or null  |          | None      | Denied environment variable names   |

**Example:**

```yaml
template_renderer_config:
  type: "jinja"
  env_config:
    prefix: "OTAI_"
    allowlist:
      - "OTAI_*"
      - "HOME"
      - "USER"
    denylist:
      - "OTAI_SECRET_*"
```

### ConcurrencySettings

Concurrency control settings.

| Field            | Type    | Required | Default  | Description                     |
|------------------|---------|----------|----------|---------------------------------|
| `max_workers`    | integer |          | `1`      | Maximum concurrent workers      |
| `when_exhausted` | string  |          | `"wait"` | Behavior when workers exhausted |

**Example:**

```yaml
concurrency:
  max_workers: 4
  when_exhausted: "wait"
```

### RetrySettings

Retry behavior configuration.

| Field            | Type    | Required | Default | Description                    |
|------------------|---------|----------|---------|--------------------------------|
| `attempts`       | integer |          | `3`     | Maximum retry attempts         |
| `delay`          | string  |          | `"5s"`  | Initial delay between retries  |
| `backoff_factor` | number  |          | `2.0`   | Exponential backoff multiplier |
| `max_delay`      | string  |          | `"30s"` | Maximum delay between retries  |
| `jitter`         | boolean |          | `True`  | Add random jitter to delays    |

**Example:**

```yaml
retry:
  attempts: 5
  delay: "3s"
  backoff_factor: 2.0
  max_delay: "60s"
  jitter: true
```

## Environment Variables

Use environment variables in configuration with the `${VAR_NAME}` syntax:

<div v-pre>

```yaml
# Required variable (fails if not set)
api_token: "${OTOBO_API_TOKEN}"

# Optional with default value
base_url: "${OTOBO_BASE_URL:-https://default.example.com}"

# In template expressions
note: "User: ${USER}, Time: {{ now() }}"
```

</div>

**Syntax:**

- `${VAR}` - Required variable (error if missing)
- `${VAR:-default}` - Optional with default value
- Variables are resolved before template rendering

## Template Expressions

Use Jinja2 template expressions for dynamic values:

<div v-pre>

```yaml
# Access context values
note_text: "Classified as {{ context.queue }} at {{ now() }}"

# Conditional logic
if: "{{ context.pipes.classify.confidence > 0.8 }}"

# Reference pipe outputs
queue_id: "{{ context.pipes.fetch_tickets.results[0].queue_id }}"
```

</div>

**Common template functions:**

<div v-pre>

- `{{ now() }}` - Current timestamp
- `{{ env.VAR_NAME }}` - Environment variable access
- `{{ context.pipes.pipe_id.result }}` - Access pipe outputs

</div>

## YAML Anchors and Aliases

Use YAML anchors to define reusable configuration blocks:

```yaml
# Define with anchor (&)
services:
  - &common_search
    StateType: "Open"
    limit: 100

# Reference with alias (*)
orchestrator:
  runners:
    - on: [ ]
      run:
        id: pipeline1
        steps:
          - id: fetch
            use: "otobo_znuny.pipes.FetchTickets"
            params:
              search: *common_search

    # Merge with << notation
    - on: [ ]
      run:
        id: pipeline2
        steps:
          - id: fetch
            use: "otobo_znuny.pipes.FetchTickets"
            params:
              search:
                <<: *common_search
                limit: 50  # Override one field
```

## Validation Rules

Configuration is validated on startup:

1. **Required fields** must be present
2. **Field types** must match schema (string, integer, boolean, array, object)
3. **Reference keys** must exist when using `depends_on`
4. **Template syntax** must be valid Jinja2
5. **Environment variables** must be set if required (no default)

Validation errors will include:

- Field path (e.g., `orchestrator.runners[0].run.steps[1].id`)
- Expected type vs actual type
- Missing required fields
- Invalid values

## Related Documentation

- [Configuration Examples](configuration/examples.md) - Complete working configurations
- [Configuration Structure](configuration/config_structure.md) - File organization and best practices
- [YAML Definitions and Anchors](configuration/defs_and_anchors.md) - Advanced YAML techniques
- [Environment Variables](configuration/environment_variables.md) - Environment variable reference
- [Template Rendering](../developers/template_rendering.md) - Template syntax and functions

---

_This reference is auto-generated from Pydantic models. Last updated: 2025-10-12_
