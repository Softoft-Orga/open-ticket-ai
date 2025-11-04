---
description: Integrate on-premise Open Ticket AI with Zendesk for automated ticket routing and classification. Build a custom OTAI plugin that updates Zendesk tickets via REST.
---

# Zendesk Integration for Open Ticket AI

Open Ticket AI (OTAI) runs fully on-premise and classifies support tickets into queues, priorities and custom labels. To integrate OTAI with **Zendesk**, you create a small plugin that provides a `ZendeskTicketsystemService`. OTAI loads this service automatically and uses it to read and update Zendesk tickets through the REST API.

## Architecture

A Zendesk integration follows the same OTAI pattern:

- a separate plugin package (`otai_zendesk`)
- a `ZendeskTicketsystemService` (Injectable)
- a `ZendeskPlugin` registering the service
- configuration in `config.yml`
- OTAI calls the service at the end of the pipeline and writes predictions back into Zendesk

This is identical to how Zammad, OTOBO/Znuny, Freshdesk, and other OTAI adapters work.

## Plugin Structure (`otai_zendesk`)

```

otai_zendesk/
src/
otai_zendesk/
zendesk_ticket_system_service.py
plugin.py
pyproject.toml

````

### `zendesk_ticket_system_service.py`

```python
from typing import Any
import aiohttp

from open_ticket_ai import Injectable
from open_ticket_ai.core.ticket_system_services import TicketSystemService


class ZendeskTicketsystemService(TicketSystemService):
    async def _request(self, method: str, path: str, **kwargs) -> Any:
        base = f"https://{self.params.domain}.zendesk.com/api/v2"
        auth = aiohttp.BasicAuth(self.params.email, self.params.api_token)
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
        return await self._request("PUT", f"/tickets/{ticket_id}", json={"ticket": data})
````

### `plugin.py`

```python
from open_ticket_ai import Plugin, Injectable

from otai_zendesk.zendesk_ticket_system_service import ZendeskTicketsystemService


class ZendeskPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            ZendeskTicketsystemService,
        ]
```

## Zendesk Parameters

Use these fields in your OTAI config:

* `domain`: your Zendesk subdomain (e.g. `mycompany`)
* `email`: Zendesk login e-mail
* `api_token`: API Token from Zendesk Admin → API → Token Access
* `timeout`: optional
* `verify`: TLS verification or CA bundle path

## Configuration Example

```yaml
ticket_systems:
  zendesk:
    use: otai_zendesk:ZendeskTicketsystemService
    params:
      domain: yourcompany
      email: support@yourcompany.com
      api_token: "{{ get_env('ZENDESK_API_TOKEN') }}"
      timeout: 10
      verify: true
```

Zendesk authentication uses Basic Auth:
`email/token` as username, and the API token as password.

OTAI discovers the plugin through your `pyproject.toml`:

```toml
[project.entry-points."otai.plugins"]
otai_zendesk = "otai_zendesk.plugin:ZendeskPlugin"
```

## How the Integration Works

1. OTAI fetches Zendesk tickets via REST
2. AI assigns queue / priority / custom labels
3. OTAI calls `update_ticket(...)`
4. Zendesk updates the ticket
5. Agents continue working in Zendesk with AI-enhanced routing

Everything runs on-premise, without Zendesk’s own AI modules.

## Benefits

* complete data control (OTAI stays local)
* no need for Zendesk’s proprietary AI
* simple REST integration
* identical plugin structure to Zammad, OTOBO/Znuny, Freshdesk, OTRS

