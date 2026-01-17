---
title: 'Zendesk-Integration für Open Ticket AI: Selbstgehostete KI-Ticketklassifizierung'
description: 'Verbinden Sie Open Ticket AI mit Zendesk für automatisiertes, vor Ort stattfindendes Ticket-Routing und -Klassifizierung. Erstellen Sie benutzerdefinierte Plugins mit REST API-Integration für intelligente Support-Automatisierung.'
lang: en
date: 2025-08-05
tags:
  - zendesk-integration
  - api-automation
  - plugin-architecture
  - self-hosted-ai
  - ticket-routing
  - rest-api-integration
category: Integration
draft: false
image: ../../../assets/images/ticketsystem-integration-ai-dark-blue.png
---

# Zendesk-Integration für Open Ticket AI

Open Ticket AI (OTAI) läuft vollständig vor Ort und klassifiziert Support‑Tickets in Warteschlangen, Prioritäten und benutzerdefinierte Labels. Um OTAI mit **Zendesk** zu integrieren, erstellen Sie ein kleines Plugin, das einen `ZendeskTicketsystemService` bereitstellt. OTAI lädt diesen Service automatisch und verwendet ihn, um Zendesk‑Tickets über die REST API zu lesen und zu aktualisieren.

## Architecture

Eine Zendesk-Integration folgt dem gleichen OTAI‑Muster:

- ein separates Plugin‑Paket (`otai_zendesk`)
- ein `ZendeskTicketsystemService` (Injectable)
- ein `ZendeskPlugin`, das den Service registriert
- Konfiguration in `config.yml`
- OTAI ruft den Service am Ende der Pipeline auf und schreibt Vorhersagen zurück in Zendesk

Dies ist identisch zu der Funktionsweise von Zammad, OTOBO/Znuny, Freshdesk und anderen OTAI‑Adaptern.

## Plugin Structure (`otai_zendesk`)

```

otai_zendesk/
src/
otai_zendesk/
zendesk_ticket_system_service.py
plugin.py
pyproject.toml

```

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
```

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

## Zendesk-Parameter

Verwenden Sie diese Felder in Ihrer OTAI‑Konfiguration:

- `domain`: Ihre Zendesk‑Subdomain (z. B. `mycompany`)
- `email`: Zendesk‑Login‑E‑Mail
- `api_token`: API‑Token von Zendesk Admin → API → Token‑Access
- `timeout`: optional
- `verify`: TLS‑Verifizierung oder Pfad zum CA‑Bundle

## Konfigurationsbeispiel

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

Zendesk‑Authentifizierung verwendet Basic Auth:  
`email/token` als Benutzername und das API‑Token als Passwort.

OTAI entdeckt das Plugin über Ihre `pyproject.toml`:

```toml
[project.entry-points."otai.plugins"]
otai_zendesk = "otai_zendesk.plugin:ZendeskPlugin"
```

## Wie die Integration funktioniert

1. OTAI ruft Zendesk‑Tickets über REST ab
2. KI weist Warteschlange / Priorität / benutzerdefinierte Labels zu
3. OTAI ruft `update_ticket(...)` auf
4. Zendesk aktualisiert das Ticket
5. Agenten arbeiten weiter in Zendesk mit KI‑unterstütztem Routing

Alles läuft vor Ort, ohne die eigenen KI‑Module von Zendesk.

## Vorteile

- vollständige Datenkontrolle (OTAI bleibt lokal)
- kein Bedarf an der proprietären KI von Zendesk
- einfache REST‑Integration
- identische Plugin‑Struktur zu Zammad, OTOBO/Znuny, Freshdesk, OTRS