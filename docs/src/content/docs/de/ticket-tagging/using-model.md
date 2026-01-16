---
title: Using Model
description: 'Konfigurieren, bereitstellen und verwenden Sie Klassifizierungsmodelle für die automatische Ticket-Kennzeichnung und -Kategorisierung.'
lang: en
nav:
  group: Ticket Tagging
  order: 3
---

# Using Model

Erfahren Sie, wie Sie Klassifizierungsmodelle für die automatische Ticket-Kennzeichnung konfigurieren, bereitstellen und verwenden.

## Übersicht

Open Ticket AI unterstützt mehrere Modellquellen und -typen für die Ticket-Klassifizierung:

- **HuggingFace Models**: Vorab trainierte und feinabgestimmte Transformer-Modelle
- **Custom Models**: Ihre eigenen trainierten Modelle
- **Ensemble Models**: Kombinieren Sie mehrere Modelle für eine höhere Genauigkeit

## Modellauswahl

### Vorab trainierte Modelle

Beginnen Sie mit vorab trainierten Modellen für eine schnelle Bereitstellung:

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

- Schnelle Bereitstellung
- Kein Training erforderlich
- Funktioniert sofort

**Nachteile**:

- Passt möglicherweise nicht zu Ihrem spezifischen Anwendungsfall
- Geringere Genauigkeit für domänenspezifische Tickets
- Generische Kategorien

### Feinabgestimmte Modelle

Verwenden Sie domänenspezifisch feinabgestimmte Modelle:

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
- Entspricht Ihrer Taxonomie

**Nachteile**:

- Erfordert Trainingsdaten
- Feinabstimmung benötigt Zeit
- Möglicherweise periodische Nachschulung erforderlich

### Modellvergleich

| Modelltyp   | Genauigkeit | Einrichtungszeit | Kosten  | Am besten geeignet für       |
| ----------- | ----------- | ---------------- | ------- | ---------------------------- |
| Pre-trained | 60-75%      | Minuten          | Niedrig | Schneller Start, Tests       |
| Fine-tuned  | 80-95%      | Tage-Wochen      | Mittel  | Produktiveinsatz             |
| Custom      | 85-98%      | Wochen-Monate    | Hoch    | Spezialisierte Anforderungen |
| Ensemble    | 90-99%      | Wochen           | Hoch    | Maximale Genauigkeit         |

## Konfiguration

### Grundkonfiguration

Minimale Einrichtung für die Klassifizierung:

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
                interval: 'PT60S' # Alle 60 Sekunden ausführen
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

Multi-Label-Klassifizierung mit Konfidenzschwellenwerten:

```yaml
steps:
  - id: classify_category
    use: 'base:ClassificationPipe'
    injects: { classification_service: 'hf_local' }
    params:
      text: '{{ ticket.subject }} {{ ticket.body }}'
      model_name: 'your-org/ticket-category-classifier'
      options:
        top_k: 3 # Top-3-Vorhersagen zurückgeben
        threshold: 0.7 # Mindest-Konfidenzschwelle

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

Modelle werden automatisch heruntergeladen und gecached:

```yaml
services:
  hf_local:
    use: 'hf-local:HFClassificationService'
    params:
      api_token: "{{ get_env('OTAI_HF_TOKEN') }}"
      cache_dir: '/app/models' # Optional: Cache-Verzeichnis angeben
```

**Erster Lauf**:

- Modell wird von HuggingFace heruntergeladen
- Lokal gecached (5-10 Sekunden für kleine Modelle, 30-60s für große)
- Bereit für Inferenz

**Nachfolgende Läufe**:

- Modell wird aus dem Cache geladen
- Schneller Start (1-5 Sekunden)

### Modell-Cache-Verwaltung

```bash
# Cache-Größe prüfen
du -sh /app/models

# Cache leeren (erfordert Neustart)
rm -rf /app/models/*

# Modell vorab herunterladen
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

## Textvorverarbeitung

### Felder kombinieren

Verbessern Sie die Genauigkeit durch Kombination mehrerer Ticket-Felder:

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

### Textbereinigung

Bereinigen Sie Eingabetexte für bessere Ergebnisse:

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

## Konfidenzschwellenwerte

### Schwellenwerte festlegen

Verwenden Sie Konfidenzscores, um die Qualität sicherzustellen:

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

### Konfidenzbasierte Weiterleitung

Leiten Sie basierend auf der Konfidenz unterschiedlich weiter:

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

### Schwellenwert-Richtlinien

| Konfidenz | Aktion                                   | Anwendungsfall                                |
| --------- | ---------------------------------------- | --------------------------------------------- |
| >0.95     | Automatische Zuweisung                   | Klassifizierungen mit hoher Sicherheit        |
| 0.80-0.95 | Automatische Zuweisung mit Kennzeichnung | Standard-Klassifizierungen                    |
| 0.60-0.80 | Agenten vorschlagen                      | Geringe Sicherheit - Überprüfung erforderlich |
| <0.60     | Manuelle Klassifizierung                 | Zu unsicher                                   |

## Multi-Label-Klassifizierung

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

### Vorhersagen überwachen

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

### Zu überwachende Metriken

Überwachen Sie diese Metriken:

- **Konfidenzverteilung**: Sind die meisten Vorhersagen hochkonfident?
- **Kategorieverteilung**: Wird eine Kategorie über-/unterrepräsentiert?
- **Manuelle Überschreibungen**: Wie oft ändern Agenten die Klassifizierung?
- **Verarbeitungszeit**: Wie lange dauert die Klassifizierung?

### Leistungsanalyse

```bash
# Klassifizierungsprotokolle anzeigen
docker compose logs open-ticket-ai | grep "Classified ticket"

# Nach Konfidenzniveau zählen
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

## Fehlerbehebung

### Modell wird nicht geladen

**Fehler**: `Model 'xyz' not found`

**Lösungen**:

1. Überprüfen Sie, ob der Modellname korrekt ist
2. Prüfen Sie, ob der HuggingFace-Token gültig ist
3. Stellen Sie sicher, dass das Modell öffentlich ist oder Sie Zugriff haben
4. Überprüfen Sie die Internetverbindung

```bash
# Modellzugriff testen
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

### Geringe Genauigkeit

**Symptome**: Klassifizierungen oft falsch

**Lösungen**:

1. Verwenden Sie ein für Ihre Domäne feinabgestimmtes Modell
2. Kombinieren Sie mehr Ticket-Felder im Eingabetext
3. Erhöhen Sie die Trainingsdaten bei Verwendung eines benutzerdefinierten Modells
4. Passen Sie den Konfidenzschwellenwert an
5. Erwägen Sie einen Ensemble-Ansatz

### Langsame Klassifizierung

**Symptome**: Hohe Latenz, langsame Verarbeitung

**Lösungen**:

1. Verwenden Sie eine kleinere Modellvariante (z.B. DistilBERT vs BERT)
2. Aktivieren Sie GPU-Beschleunigung
3. Reduzieren Sie die Länge des Eingabetextes
4. Erhöhen Sie die Hardware-Ressourcen
5. Implementieren Sie Batch-Verarbeitung

### Hohe Speichernutzung

**Fehler**: `OOM (Out of Memory)`

**Lösungen**:

1. Verwenden Sie ein kleineres Modell
2. Erhöhen Sie das Speicherlimit des Containers
3. Reduzieren Sie die Batch-Größe
4. Löschen Sie den Modell-Cache regelmäßig

```yaml
# Speicher in docker-compose.yml erhöhen
services:
  open-ticket-ai:
    deploy:
      resources:
        limits:
          memory: 4G
```

## Best Practices

### DO ✅

- Beginnen Sie mit einem kleinen, schnellen Modell zum Testen
- Überwachen Sie Konfidenzscores kontinuierlich
- Legen Sie angemessene Konfidenzschwellenwerte fest
- Kombinieren Sie mehrere Ticket-Felder für besseren Kontext
- Feinabstimmung von Modellen auf Ihre Daten für die Produktion
- Verfolgen und analysieren Sie Fehlklassifizierungen
- Implementieren Sie einen Fallback für Vorhersagen mit geringer Konfidenz

### DON'T ❌

- Ohne Tests mit repräsentativen Daten bereitstellen
- Vorhersagen mit geringer Konfidenz ignorieren
- Unnötig überkomplexe Modelle verwenden
- Leistungsüberwachung überspringen
- Tickets mit <70% Konfidenz ohne Überprüfung automatisch zuweisen
- Vergessen, Modelle bei sich ändernden Ticket-Mustern zu aktualisieren

## Beispiel-Workflows

### Einfache Queue-Klassifizierung

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

1. **Klassifizierungen testen**: Anhand von Beispiel-Tickets validieren
2. **Konfidenzschwellenwerte festlegen**: Basierend auf Ihrer Risikotoleranz
3. **Leistung überwachen**: Genauigkeit verfolgen und anpassen
4. **Modell feinabstimmen**: Mit Ihren Daten verbessern
5. **Bereitstellung skalieren**: Mehr Tickets verarbeiten

## Verwandte Dokumentation

- [Taxonomy Design](taxonomy-design.md) - Entwerfen Sie Ihre Klassifizierungskategorien
- [Tag Mapping](tag-mapping.md) - Klassifizierungen auf Ticket-Felder abbilden
- [Hardware Sizing](hardware-sizing.md) - Infrastrukturanforderungen
