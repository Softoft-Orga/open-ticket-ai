---
title: Tag Mapping
description: 'Map classification results to ticket system fields, queues, priorities, and custom attributes.'
lang: en
nav:
  group: Ticket Tagging
  order: 4
---

# Tag Mapping

Learn how to map classification results to your ticket system's fields, queues, priorities, and custom attributes.

## Overview

Tag mapping connects your classification model's output to actionable changes in your ticket system:

- **Queue Assignment**: Route tickets to the right team
- **Priority Setting**: Set appropriate urgency levels
- **Status Updates**: Change ticket states based on classification
- **Custom Fields**: Populate metadata and tags
- **Multi-field Updates**: Update multiple fields from a single classification

## Basic Mapping

### Simple Queue Mapping

Map classification labels directly to queue names:

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

- Queue names in ticket system match classification labels exactly
- Model outputs valid queue names

### Priority Mapping

Map classification to priority levels:

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

## Advanced Mapping

### Mapping Table

Use lookup tables for flexible mapping:

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

### Multi-Field Mapping

Update multiple fields based on classification:

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

## Conditional Mapping

### Confidence-Based Mapping

Different mappings based on confidence:

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

### Multi-Condition Mapping

Combine multiple factors:

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

## Custom Field Mapping

### Tagging System

Add tags based on classification:

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

### Custom Attribute Population

Map to custom fields in your ticket system:

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

## Hierarchical Mapping

### Parent-Child Queue Structure

Map to hierarchical queue structures:

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

### Category Trees

Navigate category hierarchies:

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

## Adding Notes

### Classification Note

Add a note documenting the classification:

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

### Confidence Warning

Add a note for low-confidence classifications:

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

## Error Handling

### Fallback Mapping

Handle unknown classifications:

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

### Multi-Stage Fallback

Try multiple classification strategies:

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

## Testing Mappings

### Dry Run Mode

Test mappings without updating tickets:

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

### Validation Logging

Log all mapping decisions:

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

- Validate queue/field names exist before deploying
- Use fallback mappings for unknown classifications
- Log all classification decisions for auditing
- Test mappings on sample data first
- Document your mapping logic
- Handle edge cases explicitly
- Monitor mapping accuracy over time

### DON'T ❌

- Assume classification labels match queue names exactly
- Skip validation of mapped values
- Deploy without testing on real tickets
- Hard-code values that might change
- Ignore low-confidence classifications
- Forget to handle unmapped labels
- Auto-assign critical priorities without review

## Common Patterns

### Pattern 1: Direct Mapping

```yaml
Classification → Queue Name
```

Use when: Labels match queue names exactly

### Pattern 2: Lookup Table

```yaml
Classification → Mapping Table → Queue/Priority/etc
```

Use when: Labels differ from queue names

### Pattern 3: Multi-Stage

```yaml
Classification 1 → Category
Classification 2 → Subcategory
Combine → Final Queue
```

Use when: Hierarchical categorization needed

### Pattern 4: Conditional

```yaml
Classification + Confidence → Decision Logic → Action
```

Use when: Different actions for different confidence levels

## Next Steps

After setting up tag mapping:

1. **Test Mappings**: Validate on sample tickets
2. **Monitor Accuracy**: Track correct vs incorrect mappings
3. **Refine Logic**: Adjust based on real-world results
4. **Document Changes**: Keep mapping documentation updated

## Related Documentation

- [Taxonomy Design](taxonomy-design.md) - Design your classification structure
- [Using Model](using-model.md) - Configure classification models
- [Hardware Sizing](hardware-sizing.md) - Infrastructure requirements
