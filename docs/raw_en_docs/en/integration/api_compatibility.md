# Plugin API Versioning and Compatibility

Guide to understanding plugin API versioning, compatibility, and migration between versions.

## Plugin API Versioning

Open Ticket AI uses semantic versioning for the plugin API:

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Compatibility Matrix

### Current Versions

| Open Ticket AI | Plugin API | Status | Support Until |
|---------------|------------|---------|---------------|
| 2.0.x | 2.0 | Current | TBD |
| 1.5.x | 1.5 | Maintained | 2025-12-31 |
| 1.0.x | 1.0 | Security Only | 2025-06-30 |

### Plugin Compatibility

Plugins declare compatible API versions:

```python
# plugin.py
PLUGIN_API_VERSION = "2.0"
COMPATIBLE_VERSIONS = ["2.0", "1.5"]

def setup(registry):
    if registry.api_version not in COMPATIBLE_VERSIONS:
        raise IncompatibleAPIVersion(
            f"Plugin requires API {COMPATIBLE_VERSIONS}, "
            f"but found {registry.api_version}"
        )
    # Register components
```

## Breaking Changes Policy

### What Constitutes a Breaking Change?

Changes that require plugin updates:
- Removing public methods or properties
- Changing method signatures
- Removing required parameters
- Changing return types
- Renaming public interfaces

### What Doesn't Break Compatibility?

Changes that plugins can ignore:
- Adding new optional parameters (with defaults)
- Adding new methods
- Internal implementation changes
- Performance improvements
- Bug fixes

## Version Compatibility Checking

### Automatic Checking

Open Ticket AI validates plugin compatibility on load:

```python
# Automatic validation
if plugin.api_version != current_api_version:
    if plugin.api_version not in compatible_versions:
        raise IncompatibleAPIError(
            f"Plugin {plugin.name} requires API {plugin.api_version}, "
            f"but this version uses {current_api_version}"
        )
```

### Manual Checking

Plugins can check compatibility explicitly:

```python
from open_ticket_ai import check_api_compatibility

def setup(registry):
    # Check if current API version is compatible
    if not check_api_compatibility("2.0", registry.api_version):
        raise IncompatibleAPIVersion()
```

## Migration Guides

### Migrating from 1.5 to 2.0

#### Changed: Pipe Interface

**Before (1.5)**:
```python
class MyPipe:
    def execute(self, data):
        # Process data
        return result
```

**After (2.0)**:
```python
class MyPipe(BasePipe):
    def execute(self, context: PipelineContext) -> PipeResult:
        # Access data from context
        data = context.get("data")
        # Process and return result
        return PipeResult.success(result)
```

#### Changed: Service Registration

**Before (1.5)**:
```python
def setup(registry):
    registry.register("my_service", MyService())
```

**After (2.0)**:
```python
def setup(registry):
    registry.register_service(MyService, MyServiceImpl, scope=singleton)
```

#### Changed: Configuration

**Before (1.5)**:
```yaml
my_plugin:
  setting: value
```

**After (2.0)**:
```yaml
plugins:
  - name: my_plugin
    config:
      setting: value
```

### Migrating from 1.0 to 1.5

#### Changed: Error Handling

**Before (1.0)**:
```python
def fetch_tickets(self):
    try:
        return api.get_tickets()
    except Exception:
        return []
```

**After (1.5)**:
```python
def fetch_tickets(self):
    try:
        return api.get_tickets()
    except APIError as e:
        raise TicketFetchError(f"Failed to fetch: {e}")
```

## Deprecation Process

### Step 1: Deprecation Warning

Feature marked as deprecated in version N:

```python
import warnings

def old_method(self):
    warnings.warn(
        "old_method is deprecated and will be removed in version N+2. "
        "Use new_method instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return self.new_method()
```

### Step 2: Documentation

Deprecation documented in:
- Release notes
- Migration guide
- API documentation
- Inline code comments

### Step 3: Removal

Feature removed in version N+2:
- Two major versions after deprecation
- Minimum 12 months notice
- Clear migration path provided

## Versioning Best Practices

### For Plugin Developers

1. **Declare API Version**:
```python
PLUGIN_API_VERSION = "2.0"
```

2. **Test Against Multiple Versions**:
```python
COMPATIBLE_VERSIONS = ["2.0", "1.5"]
```

3. **Handle Version Differences**:
```python
def setup(registry):
    if registry.api_version >= "2.0":
        # Use new API
        registry.register_service(MyService, MyServiceImpl)
    else:
        # Use old API
        registry.register("my_service", MyService())
```

### For Application Developers

1. **Pin Plugin Versions**:
```toml
dependencies = [
    "my-plugin>=1.5.0,<2.0.0"
]
```

2. **Test Before Upgrading**:
```bash
# Test in isolated environment
uv pip install --upgrade open-ticket-ai
uv run -m pytest
```

3. **Review Release Notes**:
- Check breaking changes
- Review migration guides
- Test affected plugins

## API Stability Guarantees

### Stable APIs

Guaranteed stable across minor versions:
- `BasePipe` interface
- `TicketSystemAdapter` interface
- Core service interfaces
- Configuration schema (backward compatible)

### Experimental APIs

May change without warning:
- APIs marked with `@experimental` decorator
- Internal implementation details
- Debug/diagnostic interfaces

```python
from open_ticket_ai.experimental import experimental_feature

@experimental
def new_feature():
    """This API is experimental and may change."""
    pass
```

## Checking Plugin Compatibility

### Command Line

```bash
# Check installed plugins
open-ticket-ai plugins list

# Check compatibility
open-ticket-ai plugins check-compatibility

# Show version info
open-ticket-ai --version
```

### Programmatic

```python
from open_ticket_ai.plugins import get_plugin_info

info = get_plugin_info("my_plugin")
print(f"Plugin API: {info.api_version}")
print(f"Compatible: {info.is_compatible()}")
```

## Getting Help

### Version Mismatch Issues

If you encounter version compatibility issues:

1. Check the compatibility matrix
2. Review migration guides
3. Check plugin documentation
4. Open an issue on GitHub

### Updating Plugins

```bash
# Update to latest compatible version
uv pip install --upgrade my-plugin

# Update to specific version
uv pip install my-plugin==2.0.0
```

## Related Documentation

- [Plugin System](../plugins/plugin_system.md)
- [Plugin Development](../plugins/plugin_development.md)
- [Custom Adapters](custom_adapters.md)
