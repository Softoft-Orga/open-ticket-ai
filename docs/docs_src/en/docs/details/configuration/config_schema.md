# Configuration Schema Reference

Complete reference for Open Ticket AI configuration schema.

## RawOpenTicketAIConfig Structure

The root configuration object with these main sections:

```yaml
plugins: []              # Plugin configurations
infrastructure: {}       # General settings
defs: {}                # Reusable definitions
orchestrator: {}        # Pipeline orchestration
```

## Plugins Section

Configure plugins to extend functionality:

```yaml
plugins:
  - name: plugin_name
    config:
      key: value
```

### Fields
- `name` (string, required): Plugin identifier
- `config` (object, optional): Plugin-specific configuration

## General Configuration Section

Application-wide settings:

```yaml
infrastructure:
  log_level: "INFO"
  environment: "production"
  max_workers: 4
```

### Common Fields
- `log_level`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- `environment`: Deployment environment
- `max_workers`: Number of worker threads

## Definitions Section

Reusable YAML definitions using anchors:

```yaml
defs:
  common_search: &common_search
    StateType: "Open"
    limit: 100
  
  queue_mapping: &queue_mapping
    billing: 1
    support: 2
    technical: 3
```

Reference definitions with `*anchor_name` or merge with `<<: *anchor_name`.

## Orchestrator Section

Pipeline scheduling and execution:

```yaml
orchestrator:
  pipelines:
    - name: pipeline_name
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: pipe1
        - pipe_name: pipe2
```

### Pipeline Fields
- `name` (string, required): Pipeline identifier
- `run_every_milli_seconds` (integer, required): Execution interval
- `pipes` (array, required): List of pipes to execute

### Pipe Configuration
- `pipe_name` (string, required): Registered pipe name
- Additional fields: Pipe-specific configuration

## Field Types and Validation

### String Fields
- Must be quoted if containing special characters
- Support template expressions with `{{ }}`
- Environment variables with `${VAR_NAME}`

### Integer Fields
- Numeric values without quotes
- Positive integers for intervals and counts
- Can use multipliers (e.g., 1000 for milliseconds)

### Boolean Fields
- `true` or `false` (lowercase, unquoted)

### Array Fields
- List of items with `-` prefix
- Can be single-line `[item1, item2]` or multi-line

### Object Fields
- Key-value pairs
- Support nesting
- Can use YAML anchors for reuse

## Required vs Optional Fields

### Required
- `orchestrator.pipelines`: At least one pipeline
- `orchestrator.pipelines[].name`: Pipeline name
- `orchestrator.pipelines[].pipes`: Pipe list
- `orchestrator.pipelines[].pipes[].pipe_name`: Pipe identifier

### Optional
- `plugins`: Plugins are optional
- `infrastructure`: Uses defaults if not specified
- `defs`: Only needed for reusable definitions
- Most pipe-specific fields have defaults

## Validation Rules

Configuration is validated on startup:
- Required fields must be present
- Field types must match schema
- Reference keys must exist
- Template syntax must be valid
- Environment variables must be set (if required)

## Environment Variable Substitution

Use environment variables in configuration:

```yaml
api_token: "${OTOBO_API_TOKEN}"
base_url: "${OTOBO_BASE_URL:-https://default.com}"
```

Syntax:
- `${VAR}`: Required variable
- `${VAR:-default}`: Optional with default value

## Template Expressions

Use Jinja2 templates for dynamic values:

```yaml
note_text: "Classified as {{ context.queue }} at {{ now() }}"
```

## Examples

See [Configuration Examples](examples.md) for complete working configurations.

## Related Documentation

- [Configuration Structure](config_structure.md)
- [YAML Definitions and Anchors](defs_and_anchors.md)
- [Environment Variables](environment_variables.md)
- [Template Rendering](../../developers/code/template_rendering.md)
