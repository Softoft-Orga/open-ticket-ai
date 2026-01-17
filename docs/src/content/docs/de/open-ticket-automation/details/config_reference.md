---
title: Konfigurationsreferenz
lang: en
nav:
  group: Details
  order: 1
---

# Konfigurationsreferenz

Open Ticket AI lädt seine YAML-Konfiguration in das `OpenTicketAIConfig`‑Modell. Das Schema ist um ein einzelnes `open_ticket_ai`‑Objekt herum aufgebaut, das API/Versions‑Metadaten, Infrastruktur‑Einstellungen, dependency‑inject‑ed Services und die Definition des Pipeline‑Orchestrators enthält. 【F:src/open_ticket_ai/core/config/config_models.py†L17-L37】

## Grundstruktur der Konfiguration

| Feld            | Typ                                             | Beschreibung                                                                                                                                                                   |
| ---------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api_version`    | `str`                                            | Optionale Versionszeichenkette, die standardmäßig auf `"1"` gesetzt ist. 【F:src/open_ticket_ai/core/config/config_models.py†L18-L21】                                                                 |
| `plugins`        | `list[str]`                                      | Python‑Module, die Plugin‑Entry‑Points bereitstellen. Jeder Plugin trägt zusätzliche Injectables zum Registry bei. 【F:src/open_ticket_ai/core/config/config_models.py†L22-L25】 |
| `infrastructure` | [`InfrastructureConfig`](#infrastructure-config) | Logging und andere host‑bezogene Anliegen. 【F:src/open_ticket_ai/core/config/config_models.py†L26-L29】                                                                          |
| `services`       | `dict[str, InjectableConfigBase]`                | Abbildung von injectable Service‑Definitionen, indiziert durch den Bezeichner, den Sie in Pipelines referenzieren. 【F:src/open_ticket_ai/core/config/config_models.py†L30-L33】                  |
| `orchestrator`   | [`PipeConfig`](#orchestrator-and-pipeconfig)     | Top‑Level‑Pipe (typischerweise ein Orchestrator), die zur Laufzeit ausgeführt wird. 【F:src/open_ticket_ai/core/config/config_models.py†L34-L36】                                             |

### Infrastruktur‑Konfiguration

`InfrastructureConfig` stellt derzeit die Logging‑Konfiguration bereit und verwendet standardmäßig das integrierte Logging‑Schema. 【F:
src/open_ticket_ai/core/config/config_models.py†L10-L14】

## Service‑Wörterbuch (`open_ticket_ai.services`)

Alle Services teilen dasselbe Basisschema, da sie Instanzen von `InjectableConfigBase` sind. Jeder Eintrag befindet sich im `services`‑Wörterbuch und verwendet den Schlüssel des Wörterbuchs als Bezeichner. 【F:
src/open_ticket_ai/core/config/config_models.py†L30-L43】

| Feld     | Typ             | Beschreibung                                                                                                                                                                                               |
| --------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `use`     | `str`            | Registry‑Bezeichner der zu instanziierenden injectable Implementierung. Standardwert ist `"otai_base:CompositePipe"`. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L9-L15】                       |
| `injects` | `dict[str, str]` | Optionale Zuordnung von Konstruktor‑Parameter‑Namen zu anderen Service‑Bezeichnern. So verbinden Sie ein injectable mit einem anderen. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L16-L20】 |
| `params`  | `dict[str, Any]` | Beliebige Konfiguration, die als Schlüsselwort‑Argumente an das Parameter‑Modell des injectables übergeben wird. 【F:src/open_ticket_ai/core/injectables/injectable_models.py†L21-L25】                                           |

Wenn die Laufzeit Services materialisiert, wird der Wörterbuch‑Schlüssel in das Modell eingefügt, wodurch der Bezeichner für dependency‑Injection‑Verbraucher verfügbar wird. 【F:src/open_ticket_ai/core/config/config_models.py†L39-L43】

### Wie Registry‑Bezeichner erstellt werden

Plugins leiten Registry‑Bezeichner aus ihrem Modulnamen ab. Jeder Plugin beginnt mit dem Präfix `otai-`; die Laufzeit entfernt dieses Präfix und verkettet den Rest mit dem Namen der injectable Klasse mittels `:`. Zum Beispiel liefert das `otai_base`‑Plugin Bezeichner wie `base:CompositePipe`. 【F:src/open_ticket_ai/core/config/app_config.py†L16-L21】【F:
src/open_ticket_ai/core/plugins/plugin.py†L18-L46】

## Orchestrator und `PipeConfig`

Pipelines werden mit `PipeConfig` beschrieben, das das gleiche Basis‑injectable‑Schema um ein `id`‑Feld erweitert, zusätzliche Schlüssel verbietet und alle Werte unveränderlich hält, um konsistentes Hashing zu gewährleisten. 【F:
src/open_ticket_ai/core/pipes/pipe_models.py†L9-L15】 Jede Pipe gibt ein `PipeResult` zurück, das Erfolg, Überspringen, Fehler und jegliche strukturierte Daten, die für nachgelagerte Schritte erzeugt wurden, anzeigt. 【F:src/open_ticket_ai/core/pipes/pipe_models.py†L17-L68】

## Aktualisiertes Konfigurationsbeispiel

Das nachstehende Snippet spiegelt die aktuelle `OpenTicketAIConfig`‑Struktur wider: Services werden durch Bezeichner indiziert, und der Orchestrator ist ein `PipeConfig`, das verschachtelte Pipes rendert und Trigger auslöst.

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

## Kern‑Injectables

Die Tabelle fasst die Kern‑Injectables zusammen, die mit den Standard‑Plugins ausgeliefert werden. Folgen Sie den Links für Parameter‑ und Ausgabedetails.

| Bezeichner                                  | Plugin             | Typ               | Zusammenfassung                                                                                                 |
| ------------------------------------------- | ------------------ | ----------------- | --------------------------------------------------------------------------------------------------------------- |
| `base:JinjaRenderer`                        | `otai_base`        | Template renderer | Asynchroner Jinja‑Renderer mit Hilfsfunktionen zum Zugriff auf Pipe‑Ausgaben. [Details](#basejinjarenderer)    |
| `base:SimpleSequentialOrchestrator`         | `otai_base`        | Orchestrator pipe | Durchläuft Kind‑Pipes nach einem Zeitplan und wiederholt bei Fehlern. [Details](#basesimplesequentialorchestrator) |
| `base:SimpleSequentialRunner`               | `otai_base`        | Runner pipe       | Führt eine `run`‑Pipe aus, wenn der `on`‑Trigger erfolgreich ist. [Details](#basesimplesequentialrunner)          |
| `base:CompositePipe`                        | `otai_base`        | Composite pipe    | Evaluert verschachtelte Pipes sequenziell und kombiniert deren Ergebnisse. [Details](#basecompositepipe)          |
| `base:ExpressionPipe`                       | `otai_base`        | Utility pipe      | Gibt Literalwerte zurück oder schlägt fehl, wenn ein `FailMarker` erzeugt wird. [Details](#baseexpressionpipe)       |
| `base:ClassificationPipe`                   | `otai_base`        | AI pipe           | Delegiert an einen `ClassificationService` und gibt die Modellausgabe zurück. [Details](#baseclassificationpipe)   |
| `base:IntervalTrigger`                      | `otai_base`        | Trigger pipe      | Gibt Erfolg aus, wenn das konfigurierte Intervall verstrichen ist. [Details](#baseintervaltrigger)                 |
| `base:FetchTicketsPipe`                     | `otai_base`        | Ticket pipe       | Lädt Tickets über einen injizierten `TicketSystemService`. [Details](#basefetchticketspipe)                       |
| `base:UpdateTicketPipe`                     | `otai_base`        | Ticket pipe       | Wendet Aktualisierungen auf ein Ticket über den injizierten Ticket‑Service an. [Details](#baseupdateticketpipe)     |
| `base:AddNotePipe`                          | `otai_base`        | Ticket pipe       | Fügt einem Ticket eine Notiz über den Ticket‑Service hinzu. [Details](#baseaddnotepipe)                            |
| `hf-local:HFClassificationService`          | `otai_hf_local`    | Service           | Hugging‑Face‑Text‑Klassifikations‑Client mit optionalem Auth‑Token. [Details](#hf-localhfclassificationservice)      |
| `otobo-znuny:OTOBOZnunyTicketSystemService` | `otai_otobo_znuny` | Service           | Asynchroner Ticket‑Service, unterstützt durch die OTOBO/Znuny‑API. [Details](#otobo-znunyotoboznuny-ticketsystemservice) |

### `base:JinjaRenderer`

- **Verwendung**: `base:JinjaRenderer`
- **Parameter**: keine (standardmäßig ein leeres `StrictBaseModel`). 【F:
  packages/otai_base/src/otai_base/template_renderers/jinja_renderer.py†L21-L38】
- **Verhalten**: Rendert Zeichenketten, Listen und Dictionaries asynchron mit Hilfs‑Globals wie `get_pipe_result` und `fail`. 【F:packages/otai_base/src/otai_base/template_renderers/jinja_renderer.py†L29-L38】

### `base:SimpleSequentialOrchestrator`

- **Verwendung**: `base:SimpleSequentialOrchestrator`
- **Parameter**:
  - `orchestrator_sleep` (`timedelta`) – Wartezeit zwischen Zyklen. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
  - `exception_sleep` (`timedelta`) – Verzögerung vor einem erneuten Versuch nach einem Fehler. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
  - `always_retry` (`bool`) – Bei `false` wird bei einem Fehler erneut geworfen. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L18】
  - `steps` (`list[PipeConfig]`) – Verschachtelte Schritte, die mit voller Template‑Unterstützung gerendert werden. 【F:
    packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L14-L27】
- **Ausgabe**: Läuft unendlich und gibt das aggregierte `PipeResult` aller Schritte pro Zyklus zurück. Fehler respektieren `always_retry`. 【F:packages/otai_base/src/otai_base/pipes/orchestrators/simple_sequential_orchestrator.py†L24-L40】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L36-L52】

### `base:SimpleSequentialRunner`

- **Verwendung**: `base:SimpleSequentialRunner`
- **Parameter**:
  - `on` (`PipeConfig`) – Trigger‑Pipe; der Runner überspringt die Ausführung, wenn sie fehlschlägt. 【F:
    packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L12-L36】
  - `run` (`PipeConfig`) – Pipe, die ausgeführt wird, wenn der Trigger erfolgreich ist. 【F:
    packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L12-L36】
- **Ausgabe**: Gibt das nachgelagerte Pipe‑Ergebnis oder ein übersprungenes `PipeResult` mit einer Diagnose‑Nachricht zurück. 【F:
  packages/otai_base/src/otai_base/pipes/pipe_runners/simple_sequential_runner.py†L26-L36】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L17-L64】

### `base:CompositePipe`

- **Verwendung**: `base:CompositePipe`
- **Parameter**: `steps` – geordnete Liste von `PipeConfig`‑Definitionen. Zusätzliche Schlüssel sind erlaubt, um benutzerdefinierte Composite‑Implementierungen zu unterstützen. 【F:packages/otai_base/src/otai_base/pipes/composite_pipe.py†L11-L33】
- **Ausgabe**: Führt jeden Schritt in Reihenfolge aus, stoppt beim ersten Fehler und kombiniert Daten aller erfolgreichen Schritte mit `PipeResult.union`. 【F:packages/otai_base/src/otai_base/pipes/composite_pipe.py†L29-L47】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L36-L52】

### `base:ExpressionPipe`

- **Verwendung**: `base:ExpressionPipe`
- **Parameter**: `expression` – Literalwert oder gerendertes Ausdrucksergebnis. 【F:
  packages/otai_base/src/otai_base/pipes/expression_pipe.py†L13-L18】
- **Ausgabe**: Gibt `PipeResult.success` mit `{"value": expression}` zurück, es sei denn, der Ausdruck evaluiert zu einem `FailMarker`, dann schlägt er fehl. 【F:packages/otai_base/src/otai_base/pipes/expression_pipe†L21-L38】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L59-L68】

### `base:ClassificationPipe`

- **Verwendung**: `base:ClassificationPipe`
- **Injects**: `classification_service` muss auf eine `ClassificationService`‑Implementierung zeigen.
- **Parameter**:
  - `text` (`str`) – Inhalt, der klassifiziert werden soll.
  - `model_name` (`str`) – Bezeichner, der an den Service weitergeleitet wird.
  - `api_token` (`str | None`) – Optionales Token, das den Standard‑Token des Services überschreibt. 【F:
    packages/otai_base/src/otai_base/pipes/classification_pipe.py†L19-L52】
- **Ausgabe**: Erfolgreiche Ergebnisse enthalten die vollständige `ClassificationResult`‑Payload (Label, Confidence, optionale Scores). 【F:packages/otai_base/src/otai_base/pipes/classification_pipe.py†L54-L63】

### `base:IntervalTrigger`

- **Verwendung**: `base:IntervalTrigger`
- **Parameter**: `interval` (`timedelta`) – erforderliche verstrichene Zeit zwischen Erfolgen. 【F:
  packages/otai_base/src/otai_base/pipes/interval_trigger_pipe.py†L11-L28】
- **Ausgabe**: Gibt Erfolg zurück, sobald das Intervall seit dem vorherigen Lauf verstrichen ist; andernfalls wird ein Fehlerschluss zurückgegeben, sodass nachgelagerte Runner die Arbeit überspringen können. 【F:packages/otai_base/src/otai_base/pipes/interval_trigger_pipe.py†L21-L30】【F:
  src/open_ticket_ai/core/pipes/pipe_models.py†L17-L64】

### `base:FetchTicketsPipe`

- **Verwendung**: `base:FetchTicketsPipe`
- **Injects**: `ticket_system` muss zu einer `TicketSystemService`‑Implementierung aufgelöst werden. 【F:
  packages/otai_base/src/otai_base/ticket_system_integration/ticket_system_service.py†L1-L27】
- **Parameter**: `ticket_search_criteria` beschreibt Queue, Limit und weitere Filter. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/fetch_tickets_pipe.py†L11-L26】
- **Ausgabe**: Erfolgsresultat mit `data.fetched_tickets`, das auf eine Liste von `UnifiedTicket`‑Datensätzen gesetzt ist. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/fetch_tickets_pipe.py†L20-L26】

### `base:UpdateTicketPipe`

- **Verwendung**: `base:UpdateTicketPipe`
- **Injects**: `ticket_system` (wie oben).
- **Parameter**:
  - `ticket_id` (`str | int`) – Ziel‑Ticket‑Bezeichner.
  - `updated_ticket` (`UnifiedTicket`) – Felder, die aktualisiert werden sollen. 【F:
    packages/otai_base/src/otai_base/pipes/ticket_system_pipes/update_ticket_pipe.py†L11-L28】
- **Ausgabe**: Gibt Erfolg zurück, wenn der Ticket‑Service die Aktualisierung bestätigt. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/update_ticket_pipe.py†L21-L31】

### `base:AddNotePipe`

- **Verwendung**: `base:AddNotePipe`
- **Injects**: `ticket_system`.
- **Parameter**:
  - `ticket_id` (`str | int`) – Ticket, das die Notiz erhält.
  - `note` (`UnifiedNote`) – Betreff/Body‑Payload. 【F:
    packages/otai_base/src/otai_base/pipes/ticket_system_pipes/add_note_pipe.py†L13-L40】
- **Ausgabe**: Gibt Erfolg zurück, nachdem der Ticket‑Service die Notiz angehängt hat. 【F:
  packages/otai_base/src/otai_base/pipes/ticket_system_pipes/add_note_pipe.py†L27-L40】

### `hf-local:HFClassificationService`

- **Verwendung**: `hf-local:HFClassificationService`
- **Parameter**: `api_token` (`str | None`) – Standard‑Hugging‑Face‑Token, das verwendet wird, wenn Anfragen kein Token enthalten. 【F:
  packages/otai_hf_local/src/otai_hf_local/hf_classification_service.py†L105-L158】
- **Verhalten**: Lädt lazily und cached eine Hugging‑Face‑Transformers‑Pipeline, loggt ein, wenn ein Token bereitgestellt wird, und stellt synchrone/asynchrone Klassifikations‑Hilfsfunktionen bereit. 【F:
  packages/otai_hf_local/src/otai_hf_local/hf_classification_service.py†L34-L163】

### `otobo-znuny:OTOBOZnunyTicketSystemService`

- **Verwendung**: `otobo-znuny:OTOBOZnunyTicketSystemService`
- **Parameter** (`RenderedOTOBOZnunyTSServiceParams`):
  - `base_url` – Basis‑URL des OTOBO/Znuny‑Endpoints.
  - `username` / `password` – Anmeldedaten für den konfigurierten Webservice.
  - `webservice_name` – optionaler Service‑Name‑Überschreibung (standardmäßig `OpenTicketAI`).
  - `operation_urls` – Zuordnung von Ticket‑Operationen zu relativen API‑Pfaden. 【F:
    packages/otai_otobo_znuny/src/otai_otobo_znuny/models.py†L44-L76】
- **Verhalten**: Erstellt und loggt einen `OTOBOZnunyClient` ein, implementiert anschließend das `TicketSystemService`‑Interface für das Suchen, Abrufen, Aktualisieren und Annotieren von Tickets. 【F:
  packages/otai_otobo_znuny/src/otai_otobo_znuny/oto_znuny_ts_service.py†L21-L135】