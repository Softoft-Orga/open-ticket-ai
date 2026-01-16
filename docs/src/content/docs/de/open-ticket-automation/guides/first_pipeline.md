---
title: First Pipeline Tutorial
description: 'Erstellen Sie Ihre erste Open Ticket AI Pipeline von Anfang bis Ende mit Orchestrierung und Klassifizierung.'
lang: de
nav:
  group: Guides
  order: 2
---

# Erstellen Ihrer ersten Pipeline

Diese Anleitung führt Sie durch den Aufbau einer funktionierenden Ticket-Klassifizierungs-Pipeline auf Basis des aktuellen Open Ticket AI Konfigurationsschemas. Sie lernen, wie Plugin-Module geladen werden, wie Services über ihre Kennung registriert werden und wie der Orchestrator vollständig aus verschachtelten `PipeConfig`-Definitionen zusammengesetzt wird.

## Konfigurationsbausteine

Die gesamte Konfiguration befindet sich unter dem Top-Level-Schlüssel `open_ticket_ai`. Jedes darunterliegende Objekt wird von Pydantic-Modellen validiert, bevor der Orchestrator startet, daher ist die Einhaltung des Schemas entscheidend.

### Plugin-Module (`open_ticket_ai.plugins`)

Plugins werden über ihren Modulnamen (Entry Point) aktiviert. Listen Sie jedes Plugin, das Sie laden möchten, als String auf. Mindestens benötigen Sie das Core-Plugin `otai-base`, um Zugriff auf die integrierten Runner, Orchestratoren und Utility-Pipes zu erhalten.

### Service-Registry (`open_ticket_ai.services`)

Services werden in einem Dictionary definiert, das durch ihre Kennung indiziert ist. Jeder Service beschreibt die zu instanziierende Implementierung via `use`, optionale Konstruktor-Abhängigkeiten via `injects` und Konfigurationsdaten via `params`. Services werden zu injizierbaren Abhängigkeiten für Pipes und andere Services. Open Ticket AI erwartet genau einen `TemplateRenderer`-Service; das folgende Beispiel registriert den Standard-Jinja-Renderer.

### Orchestrator (`open_ticket_ai.orchestrator`)

Der Orchestrator selbst ist eine `PipeConfig`. Sie wählen eine Orchestrator-Implementierung via `use` (z.B. `base:SimpleSequentialOrchestrator`) und konfigurieren sie via `params`. Im sequenziellen Orchestrator ist `params.steps` eine Liste verschachtelter `PipeConfig`-Objekte. Jeder Schritt kann eine beliebige Pipe sein – einschließlich Runner wie `SimpleSequentialRunner`, anderer Orchestratoren oder konkreter Business-Logic-Pipes.

Die folgende minimale Konfiguration zeigt die Struktur und validiert gegen das aktuelle Schema:

```yaml
open_ticket_ai:
  api_version: '1'
  plugins:
    - otai-base
  services:
    default_renderer:
      use: 'base:JinjaRenderer'
  orchestrator:
    id: orchestrator
    use: 'base:SimpleSequentialOrchestrator'
    params:
      steps: []
```

## Aufbau einer minimalen Ticket-Routing-Pipeline

Wir werden das obige Skelett zu einer lauffähigen Pipeline erweitern, die Tickets von OTOBO/Znuny abruft, die Queue mit einem Hugging Face-Modell klassifiziert, das Ticket aktualisiert und eine Notiz speichert. Jeder Abschnitt erklärt, wie die Konfiguration auf konkrete Klassen im Codebase abgebildet wird.

### Schritt 1: Plugin-Module und Template-Renderer deklarieren

Fügen Sie die Plugins hinzu, die die benötigten Injectables bereitstellen:

- `otai-base` – Core-Orchestratoren (`SimpleSequentialOrchestrator`), Runner (`SimpleSequentialRunner`), Pipes (`CompositePipe`, `FetchTicketsPipe`, `UpdateTicketPipe`, `AddNotePipe`, `ExpressionPipe`), Trigger (`IntervalTrigger`) und der Standard-`JinjaRenderer`.
- `otai-otobo-znuny` – Ticket-System-Integrationsservice (`OTOBOZnunyTicketSystemService`).
- `otai-hf-local` – On-Device-Hugging-Face-Klassifizierungsservice (`HFClassificationService`).

Behalten Sie den `default_renderer`-Service registriert, damit das Template-Rendering verfügbar ist, bevor andere Services instanziiert werden.

### Schritt 2: Externe Services verbinden

Definieren Sie Services, die durch ihre ID indiziert sind:

- `default_renderer` instanziiert `base:JinjaRenderer` und erfüllt die Anforderung, dass genau ein `TemplateRenderer` existiert.
- `otobo_znuny` verweist auf `otobo-znuny:OTOBOZnunyTicketSystemService` und übergibt Verbindungsdaten innerhalb von `params`.
- `hf_classifier` wird aufgelöst zu `hf-local:HFClassificationService` mit einem optionalen API-Token.

Diese IDs (z.B. `otobo_znuny` und `hf_classifier`) werden später aus den `injects`-Abschnitten der Pipes referenziert.

### Schritt 3: Orchestrator und Runner konfigurieren

Verwenden Sie `base:SimpleSequentialOrchestrator` für eine kontinuierlich laufende Event-Schleife. Sein `params.orchestrator_sleep` steuert die Leerlaufzeit zwischen den Zyklen. Innerhalb von `params.steps` fügen Sie einen einzelnen `SimpleSequentialRunner` hinzu. Dieser Runner erwartet zwei verschachtelte `PipeConfig`-Definitionen unter `params`:

- `on` – eine Trigger-Pipe; wir verwenden `base:IntervalTrigger` mit einem `timedelta`-Intervall (`PT60S` läuft einmal pro Minute).
- `run` – die Pipeline, die ausgeführt wird, wenn der Trigger erfolgreich ist. Hier referenzieren wir `base:CompositePipe`, die ihre eigenen `params.steps` sequenziell verarbeitet.

### Schritt 4: Die zusammengesetzten Pipeline-Schritte definieren

Innerhalb der Composite-Pipe ist jedes Element in `params.steps` eine weitere `PipeConfig`, die 1:1 auf eine Pipe-Klasse abgebildet wird:

1. **`fetch_open_tickets`** (`base:FetchTicketsPipe`) injiziert den Ticket-System-Service und lädt eingehende Tickets via `ticket_search_criteria`.
2. **`ensure_tickets_found`** (`base:ExpressionPipe`) ruft `fail()` auf, wenn keine Tickets gefunden wurden, und stoppt den Runner ordnungsgemäß.
3. **`queue_classifier`** (`base:ClassificationPipe`) injiziert den Hugging-Face-Service und klassifiziert den Ticket-Text.
4. **`update_queue`** (`base:UpdateTicketPipe`) schreibt die neue Queue-Auswahl zurück zu OTOBO/Znuny.
5. **`add_classification_note`** (`base:AddNotePipe`) erstellt einen Audit-Trail der automatisierten Klassifizierung.

Alle Parameter referenzieren frühere Ergebnisse mithilfe von Hilfsfunktionen, die vom Jinja-Renderer bereitgestellt werden (`get_pipe_result`, `fail`, `get_env`, etc.).

### Vollständige Konfiguration

Speichern Sie die folgende validierte Konfiguration als `config.yml` in Ihrem Arbeitsverzeichnis. Sie kombiniert alle oben beschriebenen Schritte und entspricht exakt dem aktuellen Schema.

```yaml
open_ticket_ai:
  api_version: '1'
  plugins:
    - otai-base
    - otai-otobo-znuny
    - otai-hf-local
  services:
    default_renderer:
      use: 'base:JinjaRenderer'
    otobo_znuny:
      use: 'otobo-znuny:OTOBOZnunyTicketSystemService'
      params:
        base_url: 'https://helpdesk.example.com/otobo/nph-genericinterface.pl'
        username: 'open_ticket_ai'
        password: "{{ get_env('OTOBO_API_TOKEN') }}"
    hf_classifier:
      use: 'hf-local:HFClassificationService'
      params:
        api_token: "{{ get_env('HF_TOKEN') }}"
  orchestrator:
    id: ticket-automation
    use: 'base:SimpleSequentialOrchestrator'
    params:
      orchestrator_sleep: 'PT60S'
      steps:
        - id: ticket-routing-runner
          use: 'base:SimpleSequentialRunner'
          params:
            on:
              id: every-minute
              use: 'base:IntervalTrigger'
              params:
                interval: 'PT60S'
            run:
              id: ticket-routing
              use: 'base:CompositePipe'
              params:
                steps:
                  - id: fetch_open_tickets
                    use: 'base:FetchTicketsPipe'
                    injects:
                      ticket_system: 'otobo_znuny'
                    params:
                      ticket_search_criteria:
                        queue:
                          name: 'OpenTicketAI::Incoming'
                        limit: 25
                  - id: ensure_tickets_found
                    use: 'base:ExpressionPipe'
                    params:
                      expression: "{{ fail('No open tickets found') if (get_pipe_result('fetch_open_tickets','fetched_tickets') | length) == 0 else 'tickets ready' }}"
                  - id: queue_classifier
                    use: 'base:ClassificationPipe'
                    injects:
                      classification_service: 'hf_classifier'
                    params:
                      text: "{{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['subject'] }} {{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['body'] }}"
                      model_name: 'softoft/otai-queue-de-bert-v1'
                  - id: update_queue
                    use: 'base:UpdateTicketPipe'
                    injects:
                      ticket_system: 'otobo_znuny'
                    params:
                      ticket_id: "{{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['id'] }}"
                      updated_ticket:
                        queue:
                          name: "{{ get_pipe_result('queue_classifier','label') }}"
                  - id: add_classification_note
                    use: 'base:AddNotePipe'
                    injects:
                      ticket_system: 'otobo_znuny'
                    params:
                      ticket_id: "{{ get_pipe_result('fetch_open_tickets','fetched_tickets')[0]['id'] }}"
                      note:
                        subject: 'Queue classification'
                        body: |
                          Auto-classified queue: {{ get_pipe_result('queue_classifier','label') }}
                          Confidence: {{ (get_pipe_result('queue_classifier','confidence') * 100) | round(1) }}%
```

## Ausführen und Überprüfen der Pipeline

1. Installieren Sie die erforderlichen Pakete (Core plus die oben aufgeführten Plugins).
2. Stellen Sie die in der Konfiguration referenzierten Anmeldedaten über Umgebungsvariablen bereit (z.B. `OTOBO_API_TOKEN`, `HF_TOKEN`).
3. Platzieren Sie die Konfigurationsdatei als `config.yml` in Ihrem Arbeitsverzeichnis, damit `AppConfig` sie automatisch erkennt.
4. Starten Sie den Orchestrator:

   ```bash
   uv run python -m open_ticket_ai.main
   ```

`AppConfig` validiert die YAML beim Start gegen das Schema. Wenn ein Abschnitt fehlt oder ein Parametername falsch ist, beendet sich die Anwendung mit einer beschreibenden Validierungsfehlermeldung, bevor Tickets verarbeitet werden. Sobald die Pipeline läuft, führt der Orchestrator den `SimpleSequentialRunner` jede Minute aus, wendet die verschachtelten `CompositePipe`-Schritte an und protokolliert den Fortschritt über die konfigurierten Services.