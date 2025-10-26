---
description: Understand Open Ticket AI's configuration lifecycle, template rendering with Jinja2, dependency injection, and how YAML transforms into runtime objects.
pageClass: full-page
aside: false
---

# Configuration & Template Rendering

Open Ticket AI allows you to create dynamic configurations using **YAML** plus **Jinja2 template
expressions** like
<div class="pre">

`{\{ ... }\}`

</div>
This lets you reuse values, read environment variables, and reference results from other pipes — all
while keeping configuration clean and declarative.

## Configuration Lifecycle

The following diagram illustrates the complete lifecycle of configuration from YAML to runtime
objects:

## Template Rendering Scope

When templates are rendered during pipe execution, the rendering scope is built from the *
*PipeContext** structure:

## Key Concepts

## Available helper functions (for `config.yml` templates)

| Function           | Parameters                                | Returns                                                          | Errors if…                    |
|--------------------|-------------------------------------------|------------------------------------------------------------------|-------------------------------|
| `at_path`          | `value: Any`, `path: str`                 | Nested value at `"a.b.c"` path; supports dicts + Pydantic models | Invalid path format           |
| `has_failed`       | `pipe_id: str`                            | `True` if the given pipe result is marked failed                 | Unknown pipe ID               |
| `get_pipe_result`  | `pipe_id: str`, `data_key: str = "value"` | Value stored in previous pipe result under given `data_key`      | Pipe or key missing           |
| `get_parent_param` | `param_key: str`                          | Inherited parent parameter value                                 | Parent missing or key missing |
| `get_env`          | `name: str`                               | Value of environment variable                                    | Env var missing               |
| `fail`             | *(none)*                                  | A “FailMarker” sentinel object to signal explicit failure paths  | —                             |

---

## Usage examples in `config.yml`

### Read an environment variable

```yaml
api:
  token: "{{ get_env('API_TOKEN') }}"
  baseUrl: "https://api.example.com"
```

### Access nested data (dict or Pydantic model)

```yaml
userCity: "{{ at_path(user, 'address.city') }}"
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

---

## Config Reference

Here is the Markdown table describing the **full config structure** clean and ready for your docs.

---

# Config Structure — Nested (single table)

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
      use: "project.services.Database"
      params:
        url: "{{ get_env('DB_URL') }}"
  orchestrator:
    id: "root"
    use: "project.pipes.CompositePipe"
    injects:
      step1: "ticket-db"
    params: { }
```

</div>
