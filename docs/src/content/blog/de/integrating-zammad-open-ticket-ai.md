---
title: 'Zammad Integration for Open Ticket AI: AI-Powered Ticket Automation via REST API'
description: 'Integrate Open Ticket AI with Zammad using the official plugin for automated classification, routing, and prioritization through REST API integration.'
lang: en
date: 2025-07-28
tags:
  - zammad-integration
  - rest-api
  - plugin-system
  - ai-automation
  - ticket-classification
  - open-source-integration
category: Integration
draft: false
image: ../../../assets/images/ai-solves-many-tickets-data-connected-systems.png
---

# Zammad-Integration für Open Ticket AI

Open Ticket AI (OTAI) enthält ein Plugin für **Zammad**, das OTAI ermöglicht, Tickets über die Zammad REST API zu lesen und zu aktualisieren. Dies ermöglicht KI-gesteuertes Routing, Priorisierung und Kategorisierung direkt in Zammad. Die aktuelle Implementierung funktioniert, ist jedoch **noch nicht vollständig getestet** und kann in realen Installationen Anpassungen erfordern.

## Architektur

Die Integration folgt dem Standard-OTAI-Plugin-Muster:

- ein separates Plugin-Paket: `otai_zammad`
- ein `ZammadTicketsystemService` (Injectable)
- ein `ZammadPlugin`, das den Service registriert
- Konfiguration in `config.yml`
- OTAI schreibt Vorhersagen zurück nach Zammad über die REST-Aufrufe des Services

Diese Struktur ist identisch zu allen OTAI Ticket‑System‑Plugins (z. B. OTOBO/Znuny, Freshdesk, OTRS).

## Zammad-Plugin-Struktur

```

otai_zammad/
src/
otai_zammad/
zammad_ticket_system_service.py
plugin.py
pyproject.toml

```

### `plugin.py`

```python
from open_ticket_ai import Injectable, Plugin

from otai_zammad.zammad_ticket_system_service import ZammadTicketsystemService


class ZammadPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            ZammadTicketsystemService,
        ]
```

Das Plugin stellt genau einen Injectable bereit: `ZammadTicketsystemService`.

## ZammadTicketsystemService-Parameter

Der Service akzeptiert diese Felder:

```yaml
base_url: The base URL of the Zammad instance (e.g. https://helpdesk.example.com)
access_token: Personal Access Token used for authentication
timeout: Optional HTTP timeout in seconds
verify: TLS verification flag or path to CA bundle
```

Diese werden direkt auf das `params`‑Modell des Services abgebildet.

## Beispielkonfiguration

_(Sie ändern lediglich „use“ zu `zammad:ZammadTicketsystemService`)_  

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

Danach wird OTAI das Plugin automatisch über den Entry‑Point in Ihrer `pyproject.toml` laden:

```toml
[project.entry-points."otai.plugins"]
otai_zammad = "otai_zammad.plugin:ZammadPlugin"
```

## Wie OTAI den Zammad‑Service nutzt

1. OTAI ruft neue oder aktualisierte Zammad‑Tickets ab
2. KI‑Modelle klassifizieren Queue, Priorität oder benutzerdefinierte Labels
3. OTAI ruft `update_ticket(...)` über die Zammad‑API auf
4. Zammad aktualisiert das Ticket
5. Agenten setzen ihren normalen Zammad‑Workflow fort, jetzt unterstützt von OTAI

Der Prozess ist identisch zu OTOBO/Znuny, Freshdesk, OTRS oder jedem anderen OTAI Ticket‑System‑Plugin.

## Aktueller Stand

Die Zammad‑Integration ist **implementiert**, aber:

- sie ist **nicht vollständig getestet**
- die API‑Abdeckung könnte unvollständig sein
- reale Zammad‑Setups könnten zusätzliche Anpassungen erfordern
- Performance‑Charakteristika (Pagination, Search‑Endpoints, große Ergebnis‑Sets) benötigen noch Benchmarking

Sie können das Plugin bereits für Prototyping und interne Tests verwenden, aber den Produktionseinsatz sollten Sie bis zur weiteren Validierung warten.

## Vorteile

- KI‑Klassifizierung vollständig on‑premise
- keine Zammad‑Cloud‑Erweiterungen oder externe KI erforderlich
- lässt sich sauber in bestehende OTAI‑Workflows integrieren
- gleiche Plugin‑Architektur wie alle anderen OTAI‑Services