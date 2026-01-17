---
title: Modell verwenden
description: 'Konfigurieren, bereitstellen und verwenden Sie Klassifizierungsmodelle für die automatisierte Ticket-Tagging und -Kategorisierung.'
lang: en
nav:
  group: Ticket Tagging
  order: 3
---

# Modell verwenden

Lernen Sie, wie Sie Klassifizierungsmodelle konfigurieren, bereitstellen und verwenden, um Tickets automatisch zu taggen.

## Überblick

Open Ticket AI unterstützt mehrere Modellquellen und -typen für die Ticketklassifizierung:

- **HuggingFace Models**: Vorgefertigte und feinabgestimmte Transformer
- **Custom Models**: Ihre eigenen trainierten Modelle
- **Ensemble Models**: Kombinieren mehrerer Modelle für höhere Genauigkeit

## Modellauswahl

### Vorgefertigte Modelle

Starten Sie mit vorgefertigten Modellen für eine schnelle Bereitstellung:

```yaml
# Using a general-purpose model
services:
  hf_local:
    use: 'hf-local:HFClassificationService'
    params:
      api_token: "{{ get_env('OTAI_HF_TOKEN') }}"

orchestrator:
  steps:
    - id: classify
      use: 'base:ClassificationPipe'
      injects: { classification_service: 'hf_local' }
      params:
        text: '{{ ticket.subject }} {{ ticket.body }}'
        model_name: 'distilbert-base-uncased-finetuned-sst-2-english'
```

**Vorteile**:

- Schnell bereitstellbar
- Kein Training erforderlich
- Funktioniert sofort

**Nachteile**:

- Passt möglicherweise nicht zu Ihrem spezifischen Anwendungsfall
- Geringere Genauigkeit für domänenspezifische Tickets
- Generische Kategorien

### Feinabgestimmte Modelle

Verwenden Sie domänenspezifische feinabgestimmte Modelle:

```yaml
orchestrator:
  steps:
    - id: classify_queue
      use: 'base:ClassificationPipe'
      injects: { classification_service: 'hf_local' }
      params:
        text: '{{ ticket.subject }} {{ ticket.body }}'
        model_name: 'softoft/EHS_Queue_Prediction'
```

**Vorteile**:

- Höhere Genauigkeit für Ihre Domäne
- Versteht Ihre Terminologie
- Passt zu Ihrer Taxonomie

**Nachteile**:

- Benötigt Trainingsdaten
- Benötigt Zeit zum Feinabstimmen
- Möglicherweise periodisches Retraining erforderlich

### Modellvergleich

| Modelltyp   | Genauigkeit | Einrichtungszeit | Kosten | Am besten für          |
| ----------- | ----------- | ---------------- | ------ | ---------------------- |
| Vorgefertigt | 60-75%     | Minuten          | Niedrig | Schnellstart, Testen |
| Feinabgestimmt | 80-95% | Tage-Wochen      | Mittel | Produktionseinsatz    |
| Custom      | 85-98%      | Wochen-Monate    | Hoch   | Spezialisierte Bedürfnisse |
| Ensemble    | 90-99%      | Wochen           | Hoch   | Maximale Genauigkeit   |

## Konfiguration

### Grundkonfiguration

Minimale Einrichtung für Klassifizierung:

```yaml
open_ticket_ai:
  api_version: '>=1.0.0'

  services:
    hf_local:
      use: 'hf-local:HFClassificationService'
      params:
        api_token: "{{ get_env('OTAI_HF_TOKEN') }}"

  orchestrator:
    use: 'base:SimpleSequentialOrchestrator'
    params:
      steps:
        - id: runner
          use: 'base:SimpleSequentialRunner'
          params:
            on:
              id: 'interval'
              use: 'base:IntervalTrigger'
              params:
                interval: 'PT60S' # Run every 60 seconds
            run:
              id: 'pipeline'
              use: 'base:CompositePipe'
              params:
                steps:
                  - id: fetch
                    use: 'base:FetchTicketsPipe'
                    injects: { ticket_system: 'otobo_znuny' }
                    params:
                      ticket_search_criteria:
                        queue: { name: 'Inbox' }
                        state: { name: 'new' }
                        limit: 10

                  - id: classify
                    use: 'base:ClassificationPipe'
                    injects: { classification_service: 'hf_local' }
                    params:
                      text: "{{ get_pipe_result('fetch','fetched_tickets')[0]['subject'] }}"
                      model_name: 'distilbert-base-uncased'
```

### Erweiterte Konfiguration

Mehrfach-Label-Klassifizierung mit Vertrauensschwellen:

```yaml
steps:
  - id: classify_category
    use: 'base:ClassificationPipe'
    injects: { classification_service: 'hf_local' }
    params:
      text: '{{ ticket.subject }} {{ ticket.body }}'
      model_name: 'your-org/ticket-category-classifier'
      options:
        top_k: 3 # Return top 3 predictions
        threshold: 0.7 # Minimum confidence threshold

  - id: classify_priority
    use: 'base:ClassificationPipe'
    injects: { classification_service: 'hf_local' }
    params:
      text: '{{ ticket.subject }} {{ ticket.body }}'
      model_name: 'your-org/ticket-priority-classifier'

  - id: select_category
    use: 'base:ExpressionPipe'
    params:
      expression: >
        {{
          get_pipe_result('classify_category', 'label')
          if get_pipe_result('classify_category', 'confidence') >= 0.8
          else 'Unclassified'
        }}
```

## Modellladen

### Lokales Modellladen

Modelle werden automatisch heruntergeladen und zwischengespeichert:

```yaml
services:
  hf_local:
    use: 'hf-local:HFClassificationService'
    params:
      api_token: "{{ get_env('OTAI_HF_TOKEN') }}"
      cache_dir: '/app/models' # Optional: specify cache location
```

**Erster Durchlauf**:

- Modell von HuggingFace heruntergeladen
- Lokal zwischengespeichert (5-10 Sekunden für kleine Modelle, 30-60s für große)
- Bereit für Inferenz

**Nachfolgende Durchläufe**:

- Modell aus dem Cache geladen
- Schneller Start (1-5 Sekunden)

### Modell-Cache-Verwaltung

```bash
# Check cache size
du -sh /app/models

# Clear cache (requires restart)
rm -rf /app/models/*

# Pre-download model
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

## Textvorverarbeitung

### Kombination von Feldern

Verbessern Sie die Genauigkeit, indem Sie mehrere Ticketfelder kombinieren:

```yaml
params:
  text: '{{ ticket.subject }} {{ ticket.body }}'
```

**Mit Priorität**:

```yaml
params:
  text: 'Priority: {{ ticket.priority }}. Subject: {{ ticket.subject }}. Body: {{ ticket.body }}'
```

**Mit Metadaten**:

```yaml
params:
  text: >
    Queue: {{ ticket.queue }}.
    Type: {{ ticket.type }}.
    Subject: {{ ticket.subject }}.
    Description: {{ ticket.body }}
```

### Textreinigung

Reinigen Sie den Eingabetext für bessere Ergebnisse:

```yaml
- id: clean_text
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {{
        (ticket.subject + ' ' + ticket.body)
        | replace('\n', ' ')
        | replace('\r', ' ')
        | trim
      }}

- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: "{{ get_pipe_result('clean_text') }}"
    model_name: 'your-model'
```

## Vertrauensschwellen

### Festlegen von Schwellenwerten

Verwenden Sie Vertrauenswerte, um Qualität sicherzustellen:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'your-model'

- id: final_category
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {{
        get_pipe_result('classify', 'label')
        if get_pipe_result('classify', 'confidence') >= 0.8
        else 'Manual Review Required'
      }}
```

### Vertrauensbasierte Weiterleitung

Leiten Sie je nach Vertrauen unterschiedlich weiter:

```yaml
- id: update_ticket
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: >
          {{
            get_pipe_result('classify', 'label')
            if get_pipe_result('classify', 'confidence') >= 0.9
            else 'Manual Classification'
          }}
      priority:
        name: >
          {{
            'High'
            if get_pipe_result('classify', 'confidence') < 0.7
            else 'Normal'
          }}
```

### Richtlinien für Schwellenwerte

| Vertrauen | Aktion                | Anwendungsfall                     |
| --------- | --------------------- | ---------------------------------- |
| >0.95     | Auto-Zuweisung        | Hochsichere Klassifizierungen      |
| 0.80-0.95 | Auto-Zuweisung mit Flag | Standardklassifizierungen          |
| 0.60-0.80 | Vorschlag für Agent   | Niedriges Vertrauen – Review nötig |
| <0.60     | Manuelle Klassifizierung | Zu unsicher                        |

## Mehrfach-Label-Klassifizierung

Klassifizieren Sie Tickets in mehrere Kategorien:

```yaml
- id: classify_multiple
  use: 'base:ClassificationPipe'
  injects: { classification_service: 'hf_local' }
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'your-org/multi-label-classifier'
    options:
      top_k: 5
      threshold: 0.6

- id: apply_tags
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {{
        get_pipe_result('classify_multiple', 'labels')
        | selectattr('confidence', '>=', 0.7)
        | map(attribute='label')
        | list
      }}
```

## Modellleistung

### Überwachung von Vorhersagen

Verfolgen Sie die Modellleistung:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'your-model'

- id: log_prediction
  use: 'base:LogPipe'
  params:
    message: >
      Classified ticket {{ ticket.id }}:
      Label: {{ get_pipe_result('classify', 'label') }}
      Confidence: {{ get_pipe_result('classify', 'confidence') }}
```

### Zu überwachende Kennzahlen

Beobachten Sie diese Kennzahlen:

- **Confidence Distribution**: Sind die meisten Vorhersagen hochsicher?
- **Category Distribution**: Ist eine Kategorie über-/unterrepräsentiert?
- **Manual Overrides**: Wie oft ändern Agenten die Klassifizierung?
- **Processing Time**: Wie lange dauert die Klassifizierung?

### Leistungsanalyse

```bash
# View classification logs
docker compose logs open-ticket-ai | grep "Classified ticket"

# Count by confidence level
docker compose logs open-ticket-ai | grep -oP 'Confidence: \K[0-9.]+' | awk '{
  if ($1 >= 0.9) high++
  else if ($1 >= 0.7) medium++
  else low++
}
END {
  print "High (>=0.9):", high
  print "Medium (0.7-0.9):", medium
  print "Low (<0.7):", low
}'
```

## Fehlersuche

### Modell wird nicht geladen

**Fehler**: `Model 'xyz' not found`

**Lösungen**:

1. Überprüfen Sie, ob der Modellname korrekt ist
2. Prüfen Sie, ob das HuggingFace‑Token gültig ist
3. Stellen Sie sicher, dass das Modell öffentlich ist oder Sie Zugriff haben
4. Prüfen Sie die Internetverbindung

```bash
# Test model access
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

### Niedrige Genauigkeit

**Symptome**: Klassifizierungen häufig inkorrekt

**Lösungen**:

1. Verwenden Sie ein feinabgestimmtes Modell für Ihre Domäne
2. Kombinieren Sie mehr Ticketfelder im Eingabetext
3. Erhöhen Sie die Trainingsdaten, wenn Sie ein Custom‑Modell nutzen
4. Passen Sie die Vertrauensschwelle an
5. Erwägen Sie einen Ensemble‑Ansatz

### Langsame Klassifizierung

**Symptome**: Hohe Latenz, langsame Verarbeitung

**Lösungen**:

1. Verwenden Sie eine kleinere Modellvariante (z. B. DistilBERT statt BERT)
2. Aktivieren Sie GPU‑Beschleunigung
3. Reduzieren Sie die Eingabetextlänge
4. Erhöhen Sie die Hardware‑Ressourcen
5. Implementieren Sie Batch‑Verarbeitung

### Hoher Speicherverbrauch

**Fehler**: `OOM (Out of Memory)`

**Lösungen**:

1. Verwenden Sie ein kleineres Modell
2. Erhöhen Sie das Container‑Speicherlimit
3. Reduzieren Sie die Batch‑Größe
4. Löschen Sie den Modell‑Cache periodisch

```yaml
# Increase memory in docker-compose.yml
services:
  open-ticket-ai:
    deploy:
      resources:
        limits:
          memory: 4G
```

## Best Practices

### DO ✅

- Beginnen Sie mit einem kleinen, schnellen Modell für Tests
- Überwachen Sie kontinuierlich die Vertrauenswerte
- Setzen Sie geeignete Vertrauensschwellen
- Kombinieren Sie mehrere Ticketfelder für besseren Kontext
- Feinabstimmung von Modellen mit Ihren Daten für die Produktion
- Verfolgen und analysieren Sie Fehlklassifizierungen
- Implementieren Sie ein Fallback für Vorhersagen mit geringem Vertrauen

### DON'T ❌

- Bereitstellen ohne Tests mit repräsentativen Daten
- Ignorieren von Vorhersagen mit niedrigem Vertrauen
- Unnötig komplexe Modelle verwenden
- Performance‑Monitoring überspringen
- Tickets mit <70 % Vertrauen automatisch zuweisen ohne Review
- Vergessen, Modelle zu aktualisieren, wenn sich Ticket‑Muster ändern

## Beispiel‑Workflows

### Einfache Queue‑Klassifizierung

```yaml
- id: classify_queue
  use: 'base:ClassificationPipe'
  injects: { classification_service: 'hf_local' }
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'softoft/EHS_Queue_Prediction'

- id: update_queue
  use: 'base:UpdateTicketPipe'
  injects: { ticket_system: 'otobo_znuny' }
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('classify_queue', 'label') }}"
```

### Prioritätserkennung mit Fallback

```yaml
- id: detect_priority
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'your-org/priority-classifier'

- id: final_priority
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {{
        get_pipe_result('detect_priority', 'label')
        if get_pipe_result('detect_priority', 'confidence') >= 0.75
        else 'Normal'
      }}

- id: update_priority
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      priority:
        name: "{{ get_pipe_result('final_priority') }}"
```

## Nächste Schritte

Nach der Konfiguration Ihres Modells:

1. **Klassifizierungen testen**: Validieren Sie an Beispiel‑Tickets
2. **Vertrauensschwellen setzen**: Basierend auf Ihrem Risikoprofil
3. **Performance überwachen**: Genauigkeit verfolgen und anpassen
4. **Modell feinabstimmen**: Mit Ihren Daten verbessern
5. **Bereitstellung skalieren**: Mehr Tickets verarbeiten

## Verwandte Dokumentation

- [Taxonomy Design](taxonomy-design.md) - Entwerfen Sie Ihre Klassifizierungskategorien
- [Tag Mapping](tag-mapping.md) - Zuordnen von Klassifizierungen zu Ticketfeldern
- [Hardware Sizing](hardware-sizing.md) - Infrastruktur‑Anforderungen