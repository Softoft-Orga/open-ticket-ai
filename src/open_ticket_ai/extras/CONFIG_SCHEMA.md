# Configuration Schema Reference

_Auto-generated from Pydantic models_

---

## Root Configuration

| Field            | Type                                            | Required | Default | Description |
|------------------|-------------------------------------------------|----------|---------|-------------|
| `open_ticket_ai` | [RawOpenTicketAIConfig](#rawopenticketaiconfig) | ✓        |         |             |

## Type Definitions

### FilterConfig

| Field   | Type           | Required | Default | Description |
|---------|----------------|----------|---------|-------------|
| `class` | string or null |          | None    |             |
| `name`  | string or null |          | None    |             |
| `()`    | string or null |          | None    |             |

### FormatterConfig

| Field     | Type           | Required | Default | Description |
|-----------|----------------|----------|---------|-------------|
| `class`   | string or null |          | None    |             |
| `format`  | string or null |          | None    |             |
| `datefmt` | string or null |          | None    |             |
| `style`   | string or null |          | None    |             |
| `()`      | string or null |          | None    |             |

### HandlerConfig

| Field       | Type           | Required | Default | Description |
|-------------|----------------|----------|---------|-------------|
| `class`     | string         | ✓        |         |             |
| `level`     | string or null |          | None    |             |
| `formatter` | string or null |          | None    |             |
| `filters`   | array or null  |          | None    |             |
| `()`        | string or null |          | None    |             |

### InfrastructureConfig

| Field                       | Type                                    | Required | Default | Description |
|-----------------------------|-----------------------------------------|----------|---------|-------------|
| `logging`                   | [LoggingDictConfig](#loggingdictconfig) |          |         |             |
| `default_template_renderer` | string                                  | ✓        |         |             |

### LoggerConfig

| Field       | Type            | Required | Default | Description |
|-------------|-----------------|----------|---------|-------------|
| `level`     | string or null  |          | None    |             |
| `handlers`  | array or null   |          | None    |             |
| `propagate` | boolean or null |          | None    |             |
| `filters`   | array or null   |          | None    |             |

### LoggingDictConfig

| Field                      | Type                              | Required | Default | Description |
|----------------------------|-----------------------------------|----------|---------|-------------|
| `version`                  | integer                           |          | `1`     |             |
| `disable_existing_loggers` | boolean or null                   |          | None    |             |
| `incremental`              | boolean or null                   |          | None    |             |
| `root`                     | [RootConfig](#rootconfig) or null |          | None    |             |
| `loggers`                  | object                            |          |         |             |
| `handlers`                 | object                            |          |         |             |
| `formatters`               | object                            |          |         |             |
| `filters`                  | object                            |          |         |             |

### OrchestratorConfig

| Field     | Type  | Required | Default | Description |
|-----------|-------|----------|---------|-------------|
| `runners` | array |          |         |             |

### PipeConfig

| Field        | Type              | Required | Default                               | Description |
|--------------|-------------------|----------|---------------------------------------|-------------|
| `uid`        | string            |          |                                       |             |
| `id`         | string            | ✓        |                                       |             |
| `use`        | string            |          | `"open_ticket_ai.base.CompositePipe"` |             |
| `injects`    | object            |          |                                       |             |
| `params`     | object            |          |                                       |             |
| `if`         | string or boolean |          | `"True"`                              |             |
| `depends_on` | string or array   |          | []                                    |             |
| `steps`      | array or null     |          | None                                  |             |

### RawOpenTicketAIConfig

| Field            | Type                                          | Required | Default | Description |
|------------------|-----------------------------------------------|----------|---------|-------------|
| `plugins`        | array                                         |          |         |             |
| `infrastructure` | [InfrastructureConfig](#infrastructureconfig) |          |         |             |
| `services`       | array                                         |          |         |             |
| `orchestrator`   | [OrchestratorConfig](#orchestratorconfig)     |          |         |             |

### RenderableConfig

| Field     | Type   | Required | Default                               | Description |
|-----------|--------|----------|---------------------------------------|-------------|
| `uid`     | string |          |                                       |             |
| `id`      | string | ✓        |                                       |             |
| `use`     | string |          | `"open_ticket_ai.base.CompositePipe"` |             |
| `injects` | object |          |                                       |             |
| `params`  | object |          |                                       |             |

### RootConfig

| Field      | Type           | Required | Default | Description |
|------------|----------------|----------|---------|-------------|
| `level`    | string or null |          | None    |             |
| `handlers` | array or null  |          | None    |             |
| `filters`  | array or null  |          | None    |             |

### RunnerDefinition

| Field | Type                      | Required | Default | Description |
|-------|---------------------------|----------|---------|-------------|
| `id`  | string or null            |          | None    |             |
| `on`  | array                     | ✓        |         |             |
| `run` | [PipeConfig](#pipeconfig) | ✓        |         |             |

### TriggerConfig

| Field     | Type   | Required | Default                               | Description |
|-----------|--------|----------|---------------------------------------|-------------|
| `uid`     | string |          |                                       |             |
| `id`      | string | ✓        |                                       |             |
| `use`     | string |          | `"open_ticket_ai.base.CompositePipe"` |             |
| `injects` | object |          |                                       |             |
| `params`  | object |          |                                       |             |

