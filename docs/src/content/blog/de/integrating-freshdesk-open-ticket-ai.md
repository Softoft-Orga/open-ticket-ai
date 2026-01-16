---
title: 'Freshdesk-Integration für Open Ticket AI: On-Premise-Klassifizierung via REST-API'
description: 'Integrieren Sie selbst gehostetes Open Ticket AI mit Freshdesk über benutzerdefinierte Plugins. Automatisieren Sie Ticket-Routing, Prioritätszuweisung und Warteschlangen-Klassifizierung via REST-API.'
lang: en
date: 2025-08-12
tags:
  - freshdesk-integration
  - api-integration
  - plugin-development
  - ticket-automation
  - on-premise-ai
  - rest-api
category: Integration
draft: false
image: ../../../assets/images/connecting-multiple-services-integration.png
---

# Freshdesk-Integration für Open Ticket AI

Open Ticket AI (OTAI) läuft vollständig on-premise und klassifiziert Support-Tickets in Warteschlangen, Prioritäten und benutzerdefinierte Kategorien. Um OTAI mit **Freshdesk** zu integrieren, erstellen Sie ein kleines Plugin, das einen `FreshdeskTicketsystemService` bereitstellt. OTAI lädt diesen Service automatisch und nutzt ihn, um Tickets über die Freshdesk REST-API zu lesen und zu aktualisieren.

## Architektur

Eine Ticketsystem-Integration in OTAI folgt immer demselben Muster:

- separates Plugin-Paket (`otai_freshdesk`)
- ein `FreshdeskTicketsystemService` (Injectable)
- ein `FreshdeskPlugin`, das den Service registriert
- Konfiguration in `config.yml`
- OTAI ruft den Service am Ende der Pipeline auf und schreibt die KI-Ergebnisse zurück nach Freshdesk

Dies ist identisch zur Funktionsweise von `otai_zammad`.

## Plugin-Struktur (`otai_freshdesk`)

```

otai_freshdesk/
src/
otai_freshdesk/
freshdesk_ticket_system_service.py
plugin.py
pyproject.toml

```

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
```

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

## Konfiguration

Fügen Sie dies Ihrer OTAI `config.yml` hinzu:

```yaml
ticket_systems:
  freshdesk:
    use: otai_freshdesk:FreshdeskTicketsystemService
    params:
      domain: yourcompany
      api_key: YOUR_FRESHDESK_API_KEY
```

OTAI entdeckt Ihr Plugin automatisch über Ihre `pyproject.toml`:

```toml
[project.entry-points."otai.plugins"]
otai_freshdesk = "otai_freshdesk.plugin:FreshdeskPlugin"
```

## So funktioniert die Integration

1.  OTAI holt Tickets von Freshdesk (`find_tickets`)
2.  KI weist Warteschlange, Priorität oder benutzerdefinierte Labels zu
3.  OTAI ruft `update_ticket(...)` auf
4.  Freshdesk aktualisiert das Ticket sofort über seine API

Alles läuft on-premise. Die Freshdesk-Authentifizierung verwendet Basic Auth mit Ihrem API-Key.

## Vorteile

- volle Datenkontrolle (OTAI bleibt lokal)
- nahtlose Nutzung der Freshdesk-UI und -Workflows
- KI-gesteuertes Routing ohne Freshdesks proprietäre KI
- saubere Plugin-Architektur identisch zu Zammad / OTOBO / Znuny