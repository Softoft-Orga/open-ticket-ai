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
  default_template_renderer: "jinja_default"

# 3. Services (formerly Definitions)
services:
  - id: service_id
    use: "module:ClassName"
    params: {}

# 4. Orchestrator (Pipelines)
orchestrator:
  runners:
    - on:
        id: trigger_id
        use: "module:TriggerClass"
      run:
        id: pipeline_id
        steps: []
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

Core infrastructure settings including logging and template renderer:

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
  
  # Default template renderer (bootstrapped first)
  default_template_renderer: "jinja_default"
```

### 3. Services

Registerable services including template renderers and ticket systems:

```yaml
services:
  # Template renderer service (bootstrapped before all other services)
  - id: "jinja_default"
    use: "open_ticket_ai.core.template_rendering:JinjaRenderer"
    params:
      env_config:
        prefix: "OTAI_"
      autoescape: false
  
  # Ticket system service (can use templating)
  - id: "otobo_znuny"
    use: "otai_otobo_znuny:OTOBOZnunyTicketSystemService"
    params:
      base_url: "http://example.com/otobo"
      password: "{{ env.OTAI_OTOBO_PASSWORD }}"  # Rendered by jinja_default
```

**Important**: The TemplateRenderer service specified in `infrastructure.default_template_renderer` 
is always instantiated first, and its params are NEVER templated (raw config only). 
All other services and pipes can use templating in their configs.

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
