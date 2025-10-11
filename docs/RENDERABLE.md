# Renderable Generic Base Class

## Overview

As of the refactoring introduced in [issue #315](https://github.com/Softoft-Orga/open-ticket-ai/issues/315), Open Ticket AI uses a generic `Renderable[ParamsT]` base class for all registerable components (pipes, services, runners). This replaces the legacy `RegisterableConfig` pattern and provides strong typing for configuration parameters.

## What Changed

### Before (Legacy Pattern)

```python
class MyPipeConfig(RenderedPipeConfig):
    my_field: str
    another_field: int
    # Fields mixed with control fields like id, use, if_, depends_on, etc.
```

### After (New Pattern with PEP 695 Generics)

```python
from pydantic import BaseModel
from open_ticket_ai.core.config.registerable import Renderable

class MyPipeParams(BaseModel):
    my_field: str
    another_field: int

class MyPipeConfig(Renderable[MyPipeParams]):
    pass
```

## Benefits

1. **Type Safety**: Parameters are strongly typed using Pydantic models
2. **Clear Separation**: Business logic parameters are separated from control fields (id, use, if_, depends_on)
3. **IDE Support**: Full autocomplete and type checking for params
4. **Automatic Validation**: Dict params are automatically converted to typed models

## Usage in Pipes

```python
class MyPipe(Pipe):
    def __init__(self, pipe_params: MyPipeConfig, *args, **kwargs):
        super().__init__(pipe_params)
        self.config = MyPipeConfig.model_validate(pipe_params.model_dump())
    
    async def _process(self) -> PipeResult:
        # Access typed params with full IDE support
        value = self.config.params.my_field
        number = self.config.params.another_field
        # ...
```

## Configuration Format

Both formats are supported for backward compatibility:

```yaml
# New format (recommended)
- id: my_pipe
  use: "MyPipe"
  params:
    my_field: "value"
    another_field: 42

# Legacy format (still works but deprecated for custom fields)
- id: my_pipe
  use: "MyPipe"
  my_field: "value"
  another_field: 42
```

## Backward Compatibility

- `RegisterableConfig` still exists and now inherits from `Renderable[BaseModel]`
- Existing pipes using `RenderedPipeConfig` continue to work
- The new pattern is recommended for all new pipes

## Migration Guide

1. Create a params model for your pipe:
   ```python
   class MyPipeParams(BaseModel):
       field1: str
       field2: int
   ```

2. Update your config class:
   ```python
   class MyPipeConfig(Renderable[MyPipeParams]):
       pass
   ```

3. Update your pipe to access `self.config.params.field_name` instead of `self.config.field_name`

4. Update your tests to put custom fields under `params` key in config dicts
