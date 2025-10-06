---
description: Configuration models for template rendering in Open Ticket AI. Learn about TemplateRendererEnvConfig, TemplateRendererConfig, and JinjaRendererConfig.
layout: page
pageClass: wide-page
title: Template Renderer Configuration
---

# Template Renderer Configuration

Open Ticket AI provides strongly-typed configuration models for template rendering. These models enable validated, documented settings for Jinja2-based template rendering with environment variable filtering and access control.

## Overview

Three configuration classes work together to provide flexible template rendering:

- **`TemplateRendererEnvConfig`**: Environment variable filtering and access control
- **`TemplateRendererConfig`**: Base configuration for all template renderers
- **`JinjaRendererConfig`**: Jinja2-specific settings extending base configuration

## TemplateRendererEnvConfig

Controls which environment variables are accessible in templates and how they are refreshed.

### Fields

- **`prefix`** (str, default: `"OTAI_"`): Primary environment variable prefix for filtering
- **`extra_prefixes`** (tuple[str, ...], default: `()`): Additional prefixes to allow
- **`allowlist`** (set[str] | None, default: `None`): Specific variable names to allow (overrides prefix filtering)
- **`denylist`** (set[str] | None, default: `None`): Specific variable names to deny
- **`key`** (str, default: `"env"`): Template variable name for accessing environment
- **`provider`** (Callable | None, default: `None`): Custom function returning environment variables
- **`refresh_on_each_render`** (bool, default: `False`): Refresh environment on each template render

### Example

```python
from open_ticket_ai.open_ticket_ai.core.template_rendering.renderer_config import TemplateRendererEnvConfig

env_config = TemplateRendererEnvConfig(
    prefix="MYAPP_",
    extra_prefixes=("SHARED_",),
    allowlist={"MYAPP_TOKEN", "MYAPP_URL"},
    denylist={"MYAPP_SECRET"},
    key="env",
    refresh_on_each_render=True
)
```

## TemplateRendererConfig

Base configuration class for template renderers. Contains environment configuration.

### Fields

- **`env_config`** (TemplateRendererEnvConfig): Environment variable configuration

### Example

```python
from open_ticket_ai.open_ticket_ai.core.template_rendering.renderer_config import (
    TemplateRendererConfig,
    TemplateRendererEnvConfig
)

config = TemplateRendererConfig(
    env_config=TemplateRendererEnvConfig(prefix="CUSTOM_")
)
```

## JinjaRendererConfig

Extends `TemplateRendererConfig` with Jinja2-specific settings.

### Fields

Inherits all fields from `TemplateRendererConfig`, plus:

- **`env`** (SandboxedEnvironment | None, default: `None`): Custom Jinja2 environment instance
- **`autoescape`** (bool, default: `False`): Enable Jinja2 autoescaping
- **`trim_blocks`** (bool, default: `True`): Trim blocks in Jinja2 templates
- **`lstrip_blocks`** (bool, default: `True`): Left-strip blocks in Jinja2 templates

### Example

```python
from open_ticket_ai.open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
    TemplateRendererEnvConfig
)

config = JinjaRendererConfig(
    env_config=TemplateRendererEnvConfig(
        prefix="OTAI_",
        key="env",
        refresh_on_each_render=False
    ),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True
)
```

## Using Configuration with JinjaRenderer

### New Config-Based Approach

```python
from open_ticket_ai.open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.open_ticket_ai.core.template_rendering.renderer_config import (
    JinjaRendererConfig,
    TemplateRendererEnvConfig
)

env_config = TemplateRendererEnvConfig(
    prefix="OTAI_",
    key="env",
    refresh_on_each_render=True
)

config = JinjaRendererConfig(
    env_config=env_config,
    autoescape=False
)

renderer = JinjaRenderer(config=config)
```

### Backward-Compatible Approach

The old parameter-based approach still works:

```python
from open_ticket_ai.open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer

renderer = JinjaRenderer(
    env_prefix="OTAI_",
    env_key="env",
    refresh_env_on_each_render=True
)
```

## Configuration in YAML

Configure template renderer in `config.yml`:

```yaml
open_ticket_ai:
  general_config:
    template_renderer:
      type: jinja
      params:
        env_prefix: "OTAI_"
        env_key: "env"
        env_allowlist:
          - OTAI_API_KEY
          - OTAI_SERVER_URL
        refresh_env_on_each_render: false
        autoescape: false
        trim_blocks: true
        lstrip_blocks: true
```

## Benefits

- **Type Safety**: Pydantic validation ensures configuration correctness
- **Documentation**: Self-documenting configuration with field descriptions
- **Flexibility**: Support both config objects and backward-compatible parameters
- **Security**: Fine-grained control over environment variable access
- **Extensibility**: Easy to extend for custom renderer implementations

## Schema

Generate JSON schema for configuration:

```python
from open_ticket_ai.open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig

schema = JinjaRendererConfig.model_json_schema()
print(schema)
```
