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

## Custom Template Helpers

In addition to standard Jinja2 features, Open Ticket AI provides custom helper functions that expose runtime data to
templates.

### `get_env(env_name)`

Reads the value of an environment variable. Rendering fails if the variable is not defined, ensuring required values
are provided.

```yaml
params:
  api_key: "{{ get_env('API_KEY') }}"
  timeout_seconds: "{{ get_env('TIMEOUT_SECONDS') | int }}"
```

### `get_pipe_result(pipe_id, data_key='value')`

Retrieves a value from a previously executed pipe. Pipe results are stored as dictionaries; use `data_key` to select a
specific entry. The helper raises a render error if the key does not exist.

```yaml
params:
  classification: "{{ get_pipe_result('classify') }}"  # reads the default `value`
  confidence: "{{ get_pipe_result('classify', 'confidence') }}"
```

### `has_failed(pipe_id)`

Returns `True` when the referenced pipe completed execution unsuccessfully (and was not skipped).

```yaml
if: "{{ not has_failed('fetch_ticket') }}"
```

### `at_path(data, path)`

Traverses nested dictionaries or Pydantic models using dot notation.

```yaml
params:
  requester_email: "{{ at_path(ticket, 'metadata.requester.email') }}"
```

### `get_parent_param(param_key)`

Makes parameters from a parent context available to nested (composite) pipes. When no parent parameter is present or
when the key is missing, rendering fails so configuration issues surface early.

```yaml
params:
  expression: "{{ get_parent_param('threshold') * 100 }}"
```

### `fail()`

Creates a special marker recognised by the Expression pipe. Returning this marker allows a template expression to
explicitly fail a pipe instead of raising an exception.

```yaml
expression: "{{ fail() if confidence < 0.6 else result }}"
```

## Template Context

Templates receive a context dictionary that varies with the rendering stage. The keys appear directly in the template
(global objects do not require a `context.` prefix).

### Global Context (Always Available)

- Jinja helpers such as `get_env`, `get_pipe_result`, and `at_path`
- Configuration values passed explicitly in the render call

### Pipeline Context

When rendering pipeline-level configuration:

- `params`: Pipeline parameters defined in `orchestrator.pipelines[].params`
- `pipe_results`: Historical execution results keyed by pipe ID, when available

### Pipe Context

When rendering individual pipes during execution:

- `params`: Parameters passed to the current pipe
- `pipe_results`: Results from previously executed pipes in the same pipeline
- `parent_params`: Parameters from the parent pipe (if the pipe is nested)

Parent parameters are now populated automatically for nested pipelines, so composite pipes can coordinate with their
children using `get_parent_param()` or by reading from `parent_params` directly. Service instances are **not** injected
into templates at this time. We plan to explore service injection in the future, but this documentation reflects the currently
implemented behaviour.

## When Rendering Happens

Different parts of your configuration are rendered at different times:

### Service Instantiation

Services in the `services` section are rendered when the application starts, before any pipelines run. They have access
only to the global context provided for service creation.

### Pipeline Creation

Pipeline definitions are rendered when pipelines are created. They have access to global context, pipeline parameters,
and (when available) previous pipeline results.

### Pipe Execution

Individual pipes are rendered just before execution. They have access to global data, pipeline-level parameters,
previous pipe results, and parent parameters if the pipe is nested.

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

> The template renderer configuration itself (`infrastructure.template_renderer_config`) is never rendered—it is used as
> raw input to bootstrap the rendering system. Rendering this configuration would create a circular dependency, since it is needed to initialize the renderer itself.

## Examples

### Using Environment Variables

```yaml
services:
  - id: api_client
    use: "mypackage:APIClient"
    params:
      base_url: "{{ get_env('API_BASE_URL') }}"
      api_key: "{{ get_env('API_KEY') }}"
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
            confidence_threshold: "{{ params.threshold }}"
```

### Pipe Dependencies

```yaml
pipes:
  - id: fetch_data
    use: "mypackage:Fetcher"

  - id: process_data
    use: "mypackage:Processor"
    params:
      input: "{{ get_pipe_result('fetch_data') }}"
    depends_on: [ fetch_data ]
    if: "{{ not has_failed('fetch_data') }}"
```

### Using Parent Parameters in a Composite Pipe

```yaml
pipes:
  - id: composite
    use: "mypackage:Composite"
    params:
      threshold: 0.75
    steps:
      - id: evaluate
        use: "mypackage:Expression"
        params:
          expression: "{{ get_parent_param('threshold') > 0.7 }}"
```

### Explicitly Failing a Pipe

```yaml
pipes:
  - id: evaluate
    use: "mypackage:Expression"
    params:
      expression: "{{ fail() if get_pipe_result('validate', 'score') < 0.5 else 'ok' }}"
```

## Best Practices

- Use environment variables for secrets and environment-specific values
- Prefer `get_env()` over directly reading `os.environ` for better error messages
- Keep templates simple and readable
- Test your templates with different context values
- Avoid complex logic in templates—prefer configuration over code
