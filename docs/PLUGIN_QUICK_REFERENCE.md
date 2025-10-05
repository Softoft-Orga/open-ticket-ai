# Plugin Developer Quick Reference

Quick reference for creating Open Ticket AI plugins.

## File Checklist

- [ ] `pyproject.toml` with metadata and entry points
- [ ] `README.md` with installation and usage instructions
- [ ] `LICENSE` (LGPL-2.1-only)
- [ ] `CHANGELOG.md`
- [ ] `__init__.py` with `get_metadata()`, `register_pipes()`, `register_services()`
- [ ] Tests directory with unit tests

## Metadata Template

```python
def get_metadata():
    return {
        "name": "open-ticket-ai-<plugin-name>",
        "version": "X.Y.Z",
        "core_api": "2.0",
        "description": "Brief description",
    }

def register_pipes():
    return [PipeClass1, PipeClass2]  # or [] if no pipes

def register_services():
    return [ServiceClass1]  # or [] if no services
```

## pyproject.toml Entry Points

```toml
[project.entry-points."open_ticket_ai.plugins"]
<plugin_short_name> = "open_ticket_ai_<plugin_name>"
```

## Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| PyPI name | `open-ticket-ai-<name>` | `open-ticket-ai-hf-local` |
| Python import | `open_ticket_ai_<name>` | `open_ticket_ai_hf_local` |
| Directory | `src/open_ticket_ai_<name>/` | `src/open_ticket_ai_hf_local/` |
| Entry point | `<short_name>` | `hf_local` |

## Required Dependencies

```toml
dependencies = [
    "open-ticket-ai>=1.0.0rc1",
    # other dependencies
]
```

## Testing

Run plugin validation:
```bash
python scripts/validate_plugins.py
```

Run contract tests:
```bash
pytest tests/contract/ -m contract
```

## Building

```bash
cd src/open_ticket_ai_<plugin_name>
python -m build
```

## Documentation

Add plugin documentation to:
- `README.md` in plugin directory
- VitePress docs: `docs/vitepress_docs/docs_src/en/developers/plugins.md`

## Full Standards

See [PLUGIN_STANDARDS.md](../PLUGIN_STANDARDS.md) for complete documentation.
