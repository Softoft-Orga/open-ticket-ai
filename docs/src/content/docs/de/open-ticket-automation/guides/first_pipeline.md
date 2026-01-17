---
title: Erste Pipeline-Anleitung
description: 'Erstellen Sie Ihre erste Open Ticket AI Pipeline End-to-End mit Orchestrierung und Klassifizierung.'
lang: en
nav:
  group: Guides
  order: 2
---

# Erstellen Ihrer ersten Pipeline

Dieser Leitfaden führt Sie durch den Aufbau einer funktionierenden Ticket‑Klassifizierungs‑Pipeline auf Basis des neuesten Open Ticket AI Konfigurationsschemas. Sie lernen, wie Plugin‑Module geladen werden, wie Services anhand ihrer Kennung registriert werden und wie der Orchestrator vollständig aus verschachtelten `PipeConfig`‑Definitionen zusammengesetzt ist.

## Bausteine der Konfiguration

Alle Konfigurationen befinden sich unter dem Top‑Level‑Schlüssel `open_ticket_ai`. Jedes darunterliegende Objekt wird von Pydantic‑Modellen validiert, bevor der Orchestrator startet, daher ist die Übereinstimmung mit dem Schema essenziell.

### Plugin‑Module (`open_ticket_ai.plugins`)

Plugins werden über den Modul‑ (Entry‑Point‑) Namen aktiviert. Listen Sie jedes Plugin, das Sie laden möchten, als Zeichenkette auf. Mindestens benötigen Sie das Kern‑Plugin `otai-base`, um auf die integrierten Runner, Orchestratoren und Hilfs‑Pipes zuzugreifen.

### Service‑Register (`open_ticket_ai.services`)

Services werden in einem Wörterbuch definiert, das durch ihre Kennung indiziert ist. Jeder Service beschreibt die zu instanzierenden Implementierung über `use`, optionale Konstruktor‑Abhängigkeiten über `injects` und Konfigurationsdaten über `params`. Services werden zu injizierbaren Abhängigkeiten für Pipes und andere Services. Open Ticket AI erwartet exakt einen `TemplateRenderer`‑Service; das nachfolgende Beispiel registriert den Standard‑Jinja‑Renderer.

### Orchestrator (`open_ticket_ai.orchestrator`)

Der Orchestrator selbst ist ein `PipeConfig`. Sie wählen eine Orchestrator‑Implementierung über `use` (z. B. `base:SimpleSequentialOrchestrator`) und konfigurieren ihn über `params`. Im sequentiellen Orchestrator ist `params.steps` eine Liste verschachtelter `PipeConfig`‑Objekte. Jeder Schritt kann jede Pipe sein – einschließlich Runner wie `SimpleSequentialRunner`, andere Orchestratoren oder konkrete Business‑Logic‑Pipes.

Die folgende minimale Konfiguration verdeutlicht die Struktur und validiert gegen das aktuelle Schema:

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

## Erstellen einer minimalen Ticket‑Routing‑Pipeline

Wir erweitern das obige Gerüst zu einer ausführbaren Pipeline, die Tickets von OTOBO/Znuny abruft, die Queue mithilfe eines Hugging‑Face‑Modells klassifiziert, das Ticket aktualisiert und eine Notiz speichert. Jeder Abschnitt erklärt, wie die Konfiguration auf konkrete Klassen im Code‑Base abgebildet wird.

### Schritt 1: Plugin‑Module und Template‑Renderer deklarieren

Fügen Sie die Plugins hinzu, die die benötigten injizierbaren Komponenten bereitstellen:

- `otai-base` – Kern‑Orchestratoren (`SimpleSequentialOrchestrator`), Runner (`SimpleSequentialRunner`), Pipes (`CompositePipe`, `FetchTicketsPipe`, `UpdateTicketPipe`, `AddNotePipe`, `ExpressionPipe`), Trigger (`IntervalTrigger`) und der Standard‑`JinjaRenderer`.
- `otai-otobo-znuny` – Ticket‑System‑Integrations‑Service (`OTOBOZnunyTicketSystemService`).
- `otai-hf-local` – On‑Device‑Hugging‑Face‑Klassifizierungs‑Service (`HFClassificationService`).

Behalten Sie den Service `default_renderer` registriert, damit das Template‑Rendering verfügbar ist, bevor ein anderer Service instanziiert wird.

### Schritt 2: Externe Services verbinden

Definieren Sie Services, die durch eine ID indiziert sind:

- `default_renderer` instanziiert `base:JinjaRenderer` und erfüllt die Anforderung, dass exakt ein `TemplateRenderer` existiert.
- `otobo_znuny` verweist auf `otobo-znuny:OTOBOZnunyTicketSystemService` und übergibt Verbindungs‑Credentials innerhalb von `params`.
- `hf_classifier` löst zu `hf-local:HFClassificationService` mit einem optionalen API‑Token auf.

Diese IDs (z. B. `otobo_znuny` und `hf_classifier`) werden später in den `injects`‑Abschnitten von Pipes referenziert.

### Schritt 3: Orchestrator und Runner konfigurieren

Verwenden Sie `base:SimpleSequentialOrchestrator` für eine kontinuierlich laufende Ereignisschleife. Sein `params.orchestrator_sleep` steuert die Leerlaufzeit zwischen den Zyklen. In `params.steps` fügen Sie einen einzelnen `SimpleSequentialRunner` hinzu. Dieser Runner erwartet zwei verschachtelte `PipeConfig`‑Definitionen unter `params`:

- `on` – eine Trigger‑Pipe; wir verwenden `base:IntervalTrigger` mit einem `timedelta`‑Intervall (`PT60S` läuft einmal pro Minute).
- `run` – die Pipeline, die ausgeführt wird, wenn der Trigger erfolgreich ist. Hier referenzieren wir `base:CompositePipe`, das seine eigenen `params.steps` sequenziell verarbeitet.

### Schritt 4: Composite‑Pipeline‑Schritte definieren

Im Composite‑Pipe ist jedes Element in `params.steps` ein weiteres `PipeConfig`, das 1:1 einer Pipe‑Klasse zugeordnet ist:

1. **`fetch_open_tickets`** (`base:FetchTicketsPipe`) injiziert den Ticket‑System‑Service und lädt eingehende Tickets über `ticket_search_criteria`.
2. **`ensure_tickets_found`** (`base:ExpressionPipe`) ruft `fail()` auf, wenn keine Tickets abgerufen wurden, und beendet den Runner sauber.
3. **`queue_classifier`** (`base:ClassificationPipe`) injiziert den Hugging‑Face‑Service und klassifiziert den Ticket‑Text.
4. **`update_queue`** (`base:UpdateTicketPipe`) schreibt die neue Queue‑Auswahl zurück zu OTOBO/Znuny.
5. **`add_classification_note`** (`base:AddNotePipe`) protokolliert eine Audit‑Spur der automatisierten Klassifizierung.

Alle Parameter referenzieren frühere Ergebnisse mittels Hilfsfunktionen, die vom Jinja‑Renderer bereitgestellt werden (`get_pipe_result`, `fail`, `get_env` usw.).

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

## Ausführen und Verifizieren der Pipeline

1. Installieren Sie die erforderlichen Pakete (Kern plus die oben aufgeführten Plugins).
2. Stellen Sie die Zugangsdaten über die in der Konfiguration referenzierten Umgebungsvariablen bereit (z. B. `OTOBO_API_TOKEN`, `HF_TOKEN`).
3. Platzieren Sie die Konfigurationsdatei unter `config.yml` in Ihrem Arbeitsverzeichnis, damit `AppConfig` sie automatisch erkennt.
4. Starten Sie den Orchestrator:

   ```bash
   uv run python -m open_ticket_ai.main
   ```

`AppConfig` validiert das YAML beim Start gegen das Schema. Fehlt ein Abschnitt oder ist ein Parametername falsch, beendet die Anwendung mit einer beschreibenden Validierungsfehlermeldung, bevor Tickets verarbeitet werden. Sobald sie läuft, führt der Orchestrator den `SimpleSequentialRunner` jede Minute aus, wendet die verschachtelten `CompositePipe`‑Schritte an und protokolliert den Fortschritt über die konfigurierten Services.