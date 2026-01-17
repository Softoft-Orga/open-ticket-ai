---
title: Vorlagen-Rendering
description: 'Leitfaden zur Template-Renderung mit Jinja2 für dynamische Konfiguration in Open Ticket AI mit Variablen, Bedingungen, Schleifen und benutzerdefinierten Erweiterungen.'
---

# Vorlagen-Rendering

Open Ticket AI verwendet Jinja2 für dynamisches Template-Rendering in Konfigurationsdateien und Textgenerierung.

## Jinja2-Template-System

Jinja2 bietet:

- Variablensubstitution
- Bedingungslogik
- Schleifen und Filter
- Benutzerdefinierte Erweiterungen

## Template-Ausdrücke in der Konfiguration

Verwenden Sie Vorlagen in YAML-Konfiguration:

```yaml
pipes:
  - pipe_name: add_note
    note_text: 'Classified as {{ context.queue }} with priority {{ context.priority }}'
```

## Benutzerdefinierte Template-Erweiterungen

Open Ticket AI stellt benutzerdefinierte Jinja2-Erweiterungen bereit:

### Kontextzugriff

Zugriff auf den Pipeline-Kontext direkt in Vorlagen:

```jinja2
{{ context.ticket.id }}
{{ context.classification_result.confidence }}
```

### Filter

Benutzerdefinierte Filter für gängige Operationen:

```jinja2
{{ ticket.created_at | format_date }}
{{ text | truncate(100) }}
{{ value | default("N/A") }}
```

### Funktionen

Hilfsfunktionen in Vorlagen verfügbar:

```jinja2
{{ now() }}
{{ random_id() }}
{{ format_priority(value) }}
```

## Template-Kontext und Variablen

Der Template-Kontext enthält:

- Pipeline-Ausführungskontext
- Umgebungsvariablen
- Konfigurationswerte
- Benutzerdefinierte Variablen

## Beispiele

### Bedingte Notiz

```yaml
note_text: >
  {% if context.priority == 'high' %}
  URGENT: This ticket requires immediate attention.
  {% else %}
  Standard priority ticket.
  {% endif %}
```

### Dynamische Queue-Zuweisung

```yaml
queue: >
  {% if 'billing' in context.ticket.subject.lower() %}
  Billing
  {% elif 'technical' in context.ticket.subject.lower() %}
  Technical Support
  {% else %}
  General
  {% endif %}
```

### Durchlaufen der Ergebnisse

```yaml
summary: >
  Processed {{ context.tickets | length }} tickets:
  {% for ticket in context.tickets %}
  - Ticket #{{ ticket.id }}: {{ ticket.status }}
  {% endfor %}
```

## Sicherheitsüberlegungen

- Vorlagen werden in einer sandboxed Umgebung ausgeführt
- Gefährliche Operationen sind deaktiviert
- Benutzereingaben werden automatisch escaped
- Verwenden Sie den `safe`-Filter nur für vertrauenswürdige Inhalte

## Verwandte Dokumentation

- [Configuration Structure](../../details/configuration/config_structure.md)
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Configuration Examples](../../details/configuration/examples.md)