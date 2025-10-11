# YAML Definitions and Anchors

Learn how to use YAML anchors and aliases to create reusable configuration definitions.

## YAML Anchors and Aliases

YAML supports anchors (`&`) and aliases (`*`) for reusing configuration blocks.

### Basic Syntax

```yaml
# Define with anchor (&)
definition: &my_anchor
  key: value
  another: data

# Reference with alias (*)
usage: *my_anchor
```

## Reusable Definitions in `defs` Section

The `defs` section stores reusable configuration:

```yaml
defs:
  # Common search criteria
  open_tickets: &open_tickets
    StateType: "Open"
    limit: 100
  
  # Queue ID mapping
  queues: &queues
    billing: 1
    support: 2
    technical: 3
  
  # Common timeout settings
  timeouts: &timeouts
    connect_timeout: 10
    read_timeout: 30
```

## Using Definitions

Reference definitions throughout your configuration:

```yaml
orchestrator:
  pipelines:
    - name: fetch_and_classify
      pipes:
        # Use the search criteria
        - pipe_name: fetch_tickets
          search: *open_tickets
        
        # Use the queue mapping
        - pipe_name: update_queue
          queue_map: *queues
```

## Merging Definitions with `<<: *anchor`

Merge definitions with additional fields:

```yaml
defs:
  base_search: &base_search
    StateType: "Open"
    limit: 100

orchestrator:
  pipelines:
    - name: search_pipeline
      pipes:
        - pipe_name: fetch_tickets
          search:
            <<: *base_search  # Merge base definition
            QueueIDs: [1, 2]  # Add additional fields
```

Result:
```yaml
search:
  StateType: "Open"
  limit: 100
  QueueIDs: [1, 2]
```

## Multiple Merges

Merge multiple definitions:

```yaml
defs:
  base_config: &base
    timeout: 30
  
  retry_config: &retry
    max_retries: 3
    retry_delay: 5

pipes:
  - pipe_name: fetch_data
    config:
      <<: [*base, *retry]  # Merge both
      additional: setting
```

## Best Practices for Reusable Configuration

### 1. Use Descriptive Names

```yaml
# Good
defs:
  open_tickets_last_hour: &recent_open
    StateType: "Open"
    create_time_after: "{{ now() - timedelta(hours=1) }}"

# Bad
defs:
  search1: &s1
    StateType: "Open"
```

### 2. Group Related Definitions

```yaml
defs:
  # Search criteria group
  searches:
    open: &search_open
      StateType: "Open"
    closed: &search_closed
      StateType: "Closed"
  
  # Queue mappings group
  queues:
    production: &queues_prod
      billing: 1
      support: 2
    development: &queues_dev
      billing: 10
      support: 20
```

### 3. Don't Overuse

Only create definitions for values used multiple times:

```yaml
# Good: Used in multiple places
defs:
  common_timeout: &timeout 30

# Bad: Used only once
defs:
  one_time_value: &unused
    rarely_used: true
```

### 4. Document Complex Definitions

```yaml
defs:
  # Advanced search: filters tickets from last 24h
  # with priority > 3 and assigned to support queues
  advanced_search: &advanced
    StateType: "Open"
    PriorityID: ">3"
    QueueIDs: [1, 2, 3]
    create_time_after: "{{ now() - timedelta(days=1) }}"
```

### 5. Environment-Specific Definitions

```yaml
defs:
  # Production settings
  prod: &prod_settings
    log_level: "WARNING"
    retry_count: 5
  
  # Development settings
  dev: &dev_settings
    log_level: "DEBUG"
    retry_count: 1

infrastructure:
  <<: *prod_settings  # Use appropriate environment
```

## Common Patterns

### Search Criteria Template

```yaml
defs:
  base_search: &base_search
    limit: 100
    OrderBy: "Created"
    OrderDirection: "DESC"
  
  open_search: &open_search
    <<: *base_search
    StateType: "Open"
  
  urgent_search: &urgent_search
    <<: *open_search
    PriorityID: ">3"
```

### Plugin Configuration

```yaml
defs:
  otobo_common: &otobo_common
    verify_ssl: true
    timeout: 30
    max_retries: 3

plugins:
  - name: otobo_znuny
    config:
      <<: *otobo_common
      base_url: "${OTOBO_URL}"
      api_token: "${OTOBO_TOKEN}"
```

### Pipe Configuration Template

```yaml
defs:
  classification_config: &classify_config
    confidence_threshold: 0.7
    fallback_queue: "General"

pipes:
  - pipe_name: classify_queue
    <<: *classify_config
  
  - pipe_name: classify_priority
    <<: *classify_config
    confidence_threshold: 0.8  # Override
```

## Limitations and Gotchas

### Cannot Override Scalars

```yaml
defs:
  base: &base
    timeout: 30

# This REPLACES, doesn't merge with scalar
config:
  <<: *base
  timeout: 60  # This works
```

### Order Matters

```yaml
# Later values override earlier
config:
  <<: *default
  timeout: 60  # Overrides default
  <<: *override  # This can override timeout again!
```

### Anchors Are File-Scoped

Anchors only work within the same YAML file. For multi-file configurations, use environment variables or include mechanisms.

## Related Documentation

- [Configuration Schema](config_schema.md)
- [Configuration Structure](config_structure.md)
- [Environment Variables](environment_variables.md)
