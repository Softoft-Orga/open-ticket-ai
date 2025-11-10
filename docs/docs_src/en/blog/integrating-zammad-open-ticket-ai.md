---
description: Integrate Open Ticket AI with Zammad using the built-in OTAI Zammad plugin. The adapter exists but is not fully tested yet.
---

# Zammad Integration for Open Ticket AI

Open Ticket AI (OTAI) includes a plugin for **Zammad**, allowing OTAI to read and update tickets through the Zammad REST API. This enables AI-driven routing, prioritization and categorization directly inside Zammad.
The current implementation works, but it is **not fully tested yet** and may require adjustments in real-world installations.

## Architecture

The integration follows the standard OTAI plugin pattern:

- a separate plugin package: `otai_zammad`
- a `ZammadTicketsystemService` (Injectable)
- a `ZammadPlugin` registering the service
- configuration in `config.yml`
- OTAI writes predictions back into Zammad through the service’s REST calls

This structure is identical to all OTAI ticket system plugins (e.g. OTOBO/Znuny, Freshdesk, OTRS).

## Zammad Plugin Structure

```

otai_zammad/
src/
otai_zammad/
zammad_ticket_system_service.py
plugin.py
pyproject.toml

````

### `plugin.py`

```python
from open_ticket_ai import Injectable, Plugin

from otai_zammad.zammad_ticket_system_service import ZammadTicketsystemService


class ZammadPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            ZammadTicketsystemService,
        ]
````

The plugin exposes exactly one injectable: `ZammadTicketsystemService`.

## ZammadTicketsystemService Parameters

The service accepts these fields:

```yaml
base_url: The base URL of the Zammad instance (e.g. https://helpdesk.example.com)
access_token: Personal Access Token used for authentication
timeout: Optional HTTP timeout in seconds
verify: TLS verification flag or path to CA bundle
```

These map directly to the service’s `params` model.

## Example Configuration

*(You just change “use” to `zammad:ZammadTicketsystemService`)*

```yaml
ticket_systems:
  zammad:
    use: zammad:ZammadTicketsystemService
    params:
      base_url: https://your-zammad-domain
      access_token: "{{ get_env('ZAMMAD_TOKEN') }}"
      timeout: 10
      verify: true
```

After this, OTAI will automatically load the plugin via the entry point in your `pyproject.toml`:

```toml
[project.entry-points."otai.plugins"]
otai_zammad = "otai_zammad.plugin:ZammadPlugin"
```

## How OTAI Uses the Zammad Service

1. OTAI fetches new or updated Zammad tickets
2. AI models classify queue, priority or custom labels
3. OTAI calls `update_ticket(...)` on the Zammad API
4. Zammad updates the ticket
5. Agents continue their normal Zammad workflow, now powered by OTAI

The process is identical to OTOBO/Znuny, Freshdesk, OTRS or any other OTAI ticket system plugin.

## Current Status

The Zammad integration is **implemented**, but:

* it is **not fully tested**
* API coverage may be incomplete
* real-world Zammad setups may require additional adjustments
* performance characteristics (pagination, search endpoints, large result sets) still need benchmarking

You can already use the plugin for prototyping and internal testing, but production use should wait until further validation.

## Benefits

* AI classification entirely on-premise
* no Zammad cloud extensions or external AI needed
* integrates cleanly into existing OTAI workflows
* same plugin architecture as all other OTAI services

