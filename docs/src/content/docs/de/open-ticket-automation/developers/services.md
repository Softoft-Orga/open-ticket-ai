---
title: Core Services
description: 'Core services documentation for Open Ticket AI covering ticket system adapters, business logic encapsulation, and dependency injection.'
---

# Core Services

Services kapseln Geschäftslogik und stellen wiederverwendbare Funktionalität für Pipes bereit. Sie werden vom Dependency-Injection-Container verwaltet.

## Service-Klassen vs. Konfigurationseinträge

Service-*Klassen* sind Python-Implementierungen, die in Paketen leben (z. B. Unterklassen von `otai_base.ticket_system_integration.TicketSystemService`).
Sie werden innerhalb von Open Ticket AI nutzbar, wenn Sie sie über das Plugin-Registry verfügbar machen.

Service-*Konfigurationseinträge* leben in `open_ticket_ai.services` innerhalb Ihrer YAML-Konfiguration. Jeder Eintrag bindet eine
Service-Klasse an einen Bezeichner, optionale Konstruktorparameter und einen Dependency-Injection-Scope. Mehrere Einträge können
auf dieselbe Klasse verweisen, während sie unterschiedliche Parameter liefern.

### Beispiel: Mehrere Services gleichzeitig konfiguriert

```yaml
open_ticket_ai:
  services:
    jinja_default:
      use: 'base:JinjaRenderer'

    otobo_znuny:
      use: 'otobo-znuny:OTOBOZnunyTicketSystemService'
      params:
        base_url: 'http://example/otobo/nph-genericinterface.pl'
        password: '${OTOBO_PASSWORD}'

    hf_local:
      use: 'hf-local:HFClassificationService'
      params:
        model_name: 'softoft/otai-queue-de-bert-v1'
```

In dieser Konfiguration werden drei unabhängige Services für die Injection verfügbar. Pipes wählen die Instanz aus, die sie benötigen, indem sie
auf den Eintragsbezeichner verweisen, zum Beispiel:

```yaml
- id: fetch_otobo
  use: 'base:FetchTicketsPipe'
  injects:
    ticket_system: 'otobo_znuny'
```

## Kern-Service-Typen

### Ticket-Services

- **TicketSystemAdapter**: Schnittstelle zu Ticketsystemen
- **TicketFetcher**: Holt Tickets ab
- **TicketUpdater**: Aktualisiert Ticket-Eigenschaften

### Klassifizierungs-Services

- **ClassificationService**: ML-basierte Klassifizierung
- **QueueClassifier**: Logik für Warteschlangenzuweisung
- **PriorityClassifier**: Logik für Prioritätszuweisung

### Utility-Services

- **TemplateRenderer**: Jinja2-Template-Rendering (kann in `defs` für Anpassungen konfiguriert werden)
- **ConfigurationService**: Zugriff auf Konfiguration
- **LoggerFactory**: Zentrale Protokollierung mit austauschbaren Backends (stdlib/structlog)

## Service-Lebenszyklus und Scopes

Wenn die Anwendung die Konfiguration lädt, wandelt sie jeden `open_ticket_ai.services`-Eintrag in eine `InjectableConfig` um und
registriert sie beim DI-Container. Jeder Eintrag liefert eine eigene injizierbare Instanz. Wenn Sie drei Ticketsystem-Services konfigurieren,
können alle drei gleichzeitig unter ihren Bezeichnern injiziert werden.

Scopes steuern, wann diese Instanzen erstellt und wiederverwendet werden. Open Ticket AI unterstützt:

- **Singleton-Scope (Standard)** – Der Container erstellt eine Instanz pro Konfigurationseintrag und verwendet sie in der gesamten Anwendung wieder.
- **Transient-Scope** – Bei jeder Injection wird eine neue Instanz erstellt.

Wählen Sie den Scope, der zum Zustandsverhalten des Services passt. Siehe den Leitfaden [Dependency Injection](dependency_injection.md)
für Details zu Scopes und die [Configuration Reference](../../details/config_reference.md) für die Struktur von `services`.

## Eigene Services erstellen

1.  Service-Schnittstelle definieren
2.  Service implementieren
3.  Mit dem DI-Container über das Injector-Modul registrieren
4.  Einen Konfigurationseintrag hinzufügen und in Pipes injizieren

## Best Practices für Services

### Empfohlen:

- Services auf eine einzige Verantwortung fokussieren
- Schnittstellen für Service-Verträge verwenden
- Services nach Möglichkeit zustandslos halten
- Abhängigkeiten injizieren, nicht selbst erstellen
- Unit-Tests für Services schreiben

### Nicht empfohlen:

- Ausführungszustand in Service-Instanzen speichern
- Direkt auf Konfiguration zugreifen (ConfigurationService injizieren)
- Zirkuläre Abhängigkeiten erzeugen
- Geschäftslogik mit Infrastrukturbelangen vermischen

## Services testen

Services sollten unabhängig von den Pipes, die sie verwenden, unit-getestet werden. Erstellen Sie Testinstanzen von Services und überprüfen Sie
ihr Verhalten mit Testdaten.

## Verwandte Dokumentation

- [Dependency Injection](dependency_injection.md)
- [Configuration Reference](../../details/config_reference.md)
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Plugin Development](plugin_development.mdx)