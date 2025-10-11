# Configuration Structure

Understanding the YAML structure and organization of Open Ticket AI configuration files.

## YAML Structure Overview

Configuration files follow this structure:

```yaml
# 1. Plugins
plugins:
  - name: plugin_name
    config: {}

# 2. Infrastructure Configuration
infrastructure:
  logging:
    version: 1

# 3. Reusable Definitions
defs:
  definition_name: &anchor_name
    key: value

# 4. Orchestrator (Pipelines)
orchestrator:
  pipelines:
    - name: pipeline_name
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: pipe_name
```

## Main Configuration Sections

### 1. Plugins

Load and configure plugins:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_URL}"
      api_token: "${OTOBO_TOKEN}"
  
  - name: hf_local
    config:
      model_name: "bert-base-uncased"
      device: "cpu"
```

### 2. Infrastructure Configuration

Core infrastructure settings (currently only logging):

```yaml
infrastructure:
  logging:
    version: 1
    disable_existing_loggers: false
    handlers:
      console:
        class: logging.StreamHandler
    formatters:
      std:
        format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    root:
      level: INFO
      handlers: [console]
```

### 3. Definitions (defs)

Reusable configuration blocks:

```yaml
defs:
  # Reusable search criteria
  open_tickets: &open_tickets
    StateType: "Open"
    limit: 100
  
  # Reusable queue mapping
  queues: &queues
    billing: 1
    support: 2
```

### 4. Orchestrator

Pipeline definitions:

```yaml
orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
          search: *open_tickets
        - pipe_name: classify_queue
        - pipe_name: update_tickets
```

## Configuration Organization Best Practices

### File Organization

**Single File**
- Good for simple setups
- Easy to understand
- Quick to edit

**Multiple Files**
- Split by environment (dev, staging, prod)
- Separate plugin configs
- Share common definitions

### Naming Conventions

- Use descriptive pipeline names: `classify_tickets`, `update_priorities`
- Use lowercase with underscores: `fetch_tickets`, not `fetchTickets`
- Group related pipes in pipelines
- Name definitions clearly: `open_tickets`, `queue_mapping`

### Comments

Use comments to document:
- Why specific values are chosen
- Dependencies between configurations
- Known limitations or gotchas

```yaml
# Fetch only open tickets to reduce API load
pipes:
  - pipe_name: fetch_tickets
    search:
      StateType: "Open"  # Critical: only process open tickets
```

### Template Usage

Use templates for dynamic values:

```yaml
pipes:
  - pipe_name: add_note
    # Template includes timestamp and confidence
    note_text: "Classified at {{ now() }} with {{ context.confidence }}% confidence"
```

### Multi-Environment Configuration

### Environment Variables

Different values per environment:

```yaml
# production.yml
infrastructure:
  logging:
    version: 1
    root:
      level: WARNING

# development.yml
infrastructure:
  logging:
    version: 1
    root:
      level: DEBUG
```

### Configuration Inheritance

Use YAML merge for shared settings:

```yaml
# base.yml
common: &common
  timeout: 30
  retry_count: 3

# Merge into specific configs
production:
  <<: *common
  environment: "prod"
```

### File Naming

- `config.yml`: Main configuration
- `config.dev.yml`: Development overrides
- `config.prod.yml`: Production overrides
- `config.test.yml`: Testing configuration

## Configuration Loading

Configuration is loaded in this order:
1. Default values
2. Base configuration file
3. Environment-specific overrides
4. Environment variables
5. Command-line arguments

## Validation

Configuration is validated on load:
- Schema compliance
- Required fields present
- Valid references
- Template syntax
- Type checking

## Related Documentation

- [Configuration Schema](config_schema.md)
- [Definitions and Anchors](defs_and_anchors.md)
- [Environment Variables](environment_variables.md)
- [Configuration Examples](examples.md)
