---
title: Schnellstartanleitung
description: 'Starten Sie Open Ticket AI in 5 Minuten. Schnellstart‑Anleitung für Python 3.13+ mit OTOBO-, Znuny- oder OTRS‑Ticket‑System‑Integration.'
lang: en
nav:
  group: Guides
  order: 1
---

# Schnellstartanleitung

Starten Sie Open Ticket AI in 5 Minuten.

## Voraussetzungen

- Python 3.13+
- Zugriff auf eine OTOBO-, Znuny- oder OTRS-Instanz
- API‑Token oder Zugangsdaten für Ihr Ticket‑System

## Installation

### Kernpaket installieren

```bash
# Using uv (recommended)
uv pip install open-ticket-ai

# Or using pip
pip install open-ticket-ai
```

### Plugins installieren

```bash
# Install OTOBO/Znuny plugin
uv pip install otai-otobo-znuny

# Install HuggingFace plugin (for ML)
uv pip install otai-hf-local

# Or install the complete bundle
uv pip install open-ticket-ai[all]
```

## Erste Konfiguration

### 1. Umgebungsvariablen setzen

```bash
export OTOBO_BASE_URL="https://your-ticket-system.com"
export OTOBO_API_TOKEN="your-api-token"
```

### 2. Konfigurationsdatei erstellen

Create `config.yml`:

```yaml
# Plugins laden
plugins:
  - name: otobo_znuny
    config:
      base_url: '${OTOBO_BASE_URL}'
      api_token: '${OTOBO_API_TOKEN}'

# Pipeline konfigurieren
orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000 # Alle 60 Sekunden ausführen
      pipes:
        # Offene Tickets abrufen
        - pipe_name: fetch_tickets
          search:
            StateType: 'Open'
            limit: 10

        # Tickets protokollieren (zum Testen)
        - pipe_name: log_tickets
```

## Ausführen Ihrer ersten Pipeline

```bash
# Run the pipeline
open-ticket-ai run --config config.yml

# Or with verbose logging
open-ticket-ai run --config config.yml --log-level DEBUG
```

You should see output like:

```
[INFO] Loading configuration from config.yml
[INFO] Initializing plugins...
[INFO] Starting orchestrator...
[INFO] Running pipeline: classify_tickets
[INFO] Fetched 10 tickets
[INFO] Pipeline completed successfully
```

## Nächste Schritte

### Klassifizierung hinzufügen

Update your config to classify tickets:

```yaml
orchestrator:
  pipelines:
    - name: classify_tickets
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
          search:
            StateType: 'Open'
            limit: 10

        # ML‑Klassifizierung hinzufügen
        - pipe_name: classify_queue
          model_name: 'bert-base-uncased'

        # Tickets aktualisieren
        - pipe_name: update_ticket
          fields:
            QueueID: '{{ context.predicted_queue_id }}'
```

### Beispiele erkunden

Sehen Sie sich komplette Beispiele an:

```bash
# List available configExamples
ls docs/raw_en_docs/config_examples/

# Try the queue classification example
cp docs/raw_en_docs/config_examples/queue_classification.yml config.yml
open-ticket-ai run --config config.yml
```

### Mehr erfahren

- [Installation Guide](installation.md) - Detaillierte Installationsanweisungen
- [First Pipeline Tutorial](first_pipeline.md) - Schritt‑für‑Schritt‑Anleitung zur Pipeline‑Erstellung
- [Configuration Reference](../details/config_reference.md) - Vollständige Konfigurationsdokumentation
- [Available Plugins](../plugins/plugin_system.md) - Plugin‑Dokumentation

## Häufige Probleme

### Verbindungsfehler

```
Error: Failed to connect to ticket system
```

**Lösung**: Überprüfen Sie, ob `OTOBO_BASE_URL` korrekt und erreichbar ist.

### Authentifizierungsfehler

```
Error: 401 Unauthorized
```

**Lösung**: Prüfen Sie, ob `OTOBO_API_TOKEN` gültig ist und die erforderlichen Berechtigungen hat.

### Plugin nicht gefunden

```
Error: Plugin 'otobo_znuny' not found
```

**Lösung**: Installieren Sie das Plugin:

```bash
uv pip install otai-otobo-znuny
```

## Hilfe erhalten

- [Troubleshooting Guide](troubleshooting.md)
- [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- [Documentation](../README.md)

## Was kommt als Nächstes?

Jetzt, wo Open Ticket AI läuft:

1. **Konfiguration anpassen**: An Ihren Arbeitsablauf anpassen
2. **Weitere Pipes hinzufügen**: Funktionalität erweitern
3. **Leistung überwachen**: Klassifizierungsgenauigkeit verfolgen
4. **Skalieren**: Mehr Tickets verarbeiten
5. **Beitragen**: Ihre Erfahrungen und Verbesserungen teilen