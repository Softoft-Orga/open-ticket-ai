---
title: Dependency Injection
description: 'Erfahren Sie, wie Open Ticket AI Dependency Injection verwendet, um Services zu verwalten, Abhängigkeiten aufzulösen und Testbarkeit mit loser Kopplung zu ermöglichen.'
lang: de
nav:
  group: Entwickler
  order: 1
---

# Dependency Injection

Open Ticket AI verwendet Dependency Injection (DI), um Services, Pipes und gemeinsame Infrastruktur zu verwalten.
Der Container ist dafür verantwortlich, Core-Singletons zu erstellen, Plugins zu laden und Factories bereitzustellen,
die Abhängigkeiten zur Laufzeit auflösen.

## Grundlagen der Komponentenregistrierung

`ComponentRegistry` verfolgt jedes injizierbare Objekt, das die Laufzeit konstruieren kann. Pipes und Services werden
in separaten Wörterbüchern gespeichert, damit die Registry klarere Fehlermeldungen und Typenerwartungen
während der Suche durchsetzen kann.【F:
src/open_ticket_ai/core/dependency_injection/component_registry.py†L12-L41】

- `register()` untersucht die Klasse, die registriert wird. Pipes (Unterklassen von `Pipe`) werden
  in `_pipes` gespeichert, während andere Unterklassen von `Injectable` in `_services` gespeichert werden.
- Wenn eine Suche fehlschlägt, enthält `InjectableNotFoundError` die Bezeichner, die aktuell geladen sind,
  um Konfigurationsprobleme leichter zu diagnostizieren.【F:
  src/open_ticket_ai/core/dependency_injection/component_registry.py†L23-L40】【F:
  src/open_ticket_ai/core/config/errors.py†L26-L34】
- `find_by_type()` führt eine gefilterte Suche über beide Sammlungen durch. Das TemplateRenderer-
  Bootstrap (unten beschrieben) verlässt sich darauf, um Services zu finden, die eine bestimmte
  Schnittstelle implementieren.【F:src/open_ticket_ai/core/dependency_injection/component_registry.py†L42-L48】

### Wie Plugins die Registry füllen

Jedes Plugin implementiert `Plugin._get_all_injectables()` und gibt jede Service- und Pipe-Klasse zurück, die
entdeckbar sein soll. Während des Anwendungsstarts findet der `PluginLoader` Entry Points in der
Gruppe `open_ticket_ai.plugins`, instanziiert das Plugin und ruft `on_load()` mit der gemeinsamen
Registry auf.【F:src/open_ticket_ai/core/plugins/plugin_loader.py†L19-L51】

`Plugin.on_load()` erstellt einen Registry-Bezeichner für jedes injizierbare Objekt. Das Präfix wird vom
Plugin-Modulnamen abgeleitet (wobei das globale `otai-` Plugin-Präfix entfernt wird) und mit dem
eigenen `get_registry_name()` des injizierbaren Objekts unter Verwendung von `:` als Trennzeichen kombiniert. Dies stellt sicher, dass Registry-IDs global eindeutig bleiben und dennoch lesbar sind (z.B. `base:MyService`).【F:
src/open_ticket_ai/core/plugins/plugin.py†L13-L44】【F:
src/open_ticket_ai/core/config/app_config.py†L13-L23】

## Container-Bootstrap-Sequenz

`AppModule` ist das Injector-Modul, das die Laufzeit verkabelt. Sein Konstruktor erstellt eifrig mehrere Singletons:

1. `AppConfig` lädt Umgebungs-, `.env`- und `config.yml`-Einstellungen und stellt das Workspace-
   Konfigurationsmodell bereit.【F:src/open_ticket_ai/core/dependency_injection/container.py†L22-L25】【F:
   src/open_ticket_ai/core/config/app_config.py†L5-L37】
2. `ComponentRegistry` wird instanziiert und in das Modul, den Plugin-Loader, die Pipe-Factory
   und Tests injiziert.【F:src/open_ticket_ai/core/dependency_injection/container.py†L25-L28】
3. `LoggerFactory` wird von `create_logger_factory()` erzeugt, damit jedes injizierbare Objekt
   strukturierte Logger erhalten kann.【F:src/open_ticket_ai/core/dependency_injection/container.py†L26-L28】【F:
   src/open_ticket_ai/core/logging/stdlib_logging_adapter.py†L1-L45】
4. `PluginLoader` erhält die Registry, die Logger-Factory und die Konfiguration. `load_plugins()` wird
   sofort ausgeführt, damit Pipes und Services von Plugins verfügbar sind, bevor der Injector andere
   Bindungen auflöst.【F:src/open_ticket_ai/core/dependency_injection/container.py†L27-L34】

Während `configure()` bindet `AppModule` diese Instanzen als Singletons und registriert den
`PipeFactory`-Typ selbst als Singleton, damit andere Komponenten ihn später anfordern können.【F:
src/open_ticket_ai/core/dependency_injection/container.py†L36-L42】

### TemplateRenderer-Auswahl und Sicherheitsvorkehrungen

Template-Rendering ist ein erforderlicher Service. Die Provider-Methode `create_renderer_from_service()`
untersucht die konfigurierten Services, filtert die Einträge, die `TemplateRenderer` implementieren, und
erzwingt, dass genau eine Konfiguration existiert.【F:
src/open_ticket_ai/core/dependency_injection/container.py†L44-L73】【F:
src/open_ticket_ai/core/dependency_injection/service_registry_util.py†L1-L17】

- Wenn mehr als ein TemplateRenderer-Service vorhanden ist, stoppt
  `MultipleConfigurationsForSingletonServiceError` den Bootstrap. Dies verhindert Mehrdeutigkeit
  darüber, welcher Renderer für das Templating verwendet werden soll.【F:
  src/open_ticket_ai/core/dependency_injection/container.py†L63-L66】【F:
  src/open_ticket_ai/core/config/errors.py†L52-L64】
- Wenn keiner gefunden wird, wird `MissingConfigurationForRequiredServiceError` ausgelöst, was signalisiert, dass die
  Konfiguration unvollständig ist und das Template-Rendering nicht fortgesetzt werden kann.【F:
  src/open_ticket_ai/core/dependency_injection/container.py†L68-L71】【F:
  src/open_ticket_ai/core/config/errors.py†L41-L50】

Nach der Validierung wird die Registry nach der konkreten Renderer-Klasse gefragt, die mit ihren
Rendering-Parametern instanziiert und als Singleton-TemplateRenderer für die Anwendung zurückgegeben wird.【F:
src/open_ticket_ai/core/dependency_injection/container.py†L72-L78】【F:
src/open_ticket_ai/core/template_rendering/template_renderer.py†L1-L52】

## Injizieren von Abhängigkeiten in Pipes und Services

Die Laufzeit-Abhängigkeitsauflösung wird von `PipeFactory` orchestriert:

- Wenn eine Pipe erstellt wird, löst die Factory jeden `injects`-Eintrag in der Pipe-Konfiguration auf. Jede
  Zuordnung verknüpft ein Konstruktorargument (wie `ticket_client`) mit dem Bezeichner eines
  konfigurierten Services. Die Factory holt die Service-Konfiguration, rendert ihre Parameter,
  instanziiert den Service und übergibt ihn an den Pipe-Konstruktor.【F:
  src/open_ticket_ai/core/pipes/pipe_factory.py†L19-L74】
- Services und Pipes müssen `logger_factory` in ihren Konstruktoren akzeptieren (bereitgestellt durch
  `Injectable.__init__`), damit sie namespaced Logs ausgeben können, ohne Logging-Backends neu zu konfigurieren.【F:
  src/open_ticket_ai/core/injectables/injectable.py†L11-L24】【F:
  src/open_ticket_ai/core/logging/logging_iface.py†L7-L23】
- Verwenden Sie das Registry-Namensschema, das von `Plugin._get_registry_name()` erzeugt wird, wenn Sie `use`
  Ziele in der Konfiguration deklarieren. Dies stellt sicher, dass die Factory die richtige Klasse nachschlagen kann (z.B.
  `base:HttpTicketPipe`).【F:src/open_ticket_ai/core/plugins/plugin.py†L25-L44】

Pipes erhalten ihre Parameter durch Templating vor der Instanziierung. `PipeFactory` rendert den
`params`-Block mit dem aktiven `TemplateRenderer`, konstruiert dann die Pipe mit den gerenderten
`PipeConfig`, dem `PipeContext`, Referenzen auf sich selbst (zum Erstellen verschachtelter Pipes) und allen injizierten
Services.【F:src/open_ticket_ai/core/pipes/pipe_factory.py†L31-L61】

Services folgen demselben Muster: Sobald ausgewählt, rendert die Factory die Service-Konfiguration
gegen einen leeren Scope und baut das injizierbare Objekt. Da jeder Service von `Injectable` abgeleitet ist,
parsen sie automatisch typisierte Parameter über ihr `ParamsModel` und erhalten einen Logger, der nach ihrem
Konfigurations-ID benannt ist.【F:src/open_ticket_ai/core/pipes/pipe_factory.py†L62-L74】【F:
src/open_ticket_ai/core/injectables/injectable.py†L11-L24】

### Praktische Tipps

- Definieren Sie ein beschreibendes `ParamsModel` für Ihre Pipe- oder Service-Unterklasse, damit die Konfiguration
  während der Konstruktion automatisch validiert wird.【F:
  src/open_ticket_ai/core/injectables/injectable.py†L9-L24】
- Halten Sie Inject-IDs konsistent über Konfiguration und Laufzeit hinweg, indem Sie das oben beschriebene Registry-Präfix wiederverwenden.
- Wenn Sie neue Plugins erstellen, geben Sie alle injizierbaren Klassen aus `_get_all_injectables()` zurück, damit sie
  während des Bootstraps automatisch registriert werden.【F:src/open_ticket_ai/core/plugins/plugin.py†L37-L44】
- Wenn eine Pipe eine andere Pipe benötigt, injizieren Sie `PipeFactory` und rufen Sie
  `await pipe_factory.create_pipe(...)` auf, anstatt sie direkt zu instanziieren. Die Factory wird
  dann Templating, Logging und Abhängigkeitsauflösung für verschachtelte Pipes handhaben.【F:
  src/open_ticket_ai/core/pipes/pipe_factory.py†L19-L61】

## Verwandte Dokumentation

- [Services](services.md)