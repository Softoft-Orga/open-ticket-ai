---
title: 'Ticket-System-Integration'
description: 'Integration externer Ticketing-Plattformen mit Open Ticket AI unter Verwendung der Basisklasse TicketSystemService.'
---

# Ticket System Integration

Die Basisklasse `TicketSystemService` definiert einen minimalen Vertrag für Adapter, die externe Ticketing-Plattformen mit Open Ticket AI integrieren. Die Klasse stellt benannte Coroutine-Methoden bereit, die stets `UnifiedTicket`-Daten zurückgeben, während sie flexible Schlüsselwortargumente für plattformspezifisches Verhalten akzeptieren.

## Flexible Adapter Contracts

Adapter müssen Implementierungen für diese Methoden bereitstellen:

- `find_tickets`
- `find_first_ticket`
- `get_ticket`
- `create_ticket`
- `update_ticket`
- `add_note`

Jede Methode kann Schlüsselwortargumente (`**kwargs`) akzeptieren, die aus einer YAML-Konfiguration gerendert werden. Dies ermöglicht es jedem Adapter, die Argumentstrukturen, die das zugrunde liegende SDK erwartet, offenzulegen, ohne sie zunächst in ein starres Schema zu zwängen. Methoden können weiterhin Hilfsmodelle wie `UnifiedTicket` akzeptieren, aber die Adapter sind dafür verantwortlich, ihre nativen Modelle vor der Rückgabe der Ergebnisse in `UnifiedTicket` zu konvertieren.

## When to Use Unified Models

Unified-Modelle bleiben für Teams verfügbar, die eine normalisierte Nutzlast wünschen. Jeder Adapter kann Konverter-Hilfsfunktionen bereitstellen (zum Beispiel `otai_otobo_znuny.models.otobo_ticket_to_unified_ticket`), um die Übersetzung von nativen Ticketdarstellungen in das einheitliche Schema zu zentralisieren. Adapter können dieselben Hilfsfunktionen intern verwenden, und Aufrufer können sie erneut nutzen, wenn sie mit nativen Modellen arbeiten, die direkt aus dem Upstream‑SDK abgerufen werden.

## YAML Examples

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

Die obigen YAML‑Snippets werden in Schlüsselwortargumente gerendert, die direkt an Adapter‑Methoden übergeben werden. Sie können auch in Unified‑Modelle in benutzerdefinierten Pipes konvertiert werden, wenn der Workflow normalisierte Daten erwartet.

## Migrating Existing Adapters

1. Entfernen Sie `@abstractmethod`-Implementierungen und erzwingen Sie nur die Methodennamen, die in `TicketSystemService` definiert sind.  
2. Akzeptieren Sie Schlüsselwortargumente (zum Beispiel `async def create_ticket(self, **kwargs)`) oder behalten Sie optionale Unified-Modelle bei, wenn sie Konvertierungen vereinfachen.  
3. Konvertieren Sie native SDK-Antworten in `UnifiedTicket`-Instanzen, bevor Sie von `find_tickets`, `find_first_ticket`, `get_ticket` und `create_ticket` zurückkehren.  
4. Bieten Sie Hilfsfunktionen für Verbraucher an, die direkt mit nativen Ticketobjekten arbeiten müssen.

Adapter, die nach diesen Richtlinien gebaut werden, bleiben mit bestehenden Pipelines kompatibel und erhalten gleichzeitig die Flexibilität, reichhaltigere plattformspezifische Funktionen offenzulegen.