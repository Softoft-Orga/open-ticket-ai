---
description: Template rendering guide using Jinja2 for dynamic configuration in Open Ticket AI with variables, conditionals, loops, and custom extensions.
---

# Template Rendering

Open Ticket AI uses Jinja2 for dynamic template rendering in configuration files and text generation.

## Jinja2 Template System

Jinja2 provides:

- Variable substitution
- Conditional logic
- Loops and filters
- Custom extensions

## Template Expressions in Configuration

Use templates in YAML configuration:

```yaml
pipes:
  - pipe_name: add_note
    note_text: "Classified as {{ context.queue }} with priority {{ context.priority }}"
```

## Custom Template Extensions

Open Ticket AI provides custom Jinja2 extensions:

### Context Access

Access pipeline context directly in templates:

```jinja2
{{ context.ticket.id }}
{{ context.classification_result.confidence }}
```

### Filters

Custom filters for common operations:

```jinja2
{{ ticket.created_at | format_date }}
{{ text | truncate(100) }}
{{ value | default("N/A") }}
```

### Functions

Helper functions available in templates:

```jinja2
{{ now() }}
{{ random_id() }}
{{ format_priority(value) }}
```

## Template Context and Variables

The template context includes:

- Pipeline execution context
- Environment variables
- Configuration values
- Custom variables

## Examples

### Conditional Note

```yaml
note_text: >
  {% if context.priority == 'high' %}
  URGENT: This ticket requires immediate attention.
  {% else %}
  Standard priority ticket.
  {% endif %}
```

### Dynamic Queue Assignment

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

### Loop Through Results

```yaml
summary: >
  Processed {{ context.tickets | length }} tickets:
  {% for ticket in context.tickets %}
  - Ticket #{{ ticket.id }}: {{ ticket.status }}
  {% endfor %}
```

## Security Considerations

- Templates run in a sandboxed environment
- Dangerous operations are disabled
- User input is automatically escaped
- Use `safe` filter only for trusted content

## Related Documentation

- [Configuration Structure](../../details/configuration/config_structure.md)
- [Pipeline Architecture](../../concepts/pipeline-architecture.md)
- [Configuration Examples](../../details/configuration/examples.md)
