# OTAI CLI Usage Guide

The Open Ticket AI (OTAI) command-line interface provides tools for managing plugins and accessing plugin-specific functionality.

## Installation

The CLI is automatically available after installing Open Ticket AI:

```bash
pip install open-ticket-ai
```

## Basic Commands

### Getting Help

```bash
# Show general help
otai --help

# Show version
otai --version

# Show plugin subcommand help
otai plugin --help
```

## Plugin Management

### List Installed Plugins

Display all installed OTAI plugins with their metadata:

```bash
otai plugin list
```

Example output:
```
Installed plugins:

  • open-ticket-ai-hf-local
    Version: 1.0.0rc1
    Core API: 2.0
    Description: Hugging Face local text classification plugin for Open Ticket AI

  • open-ticket-ai-otobo-znuny-plugin
    Version: 1.0.0rc1
    Core API: 2.0
    Description: OTOBO/Znuny ticket system integration plugin for Open Ticket AI
```

### Install a Plugin

Install a plugin from PyPI or a local path:

```bash
# Install from PyPI
otai plugin install open-ticket-ai-otobo-znuny-plugin

# Install from local path
otai plugin install /path/to/plugin

# Install from git repository
otai plugin install git+https://github.com/user/plugin.git
```

### Remove a Plugin

Uninstall a plugin:

```bash
otai plugin remove open-ticket-ai-otobo-znuny-plugin
```

## Plugin-Specific Commands

Plugins can expose their own CLI commands through the `register_cli_commands()` hook. These commands are automatically discovered and registered when the CLI starts.

### Example: Plugin with Setup Command

If a plugin named `otobo_znuny_plugin` exposes a setup command:

```bash
otai otobo_znuny_plugin setup
```

### Discovering Plugin Commands

To see all available commands including those from plugins:

```bash
otai --help
```

Commands from plugins will appear in the list of available commands.

## Development and Testing

### Running from Source

During development, you can run the CLI directly from source:

```bash
# From the repository root
PYTHONPATH=src python -m open_ticket_ai.cli.main --help
```

### Testing CLI Commands

The CLI can be tested programmatically using Click's testing utilities:

```python
from click.testing import CliRunner
from open_ticket_ai.open_ticket_ai.cli import cli

runner = CliRunner()
result = runner.invoke(cli, ['plugin', 'list'])
print(result.output)
```

## Troubleshooting

### Plugin Not Found After Installation

If a plugin doesn't appear after installation:

1. Verify the plugin is installed:
   ```bash
   pip list | grep open-ticket-ai
   ```

2. Check the plugin entry points:
   ```python
   import importlib.metadata as md
   for ep in md.entry_points(group='open_ticket_ai.plugins'):
       print(ep.name)
   ```

3. Ensure the plugin implements the required `get_metadata()` function

### Permission Errors During Installation

If you encounter permission errors:

```bash
# Install for current user only
otai plugin install --user open-ticket-ai-<plugin-name>

# Or use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
otai plugin install open-ticket-ai-<plugin-name>
```

## Advanced Usage

### Installing Development Versions

Install a plugin in editable mode for development:

```bash
cd src/open_ticket_ai_<plugin_name>
pip install -e .
```

Then verify:
```bash
otai plugin list
```

### Plugin Dependencies

When installing a plugin, its dependencies are automatically installed:

```bash
otai plugin install open-ticket-ai-hf-local
# This will also install transformers, torch, etc.
```

## See Also

- [Plugin Developer Guide](../vitepress_docs/docs_src/en/developers/plugins.md)
- [Plugin Standards](PLUGIN_STANDARDS.md)
- [Plugin Quick Reference](PLUGIN_QUICK_REFERENCE.md)
