# Deprecation Policy

This document defines the deprecation policy for Open Ticket AI Core and plugins.

## Guiding Principles

1. **Stability**: Users should have confidence that their integrations will continue working
2. **Clear Communication**: Deprecations must be announced prominently and early
3. **Migration Path**: Always provide alternatives before removing functionality
4. **Reasonable Timeline**: Allow sufficient time for users to migrate

## Core Package Deprecations

### Timeline

When deprecating functionality in the Core package:

1. **Announcement (Version N)**: 
   - Add `warnings.warn()` with `DeprecationWarning` to deprecated function/class
   - Document in CHANGELOG under "Deprecated" section
   - Update documentation with deprecation notice and migration guide

2. **Retention (Versions N+1, N+2)**:
   - Keep deprecated functionality for minimum **1-2 MINOR versions**
   - Continue showing deprecation warnings
   - Maintain tests for deprecated code

3. **Removal (Version N+MAJOR)**:
   - Remove only in next **MAJOR version**
   - Document removal in CHANGELOG under "Breaking Changes"
   - Update migration guide with examples

### Example Timeline

```
Version 1.5.0: Feature X marked deprecated
  ├─ warnings.warn("Feature X deprecated, use Feature Y instead", DeprecationWarning)
  ├─ CHANGELOG: "Deprecated: Feature X, migrate to Feature Y"
  └─ Docs: Migration guide added

Version 1.6.0: Feature X still available
  └─ Deprecation warnings continue

Version 1.7.0: Feature X still available (optional)
  └─ Deprecation warnings continue

Version 2.0.0: Feature X removed
  ├─ CHANGELOG: "Breaking: Removed Feature X (deprecated in 1.5.0)"
  └─ Tests for Feature X removed
```

### Deprecation Example

```python
import warnings

def old_function(arg: str) -> str:
    warnings.warn(
        "old_function is deprecated and will be removed in version 2.0.0. "
        "Use new_function instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function(arg)

def new_function(arg: str) -> str:
    return f"processed: {arg}"
```

## Plugin API Deprecations

### Breaking Changes

When the Plugin API changes in incompatible ways:

1. **Announcement**: Communicate to plugin maintainers via:
   - GitHub Discussions/Issues
   - CHANGELOG with "Breaking Changes" section
   - Updated plugin developer documentation

2. **Shim Layer**: Provide compatibility shim for 1-2 minor releases
   ```python
   def register_pipes_old(registry) -> None:
       warnings.warn(
           "register_pipes without context parameter is deprecated. "
           "Update to register_pipes(registry, context) signature.",
           DeprecationWarning,
           stacklevel=2
       )
       return register_pipes(registry, context=None)
   ```

3. **Version Bump**: Increment Plugin API MAJOR version (e.g., 2.0 → 3.0)

4. **Core MAJOR Bump**: Bump Core package MAJOR version to signal breaking change

### Plugin API Version

The Plugin API version is tracked in `tests/contract/test_plugin_contract.py`:

```python
REQUIRED_CORE_API = "2.0"
```

- **MAJOR**: Breaking changes requiring plugin updates
- **MINOR**: New capabilities, backward-compatible

### Migration Period

Plugin maintainers have **minimum 1-2 MINOR releases** to update their plugins before shim removal.

Example:
```
Version 1.5.0: Plugin API 2.0, new contract introduced with shim
Version 1.6.0: Plugin API 2.0, shim still active with warnings
Version 2.0.0: Plugin API 3.0, old contract shim removed
```

## Plugin Package Deprecations

Plugin maintainers should follow similar principles:

1. Mark deprecated functionality with warnings
2. Keep deprecated code for 1-2 MINOR versions
3. Remove only in MAJOR version
4. Maintain compatibility with Core version range

## Communication Channels

### Announcing Deprecations

1. **CHANGELOG.md**: Always document in "Deprecated" section
2. **Code Warnings**: Use Python `warnings` module
3. **Documentation**: Update guides with migration instructions
4. **GitHub Releases**: Highlight in release notes
5. **GitHub Discussions**: Create discussion for major deprecations

### CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [1.5.0] - 2024-01-15

### Deprecated
- `old_function()` in favor of `new_function()`. Will be removed in 2.0.0.
- Plugin API: `register_pipes(registry)` - use `register_pipes(registry, context)` instead

### Breaking Changes (for major versions)
- Removed `old_function()` (deprecated in 1.5.0)
```

## Exceptions

The deprecation timeline may be shortened only when:

1. **Security Issues**: Immediate removal for security vulnerabilities
2. **Data Corruption**: Features that could cause data loss
3. **Broken Functionality**: Features that fundamentally don't work

In these cases:
- Document clearly in CHANGELOG with rationale
- Provide immediate migration guide
- Consider emergency patch releases

## Testing Deprecated Code

1. Keep tests for deprecated functionality during retention period
2. Suppress deprecation warnings in tests:
   ```python
   import warnings
   
   with warnings.catch_warnings():
       warnings.simplefilter("ignore", DeprecationWarning)
       result = old_function()
   ```
3. Remove tests when removing deprecated code

## Version Numbering Impact

- **PATCH** (1.0.x): Never deprecate or remove functionality
- **MINOR** (1.x.0): Can deprecate, never remove
- **MAJOR** (x.0.0): Can remove previously deprecated functionality

## FAQ

### Can I remove deprecated code in a minor release?

No. Removal only happens in MAJOR releases.

### How long must deprecated code be kept?

Minimum 1-2 MINOR versions, preferably 2.

### What if nobody uses the deprecated feature?

Still follow the process. Usage patterns may not be visible.

### Can plugins have different deprecation timelines?

Yes, but they should follow similar principles for user trust.

### How do I deprecate a configuration field?

Use Pydantic validators to issue warnings:
```python
from pydantic import field_validator

class Config(BaseModel):
    old_field: str | None = None
    
    @field_validator('old_field')
    @classmethod
    def warn_old_field(cls, v):
        if v is not None:
            warnings.warn(
                "old_field is deprecated, use new_field instead",
                DeprecationWarning,
                stacklevel=2
            )
        return v
```

## References

- [PEP 387 – Backwards Compatibility Policy](https://peps.python.org/pep-0387/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
