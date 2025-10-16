# Configuration Schema Reference

_Auto-generated from Pydantic models_

---

## Root Configuration

| Field                          | Type                                            | Required | Default                                                  | Description |
|--------------------------------|-------------------------------------------------|----------|----------------------------------------------------------|-------------|
| `open_ticket_ai`               | [RawOpenTicketAIConfig](#rawopenticketaiconfig) | ✓        |                                                          |             |
| └─ `plugins`                   | array of string                                 |          |                                                          |             |
| └─ `infrastructure`            | [InfrastructureConfig](#infrastructureconfig)   |          |                                                          |             |
| └─ `logging`                   | [LoggingConfig](#loggingconfig)                 |          |                                                          |             |
| └─ `level`                     | string                                          |          | `"INFO"`                                                 |             |
| └─ `log_to_file`               | boolean                                         |          | `False`                                                  |             |
| └─ `log_file_path`             | string or null                                  |          | `None`                                                   |             |
| └─ `log_format`                | string                                          |          | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |             |
| └─ `date_format`               | string                                          |          | `"%Y-%m-%d %H:%M:%S"`                                    |             |
| └─ `default_template_renderer` | string                                          | ✓        |                                                          |             |
| └─ `services`                  | array of [RenderableConfig](#renderableconfig)  |          |                                                          |             |
| └─ `uid`                       | string                                          |          |                                                          |             |
| └─ `id`                        | string                                          | ✓        |                                                          |             |
| └─ `use`                       | string                                          |          | `"open_ticket_ai.base.CompositePipe"`                    |             |
| └─ `injects`                   | object                                          |          |                                                          |             |
| └─ `params`                    | object                                          |          |                                                          |             |
| └─ `orchestrator`              | [OrchestratorConfig](#orchestratorconfig)       |          |                                                          |             |
| └─ `runners`                   | array of [RunnerDefinition](#runnerdefinition)  |          |                                                          |             |
| └─ `id`                        | string or null                                  |          | `None`                                                   |             |
| └─ `on`                        | array of [TriggerConfig](#triggerconfig)        | ✓        |                                                          |             |
| └─ `run`                       | [PipeConfig](#pipeconfig)                       | ✓        |                                                          |             |

## Type Definitions

### InfrastructureConfig

| Field                       | Type                            | Required | Default                                                  | Description |
|-----------------------------|---------------------------------|----------|----------------------------------------------------------|-------------|
| `logging`                   | [LoggingConfig](#loggingconfig) |          |                                                          |             |
| └─ `level`                  | string                          |          | `"INFO"`                                                 |             |
| └─ `log_to_file`            | boolean                         |          | `False`                                                  |             |
| └─ `log_file_path`          | string or null                  |          | `None`                                                   |             |
| └─ `log_format`             | string                          |          | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |             |
| └─ `date_format`            | string                          |          | `"%Y-%m-%d %H:%M:%S"`                                    |             |
| `default_template_renderer` | string                          | ✓        |                                                          |             |

### LoggingConfig

| Field           | Type           | Required | Default                                                  | Description |
|-----------------|----------------|----------|----------------------------------------------------------|-------------|
| `level`         | string         |          | `"INFO"`                                                 |             |
| `log_to_file`   | boolean        |          | `False`                                                  |             |
| `log_file_path` | string or null |          | `None`                                                   |             |
| `log_format`    | string         |          | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |             |
| `date_format`   | string         |          | `"%Y-%m-%d %H:%M:%S"`                                    |             |

### OrchestratorConfig

| Field           | Type                                           | Required | Default                               | Description |
|-----------------|------------------------------------------------|----------|---------------------------------------|-------------|
| `runners`       | array of [RunnerDefinition](#runnerdefinition) |          |                                       |             |
| └─ `id`         | string or null                                 |          | `None`                                |             |
| └─ `on`         | array of [TriggerConfig](#triggerconfig)       | ✓        |                                       |             |
| └─ `uid`        | string                                         |          |                                       |             |
| └─ `id`         | string                                         | ✓        |                                       |             |
| └─ `use`        | string                                         |          | `"open_ticket_ai.base.CompositePipe"` |             |
| └─ `injects`    | object                                         |          |                                       |             |
| └─ `params`     | object                                         |          |                                       |             |
| └─ `run`        | [PipeConfig](#pipeconfig)                      | ✓        |                                       |             |
| └─ `uid`        | string                                         |          |                                       |             |
| └─ `id`         | string                                         | ✓        |                                       |             |
| └─ `use`        | string                                         |          | `"open_ticket_ai.base.CompositePipe"` |             |
| └─ `injects`    | object                                         |          |                                       |             |
| └─ `params`     | object                                         |          |                                       |             |
| └─ `if`         | string or boolean                              |          | `"True"`                              |             |
| └─ `depends_on` | string or array of string                      |          | `[]`                                  |             |
| └─ `steps`      | array of [PipeConfig](#pipeconfig) or null     |          | `None`                                |             |

### PipeConfig

| Field        | Type                                       | Required | Default                               | Description |
|--------------|--------------------------------------------|----------|---------------------------------------|-------------|
| `uid`        | string                                     |          |                                       |             |
| `id`         | string                                     | ✓        |                                       |             |
| `use`        | string                                     |          | `"open_ticket_ai.base.CompositePipe"` |             |
| `injects`    | object                                     |          |                                       |             |
| `params`     | object                                     |          |                                       |             |
| `if`         | string or boolean                          |          | `"True"`                              |             |
| `depends_on` | string or array of string                  |          | `[]`                                  |             |
| `steps`      | array of [PipeConfig](#pipeconfig) or null |          | `None`                                |             |

### RawOpenTicketAIConfig

| Field                          | Type                                           | Required | Default                                                  | Description |
|--------------------------------|------------------------------------------------|----------|----------------------------------------------------------|-------------|
| `plugins`                      | array of string                                |          |                                                          |             |
| `infrastructure`               | [InfrastructureConfig](#infrastructureconfig)  |          |                                                          |             |
| └─ `logging`                   | [LoggingConfig](#loggingconfig)                |          |                                                          |             |
| └─ `level`                     | string                                         |          | `"INFO"`                                                 |             |
| └─ `log_to_file`               | boolean                                        |          | `False`                                                  |             |
| └─ `log_file_path`             | string or null                                 |          | `None`                                                   |             |
| └─ `log_format`                | string                                         |          | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |             |
| └─ `date_format`               | string                                         |          | `"%Y-%m-%d %H:%M:%S"`                                    |             |
| └─ `default_template_renderer` | string                                         | ✓        |                                                          |             |
| `services`                     | array of [RenderableConfig](#renderableconfig) |          |                                                          |             |
| └─ `uid`                       | string                                         |          |                                                          |             |
| └─ `id`                        | string                                         | ✓        |                                                          |             |
| └─ `use`                       | string                                         |          | `"open_ticket_ai.base.CompositePipe"`                    |             |
| └─ `injects`                   | object                                         |          |                                                          |             |
| └─ `params`                    | object                                         |          |                                                          |             |
| `orchestrator`                 | [OrchestratorConfig](#orchestratorconfig)      |          |                                                          |             |
| └─ `runners`                   | array of [RunnerDefinition](#runnerdefinition) |          |                                                          |             |
| └─ `id`                        | string or null                                 |          | `None`                                                   |             |
| └─ `on`                        | array of [TriggerConfig](#triggerconfig)       | ✓        |                                                          |             |
| └─ `uid`                       | string                                         |          |                                                          |             |
| └─ `id`                        | string                                         | ✓        |                                                          |             |
| └─ `use`                       | string                                         |          | `"open_ticket_ai.base.CompositePipe"`                    |             |
| └─ `injects`                   | object                                         |          |                                                          |             |
| └─ `params`                    | object                                         |          |                                                          |             |
| └─ `run`                       | [PipeConfig](#pipeconfig)                      | ✓        |                                                          |             |
| └─ `uid`                       | string                                         |          |                                                          |             |
| └─ `id`                        | string                                         | ✓        |                                                          |             |
| └─ `use`                       | string                                         |          | `"open_ticket_ai.base.CompositePipe"`                    |             |
| └─ `injects`                   | object                                         |          |                                                          |             |
| └─ `params`                    | object                                         |          |                                                          |             |
| └─ `if`                        | string or boolean                              |          | `"True"`                                                 |             |
| └─ `depends_on`                | string or array of string                      |          | `[]`                                                     |             |
| └─ `steps`                     | array of [PipeConfig](#pipeconfig) or null     |          | `None`                                                   |             |

### RenderableConfig

| Field     | Type   | Required | Default                               | Description |
|-----------|--------|----------|---------------------------------------|-------------|
| `uid`     | string |          |                                       |             |
| `id`      | string | ✓        |                                       |             |
| `use`     | string |          | `"open_ticket_ai.base.CompositePipe"` |             |
| `injects` | object |          |                                       |             |
| `params`  | object |          |                                       |             |

### RunnerDefinition

| Field           | Type                                       | Required | Default                               | Description |
|-----------------|--------------------------------------------|----------|---------------------------------------|-------------|
| `id`            | string or null                             |          | `None`                                |             |
| `on`            | array of [TriggerConfig](#triggerconfig)   | ✓        |                                       |             |
| └─ `uid`        | string                                     |          |                                       |             |
| └─ `id`         | string                                     | ✓        |                                       |             |
| └─ `use`        | string                                     |          | `"open_ticket_ai.base.CompositePipe"` |             |
| └─ `injects`    | object                                     |          |                                       |             |
| └─ `params`     | object                                     |          |                                       |             |
| `run`           | [PipeConfig](#pipeconfig)                  | ✓        |                                       |             |
| └─ `uid`        | string                                     |          |                                       |             |
| └─ `id`         | string                                     | ✓        |                                       |             |
| └─ `use`        | string                                     |          | `"open_ticket_ai.base.CompositePipe"` |             |
| └─ `injects`    | object                                     |          |                                       |             |
| └─ `params`     | object                                     |          |                                       |             |
| └─ `if`         | string or boolean                          |          | `"True"`                              |             |
| └─ `depends_on` | string or array of string                  |          | `[]`                                  |             |
| └─ `steps`      | array of [PipeConfig](#pipeconfig) or null |          | `None`                                |             |

### TriggerConfig

| Field     | Type   | Required | Default                               | Description |
|-----------|--------|----------|---------------------------------------|-------------|
| `uid`     | string |          |                                       |             |
| `id`      | string | ✓        |                                       |             |
| `use`     | string |          | `"open_ticket_ai.base.CompositePipe"` |             |
| `injects` | object |          |                                       |             |
| `params`  | object |          |                                       |             |

