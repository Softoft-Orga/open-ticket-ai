---
title: Dependency Injection
description: 'Learn how Open Ticket AI uses dependency injection to manage services, resolve dependencies, and enable testability with loose coupling.'
lang: en
nav:
  group: Developers
  order: 1
---

# Dependency Injection

Open Ticket AI verwendet Dependency Injection (DI), um Services, Pipes und gemeinsam genutzte Infrastruktur zu verwalten. Der Container ist dafür verantwortlich, Kern‑Singletons zu erstellen, Plugins zu laden und Factories bereitzustellen, die Abhängigkeiten zur Laufzeit auflösen.

## Grundlagen des Component Registry

`ComponentRegistry` verfolgt jedes Injectable, das die Laufzeit konstruieren kann. Pipes und Services werden in separaten Dictionaries gespeichert, sodass das Registry klarere Fehlermeldungen und Typ‑Erwartungen bei der Suche durchsetzen kann.

- `register()` inspiziert die zu registrierende Klasse. Pipes (Unterklassen von `Pipe`) werden in `_pipes` gespeichert, während andere Unterassen von `Injectable` in `_services` abgelegt werden.
- Wenn eine Suche fehlschlägt, enthält `InjectableNotFoundError` die aktuell geladenen Identifier, um Konfigurationsprobleme leichter diagnostizieren zu können.
- `find_by_type()` führt eine gefilterte Suche über beide Sammlungen durch. Der TemplateRenderer‑Bootstrap (nachfolgend beschrieben) nutzt dies, um Services zu finden, die ein bestimmtes Interface implementieren.

### Wie Plugins das Registry füllen

Jedes Plugin implementiert `Plugin._get_all_injectables()` und gibt jede Service‑ und Pipe‑Klasse zurück, die auffindbar sein soll. Beim Anwendungsstart sucht der `PluginLoader` nach Entry‑Points in der Gruppe `open_ticket_ai.plugins`, instanziiert das Plugin und ruft `on_load()` mit dem gemeinsamen Registry auf.

`Plugin.on_load()` erstellt für jedes Injectable einen Registry‑Identifier. Das Präfix wird aus dem Plugin‑Modulnamen abgeleitet (mit dem globalen `otai-`‑Plugin‑Präfix entfernt) und mit dem eigenen `get_registry_name()` des Injectables mittels `:` als Trennzeichen kombiniert. Das stellt sicher, dass Registry‑IDs global eindeutig bleiben und dennoch lesbar sind (z. B. `base:MyService`).

## Ablauf des Container‑Bootstraps

`AppModule` ist das Injector‑Modul, das die Laufzeit zusammenfügt. Sein Konstruktor erstellt eifrig mehrere Singletons:

1. `AppConfig` lädt Umgebungs‑, `.env`‑ und `config.yml`‑Einstellungen und stellt das Workspace‑Konfigurationsmodell bereit.
2. `ComponentRegistry` wird instanziiert und in das Modul, den PluginLoader, die PipeFactory und die Tests injiziert.
3. `LoggerFactory` wird von `create_logger_factory()` erzeugt, sodass jedes Injectable strukturierte Logger erhalten kann.
4. `PluginLoader` erhält das Registry, die LoggerFactory und die Konfiguration. `load_plugins()` wird sofort ausgeführt, sodass Pipes und Services aus Plugins verfügbar sind, bevor der Injector andere Bindungen auflöst.

Während `configure()` bindet `AppModule` diese Instanzen als Singletons und registriert den Typ `PipeFactory` selbst als Singleton, damit andere Komponenten ihn später anfordern können.

### Auswahl des TemplateRenderer und Schutzmechanismen

Template‑Rendering ist ein erforderlicher Service. Die Provider‑Methode `create_renderer_from_service()` inspiziert die konfigurierten Services, filtert die Einträge, die `TemplateRenderer` implementieren, und stellt sicher, dass genau eine Konfiguration existiert.

- Wenn mehr als ein TemplateRenderer‑Service vorhanden ist, stoppt `MultipleConfigurationsForSingletonServiceError` den Bootstrap. Das verhindert Mehrdeutigkeiten darüber, welcher Renderer für das Templating verwendet werden soll.
- Wenn keiner gefunden wird, wird `MissingConfigurationForRequiredServiceError` ausgelöst, was signalisiert, dass die Konfiguration unvollständig ist und das Template‑Rendering nicht fortgesetzt werden kann.

Nach der Validierung wird das Registry nach der konkreten Renderer‑Klasse gefragt, die mit ihren gerenderten Parametern instanziiert und als Singleton‑TemplateRenderer für die Anwendung zurückgegeben wird.

## Injizieren von Abhängigkeiten in Pipes und Services

Die Laufzeit‑Abhängigkeitsauflösung wird von `PipeFactory` orchestriert:

- Wenn eine Pipe erstellt wird, löst die Factory jeden `injects`‑Eintrag in der Pipe‑Konfiguration auf. Jede Zuordnung verknüpft ein Konstruktor‑Argument (z. B. `ticket_client`) mit dem Identifier eines konfigurierten Services. Die Factory holt die Service‑Konfiguration, rendert deren Parameter, instanziiert den Service und übergibt ihn dem Pipe‑Konstruktor.
- Services und Pipes müssen `logger_factory` in ihren Konstruktoren akzeptieren (bereitgestellt von `Injectable.__init__`), damit sie namespaced Logs ausgeben können, ohne die LoggingBackends neu zu konfigurieren.
- Verwenden Sie das vom `Plugin._get_registry_name()` erzeugte Registry‑Namensschema, wenn Sie `use`‑Ziele in der Konfiguration deklarieren. Das stellt sicher, dass die Factory die korrekte Klasse finden kann (z. B. `base:HttpTicketPipe`).

Pipes erhalten ihre Parameter durch Templating vor der Instanziierung. `PipeFactory` rendert den `params`‑Block mit dem aktiven `TemplateRenderer` und erstellt anschließend die Pipe mit dem gerenderten `PipeConfig`, dem `PipeContext`, Referenzen auf sich selbst (für das Erzeugen verschachtelter Pipes) und allen injizierten Services.

Services folgen dem gleichen Muster: Sobald sie ausgewählt sind, rendert die Factory die Service‑Konfiguration gegen einen leeren Scope und baut das Injectable. Da jeder Service von `Injectable` erbt, parsen sie automatisch typisierte Parameter über ihr `ParamsModel` und erhalten einen Logger, der nach ihrer Konfigurations‑ID benannt ist.

### Praktische Tipps

- Definieren Sie ein beschreibendes `ParamsModel` in Ihrer Pipe‑ oder Service‑Unterklasse, damit die Konfiguration automatisch während der Konstruktion validiert wird.
- Behalten Sie injizierte IDs konsistent über Konfiguration und Laufzeit hinweg, indem Sie das oben beschriebene Registry‑Präfix wiederverwenden.
- Wenn Sie neue Plugins erstellen, geben Sie alle Injectable‑Klassen aus `_get_all_injectables()` zurück, damit sie beim Bootstrap automatisch registriert werden.
- Wenn eine Pipe eine andere Pipe benötigt, injizieren Sie `PipeFactory` und rufen `await pipe_factory.create_pipe(...)` auf, anstatt sie direkt zu instanziieren. Die Factory übernimmt das Templating, Logging und die Abhängigkeitsauflösung für verschachtelte Pipes.

## Verwandte Dokumentation

- [Services](services.md)