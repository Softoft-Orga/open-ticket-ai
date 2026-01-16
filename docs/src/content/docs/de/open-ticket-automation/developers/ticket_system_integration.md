---
title: 'Ticket System Integration'
description: 'Integration of external ticketing platforms with Open Ticket AI using the TicketSystemService base class.'
---

# Ticket System Integration

Die Basisklasse `TicketSystemService` definiert einen minimalen Vertrag für Adapter, die externe Ticketing-Plattformen mit Open Ticket AI integrieren. Die Klasse stellt benannte Coroutine-Methoden bereit, die immer `UnifiedTicket`-Daten zurückgeben, während sie flexible Schlüsselwortargumente für plattformspezifisches Verhalten akzeptieren.

## Flexible Adapter-Verträge

Adapter müssen Implementierungen für diese Methoden bereitstellen:

- `find_tickets`
- `find_first_ticket`
- `get_ticket`
- `create_ticket`
- `update_ticket`
- `add_note`

Jede Methode kann Schlüsselwortargumente (`**kwargs`) akzeptieren, die aus der YAML-Konfiguration gerendert werden. Dies ermöglicht es jedem Adapter, die Argumentformen, die das zugrundeliegende SDK erwartet, offenzulegen, ohne sie zuerst in ein starres Schema zu pressen. Methoden können weiterhin Hilfsmodelle wie `UnifiedTicket` akzeptieren, aber Adapter sind dafür verantwortlich, ihre nativen Modelle vor der Rückgabe der Ergebnisse wieder in `UnifiedTicket` umzuwandeln.

## Wann einheitliche Modelle zu verwenden sind

Einheitliche Modelle bleiben für Teams verfügbar, die eine normalisierte Nutzlast wünschen. Jeder Adapter kann Konverter-Hilfsfunktionen bereitstellen (z. B. `otai_otobo_znuny.models.otobo_ticket_to_unified_ticket`), um die Übersetzung von nativen Ticket-Repräsentationen in das einheitliche Schema zu zentralisieren. Adapter können dieselben Hilfsfunktionen intern verwenden, und Aufrufer können sie wiederverwenden, wenn sie mit nativen Modellen arbeiten, die direkt vom Upstream-SDK abgerufen wurden.

## YAML-Beispiele

```yaml
services:
  - id: 'otobo'
    use: 'otobo-znuny:OTOBOZnunyTicketSystemService'
    params:
      webservice_name: 'GenericTicketConnector'
      base_url: 'https://helpdesk.example.com'
      username: 'agent'
      password: '${{ secrets.OTOBO_PASSWORD }}'

pipes:
  - id: 'fetch-open'
    use: 'otai_base:pipes.ticket_system_pipes.FetchTicketsPipe'
    params:
      ticket_search_criteria:
        queue:
          id: '5'
        limit: 20

  - id: 'create'
    use: 'my_plugin:CreateTicketPipe'
    params:
      ticket_payload:
        subject: '{{ context.subject }}'
        body: '{{ context.body }}'
```

Die obigen YAML-Ausschnitte werden in Schlüsselwortargumente gerendert, die direkt an die Adapter-Methoden übergeben werden. Sie können auch in benutzerdefinierten Pipes in einheitliche Modelle umgewandelt werden, wenn der Workflow normalisierte Daten erwartet.

## Migration bestehender Adapter

1. Entfernen Sie `@abstractmethod`-Implementierungen und erzwingen Sie nur die auf `TicketSystemService` definierten Methodennamen.
2. Akzeptieren Sie Schlüsselwortargumente (z. B. `async def create_ticket(self, **kwargs)`) oder behalten Sie optionale einheitliche Modelle bei, wenn sie Konvertierungen vereinfachen.
3. Wandeln Sie native SDK-Antworten in `UnifiedTicket`-Instanzen um, bevor Sie sie aus `find_tickets`, `find_first_ticket`, `get_ticket` und `create_ticket` zurückgeben.
4. Bieten Sie Hilfsfunktionen für Consumer an, die direkt mit nativen Ticket-Objekten arbeiten müssen.

Adapter, die nach diesen Richtlinien erstellt wurden, bleiben mit bestehenden Pipelines kompatibel und gewinnen gleichzeitig die Flexibilität, umfangreichere plattformspezifische Funktionen offenzulegen.