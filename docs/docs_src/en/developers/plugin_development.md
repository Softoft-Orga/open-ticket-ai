---
description: Complete guide to developing custom plugins for Open Ticket AI including project structure, entry points, and best practices.
---

## TODO plugin package name otai-* needs entrypoint set to PluginFactory. Plugin returns list of injectables.

# Plugin Development Guide

Learn how to create custom plugins to extend Open Ticket AI functionality.

## Creating a New Plugin

### 1. Project Structure

Create a Python package with this structure:

```
my_plugin/
├── pyproject.toml
├── src/
│   └── my_plugin/
│       ├── __init__.py
│       ├── pipes/
│       │   └── my_pipe.py
│       ├── services/
│       │   └── my_service.py
│       └── plugin.py
└── tests/
    └── test_my_plugin.py
```

### 2. Plugin Entry Point

Define entry point in `pyproject.toml`:

```toml
[project.entry-points."open_ticket_ai.plugins"]
my_plugin = "my_plugin.plugin:setup"
```

### 3. Setup Function

Implement the setup function in `plugin.py`:

```python
def setup(registry):
    """Register plugin components."""
    from my_plugin.pipes.my_pipe import MyPipe
    from my_plugin.services.my_service import MyService, MyServiceImpl

    registry.register_pipe("my_pipe", MyPipe)
    registry.register_service(MyService, MyServiceImpl)
```

## Plugin Interface Requirements

### Required Functions

Every plugin must provide:

- `setup(registry)`: Register plugin components

### Optional Functions

Plugins may provide:

- `configure(config)`: Plugin-specific configuration
- `validate()`: Validate plugin installation
- `cleanup()`: Cleanup on shutdown

## Registering Services and Pipes

### Register a Pipe

```python
from open_ticket_ai.pipeline import BasePipe


class MyPipe(BasePipe):
    def execute(self, context):
        # Pipe logic
        return PipeResult.succeeded()


# In setup function
registry.register_pipe("my_pipe", MyPipe)
```

### Register a Service

```python
from injector import singleton


class MyService:
    def do_work(self):
        pass


# In setup function
registry.register_service(MyService, MyServiceImpl, scope=singleton)
```

## Plugin Packaging and Distribution

### Using uv

```bash
# Build plugin
uv build

# Publish to PyPI
uv publish
```

### Installation

Users install plugins via pip/uv:

```bash
uv pip install my-plugin
```

## Testing Plugins

### Unit Tests

Test individual components:

```python
def test_my_pipe():
    pipe = MyPipe()
    context = PipelineContext()
    result = pipe.execute(context)
    assert result.succeeded
```

### Integration Tests

Test plugin integration:

```python
def test_plugin_registration():
    registry = UnifiedRegistry()
    setup(registry)
    assert registry.has_pipe("my_pipe")
```

### E2E Tests

Test complete workflows:

```python
def test_pipeline_with_plugin():
    config = load_config("test_config.yml")
    pipeline = create_pipeline(config)
    result = pipeline.run()
    assert result.succeeded
```

## Best Practices

### Do:

- Follow naming conventions
- Document configuration options
- Provide examples
- Write comprehensive tests
- Version your plugin
- Declare API dependencies

### Don't:

- Modify core system behavior
- Create circular dependencies
- Store state in pipes
- Ignore error handling
- Skip documentation

## Example Plugin

See the [HuggingFace Local plugin](../plugins/hf_local.md) for a complete example.

## Related Documentation

- [Plugin System](../plugins/plugin_system.md)
- [Dependency Injection](dependency_injection.md)
- [Services](services.md)
- [Pipeline Architecture](../concepts/pipeline-architecture.md)
