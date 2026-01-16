---
title: 'Zammad Integration für Open Ticket AI: KI-gestützte Ticket-Automatisierung via REST API'
description: 'Integrieren Sie Open Ticket AI mit Zammad über das offizielle Plugin für automatisierte Klassifizierung, Routing und Priorisierung durch REST API Integration.'
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

# Zammad Integration für Open Ticket AI

Open Ticket AI (OTAI) enthält ein Plugin für **Zammad**, das es OTAI ermöglicht, Tickets über die Zammad REST API zu lesen und zu aktualisieren. Dies ermöglicht KI-gestütztes Routing, Priorisierung und Kategorisierung direkt innerhalb von Zammad.
Die aktuelle Implementierung funktioniert, ist jedoch **noch nicht vollständig getestet** und kann in realen Installationen Anpassungen erfordern.

## Architektur

Die Integration folgt dem Standard-OTAI-Plugin-Muster:

- ein separates Plugin-Paket: `otai_zammad`
- ein `ZammadTicketsystemService` (Injectable)
- ein `ZammadPlugin`, das den Service registriert
- Konfiguration in `config.yml`
- OTAI schreibt Vorhersagen über REST-Aufrufe des Services zurück in Zammad

Diese Struktur ist identisch zu allen OTAI-Ticketsystem-Plugins (z.B. OTOBO/Znuny, Freshdesk, OTRS).

## Zammad Plugin Struktur

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

Das Plugin stellt genau ein Injectable bereit: `ZammadTicketsystemService`.

## ZammadTicketsystemService Parameter

Der Service akzeptiert folgende Felder:

```yaml
base_url: Die Basis-URL der Zammad-Instanz (z.B. https://helpdesk.example.com)
access_token: Personal Access Token für die Authentifizierung
timeout: Optionaler HTTP-Timeout in Sekunden
verify: TLS-Verifizierungsflag oder Pfad zum CA-Bundle
```

Diese Felder werden direkt auf das `params`-Modell des Services abgebildet.

## Beispielkonfiguration

_(Sie ändern einfach "use" zu `zammad:ZammadTicketsystemService`)_

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

Danach lädt OTAI das Plugin automatisch über den Entry Point in Ihrer `pyproject.toml`:

```toml
[project.entry-points."otai.plugins"]
otai_zammad = "otai_zammad.plugin:ZammadPlugin"
```

## Wie OTAI den Zammad Service nutzt

1. OTAI ruft neue oder aktualisierte Zammad-Tickets ab
2. KI-Modelle klassifizieren Queue, Priorität oder benutzerdefinierte Labels
3. OTAI ruft `update_ticket(...)` auf der Zammad API auf
4. Zammad aktualisiert das Ticket
5. Agents setzen ihren normalen Zammad-Workflow fort, jetzt unterstützt durch OTAI

Der Prozess ist identisch zu OTOBO/Znuny, Freshdesk, OTRS oder jedem anderen OTAI-Ticketsystem-Plugin.

## Aktueller Status

Die Zammad-Integration ist **implementiert**, jedoch:

- ist sie **nicht vollständig getestet**
- die API-Abdeckung kann unvollständig sein
- reale Zammad-Setups können zusätzliche Anpassungen erfordern
- Leistungsmerkmale (Paginierung, Such-Endpoints, große Ergebnismengen) müssen noch bewertet werden

Sie können das Plugin bereits für Prototyping und interne Tests nutzen, aber der Produktiveinsatz sollte bis zur weiteren Validierung warten.

## Vorteile

- KI-Klassifizierung vollständig On-Premise
- keine Zammad Cloud Extensions oder externe KI erforderlich
- integriert sich sauber in bestehende OTAI-Workflows
- gleiche Plugin-Architektur wie alle anderen OTAI-Services
