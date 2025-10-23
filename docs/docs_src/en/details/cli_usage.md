# OTAI CLI Usage Guide

The Open Ticket AI (OTAI) command-line interface provides tools for managing configurations, validating settings, and
running the OTAI application.

## Installation

The CLI is automatically available after installing Open Ticket AI:

```bash
pip install open-ticket-ai
```

Or when working from source:

```bash
uv sync
```

## Basic Commands

### Getting Help

```bash
# Show general help
open-ticket-ai --help

# Show help for a specific command
open-ticket-ai init --help
open-ticket-ai run --help
open-ticket-ai check-config --help
```

## Configuration Management

### Initialize from Template

Create a new configuration file from one of the available templates:

```bash
# Initialize with default output (config.yml)
open-ticket-ai init queue_classification

# Specify custom output path
open-ticket-ai init queue_classification --output my-config.yml

# Overwrite existing file
open-ticket-ai init complete_workflow --output config.yml --force
```

**Available Templates:**

- `queue_classification` - Classify tickets into queues
- `priority_classification` - Assign priority levels to tickets
- `add_note_when_in_queue` - Automatically add notes based on queue
- `create_ticket_on_condition` - Create tickets when conditions are met
- `complete_workflow` - Full workflow with multiple steps

After initialization, the CLI will guide you with next steps:

```
✅ Successfully initialized config from template 'queue_classification'
   Created: config.yml

📝 Next steps:
   1. Edit config.yml to customize your configuration
   2. Update environment variables (server addresses, credentials)
   3. Validate with: open-ticket-ai check-config config.yml
   4. Start with: open-ticket-ai run --config config.yml
```

### Validate Configuration

Check if your configuration file is valid before running:

```bash
# Validate config.yml in current directory
open-ticket-ai check-config

# Validate a specific config file
open-ticket-ai check-config my-config.yml
```

Example output:

```
🔍 Validating config file: config.yml
✅ Config file is valid!
   - Plugins: 2
   - Services: 1
   - Orchestrator steps: 3
```

If there are errors, you'll see detailed validation messages:

```
❌ Config validation failed:

  orchestrator -> runners -> 0 -> use: Plugin 'nonexistent_plugin' not found
  services -> 0 -> base_url: Field required
```

## Running the Application

### Run with Configuration File

Start the OTAI application with a configuration file:

```bash
# Using --config option
open-ticket-ai run --config config.yml

# Using environment variable
set OPEN_TICKET_AI_CONFIG=config.yml
open-ticket-ai run
```

The application will:

1. Load and validate the configuration
2. Initialize all plugins and services
3. Start the orchestrator with configured runners
4. Begin processing tickets according to your workflow

Press `Ctrl+C` to gracefully shut down the application.

## Plugin Management (Future Feature)

:::warning Under Development
Plugin management commands are placeholders for a future release. Currently, plugins should be installed using standard
Python package managers.
:::

### Current Plugin Installation

Install OTAI plugins using pip or uv:

```bash
# Using pip
pip install otai-hf-local
pip install otai-otobo-znuny

# Using uv (from workspace)
uv sync
```

### Planned Commands

These commands will be available in a future version:

```bash
# List installed plugins (not yet implemented)
open-ticket-ai plugin list

# Install a plugin (not yet implemented)
open-ticket-ai plugin install otai-hf-local

# Remove a plugin (not yet implemented)
open-ticket-ai plugin remove otai-hf-local
```

## Plugin-Specific Commands

Some OTAI plugins expose their own CLI commands. These are separate from the main `open-ticket-ai` command and use their
own entry points.

### Example: OTOBO/Znuny Plugin Setup

The OTOBO/Znuny plugin provides an interactive setup wizard:

```bash
# Interactive setup with prompts
otai-otobo-znuny setup

# With command-line options
otai-otobo-znuny setup \
  --otai_base-url https://ticket.example.com \
  --webservice-name OpenTicketAI \
  --username otai_user \
  --password <your-password> \
  --output-config config.yml
```

The setup wizard will:

1. Prompt for connection details
2. Optionally verify the connection to your ticket system
3. Generate a configuration file ready to use with OTAI
4. Provide guidance on next steps

:::tip
Each plugin may expose its own commands. Check the plugin's documentation for available CLI functionality.
:::

## Development and Testing

### Running from Source

During development, you can run the CLI directly from source:

```bash
# From the repository root
uv run open-ticket-ai --help

# Or using Python directly
uv run python -m open_ticket_ai.core.cli.main --help
```

### Testing CLI Commands

The CLI uses Typer and can be tested programmatically:

```python
from typer.testing import CliRunner
from open_ticket_ai.core.cli.main import CLI

runner = CliRunner()
cli = CLI()

# Test config validation
result = runner.invoke(cli.app, ['check-config', 'config.yml'])
assert result.exit_code == 0
print(result.output)
```

## Environment Variables

### OPEN_TICKET_AI_CONFIG

Set the default configuration file path:

```bash
# Windows
set OPEN_TICKET_AI_CONFIG=C:\path\to\config.yml

# Linux/Mac
export OPEN_TICKET_AI_CONFIG=/path/to/config.yml
```

When this variable is set, you can run OTAI without specifying `--config`:

```bash
open-ticket-ai run
```

### Other Environment Variables

Configuration files can reference environment variables for sensitive data:

```yaml
open_ticket_ai:
  services:
    - id: "otobo_znuny"
      username: "otai_user"
      password: "{{ env.OTAI_OTOBO_PASSWORD }}"
```

## Troubleshooting

### Command Not Found

If `open-ticket-ai` command is not found after installation:

1. **Check installation:**
   ```bash
   pip show open-ticket-ai
   ```

2. **Verify Python scripts directory is in PATH:**
   ```bash
   # Windows - check if Scripts directory is in PATH
   echo %PATH%
   
   # The path should include something like:
   # C:\Python313\Scripts or C:\Users\YourName\AppData\Local\Programs\Python\Python313\Scripts
   ```

3. **Use Python module syntax as fallback:**
   ```bash
   python -m open_ticket_ai.core.cli.main --help
   ```

### Configuration Validation Errors

If you see validation errors:

1. **Check YAML syntax:**
    - Ensure proper indentation (use spaces, not tabs)
    - Verify all quotes are properly closed
    - Check that lists use proper `- ` format

2. **Verify plugin names:**
    - Plugin `use` fields must match installed plugin entry points
    - Check `open-ticket-ai plugin list` (when implemented) or installed packages

3. **Check required fields:**
    - Each service must have required configuration fields
    - Use `check-config` to see detailed error locations

### Permission Errors

If you encounter permission errors when reading/writing config files:

```bash
# Windows - run as administrator if needed
# Or ensure the file/directory has write permissions

# Check file permissions
icacls config.yml
```

## Advanced Usage

### Custom Configuration Templates

You can create your own configuration templates in the `data/templates/` directory:

1. Create a new `.yml` file in `data/templates/`
2. Add comments at the top to describe the template
3. The template will appear in `init` command

### Chaining Commands

Validate and run in sequence:

```bash
# Windows
open-ticket-ai check-config config.yml && open-ticket-ai run --config config.yml

# Check exit codes
open-ticket-ai check-config config.yml
if %ERRORLEVEL% EQU 0 (
    open-ticket-ai run --config config.yml
)
```

## See Also

- [Configuration Guide](./configuration.md)
- [Plugin Developer Guide](../developers/plugins.md)
- [Available Templates Quick Reference](../../../../data/templates/QUICK_REFERENCE.md)
- [OTOBO/Znuny Plugin Documentation](../../../../packages/otai_otobo_znuny/README.md)
