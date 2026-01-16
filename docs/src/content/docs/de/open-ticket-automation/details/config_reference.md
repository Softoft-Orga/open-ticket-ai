---
title: Konfigurationsreferenz
lang: de
nav:
  group: Details
  order: 1
---

# Konfigurationsreferenz

Open Ticket AI lädt seine YAML-Konfiguration in das `OpenTicketAIConfig`-Modell. Das Schema basiert auf einem einzelnen
`open_ticket_ai`-Objekt, das API-/Versions-Metadaten, Infrastruktureinstellungen, Dependency-Injected Services und die
Definition des Pipeline-Orchestrators enthält. 【F:src/open_ticket_ai/core/config/config_models.py†L17-L37】

## Grundstruktur der Konfiguration

| Feld             | Typ                                                    | Beschreibung                                                                                                                                                                         |
| ---------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `api_version`    | `str`                                                  | Optionale Versionszeichenkette, standardmäßig `"1"`. 【F:src/open_ticket_ai/core/config/config_models.py†L18-L21】                                                                   |
| `plugins`        | `list[str]`                                            | Python-Module, die Plugin-Einstiegspunkte bereitstellen. Jedes Plugin trägt zusätzliche Injectables zur Registry bei. 【F:src/open_ticket_ai/core/config/config_models.py†L22-L25】  |
| `infrastructure` | [`InfrastructureConfig`](#infrastruktur-konfiguration) | Logging und andere Host-Level-Angelegenheiten. 【F:src/open_ticket_ai/core/config/config_models.py†L26-L29】                                                                         |
| `services`       | `dict[str, InjectableConfigBase]`                      | Map von Injectable-Service-Definitionen, die durch den Bezeichner referenziert werden, den Sie in Pipelines verwenden. 【F:src/open_ticket_ai/core/config/config_models.py†L30-L33】 |
| `orchestrator`   | [`PipeConfig`](#orchestrator-und-pipeconfig)           | Top-Level Pipe (typischerweise ein Orchestrator), die von der Runtime ausgeführt wird. 【F:src/open_ticket_ai/core/config/config_models.py†L34-L36】                                 |

### Infrastruktur-Konfiguration

`InfrastructureConfig` stellt derzeit Logging-Konfiguration bereit und verwendet standardmäßig das eingebaute Logging-Schema. 【F:
src/open_ticket_ai/core/config/config_models.py†L10-L14】

## Services-Dictionary (`open_ticket_ai.services`)

Alle Services teilen sich dasselbe Basisschema, da sie Instanzen von `InjectableConfigBase` sind. Jeder Eintrag befindet sich unter dem
`services`-Dictionary und verwendet den Dictionary-Schlüssel als seinen Bezeichner. 【F:
src/open_ticket_ai/core/config/config_models.py†L30-L43】

| Feld      | Typ              | Beschreibung                                                                                                                                                                                                 |
| --------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `use`     | `str`            | Registry-Bezeichner der zu instanziierenden Injectable-Implementierung. Standardwert ist `"otai_base:CompositePipe"`. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L9-L15】                  |
| `injects` | `dict[str, str]` | Optionale Zuordnung von Konstruktor-Parameternamen zu anderen Service-Bezeichnern. So verbinden Sie ein Injectable mit einem anderen. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L16-L20】 |
| `params`  | `dict[str, Any]` | Beliebige Konfiguration, die als Keyword-Argumente an das Parameter-Modell des Injectables übergeben wird. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L21-L25】                            |

Wenn die Runtime Services materialisiert, wird der Dictionary-Schlüssel in das Modell integriert, wodurch der Bezeichner für Dependency-Injection-Consumer verfügbar wird. 【F:src/open_ticket_ai/core/config/config_models.py†L39-L43】

### Wie Registry-Bezeichner aufgebaut werden

Plugins leiten Registry-Bezeichner von ihrem Modulnamen ab. Jedes Plugin beginnt mit dem Präfix `otai-`; die Runtime
entfernt dieses Präfix und verkettet den Rest mit dem Injectable-Klassennamen unter Verwendung von `:`. Beispielsweise trägt das `otai_base`
Plugin Bezeichner wie `base:CompositePipe` bei. 【F:src/open_ticket_ai/core/config/app_config.py†L16-L21】【F:
src/open_ticket_ai/core/plugins/plugin.py†L18-L46】

## Orchestrator und `PipeConfig`

Pipelines werden mit `PipeConfig` beschrieben, das dasselbe Basis-Injectable-Schema um ein `id`-Feld erweitert, zusätzliche Schlüssel verbietet
und alle Werte für konsistentes Hashing unveränderlich hält. 【F:
src/open_ticket_ai/core/pipes/pipe_models.py†L9-L15】 Jede Pipe gibt ein `PipeResult` zurück, das Erfolg, Überspringen, Fehler
und alle für nachfolgende Schritte erzeugten strukturierten Daten angibt. 【F:src/open_ticket_ai/core/pipes/pipe_models.py†L17-L68】

## Aktualisiertes Konfigurationsbeispiel

Der folgende Ausschnitt spiegelt die aktuelle `OpenTicketAIConfig`-Struktur wider: Services sind durch Bezeichner indiziert, und der
Orchestrator ist eine `PipeConfig`, die verschachtelte Pipes und Trigger rendert.

```yaml
open_ticket_ai:
  api_version: '1'
  plugins:
    - otai_base
    - otai_hf_local
    - otai_otobo_znuny

  infrastructure:
    logging:
      version: 1
      root:
        level: INFO

  services:
    ticketing:
      use: 'otobo-znuny:OTOBOZnunyTicketSystemService'
      params:
        base_url: '${OTOBO_BASE_URL}'
        username: '${OTOBO_USERNAME}'
        password: '${OTOBO_PASSWORD}'
    classifier:
      use: 'hf-local:HFClassificationService'
      params:
        api_token: '${HF_TOKEN}'
    renderer:
      use: 'base:JinjaRenderer'

  orchestrator:
    id: support-orchestrator
    use: 'base:SimpleSequentialOrchestrator'
    params:
      orchestrator_sleep: '0:00:05'
      exception_sleep: '0:01:00'
      steps:
        - id: ticket-runner
          use: 'base:SimpleSequentialRunner'
          params:
            on:
              id: every-minute
              use: 'base:IntervalTrigger'
              params:
                interval: '0:01:00'
            run:
              id: ticket-flow
              use: 'base:CompositePipe'
              params:
                steps:
                  - id: fetch
                    use: 'base:FetchTicketsPipe'
                    injects:
                      ticket_system: ticketing
                    params:
                      ticket_search_criteria:
                        queue:
                          id: Raw
                          name: Raw
                        limit: 1
                  - id: classify
                    use: 'base:ClassificationPipe'
                    injects:
                      classification_service: classifier
                    params:
                      text: "{{ get_pipe_result('fetch').data.fetched_tickets[0].body }}"
                      model_name: 'distilbert-base-uncased'
                  - id: respond
                    use: 'base:AddNotePipe'
                    injects:
                      ticket_system: ticketing
                    params:
                      ticket_id: "{{ get_pipe_result('fetch').data.fetched_tickets[0].id }}"
                      note:
                        subject: 'Classification result'
                        body: "{{ get_pipe_result('classify').data.label }}"
```

## Kern-Injectables

Die Tabelle fasst die Kern-Injectables zusammen, die mit den Standard-Plugins ausgeliefert werden. Folgen Sie den Links für Parameter- und Ausgabedetails.

| Bezeichner                                  | Plugin             | Art               | Zusammenfassung                                                                                                              |
| ------------------------------------------- | ------------------ | ----------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `base:JinjaRenderer`                        | `otai_base`        | Template-Renderer | Asynchroner Jinja-Renderer mit Helfern für den Zugriff auf Pipe-Ausgaben. [Details](#basejinjarenderer)                      |
| `base:SimpleSequentialOrchestrator`         | `otai_base`        | Orchestrator-Pipe | Durchläuft untergeordnete Pipes nach einem Zeitplan und wiederholt bei Fehlern. [Details](#basesimplesequentialorchestrator) |
| `base:SimpleSequentialRunner`               | `otai_base`        | Runner-Pipe       | Führt eine `run`-Pipe aus, wenn der `on`-Trigger erfolgreich ist. [Details](#basesimplesequentialrunner)                     |
| `base:CompositePipe`                        | `otai_base`        | Composite-Pipe    | Wertet verschachtelte Pipes sequentiell aus und fusioniert ihre Ergebnisse. [Details](#basecompositepipe)                    |
| `base:ExpressionPipe`                       | `otai_base`        | Utility-Pipe      | Gibt Literalwerte zurück oder schlägt fehl, wenn ein `FailMarker` erzeugt wird. [Details](#baseexpressionpipe)               |
| `base:ClassificationPipe`                   | `otai_base`        | AI-Pipe           | Delegiert an einen `ClassificationService` und gibt die Modellausgabe zurück. [Details](#baseclassificationpipe)             |
| `base:IntervalTrigger`                      | `otai_base`        | Trigger-Pipe      | Gibt Erfolg aus, wenn das konfigurierte Intervall abgelaufen ist. [Details](#baseintervaltrigger)                            |
| `base:FetchTicketsPipe`                     | `otai_base`        | Ticket-Pipe       | Lädt Tickets über einen injizierten `TicketSystemService`. [Details](#basefetchticketspipe)                                  |
| `base:UpdateTicketPipe`                     | `otai_base`        | Ticket-Pipe       | Wendet Aktualisierungen auf ein Ticket über den injizierten Ticket-Service an. [Details](#baseupdateticketpipe)              |
| `base:AddNotePipe`                          | `otai_base`        | Ticket-Pipe       | Fügt einem Ticket über den Ticket-Service eine Notiz hinzu. [Details](#baseaddnotepipe)                                      |
| `hf-local:HFClassificationService`          | `otai_hf_local`    | Service           | Hugging Face Text-Klassifikations-Client mit optionalem Auth-Token. [Details](#hf-localhfclassificationservice)              |
| `otobo-znuny:OTOBOZnunyTicketSystemService` | `otai_otobo_znuny` | Service           | Asynchroner Ticket-Service basierend auf der OTOBO/Znuny API. [Details](#otobo-znunyotoboznuny-ticketsystemservice)          |

### `base:JinjaRenderer`

- **Use**: `base:JinjaRenderer`
- **Params**: keine (Standardwert ist ein leeres `StrictBaseModel`). 【F:
  packages/otai_base/src/otai_base/template_renderers/jinja_renderer.py†L21-L38】
- **Verhalten**: Rendert Zeichenketten, Listen und Dictionaries asynchron mit Helfer-Globals wie `get_pipe_result` und
  `fail`. 【F:packages/otai_base/src/otai_base/template_renderers/jinja_renderer.py†L29-L38】

### `base:SimpleSequentialOrchestrator`

- **Use**: `base:SimpleSequentialOrchestrator`
- **Params**:
  - `orchestrator_sleep` (`timedelta`) – Wartezeit zwischen Zyklen. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
  - `exception_sleep` (`timedelta`) – Verzögerung vor Wiederholung nach einem Fehler. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
  - `always_retry` (`bool`) – Fehler erneut auslösen, wenn `false`. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
  - `steps` (`list[PipeConfig]`) – Verschachtelte Schritte, die mit voller Template-Unterstützung gerendert werden. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L27】
- **Ausgabe**: Läuft unendlich und gibt das aggregierte `PipeResult` aller Schritte pro Zyklus zurück. Fehler respektieren
  `always_retry`. 【F:packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L24-L40】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L36-L52】

### `base:SimpleSequentialRunner`

- **Use**: `base:SimpleSequentialRunner`
- **Params**:
  - `on` (`PipeConfig`) – Trigger-Pipe; der Runner überspringt die Ausführung, wenn sie fehlschlägt. 【F:
    packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L12-L36】
  - `run` (`PipeConfig`) – Pipe, die ausgeführt wird, wenn der Trigger erfolgreich ist. 【F:
    packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L12-L36】
- **Ausgabe**: Gibt das Ergebnis der nachgelagerten Pipe oder ein übersprungenes `PipeResult` mit einer Diagnosemeldung zurück. 【F:
  packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L26-L36】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L17-L64】

### `base:CompositePipe`

- **Use**: `base:CompositePipe`
- **Params**: `steps` – geordnete Liste von `PipeConfig`-Definitionen. Zusätzliche Schlüssel sind erlaubt, um benutzerdefinierte Composite-
  Implementierungen zu unterstützen. 【F:packages/otai_base/src/otai_base/pipes/composite_pipe.py†L11-L33】
- **Ausgabe**: Führt jeden Schritt in Reihenfolge aus, stoppt beim ersten Fehler und fusioniert Daten aller erfolgreichen Schritte mit
  `PipeResult.union`. 【F:packages/otai_base/src/otai_base/pipes/composite_pipe.py†L29-L47】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L36-L52】

### `base:ExpressionPipe`

- **Use**: `base:ExpressionPipe`
- **Params**: `expression` – Literalwert oder gerendertes Ausdrucksergebnis. 【F:
  packages/otai_base/src/otai_base/pipes/expression_pipe.py†L13-L18】
- **Ausgabe**: Gibt `PipeResult.success` mit `{"value": expression}` zurück, es sei denn, der Ausdruck ergibt einen
  `FailMarker`, in diesem Fall schlägt er fehl. 【F:packages/otai_base/src/otai_base/pipes/expression_pipe†L21-L38】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L59-L68】

### `base:ClassificationPipe`

- **Use**: `base:ClassificationPipe`
- **Injects**: `classification_service` muss auf eine `ClassificationService`-Implementierung zeigen.
- **Params**:
  - `text` (`str`) – zu klassifizierender Inhalt.
  - `model_name` (`str`) – Bezeichner, der an den Service weitergeleitet wird.
  - `api_token` (`str | None`) – Optionales Token, das den Service-Standard überschreibt. 【F:
    packages/otai_base/src/otai_base/pipes/classification_pipe.py†L19-L52】
- **Ausgabe**: Erfolgreiche Ergebnisse enthalten die vollständige `ClassificationResult`-Nutzlast (Label, Konfidenz, optionale Scores).
  【F:packages/otai_base/src/otai_base/pipes/classification_pipe.py†L54-L63】

### `base:IntervalTrigger`

- **Use**: `base:IntervalTrigger`
- **Params**: `interval` (`timedelta`) – Erforderliche verstrichene Zeit zwischen Erfolgen. 【F:
  packages/otai_base/src/otai_base/pipes/interval_trigger_pipe.py†L11-L28】
- **Ausgabe**: Gibt Erfolg zurück, sobald das Intervall seit dem vorherigen Lauf verstrichen ist; andernfalls gibt es ein Fehlerergebnis zurück,
  damit nachgelagerte Runner Arbeit überspringen können. 【F:packages/otai_base/src/otai_base/pipes/interval_trigger_pipe.py†L21-L30】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L17-L64】

### `base:FetchTicketsPipe`

- **Use**: `base:FetchTicketsPipe`
- **Injects**: `ticket_system` muss zu einer `TicketSystemService`-Implementierung aufgelöst werden. 【F:
  packages/otai_base/src/otai_base/ticket_system_integration/ticket_system_service.py†L1-L27】
- **Params**: `ticket_search_criteria`, die Warteschlange, Limit und andere Filter beschreibt. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/fetch_tickets_pipe.py†L11-L26】
- **Ausgabe**: Erfolgsergebnis mit `data.fetched_tickets`, das auf eine Liste von `UnifiedTicket`-Datensätzen gesetzt ist. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/fetch_tickets_pipe.py†L20-L26】

### `base:UpdateTicketPipe`

- **Use**: `base:UpdateTicketPipe`
- **Injects**: `ticket_system` (wie oben).
- **Params**:
  - `ticket_id` (`str | int`) – Ziel-Ticket-Bezeichner.
  - `updated_ticket` (`UnifiedTicket`) – Zu aktualisierende Felder. 【F:
    packages/otai_base/src/otai_base/pipes/ticket_system_pipes/update_ticket_pipe.py†L11-L28】
- **Ausgabe**: Gibt Erfolg zurück, wenn der Ticket-Service die Aktualisierung bestätigt. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/update_ticket_pipe.py†L21-L31】

### `base:AddNotePipe`

- **Use**: `base:AddNotePipe`
- **Injects**: `ticket_system`.
- **Params**:
  - `ticket_id` (`str | int`) – Ticket, das die Notiz erhält.
  - `note` (`UnifiedNote`) – Subject/Body-Nutzlast. 【F:
    packages/otai_base/src/otai_base/pipes/ticket_system_pipes/add_note_pipe.py†L13-L40】
- **Ausgabe**: Gibt Erfolg zurück, nachdem die Anhängung der Notiz an den Ticket-Service delegiert wurde. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/add_note_pipe.py†L27-L40】

### `hf-local:HFClassificationService`

- **Use**: `hf-local:HFClassificationService`
- **Params**: `api_token` (`str | None`) – Standard-Hugging Face-Token, der verwendet wird, wenn Anfragen keinen Token angeben. 【F:
  packages/otai_hf_local/src/otai_hf_local/hf_classification_service.py†L105-L158】
- **Verhalten**: Lädt und cached einen Hugging Face Transformers-Pipeline verzögert, loggt sich ein, wenn ein Token bereitgestellt wird, und
  stellt synchrone/asynchrone Klassifikations-Helfer bereit. 【F:
  packages/otai_hf_local/src/otai_hf_local/hf_classification_service.py†L34-L163】

### `otobo-znuny:OTOBOZnunyTicketSystemService`

- **Use**: `otobo-znuny:OTOBOZnunyTicketSystemService`
- **Params** (`RenderedOTOBOZnunyTSServiceParams`):
  - `base_url` – OTOBO/Znuny Endpunkt-Basis-URL.
  - `username` / `password` – Anmeldedaten für den konfigurierten Web-Service.
  - `webservice_name` – Optionaler Service-Name-Override (Standardwert ist `OpenTicketAI`).
  - `operation_urls` – Zuordnung von Ticket-Operationen zu relativen API-Pfaden. 【F:
    packages/otai_otobo_znuny/src/otai_otobo_znuny/models.py†L44-L76】
- **Verhalten**: Erstellt und loggt einen `OTOBOZnunyClient` ein und implementiert dann die `TicketSystemService`-Schnittstelle für
  Suchen, Abrufen, Aktualisieren und Kommentieren von Tickets. 【F:
  packages/otai_otobo_znuny/src/otai_otobo_znuny/oto_znuny_ts_service.py†L21-L135】
