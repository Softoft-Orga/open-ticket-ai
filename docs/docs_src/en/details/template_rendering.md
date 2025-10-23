# TODO

luckily not much changed.the custom fucntins changed, but still jinjaa2.
planning on extending this adding possibility to inject the services into the templates so that you can do await
ticket_system.add_note(...) directly from the template.

# Template Rendering

Open Ticket AI uses template rendering to make configurations dynamic and adaptable to different environments and
runtime conditions. This allows you to customize behavior without changing code.

## What is Template Rendering?

Template rendering processes special placeholders in your configuration files, replacing them with actual values at
runtime. This enables:

- Using environment variables in configs
- Referencing results from previous pipeline steps
- Conditional logic based on context
- Dynamic service configurations

## Jinja2 Templates

Open Ticket AI uses [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/), a powerful templating engine for Python.
Jinja2 provides:

- Variable substitution: `{{ variable }}`
- Conditional blocks: `{% if condition %}...{% endif %}`
- Loops: `{% for item in list %}...{% endfor %}`
- Filters: `{{ value | filter }}`

For complete Jinja2 documentation, visit the [official Jinja2 site](https://jinja.palletsprojects.com/en/3.1.x/).

## Custom Template Functions

In addition to standard Jinja2 features, Open Ticket AI provides custom functions for accessing runtime data:

### `env(key, default=None)`

Access environment variables:

```yaml
params:
  api_key: "{{ env('API_KEY') }}"
  timeout: "{{ env('TIMEOUT', '30') }}"
```

### `pipe_result(pipe_id)`

Access results from previous pipes in the current pipeline:

```yaml
params:
  ticket_data: "{{ pipe_result('fetch_tickets').data }}"
```

### `has_failed(pipe_id)`

Check if a previous pipe failed:

```yaml
if: "{{ not has_failed('validate_input') }}"
```

### `at_path(data, path)`

Navigate nested data structures:

```yaml
params:
  user_name: "{{ at_path(ticket, 'metadata.user.name') }}"
```

## Available Context

Templates have access to different variables depending on when they're rendered:

### Global Context (Always Available)

- Environment variables via `env()` function
- Infrastructure configuration values

### Pipeline Context

When rendering pipeline-level configurations:

- `context.params`: Pipeline parameters from `orchestrator.pipelines[].params`
- Results from previous pipeline runs

### Pipe Context

When rendering individual pipes:

- `context.params`: Current pipe parameters
- `context.pipes[pipe_id]`: Results from previous pipes in this pipeline
- All parent contexts

## When Rendering Happens

Different parts of your configuration are rendered at different times:

### Service Instantiation

Services in the `services` section are rendered when the application starts, before any pipelines run. They have access
to global context only.

### Pipeline Creation

Pipeline definitions are rendered when pipelines are created. They have access to global and pipeline context.

### Pipe Execution

Individual pipes are rendered just before execution. They have access to global, pipeline, and pipe context.

## What Gets Rendered

Template rendering applies to string values in these configuration sections:

### Services

- `params` values
- `injects` keys and values

### Orchestrator

- `pipelines[].params` values
- `pipelines[].pipes[].params` values
- `pipelines[].pipes[].if` conditions
- `pipelines[].pipes[].depends_on` lists

### Pipes

- All parameter values
- Conditional expressions
- Dependency specifications

Note: The template renderer configuration itself (`infrastructure.template_renderer_config`) is never rendered - it's
used raw to bootstrap the rendering system.

## Examples

### Using Environment Variables

```yaml
services:
  - id: api_client
    use: "mypackage:APIClient"
    params:
      base_url: "{{ env('API_BASE_URL', 'https://api.example.com') }}"
      api_key: "{{ env('API_KEY') }}"
```

### Pipeline Parameters

```yaml
orchestrator:
  pipelines:
    - name: process_tickets
      params:
        threshold: 0.8
      pipes:
        - id: classify
          use: "mypackage:Classifier"
          params:
            confidence_threshold: "{{ context.params.threshold }}"
```

### Pipe Dependencies

```yaml
pipes:
  - id: fetch_data
    use: "mypackage:Fetcher"

  - id: process_data
    use: "mypackage:Processor"
    params:
      input: "{{ pipe_result('fetch_data').data }}"
    depends_on: [ fetch_data ]
    if: "{{ not has_failed('fetch_data') }}"
```

## Best Practices

- Use environment variables for secrets and environment-specific values
- Keep templates simple and readable
- Test your templates with different context values
- Use the `env()` function with defaults for optional variables
- Avoid complex logic in templates - prefer configuration over code
