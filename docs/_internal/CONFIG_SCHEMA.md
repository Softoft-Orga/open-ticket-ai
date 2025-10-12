# Configuration Schema Reference

_Auto-generated from Pydantic models_

---

## Root Configuration

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `open_ticket_ai` | [RawOpenTicketAIConfig](#rawopenticketaiconfig) | ✓ |  |  |


## Type Definitions

### ConcurrencySettings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `max_workers` | integer |  | `1` |  |
| `when_exhausted` | string |  | `"wait"` |  |


### FilterConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `class` | string or null |  | None |  |
| `name` | string or null |  | None |  |
| `()` | string or null |  | None |  |


### FormatterConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `class` | string or null |  | None |  |
| `format` | string or null |  | None |  |
| `datefmt` | string or null |  | None |  |
| `style` | string or null |  | None |  |
| `()` | string or null |  | None |  |


### HandlerConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `class` | string | ✓ |  |  |
| `level` | string or null |  | None |  |
| `formatter` | string or null |  | None |  |
| `filters` | array or null |  | None |  |
| `()` | string or null |  | None |  |


### InfrastructureConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `logging` | [LoggingDictConfig](#loggingdictconfig) |  |  |  |
| `template_renderer_config` | [TemplateRendererConfig](#templaterendererconfig) |  |  | (Deprecated) in future versions will be set through the services section |


### LoggerConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `level` | string or null |  | None |  |
| `handlers` | array or null |  | None |  |
| `propagate` | boolean or null |  | None |  |
| `filters` | array or null |  | None |  |


### LoggingDictConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `version` | integer |  | `1` |  |
| `disable_existing_loggers` | boolean or null |  | None |  |
| `incremental` | boolean or null |  | None |  |
| `root` | [RootConfig](#rootconfig) or null |  | None |  |
| `loggers` | object |  |  |  |
| `handlers` | object |  |  |  |
| `formatters` | object |  |  |  |
| `filters` | object |  |  |  |


### OrchestratorConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `defaults` | object or null |  | None |  |
| `runners` | array |  |  |  |


### PipeConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `uid` | string |  |  |  |
| `id` | string or null |  | None |  |
| `use` | string |  | `"open_ticket_ai.base.CompositePipe"` |  |
| `injects` | object |  |  |  |
| `params` | any |  |  |  |
| `if` | string or boolean |  | `"True"` |  |
| `depends_on` | string or array |  | [] |  |
| `steps` | array or null |  | None |  |


### RawOpenTicketAIConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `plugins` | array |  |  |  |
| `infrastructure` | [InfrastructureConfig](#infrastructureconfig) |  |  |  |
| `services` | array |  |  |  |
| `orchestrator` | [OrchestratorConfig](#orchestratorconfig) |  |  |  |


### RenderableConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `uid` | string |  |  |  |
| `id` | string or null |  | None |  |
| `use` | string |  | `"open_ticket_ai.base.CompositePipe"` |  |
| `injects` | object |  |  |  |
| `params` | any |  |  |  |


### RetrySettings

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `attempts` | integer |  | `3` |  |
| `delay` | string |  | `"5s"` |  |
| `backoff_factor` | number |  | `2.0` |  |
| `max_delay` | string |  | `"30s"` |  |
| `jitter` | boolean |  | `True` |  |


### RootConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `level` | string or null |  | None |  |
| `handlers` | array or null |  | None |  |
| `filters` | array or null |  | None |  |


### RunnerDefinition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | string or null |  | None |  |
| `on` | array |  |  |  |
| `run` | [PipeConfig](#pipeconfig) | ✓ |  |  |
| `params` | [RunnerParams](#runnerparams) |  |  |  |


### RunnerParams

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `concurrency` | [ConcurrencySettings](#concurrencysettings) or null |  | None |  |
| `retry` | [RetrySettings](#retrysettings) or null |  | None |  |
| `timeout` | string or null |  | None |  |
| `retry_scope` | string |  | `"pipeline"` |  |
| `priority` | integer |  | `10` |  |


### TemplateRendererConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `type` | string | ✓ |  | Type of template renderer |
| `env_config` | [TemplateRendererEnvConfig](#templaterendererenvconfig) |  |  | Environment variable configuration |


### TemplateRendererEnvConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `prefix` | string or null |  | `"OTAI_"` | Primary environment variable prefix |
| `allowlist` | array or null |  | None | Allowed environment variable names |
| `denylist` | array or null |  | None | Denied environment variable names |


### TriggerDefinition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `uid` | string |  |  |  |
| `id` | string or null |  | None |  |
| `use` | string |  | `"open_ticket_ai.base.CompositePipe"` |  |
| `injects` | object |  |  |  |
| `params` | any |  |  |  |

