# OTOBO/Znuny Plugin - Backward Compatibility Location

**⚠️ This directory is maintained for backward compatibility only.**

## Important Notice

The OTOBO/Znuny plugin has been extracted into a standalone PyPI package.

**New Location:** `packages/open_ticket_ai_otobo_znuny_plugin/`

## For New Projects

Install the plugin from PyPI:

# open-ticket-ai-otobo-znuny-plugin

OTOBO/Znuny ticket system integration plugin for Open Ticket AI.

This plugin provides seamless integration with OTOBO and Znuny ticket systems.

## Installation

```bash
pip install open-ticket-ai-otobo-znuny-plugin
```

Or with Open Ticket AI extras:

```bash
pip install open-ticket-ai[otobo-znuny]
```

## For Existing Projects

Existing code using `open_ticket_ai_otobo_znuny_plugin` will continue to work as this location is maintained for backward compatibility.

However, we recommend migrating to the standalone package:
## Requirements

1. Install the plugin package: `pip install open-ticket-ai-otobo-znuny-plugin`
2. Your existing imports will continue to work without changes
- Python >= 3.13
- open-ticket-ai >= 1.0.0rc1
- otobo-znuny >= 1.4.0

## Documentation
## Usage

- [Plugin README](../../packages/open_ticket_ai_otobo_znuny_plugin/README.md)
- [Installation Guide](https://open-ticket-ai.com/en/guide/available-plugins.html)
- [Developer Guide](../../packages/open_ticket_ai_otobo_znuny_plugin/DEVELOPER.md)
This plugin integrates with the Open Ticket AI pipeline system. See the main [Open Ticket AI documentation](https://open-ticket-ai.com) for configuration examples.

## Migration Path
## License

This backward-compatibility layer may be removed in a future major version. We recommend:

1. Installing the standalone plugin package
2. Testing your configuration works with the new package
3. Removing dependency on the bundled version (optional)

The plugin API remains unchanged, so migration is seamless.
LGPL-2.1-only
