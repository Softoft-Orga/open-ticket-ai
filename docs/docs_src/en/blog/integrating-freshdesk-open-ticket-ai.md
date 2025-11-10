---
description: Integrate on-premise Open Ticket AI with Freshdesk for automated ticket routing and classification. Build a custom OTAI plugin that updates Freshdesk tickets via REST.
---

# Freshdesk Integration for Open Ticket AI

Open Ticket AI (OTAI) runs fully on-premise and classifies support tickets into queues, priorities and custom categories. To integrate OTAI with **Freshdesk**, you create a small plugin that provides a `FreshdeskTicketsystemService`. OTAI loads this service automatically and uses it to read and update tickets through the Freshdesk REST API.

## Architecture

A ticket system integration in OTAI always follows the same pattern:

- separate plugin package (`otai_freshdesk`)
- a `FreshdeskTicketsystemService` (Injectable)
- a `FreshdeskPlugin` registering the service
- configuration in `config.yml`
- OTAI calls the service at the end of the pipeline and writes AI results back to Freshdesk

This is identical to how `otai_zammad` works.

## Plugin Structure (`otai_freshdesk`)

```

otai_freshdesk/
src/
otai_freshdesk/
freshdesk_ticket_system_service.py
plugin.py
pyproject.toml

````

### `freshdesk_ticket_system_service.py`

```python
from typing import Any
import aiohttp

from open_ticket_ai import Injectable
from open_ticket_ai.core.ticket_system_services import TicketSystemService


class FreshdeskTicketsystemService(TicketSystemService):
    async def _request(self, method: str, path: str, **kwargs) -> Any:
        base = f"https://{self.params.domain}.freshdesk.com/api/v2"
        auth = aiohttp.BasicAuth(self.params.api_key, "X")
        url = f"{base}{path}"
        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.request(method, url, **kwargs) as resp:
                return await resp.json()

    async def find_tickets(self, query: dict) -> list[dict]:
        return await self._request("GET", "/tickets", params=query)

    async def find_first_ticket(self, query: dict) -> dict | None:
        tickets = await self.find_tickets(query)
        return tickets[0] if tickets else None

    async def update_ticket(self, ticket_id: str, data: dict) -> dict:
        return await self._request("PUT", f"/tickets/{ticket_id}", json=data)
````

### `plugin.py`

```python
from open_ticket_ai import Plugin, Injectable

from otai_freshdesk.freshdesk_ticket_system_service import FreshdeskTicketsystemService


class FreshdeskPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            FreshdeskTicketsystemService,
        ]
```

## Configuration

Add this to your OTAI `config.yml`:

```yaml
ticket_systems:
  freshdesk:
    use: otai_freshdesk:FreshdeskTicketsystemService
    params:
      domain: yourcompany
      api_key: YOUR_FRESHDESK_API_KEY
```

OTAI discovers your plugin automatically through your `pyproject.toml`:

```toml
[project.entry-points."otai.plugins"]
otai_freshdesk = "otai_freshdesk.plugin:FreshdeskPlugin"
```

## How the Integration Works

1. OTAI fetches tickets from Freshdesk (`find_tickets`)
2. AI assigns queue, priority, or custom labels
3. OTAI calls `update_ticket(...)`
4. Freshdesk updates the ticket instantly through its API

Everything runs on-premise. Freshdesk authentication uses basic auth with your API key.

## Benefits

* full data control (OTAI remains local)
* seamless use of Freshdesk UI and workflows
* AI-driven routing without Freshdesk’s proprietary AI
* clean plugin architecture identical to Zammad / OTOBO / Znuny
