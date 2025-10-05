# CLI Tool Reference

Open Ticket AI provides a command-line interface (CLI) tool called `otai` for managing OTAI core features. This tool simplifies common workflows like starting the application, validating configuration, initializing new configs, and managing plugins.

## Installation

The `otai` CLI is automatically installed when you install the open-ticket-ai package:

```bash
pip install open-ticket-ai
```

After installation, you can verify the CLI is available:

```bash
otai --help
```

## Commands

### start

Start the main OTAI application with a configuration file.

```bash
otai start [--config PATH]
```

**Options:**
- `--config`, `-c`: Path to config.yml file (optional if `OPEN_TICKET_AI_CONFIG` environment variable is set)

**Examples:**

```bash
# Start with config from environment variable
export OPEN_TICKET_AI_CONFIG=/path/to/config.yml
otai start

# Start with explicit config path
otai start --config config.yml
```

### check-config

Validate the syntax and structure of a configuration file.

```bash
otai check-config [CONFIG_PATH]
```

**Arguments:**
- `CONFIG_PATH`: Path to config.yml file to validate (default: config.yml)

**Example:**

```bash
otai check-config config.yml
```

**Output:**

```
🔍 Validating config file: config.yml
✅ Config file is valid!
   - Plugins: 0
   - Definitions: 5
   - Orchestrator steps: 1
```

### init

Initialize a new configuration file from a predefined template.

```bash
otai init TEMPLATE [--output PATH] [--force]
```

**Arguments:**
- `TEMPLATE`: Template name (see available templates below)

**Options:**
- `--output`, `-o`: Output file path (default: config.yml)
- `--force`, `-f`: Overwrite existing file

**Available Templates:**

- `add_note`: AI adds notes to tickets in specific queue
- `create_ticket`: Create tickets based on conditions
- `queue_classification`: Automatic queue classification
- `priority_classification`: Automatic priority classification
- `complete_workflow`: Complete workflow example with multiple steps

**Example:**

```bash
# Initialize queue classification config
otai init queue_classification

# Initialize to custom path
otai init priority_classification --output my-config.yml

# Overwrite existing file
otai init add_note --output config.yml --force
```

**Output:**

```
✅ Successfully initialized config from template 'queue_classification'
   Created: config.yml

📝 Next steps:
   1. Edit config.yml to customize your configuration
   2. Update environment variables (server addresses, credentials)
   3. Validate with: otai check-config config.yml
   4. Start with: otai start --config config.yml
```

### plugin list

List all installed OTAI plugins.

```bash
otai plugin list
```

**Example Output:**

```
📦 Installed OTAI plugins:

  • open-ticket-ai-hf-local (v1.0.0)
    HuggingFace local inference for text classification
    Core API: 2.0

  • open-ticket-ai-otobo-znuny-plugin (v1.0.0)
    OTOBO/Znuny ticket system integration
    Core API: 2.0
```

### plugin install

Install an OTAI plugin from PyPI.

```bash
otai plugin install PACKAGE_NAME [--upgrade]
```

**Arguments:**
- `PACKAGE_NAME`: Plugin package name to install

**Options:**
- `--upgrade`, `-U`: Upgrade if already installed

**Examples:**

```bash
# Install a plugin
otai plugin install open-ticket-ai-hf-local

# Install or upgrade to latest version
otai plugin install open-ticket-ai-hf-local --upgrade
```

### plugin remove

Uninstall an OTAI plugin.

```bash
otai plugin remove PACKAGE_NAME [--yes]
```

**Arguments:**
- `PACKAGE_NAME`: Plugin package name to remove

**Options:**
- `--yes`, `-y`: Skip confirmation prompt

**Examples:**

```bash
# Remove with confirmation
otai plugin remove open-ticket-ai-hf-local

# Remove without confirmation
otai plugin remove open-ticket-ai-hf-local --yes
```

### upgrade

Check for new OTAI versions and upgrade.

```bash
otai upgrade [--check-only]
```

**Options:**
- `--check-only`: Only check for updates, don't install

**Examples:**

```bash
# Check for updates
otai upgrade --check-only

# Upgrade to latest version
otai upgrade
```

### version

Display the current OTAI version.

```bash
otai version
```

**Output:**

```
Open Ticket AI version: 1.0.0rc1
```

## Environment Variables

### OPEN_TICKET_AI_CONFIG

Path to the configuration file. Used by the `start` command when `--config` option is not provided.

```bash
export OPEN_TICKET_AI_CONFIG=/path/to/config.yml
otai start
```

## Common Workflows

### Quick Start with Template

```bash
# 1. Initialize config from template
otai init queue_classification

# 2. Edit config.yml to customize
# (update server addresses, credentials, etc.)

# 3. Validate configuration
otai check-config config.yml

# 4. Start the application
otai start --config config.yml
```

### Plugin Management

```bash
# List available plugins
otai plugin list

# Install plugins
otai plugin install open-ticket-ai-hf-local
otai plugin install open-ticket-ai-otobo-znuny-plugin

# Verify plugins are installed
otai plugin list

# Remove a plugin
otai plugin remove open-ticket-ai-hf-local
```

### Upgrading OTAI

```bash
# Check for new versions
otai upgrade --check-only

# Upgrade to latest version
otai upgrade

# Verify new version
otai version
```

## Configuration File Structure

For detailed information about configuration file structure, see the [Configuration Examples](/en/_config_examples/) section.

All configuration files follow this basic structure:

```yaml
open_ticket_ai:
  plugins: []
  general_config: {}
  defs: []
  orchestrator: []
```

## Troubleshooting

### Config file not found

If you get an error about config file not found:

```
❌ Error: OPEN_TICKET_AI_CONFIG environment variable not set
```

Make sure to either:
1. Set the environment variable: `export OPEN_TICKET_AI_CONFIG=/path/to/config.yml`
2. Use the `--config` option: `otai start --config config.yml`

### Plugin not found

If a plugin is not found after installation:

```bash
# Verify plugin is installed
pip list | grep open-ticket-ai

# Reinstall if necessary
otai plugin install open-ticket-ai-hf-local --upgrade
```

### Config validation errors

If your config file has validation errors:

```bash
# Check the specific error message
otai check-config config.yml

# Compare with template examples
otai init queue_classification --output example.yml
```

## See Also

- [Developer Information](/en/developers/developer-information)
- [Available Plugins](/en/guide/available-plugins)
- [Configuration Examples](/en/_config_examples/)
