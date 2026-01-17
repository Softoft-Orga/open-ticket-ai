---
title: Tag Mapping
description: 'Klassifizierungsergebnisse auf Ticket-System-Felder, Queues, Prioritäten und benutzerdefinierte Attribute abbilden.'
lang: en
nav:
  group: Ticket Tagging
  order: 4
---

# Tag Mapping

Erfahren Sie, wie Sie Klassifizierungsergebnisse auf die Felder, Queues, Prioritäten und benutzerdefinierten Attribute Ihres Ticket-Systems abbilden.

## Übersicht

Tag mapping verbindet die Ausgabe Ihres Klassifizierungsmodells mit umsetzbaren Änderungen in Ihrem Ticket-System:

- **Queue Assignment**: Tickets an das richtige Team weiterleiten
- **Priority Setting**: Angemessene Dringlichkeitsstufen festlegen
- **Status Updates**: Ticket-Status basierend auf der Klassifizierung ändern
- **Custom Fields**: Metadaten und Tags befüllen
- **Multi-field Updates**: Mehrere Felder aus einer einzigen Klassifizierung aktualisieren

## Grundlegende Zuordnung

### Einfache Queue-Zuordnung

Klassifizierungslabels direkt auf Queue-Namen abbilden:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'your-model'

- id: update_queue
  use: 'base:UpdateTicketPipe'
  injects: { ticket_system: 'otobo_znuny' }
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('classify', 'label') }}"
```

**Requirements**:

- Queue-Namen im Ticket-System müssen exakt den Klassifizierungslabels entsprechen
- Modell gibt gültige Queue-Namen aus

### Prioritätszuordnung

Klassifizierung auf Prioritätsstufen abbilden:

```yaml
- id: classify_priority
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'priority-classifier'

- id: update_priority
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      priority:
        name: "{{ get_pipe_result('classify_priority', 'label') }}"
```

## Erweiterte Zuordnung

### Mapping-Tabelle

Verwenden Sie Lookup-Tabellen für flexible Zuordnungen:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'category-classifier'

- id: map_to_queue
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set mapping = {
        'Hardware Issue': 'IT - Hardware Support',
        'Software Issue': 'IT - Software Support',
        'Network Problem': 'IT - Network Team',
        'Password Reset': 'IT - Help Desk',
        'Access Request': 'IT - Security',
        'Email Issue': 'IT - Email Support',
        'Printer Problem': 'IT - Office Equipment'
      } -%}
      {{ mapping.get(get_pipe_result('classify', 'label'), 'IT - General') }}

- id: update_queue
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('map_to_queue') }}"
```

### Mehrfeld-Zuordnung

Aktualisieren Sie mehrere Felder basierend auf der Klassifizierung:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'ticket-classifier'

- id: apply_mapping
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set mappings = {
        'Critical Outage': {
          'queue': 'Emergency Response',
          'priority': 'Critical',
          'type': 'Incident',
          'sla': '1 Hour Response'
        },
        'Hardware Failure': {
          'queue': 'Hardware Support',
          'priority': 'High',
          'type': 'Problem',
          'sla': '4 Hour Response'
        },
        'Password Reset': {
          'queue': 'Help Desk',
          'priority': 'Normal',
          'type': 'Service Request',
          'sla': 'Standard'
        }
      } -%}
      {{ mappings.get(get_pipe_result('classify', 'label'), {
        'queue': 'General Support',
        'priority': 'Normal',
        'type': 'Request',
        'sla': 'Standard'
      }) }}

- id: update_ticket
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('apply_mapping')['queue'] }}"
      priority:
        name: "{{ get_pipe_result('apply_mapping')['priority'] }}"
      type:
        name: "{{ get_pipe_result('apply_mapping')['type'] }}"
```

## Bedingte Zuordnung

### Vertrauensbasierte Zuordnung

Unterschiedliche Zuordnungen basierend auf dem Vertrauen:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'classifier'

- id: determine_queue
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set confidence = get_pipe_result('classify', 'confidence') -%}
      {%- set label = get_pipe_result('classify', 'label') -%}
      {%- if confidence >= 0.9 -%}
        {{ label }}
      {%- elif confidence >= 0.7 -%}
        Classification Queue - {{ label }}
      {%- else -%}
        Manual Classification Required
      {%- endif -%}

- id: update_queue
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('determine_queue') }}"
```

### Mehrfachbedingte Zuordnung

Kombinieren Sie mehrere Faktoren:

```yaml
- id: classify_type
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'type-classifier'

- id: classify_urgency
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.body }}'
    model_name: 'urgency-classifier'

- id: determine_priority
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set type = get_pipe_result('classify_type', 'label') -%}
      {%- set urgency = get_pipe_result('classify_urgency', 'label') -%}
      {%- if type == 'Outage' or urgency == 'Critical' -%}
        Critical
      {%- elif type == 'Security' or urgency == 'High' -%}
        High
      {%- elif urgency == 'Low' -%}
        Low
      {%- else -%}
        Normal
      {%- endif -%}

- id: update_priority
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      priority:
        name: "{{ get_pipe_result('determine_priority') }}"
```

## Benutzerdefinierte Feldzuordnung

### Tagging-System

Tags basierend auf der Klassifizierung hinzufügen:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'classifier'
    options:
      top_k: 3

- id: generate_tags
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {{
        get_pipe_result('classify', 'labels')
        | selectattr('confidence', '>=', 0.6)
        | map(attribute='label')
        | map('lower')
        | map('replace', ' ', '-')
        | list
        | join(', ')
      }}

- id: update_tags
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      dynamic_fields:
        - name: 'Tags'
          value: "{{ get_pipe_result('generate_tags') }}"
```

### Befüllung benutzerdefinierter Attribute

Auf benutzerdefinierte Felder in Ihrem Ticket-System abbilden:

```yaml
- id: classify_category
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'category-classifier'

- id: classify_subcategory
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.body }}'
    model_name: 'subcategory-classifier'

- id: update_custom_fields
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      dynamic_fields:
        - name: 'AutoCategory'
          value: "{{ get_pipe_result('classify_category', 'label') }}"
        - name: 'AutoSubcategory'
          value: "{{ get_pipe_result('classify_subcategory', 'label') }}"
        - name: 'ClassificationConfidence'
          value: "{{ get_pipe_result('classify_category', 'confidence') }}"
        - name: 'ClassifiedAt'
          value: '{{ now().isoformat() }}'
```

## Hierarchische Zuordnung

### Parent-Child-Queue-Struktur

Auf hierarchische Queue-Strukturen abbilden:

```yaml
- id: classify_department
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'department-classifier'

- id: classify_team
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.body }}'
    model_name: 'team-classifier'

- id: build_queue_path
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set dept = get_pipe_result('classify_department', 'label') -%}
      {%- set team = get_pipe_result('classify_team', 'label') -%}
      {{ dept }} :: {{ team }}

- id: update_queue
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('build_queue_path') }}"
```

**Example Output**:

- `IT :: Hardware Support`
- `IT :: Software Development`
- `HR :: Recruitment`

### Kategorienbäume

Durch Kategorienhierarchien navigieren:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'classifier'

- id: map_to_hierarchy
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set hierarchy = {
        'Desktop Issues': ['IT', 'Hardware', 'Desktop'],
        'Laptop Issues': ['IT', 'Hardware', 'Laptop'],
        'Software Bugs': ['IT', 'Software', 'Application'],
        'Network Down': ['IT', 'Infrastructure', 'Network']
      } -%}
      {%- set label = get_pipe_result('classify', 'label') -%}
      {{ hierarchy.get(label, ['General', 'Support', 'Unknown']) }}

- id: update_categories
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      dynamic_fields:
        - name: 'Category1'
          value: "{{ get_pipe_result('map_to_hierarchy')[0] }}"
        - name: 'Category2'
          value: "{{ get_pipe_result('map_to_hierarchy')[1] }}"
        - name: 'Category3'
          value: "{{ get_pipe_result('map_to_hierarchy')[2] }}"
```

## Hinweise hinzufügen

### Klassifizierungs-Hinweis

Fügen Sie eine Notiz hinzu, die die Klassifizierung dokumentiert:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'classifier'

- id: add_classification_note
  use: 'base:AddNotePipe'
  injects: { ticket_system: 'otobo_znuny' }
  params:
    ticket_id: '{{ ticket.id }}'
    note:
      subject: 'Automated Classification'
      body: >
        This ticket was automatically classified as: {{ get_pipe_result('classify', 'label') }}
        Confidence: {{ (get_pipe_result('classify', 'confidence') * 100) | round(1) }}%
        Classified at: {{ now().strftime('%Y-%m-%d %H:%M:%S') }}
      content_type: 'text/plain; charset=utf8'
```

### Vertrauenswarnung

Fügen Sie eine Notiz für Klassifizierungen mit geringem Vertrauen hinzu:

```yaml
- id: check_confidence
  use: 'base:ExpressionPipe'
  params:
    expression: "{{ get_pipe_result('classify', 'confidence') < 0.7 }}"

- id: add_warning_note
  use: 'base:AddNotePipe'
  injects: { ticket_system: 'otobo_znuny' }
  params:
    ticket_id: '{{ ticket.id }}'
    note:
      subject: '⚠️ Low Confidence Classification'
      body: >
        Automated classification has low confidence ({{ (get_pipe_result('classify', 'confidence') * 100) | round(1) }}%).
        Predicted: {{ get_pipe_result('classify', 'label') }}
        Please review and reclassify if necessary.
      content_type: 'text/plain; charset=utf8'
    condition: "{{ get_pipe_result('check_confidence') }}"
```

## Fehlerbehandlung

### Fallback-Zuordnung

Unbekannte Klassifizierungen behandeln:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'classifier'

- id: validate_classification
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set valid_queues = [
        'IT - Hardware',
        'IT - Software',
        'IT - Network',
        'HR - General',
        'Finance - Invoicing'
      ] -%}
      {%- set label = get_pipe_result('classify', 'label') -%}
      {{ label if label in valid_queues else 'Unclassified' }}

- id: update_queue
  use: 'base:UpdateTicketPipe'
  params:
    ticket_id: '{{ ticket.id }}'
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('validate_classification') }}"
```

### Mehrstufiger Fallback

Versuchen Sie mehrere Klassifizierungsstrategien:

```yaml
- id: primary_classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }} {{ ticket.body }}'
    model_name: 'primary-classifier'

- id: check_confidence
  use: 'base:ExpressionPipe'
  params:
    expression: "{{ get_pipe_result('primary_classify', 'confidence') >= 0.8 }}"

- id: fallback_classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'fallback-classifier'
  condition: "{{ not get_pipe_result('check_confidence') }}"

- id: final_label
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- if get_pipe_result('check_confidence') -%}
        {{ get_pipe_result('primary_classify', 'label') }}
      {%- else -%}
        {{ get_pipe_result('fallback_classify', 'label') if get_pipe_result('fallback_classify', 'confidence') >= 0.6 else 'Manual Review' }}
      {%- endif -%}
```

## Mapping testen

### Trockenlauf-Modus

Testen Sie Zuordnungen, ohne Tickets zu aktualisieren:

```yaml
- id: classify
  use: 'base:ClassificationPipe'
  params:
    text: '{{ ticket.subject }}'
    model_name: 'classifier'

- id: log_mapping
  use: 'base:LogPipe'
  params:
    level: 'INFO'
    message: >
      [DRY RUN] Would update ticket {{ ticket.id }}:
      From: {{ ticket.queue }}
      To: {{ get_pipe_result('classify', 'label') }}
      Confidence: {{ get_pipe_result('classify', 'confidence') }}

# Comment out update in dry run mode
# - id: update_queue
#   use: "base:UpdateTicketPipe"
#   params: ...
```

### Validierungs-Logging

Alle Zuordnungsentscheidungen protokollieren:

```yaml
- id: map_queue
  use: 'base:ExpressionPipe'
  params:
    expression: >
      {%- set mapping = {...} -%}
      {{ mapping.get(get_pipe_result('classify', 'label'), 'Default Queue') }}

- id: log_decision
  use: 'base:LogPipe'
  params:
    level: 'INFO'
    message: >
      Ticket {{ ticket.id }} mapping:
      Classification: {{ get_pipe_result('classify', 'label') }}
      Confidence: {{ get_pipe_result('classify', 'confidence') }}
      Mapped Queue: {{ get_pipe_result('map_queue') }}
      Original Queue: {{ ticket.queue }}
```

## Best Practices

### DO ✅

- Validieren Sie, dass Queue-/Feldnamen existieren, bevor Sie bereitstellen
- Verwenden Sie Fallback-Zuordnungen für unbekannte Klassifizierungen
- Protokollieren Sie alle Klassifizierungsentscheidungen für Audits
- Testen Sie Zuordnungen zuerst mit Beispieldaten
- Dokumentieren Sie Ihre Zuordnungslogik
- Behandeln Sie Randfälle explizit
- Überwachen Sie die Genauigkeit der Zuordnungen im Laufe der Zeit

### DON'T ❌

- Annehmen, dass Klassifizierungslabels exakt den Queue-Namen entsprechen
- Validierung der zugeordneten Werte überspringen
- Bereitstellen, ohne mit echten Tickets zu testen
- Werte hartkodieren, die sich ändern könnten
- Klassifizierungen mit geringem Vertrauen ignorieren
- Vergessen, nicht zugeordnete Labels zu behandeln
- Kritische Prioritäten automatisch zuweisen ohne Überprüfung

## Gemeinsame Muster

### Muster 1: Direkte Zuordnung

```yaml
Classification → Queue Name
```

Verwendung: Labels stimmen exakt mit Queue-Namen überein

### Muster 2: Lookup-Tabelle

```yaml
Classification → Mapping Table → Queue/Priority/etc
```

Verwendung: Labels unterscheiden sich von Queue-Namen

### Muster 3: Mehrstufig

```yaml
Classification 1 → Category
Classification 2 → Subcategory
Combine → Final Queue
```

Verwendung: Hierarchische Kategorisierung erforderlich

### Muster 4: Bedingt

```yaml
Classification + Confidence → Decision Logic → Action
```

Verwendung: Unterschiedliche Aktionen für verschiedene Vertrauensstufen

## Nächste Schritte

Nach dem Einrichten des Tag-Mappings:

1. **Test Mappings**: Auf Beispieltickets validieren
2. **Monitor Accuracy**: Korrekte vs. inkorrekte Zuordnungen verfolgen
3. **Refine Logic**: Anhand realer Ergebnisse anpassen
4. **Document Changes**: Mapping-Dokumentation aktuell halten

## Verwandte Dokumentation

- [Taxonomy Design](taxonomy-design.md) - Design your classification structure
- [Using Model](using-model.md) - Configure classification models
- [Hardware Sizing](hardware-sizing.md) - Infrastructure requirements