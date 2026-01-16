---
title: Tag Mapping
description: 'Klassifikationsergebnisse auf Ticket-System-Felder, Queues, Prioritäten und benutzerdefinierte Attribute abbilden.'
lang: en
nav:
  group: Ticket Tagging
  order: 4
---

# Tag Mapping

Erfahren Sie, wie Sie Klassifikationsergebnisse auf die Felder, Queues, Prioritäten und benutzerdefinierten Attribute Ihres Ticket-Systems abbilden.

## Überblick

Tag Mapping verbindet die Ausgabe Ihres Klassifikationsmodells mit umsetzbaren Änderungen in Ihrem Ticket-System:

- **Queue-Zuweisung**: Tickets an das richtige Team weiterleiten
- **Prioritätsfestlegung**: Angemessene Dringlichkeitsstufen setzen
- **Status-Updates**: Ticketstatus basierend auf der Klassifikation ändern
- **Benutzerdefinierte Felder**: Metadaten und Tags befüllen
- **Multi-Feld-Updates**: Mehrere Felder aus einer einzigen Klassifikation aktualisieren

## Grundlegendes Mapping

### Einfaches Queue-Mapping

Klassifikationslabels direkt auf Queue-Namen abbilden:

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

**Anforderungen**:

- Queue-Namen im Ticket-System stimmen exakt mit den Klassifikationslabels überein
- Das Modell gibt gültige Queue-Namen aus

### Prioritäts-Mapping

Klassifikation auf Prioritätsstufen abbilden:

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

## Erweitertes Mapping

### Mapping-Tabelle

Verwenden Sie Lookup-Tabellen für flexibles Mapping:

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

### Multi-Feld-Mapping

Mehrere Felder basierend auf der Klassifikation aktualisieren:

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

## Bedingtes Mapping

### Konfidenzbasiertes Mapping

Verschiedene Mappings basierend auf der Konfidenz:

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

### Multi-Bedingungs-Mapping

Mehrere Faktoren kombinieren:

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

## Benutzerdefiniertes Feld-Mapping

### Tagging-System

Tags basierend auf der Klassifikation hinzufügen:

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

### Benutzerdefinierte Attribut-Befüllung

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

## Hierarchisches Mapping

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

**Beispielausgabe**:

- `IT :: Hardware Support`
- `IT :: Software Development`
- `HR :: Recruitment`

### Kategoriebäume

Kategoriehierarchien navigieren:

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

## Notizen hinzufügen

### Klassifikationsnotiz

Eine Notiz hinzufügen, die die Klassifikation dokumentiert:

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

### Konfidenzwarnung

Eine Notiz für Klassifikationen mit niedriger Konfidenz hinzufügen:

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

### Fallback-Mapping

Unbekannte Klassifikationen behandeln:

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

Mehrere Klassifikationsstrategien ausprobieren:

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

## Mappings testen

### Dry-Run-Modus

Mappings testen, ohne Tickets zu aktualisieren:

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

### Validierungsprotokollierung

Alle Mapping-Entscheidungen protokollieren:

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

- Vor dem Deployment prüfen, ob Queue-/Feldnamen existieren
- Fallback-Mappings für unbekannte Klassifikationen verwenden
- Alle Klassifikationsentscheidungen zur Nachverfolgung protokollieren
- Mappings zuerst mit Beispieldaten testen
- Ihre Mapping-Logik dokumentieren
- Randfälle explizit behandeln
- Mapping-Genauigkeit überwachen

### DON'T ❌

- Annehmen, dass Klassifikationslabels exakt mit Queue-Namen übereinstimmen
- Validierung der abgebildeten Werte überspringen
- Ohne Tests mit echten Tickets deployen
- Werte hartkodieren, die sich ändern könnten
- Klassifikationen mit niedriger Konfidenz ignorieren
- Vergessen, nicht abgebildete Labels zu behandeln
- Kritische Prioritäten ohne Überprüfung automatisch zuweisen

## Häufige Muster

### Muster 1: Direktes Mapping

```yaml
Klassifikation → Queue-Name
```

Verwenden, wenn: Labels exakt mit Queue-Namen übereinstimmen

### Muster 2: Lookup-Tabelle

```yaml
Klassifikation → Mapping-Tabelle → Queue/Priorität/etc
```

Verwenden, wenn: Labels sich von Queue-Namen unterscheiden

### Muster 3: Mehrstufig

```yaml
Klassifikation 1 → Kategorie
Klassifikation 2 → Unterkategorie
Kombinieren → Finale Queue
```

Verwenden, wenn: Hierarchische Kategorisierung benötigt wird

### Muster 4: Bedingt

```yaml
Klassifikation + Konfidenz → Entscheidungslogik → Aktion
```

Verwenden, wenn: Unterschiedliche Aktionen für verschiedene Konfidenzstufen

## Nächste Schritte

Nach dem Einrichten des Tag Mappings:

1. **Mappings testen**: Anhand von Beispiel-Tickets validieren
2. **Genauigkeit überwachen**: Korrekte vs. falsche Mappings verfolgen
3. **Logik verfeinern**: Basierend auf realen Ergebnissen anpassen
4. **Änderungen dokumentieren**: Mapping-Dokumentation aktuell halten

## Verwandte Dokumentation

- [Taxonomy Design](taxonomy-design.md) - Ihre Klassifikationsstruktur entwerfen
- [Using Model](using-model.md) - Klassifikationsmodelle konfigurieren
- [Hardware Sizing](hardware-sizing.md) - Infrastrukturanforderungen
