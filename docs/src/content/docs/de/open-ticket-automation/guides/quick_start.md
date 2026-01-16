---
title: Schnellstart-Anleitung
description: 'Starten Sie mit Open Ticket AI in 5 Minuten. Schnelle Einrichtungsanleitung für Python 3.13+ mit OTOBO-, Znuny- oder OTRS-Ticketsystem-Integration.'
lang: en
nav:
  group: Anleitungen
  order: 1
---

# Schnellstart-Anleitung

Starten Sie mit Open Ticket AI in 5 Minuten.

## Voraussetzungen

- Python 3.13+
- Zugriff auf eine OTOBO-, Znuny- oder OTRS-Instanz
- API-Token oder Zugangsdaten für Ihr Ticketsystem

## Installation

### Kernpaket installieren

```bash
# Mit uv (empfohlen)
uv pip install open-ticket-ai

# Oder mit pip
pip install open-ticket-ai
```

### Plugins installieren

```bash
# OTOBO/Znuny-Plugin installieren
uv pip install otai-otobo-znuny

# HuggingFace-Plugin installieren (für ML)
uv pip install otai-hf-local

# Oder das komplette Bundle installieren
uv pip install open-ticket-ai[all]
```

## Erste Konfiguration

### 1. Umgebungsvariablen setzen

```bash
export OTOBO_BASE_URL="https://your-ticket-system.com"
export OTOBO_API_TOKEN="your-api-token"
```

### 2. Konfigurationsdatei erstellen

Erstellen Sie `config.yml`:

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

## Ihre erste Pipeline ausführen

```bash
# Die Pipeline ausführen
open-ticket-ai run --config config.yml

# Oder mit ausführlicher Protokollierung
open-ticket-ai run --config config.yml --log-level DEBUG
```

Sie sollten eine Ausgabe wie folgt sehen:

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

Aktualisieren Sie Ihre Konfiguration, um Tickets zu klassifizieren:

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

        # ML-Klassifizierung hinzufügen
        - pipe_name: classify_queue
          model_name: 'bert-base-uncased'

        # Tickets aktualisieren
        - pipe_name: update_ticket
          fields:
            QueueID: '{{ context.predicted_queue_id }}'
```

### Beispiele erkunden

Sehen Sie sich vollständige Beispiele an:

```bash
# Verfügbare Konfigurationsbeispiele auflisten
ls docs/raw_en_docs/config_examples/

# Das Queue-Klassifizierungsbeispiel ausprobieren
cp docs/raw_en_docs/config_examples/queue_classification.yml config.yml
open-ticket-ai run --config config.yml
```

### Mehr erfahren

- [Installationsanleitung](installation.md) - Detaillierte Installationsanweisungen
- [Erste Pipeline-Anleitung](first_pipeline.md) - Schritt-für-Schritt-Erstellung einer Pipeline
- [Konfigurationsreferenz](../details/config_reference.md) - Vollständige Konfigurationsdokumentation
- [Verfügbare Plugins](../plugins/plugin_system.md) - Plugin-Dokumentation

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

- [Fehlerbehebungsanleitung](troubleshooting.md)
- [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- [Dokumentation](../README.md)

## Was kommt als Nächstes?

Jetzt, da Open Ticket AI läuft:

1. **Konfiguration anpassen**: An Ihren Workflow anpassen
2. **Weitere Pipes hinzufügen**: Funktionalität erweitern
3. **Leistung überwachen**: Klassifizierungsgenauigkeit verfolgen
4. **Hochskalieren**: Mehr Tickets verarbeiten
5. **Mitwirken**: Teilen Sie Ihre Erfahrungen und Verbesserungen