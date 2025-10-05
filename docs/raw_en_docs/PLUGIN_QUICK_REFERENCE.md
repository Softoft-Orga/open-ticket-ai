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

def register_cli_commands():  # optional
    import click
    
    @click.group()
    def my_plugin():
        """My plugin CLI commands."""
        pass
    
    @my_plugin.command()
    def setup():
        """Setup the plugin."""
        click.echo("Setting up...")
    
    return my_plugin
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

## CLI Commands

### Plugin Management

```bash
# List installed plugins
otai plugin list

# Install a plugin
otai plugin install open-ticket-ai-<plugin-name>

# Remove a plugin
otai plugin remove open-ticket-ai-<plugin-name>
```

### Plugin-specific Commands

If a plugin exposes CLI commands via `register_cli_commands()`:
```bash
otai <plugin_command> <subcommand>
```

## Documentation

Add plugin documentation to:
- `README.md` in plugin directory
- VitePress docs: `docs/vitepress_docs/docs_src/en/developers/plugins.md`

## Full Standards

See [PLUGIN_STANDARDS.md](PLUGIN_STANDARDS.md) for complete documentation.
