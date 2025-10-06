# Template Renderer Configuration Example

This document shows how to configure the template renderer using the new configuration models.

## Basic Configuration (Default Settings)

```yaml
open_ticket_ai:
  general_config:
    template_renderer:
      type: jinja
      params:
        env_prefix: "OTAI_"
        env_key: "env"
```

## Advanced Configuration

```yaml
open_ticket_ai:
  general_config:
    template_renderer:
      type: jinja
      params:
        # Environment variable filtering
        env_prefix: "OTAI_"
        env_extra_prefixes:
          - "SHARED_"
          - "CUSTOM_"
        
        # Environment variable access control
        env_allowlist:
          - "OTAI_API_KEY"
          - "OTAI_SERVER_URL"
          - "OTAI_DATABASE_URL"
        
        # Optional: Deny specific variables even if they match prefix
        # env_denylist:
        #   - "OTAI_SECRET_KEY"
        
        # Template key for accessing environment variables
        env_key: "env"
        
        # Refresh environment variables on each render (useful for testing)
        refresh_env_on_each_render: false
        
        # Jinja2 specific settings
        autoescape: false
        trim_blocks: true
        lstrip_blocks: true
```

## Using Environment Variables in Templates

With the configuration above, you can access environment variables in your templates:

```jinja2
# Using the env mapping
Server: {{ env.OTAI_SERVER_URL }}

# Using env_get function with default value
API Key: {{ env_get('OTAI_API_KEY', 'not-set') }}
```

## Security Best Practices

1. **Use prefix filtering**: Set `env_prefix` to limit which environment variables are accessible
2. **Use allowlist**: For production, explicitly list allowed variables with `env_allowlist`
3. **Avoid denylist alone**: Denylist is additive to other filters, use it with prefix or allowlist
4. **Disable refresh in production**: Set `refresh_env_on_each_render: false` for better performance

## Migration from Old Configuration

If you have existing configuration using the old parameter names, it continues to work:

### Old Style (Still Supported)
```yaml
template_renderer:
  type: jinja
  params:
    env_prefix: "OTAI_"
    env_key: "env"
    env_allowlist: ["OTAI_VAR1", "OTAI_VAR2"]
```

### New Style (Recommended)
Both styles are equivalent and work the same way. The renderer automatically converts old-style parameters to the new config objects internally.

## Python API Usage

You can also use the configuration classes directly in Python:

```python
from open_ticket_ai.core import (
    JinjaRenderer,
    JinjaRendererConfig,
    TemplateRendererEnvConfig,
)

# Create config objects
env_config = TemplateRendererEnvConfig(
    prefix="OTAI_",
    key="env",
    allowlist={"OTAI_API_KEY", "OTAI_SERVER_URL"},
    refresh_on_each_render=False,
)

config = JinjaRendererConfig(
    env_config=env_config,
    autoescape=False,
    trim_blocks=True,
)

# Create renderer with config
renderer = JinjaRenderer(config=config)

# Or use old parameter style (still works)
renderer = JinjaRenderer(
    env_prefix="OTAI_",
    env_key="env",
    env_allowlist={"OTAI_API_KEY"},
)
```
