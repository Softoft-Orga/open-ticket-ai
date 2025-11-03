---
description: Understand Open Ticket AI's configuration lifecycle, template rendering with Jinja2, dependency injection, and how YAML transforms into runtime objects.
pageClass: full-page
aside: true
---

# Configuration & Template Rendering

Open Ticket AI allows you to create dynamic configurations using **YAML** plus **Jinja2 template
expressions** like
<div class="pre">
<code>{ { ... } }</code> without spaces
</div>
This lets you reuse values, read environment variables, and reference results from other pipes — all
while keeping configuration clean and declarative.

<InlineExample class="mb-3" slug="fetch-addnote" />

## Key Concepts

# Injectable Configuration Structure

Both **Services** and **Pipes** in Open Ticket AI use the same configuration structure called
`InjectableConfig`. Understanding these three core attributes will help you configure any component
in the system.

## Configuration Attributes

| Attribute | Type             | Description                                                                                           | Example                            |
|-----------|------------------|-------------------------------------------------------------------------------------------------------|------------------------------------|
| `use`     | `TEXT`           | Identifies which component to create. Format: `plugin-name:ComponentName`                             | `"base:FetchTicketsPipe"`          |
| `injects` | name:value pairs | Maps constructor parameter names to service IDs, connecting dependencies to this component            | `{ ticket_system: "otobo_znuny" }` |
| `params`  | name:value pairs | Configuration parameters specific to this component. Each component type expects different parameters | `{ limit: 25, queue: "Support" }`  |

## Key Differences: Services vs. Pipes

While both use `InjectableConfig`, they differ in usage:

### Services

- Defined once in the `services` section
- Reusable across multiple pipes
- Must have an `id` field for reference
- Usually represent external systems

**Example:**

```yaml
services:
  otobo_znuny:
    use: "otobo-znuny:OTOBOZnunyTicketSystemService"
    injects: { }
    params:
      base_url: "https://helpdesk.example.com"
      password: "{{ get_env('OTOBO_PASSWORD') }}"
```

### Pipes

- Defined inside pipeline `steps`
- Execute actions in sequence
- Also have an `id` field to reference results
- Use services via `injects` to perform work

**Example:**

```yaml
steps:
  - id: fetch_tickets
    use: "base:FetchTicketsPipe"
    injects:
      ticket_system: "otobo_znuny"
    params:
      ticket_search_criteria:
        limit: 25
```

## Template Rendering

All `params` and `injects` values support Jinja2 templating for dynamic configuration:

```yaml
params:
  api_key: "{{ get_env('API_KEY') }}"
  queue: "{{ get_pipe_result('classify', 'label') }}"
```

---

**Related:
** [Template Rendering](../details/_template_rendering.md) · [Dependency Injection](../developers/dependency_injection.md)

## Config Reference

Here is the Markdown table describing the **full config structure** clean and ready for your docs.

| Path                                        | Type                              | Description                                                   | Example                                       |                      |
|---------------------------------------------|-----------------------------------|---------------------------------------------------------------|-----------------------------------------------|----------------------|
| `otai`                                      | `OpenTicketAIConfig`              | Main application config root.                                 |                                               |                      |
| `otai.api_version`                          | `str`                             | API version for compatibility.                                | `"1"`                                         |                      |
| `otai.plugins[]`                            | `list[str]`                       | Python module paths of plugins to load.                       | `"otai_hf_local"`                             |                      |
| `otai.infrastructure`                       | `InfrastructureConfig`            | Infra-level settings.                                         |                                               |                      |
| `otai.infrastructure.logging`               | `LoggingConfig`                   | Logging configuration.                                        |                                               |                      |
| `otai.infrastructure.logging.level`         | `str`                             | Min log level.                                                | `"INFO"`                                      |                      |
| `otai.infrastructure.logging.log_to_file`   | `bool`                            | Enable file logging.                                          | `false`                                       |                      |
| `otai.infrastructure.logging.log_file_path` | `str                              | None`                                                         | Log file path when enabled.                   | `"/var/log/app.log"` |
| `otai.infrastructure.logging.log_format`    | `str`                             | Python logging format string.                                 | `"%(asctime)s - %(levelname)s - %(message)s"` |                      |
| `otai.infrastructure.logging.date_format`   | `str`                             | Date format for logs.                                         | `"%Y-%m-%d %H:%M:%S"`                         |                      |
| `otai.services`                             | `dict[str, InjectableConfigBase]` | Map of service-id → DI config.                                |                                               |                      |
| `otai.services.<id>`                        | `InjectableConfigBase`            | One service definition.                                       |                                               |                      |
| `otai.services.<id>.use`                    | `str`                             | Python class path to instantiate.                             | `"pkg.mod.Class"`                             |                      |
| `otai.services.<id>.injects`                | `dict[str,str]`                   | DI bindings: ctor-param → service-id.                         | `{ "db": "ticket-db" }`                       |                      |
| `otai.services.<id>.params`                 | `dict[str,Any]`                   | Constructor params (templating allowed).                      | `{ "url": "{\{ get_env('DB_URL') }\}" }`      |                      |
| `otai.services.<id>.id`                     | `str`                             | Optional explicit identifier (when using `InjectableConfig`). | `"ticket-db"`                                 |                      |
| `otai.orchestrator`                         | `PipeConfig`                      | Orchestrator pipeline root.                                   |                                               |                      |
| `otai.orchestrator.id`                      | `str`                             | Pipe identifier (for referencing). (inherits)                 | `"root"`                                      |                      |
| `otai.orchestrator.use`                     | `str`                             | Python class path of the Pipe. (inherits)                     | `"project.pipes.CompositePipe"`               |                      |
| `otai.orchestrator.injects`                 | `dict[str,str]`                   | DI to sub-pipes/services. (inherits)                          | `{ "step1": "ticket-db" }`                    |                      |
| `otai.orchestrator.params`                  | `dict[str,Any]`                   | Pipe parameters (templating allowed). (inherits)              | `{}`                                          |                      |

**Tiny example**
<div class="pre">

```yaml
otai:
  api_version: "1"
  plugins: [ ]
  infrastructure:
    logging:
      level: "INFO"
  services:
    ticket-db:
      use: "plugin_name:Database"
      params:
        url: "{{ get_env('DB_URL') }}"
  orchestrator:
    id: "root"
    use: "base:CompositePipe"
    injects:
      step1: "ticket-db"
    params: { }
```

</div>

## Available helper functions (for `config.yml` templates)

| Function           | Parameters                                          | Returns                                                          | Errors if…                    |
|--------------------|-----------------------------------------------------|------------------------------------------------------------------|-------------------------------|
| `at_path`          | `value: Any`, `path: text`                          | Nested value at `"a.b.c"` path; supports dicts + Pydantic models | Invalid path format           |
| `has_failed`       | `pipe_id: text`                                     | `True` if the given pipe result is marked failed                 | Unknown pipe ID               |
| `get_pipe_result`  | `pipe_id: text`, `data_key: text;default = "value"` | Value stored in previous pipe result under given `data_key`      | Pipe or key missing           |
| `get_parent_param` | `param_key: text`                                   | Inherited parent parameter value                                 | Parent missing or key missing |
| `get_env`          | `name: text`                                        | Value of environment variable                                    | Env var missing               |
| `fail`             | *(none)*                                            | A “FailMarker” sentinel object to signal explicit failure paths  | —                             |

---

## Usage examples in `config.yml`

### Read an environment variable

```yaml
api:
  token: "{{ get_env('API_TOKEN') }}"
  baseUrl: "https://api.example.com"
```

### Consume a previous pipe’s result

```yaml
classification:
  label: "{{ get_pipe_result('classify_ticket', 'label') }}"
  confidence: "{{ get_pipe_result('classify_ticket', 'score') }}"
  isLowConfidence: "{{ get_pipe_result('classify_ticket', 'score') < 0.6 }}"
```

### Check if a pipe failed

```yaml
shouldRetry: "{{ has_failed('fetch_customer') }}"
```

### Read a parent parameter

```yaml
timeoutMs: "{{ get_parent_param('timeoutMs') }}"
```

### Emit an explicit failure marker

```yaml
result: "{{ fail() }}"
```

### Access nested data (dict or Pydantic model)

```yaml
userCity: "{{ at_path(user, 'address.city') }}"
```

## Full Examples / Templates

See full working examples of config.yml

[Config Examples](../users/config_examples.md).
