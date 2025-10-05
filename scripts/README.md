# Scripts

This directory contains utility scripts for the Open Ticket AI project.

## validate_plugins.py

Validates that all installed plugins conform to the plugin standards defined in [PLUGIN_STANDARDS.md](../PLUGIN_STANDARDS.md).

### Usage

```bash
python scripts/validate_plugins.py
```

### What it checks

- Plugin entry points are registered correctly
- Required metadata fields are present (name, version, core_api, description)
- Core API version compatibility
- Required hooks exist (register_pipes, register_services)
- Hooks return correct types (lists)

### Exit codes

- 0: All plugins valid
- 1: Validation errors found

### Example output

```
Validating plugins in group 'open_ticket_ai.plugins'...
Required core API: 2.0

Checking plugin: hf_local
  ✅ Plugin 'hf_local' metadata: {'name': 'open-ticket-ai-hf-local', 'version': '1.0.0rc1', 'core_api': '2.0', 'description': 'Hugging Face local text classification plugin for Open Ticket AI'}
Checking plugin: otobo_znuny
  ✅ Plugin 'otobo_znuny' metadata: {'name': 'open-ticket-ai-otobo-znuny-plugin', 'version': '1.0.0rc1', 'core_api': '2.0', 'description': 'OTOBO/Znuny ticket system integration plugin for Open Ticket AI'}

Found 2 plugin(s)

✅ All plugins validated successfully!
```
