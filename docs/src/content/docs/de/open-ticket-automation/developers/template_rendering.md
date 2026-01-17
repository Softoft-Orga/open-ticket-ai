---
title: Template Rendering
description: 'Anleitung zur Template-Renderung mit Jinja2 für dynamische Konfiguration in Open Ticket AI mit Variablen, Bedingungen, Schleifen und benutzerdefinierten Erweiterungen.'
---

# Template Rendering

Open Ticket AI verwendet Jinja2 für die dynamische Template-Renderung in Konfigurationsdateien und zur Texterzeugung.

## Jinja2 Template System

Jinja2 bietet:

- Variablenersetzung
- Bedingte Logik
- Schleifen und Filter
- Benutzerdefinierte Erweiterungen

## Template-Ausdrücke in der Konfiguration

Verwenden Sie Templates in der YAML-Konfiguration:

```yaml
pipes:
  - pipe_name: add_note
    note_text: 'Classified as {{ context.queue }} with priority {{ context.priority }}'
```

## Benutzerdefinierte Template-Erweiterungen

Open Ticket AI stellt benutzerdefinierte Jinja2-Erweiterungen bereit:

### Kontextzugriff

Greifen Sie direkt auf den Pipeline-Kontext in Templates zu:

```jinja2
{{ context.ticket.id }}
{{ context.classification_result.confidence }}
```

### Filter

Benutzerdefinierte Filter für häufige Operationen:

```jinja2
{{ ticket.created_at | format_date }}
{{ text | truncate(100) }}
{{ value | default("N/A") }}
```

### Funktionen

Hilfsfunktionen, die in Templates verfügbar sind:

```jinja2
{{ now() }}
{{ random_id() }}
{{ format_priority(value) }}
```

## Template-Kontext und Variablen

Der Template-Kontext umfasst:

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

### Schleife durch Ergebnisse

```yaml
summary: >
  Processed {{ context.tickets | length }} tickets:
  {% for ticket in context.tickets %}
  - Ticket #{{ ticket.id }}: {{ ticket.status }}
  {% endfor %}
```

## Sicherheitsüberlegungen

- Templates laufen in einer abgeschotteten Umgebung
- Gefährliche Operationen sind deaktiviert
- Benutzereingaben werden automatisch maskiert
- Verwenden Sie den `safe`-Filter nur für vertrauenswürdige Inhalte

## Verwandte Dokumentation

- [Configuration Structure](../../details/configuration/config_structure.md)
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Configuration Examples](../../details/configuration/examples.md)