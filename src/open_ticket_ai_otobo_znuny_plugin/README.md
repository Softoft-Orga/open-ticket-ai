# OTOBO/Znuny Plugin - Backward Compatibility Location

**⚠️ This directory is maintained for backward compatibility only.**

## Important Notice

The OTOBO/Znuny plugin has been extracted into a standalone PyPI package.

**New Location:** `packages/open_ticket_ai_otobo_znuny_plugin/`

## For New Projects

Install the plugin from PyPI:

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

1. Install the plugin package: `pip install open-ticket-ai-otobo-znuny-plugin`
2. Your existing imports will continue to work without changes

## Documentation

- [Plugin README](../../packages/open_ticket_ai_otobo_znuny_plugin/README.md)
- [Installation Guide](https://open-ticket-ai.com/en/guide/available-plugins.html)
- [Developer Guide](../../packages/open_ticket_ai_otobo_znuny_plugin/DEVELOPER.md)

## Migration Path

This backward-compatibility layer may be removed in a future major version. We recommend:

1. Installing the standalone plugin package
2. Testing your configuration works with the new package
3. Removing dependency on the bundled version (optional)

The plugin API remains unchanged, so migration is seamless.
