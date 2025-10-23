---
description: Step-by-step tutorial for creating your first ticket classification pipeline with Open Ticket AI including fetching, classification, and updates.
---

### TODO the main points didnt changed but the details like the settings config structure.

# Creating Your First Pipeline

Step-by-step tutorial for creating a complete ticket classification pipeline.

## Overview

In this tutorial, you'll create a pipeline that:

1. Fetches open tickets from your ticket system
2. Classifies them into queues
3. Assigns priority levels
4. Updates tickets with classifications
5. Adds notes documenting the changes

## Prerequisites

- Open Ticket AI installed
- OTOBO/Znuny instance with API access
- Environment variables configured

## Understanding Configuration Sections

A complete configuration has four main sections:

### 1. Plugins

Load and configure plugins:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"
```

### 2. General Config (Optional)

Application-wide settings:

```yaml
infrastructure:
  log_level: "INFO"
  max_workers: 4
```

### 3. Definitions (Optional)

Reusable configuration blocks:

```yaml
services:
  search_criteria: &search
    StateType: "Open"
    limit: 50
```

### 4. Orchestrator

Pipeline definitions:

```yaml
orchestrator:
  pipelines:
    - name: my_pipeline
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: step1
        - pipe_name: step2
```

## Step-by-Step Pipeline Creation

### Step 1: Start with Basic Structure

Create `config.yml`:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"

orchestrator:
  pipelines:
    - name: ticket_classifier
      run_every_milli_seconds: 60000
      pipes: [ ]  # We'll add pipes here
```

### Step 2: Add Ticket Fetching

Add a pipe to fetch tickets:

```yaml
orchestrator:
  pipelines:
    - name: ticket_classifier
      run_every_milli_seconds: 60000
      pipes:
        # Fetch open tickets
        - pipe_name: fetch_tickets
          search:
            StateType: "Open"
            QueueIDs: [ 1, 2, 3 ]  # Your queue IDs
            limit: 50
```

Test this step:

```bash
open-ticket-ai run --config config.yml --dry-run
```

### Step 3: Add Queue Classification

Add queue classification pipe:

```yaml
pipes:
  - pipe_name: fetch_tickets
    search:
      StateType: "Open"
      limit: 50

  # Classify queue
  - pipe_name: classify_queue
    model_name: "bert-base-uncased"
    confidence_threshold: 0.7
    queue_mapping:
      billing: 1
      support: 2
      technical: 3
```

### Step 4: Add Priority Classification

Add priority assignment:

```yaml
pipes:
  - pipe_name: fetch_tickets
    # ... (as before)

  - pipe_name: classify_queue
    # ... (as before)

  # Classify priority
  - pipe_name: classify_priority
    confidence_threshold: 0.7
    priority_mapping:
      low: 1
      normal: 2
      high: 3
      urgent: 4
```

### Step 5: Update Tickets

Add pipe to update tickets:

```yaml
pipes:
  # ... (previous pipes)

  # Update ticket with classifications
  - pipe_name: update_ticket
    fields:
      QueueID: "{{ context.predicted_queue_id }}"
      PriorityID: "{{ context.predicted_priority_id }}"
```

### Step 6: Add Documentation Note

Add a note to each ticket:

```yaml
pipes:
  # ... (previous pipes)

  # Add note documenting classification
  - pipe_name: add_note
    note_text: |
      Automatically classified by AI:
      - Queue: {{ context.predicted_queue }}
      - Priority: {{ context.predicted_priority }}
      - Confidence: {{ context.confidence }}%
      - Timestamp: {{ now() }}
    note_type: "internal"
```

### Step 7: Complete Configuration

Your complete `config.yml`:

```yaml
plugins:
  - name: otobo_znuny
    config:
      base_url: "${OTOBO_BASE_URL}"
      api_token: "${OTOBO_API_TOKEN}"

  - name: hf_local
    config:
      model_name: "bert-base-uncased"
      device: "cpu"

infrastructure:
  log_level: "INFO"

services:
  # Reusable search criteria
  open_tickets: &open_tickets
    StateType: "Open"
    limit: 50

  # Queue mapping
  queues: &queues
    billing: 1
    support: 2
    technical: 3

  # Priority mapping
  priorities: &priorities
    low: 1
    normal: 2
    high: 3
    urgent: 4

orchestrator:
  pipelines:
    - name: ticket_classifier
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
          search: *open_tickets

        - pipe_name: classify_queue
          confidence_threshold: 0.7
          queue_mapping: *queues

        - pipe_name: classify_priority
          confidence_threshold: 0.7
          priority_mapping: *priorities

        - pipe_name: update_ticket
          fields:
            QueueID: "{{ context.predicted_queue_id }}"
            PriorityID: "{{ context.predicted_priority_id }}"

        - pipe_name: add_note
          note_text: |
            Auto-classified:
            Queue: {{ context.predicted_queue }}
            Priority: {{ context.predicted_priority }}
            Confidence: {{ context.confidence }}%
          note_type: "internal"
```

## Testing and Debugging

### Dry Run

Test without making changes:

```bash
open-ticket-ai run --config config.yml --dry-run
```

### Verbose Logging

Enable debug logging:

```bash
open-ticket-ai run --config config.yml --log-level DEBUG
```

### Limit Processing

Process only a few tickets:

```bash
# Modify config temporarily
search:
  StateType: "Open"
  limit: 5  # Start small
```

### Validate Configuration

Check for errors:

```bash
open-ticket-ai validate --config config.yml
```

## Common Patterns

### Conditional Execution

Execute pipes based on conditions:

```yaml
- pipe_name: add_urgent_note
  if: "{{ context.priority == 'urgent' }}"
  note_text: "URGENT: Requires immediate attention"
```

### Error Handling

Handle errors gracefully:

```yaml
- pipe_name: classify_queue
  on_error: continue  # Continue pipeline on error
  fallback_queue: "General"  # Fallback value
```

### Batching

Process tickets in batches:

```yaml
- pipe_name: fetch_tickets
  search:
    StateType: "Open"
    limit: 100
  batch_size: 10  # Process 10 at a time
```

## Optimizing Your Pipeline

### Performance Tips

1. **Adjust Interval**: Don't run too frequently

```yaml
run_every_milli_seconds: 300000  # Every 5 minutes
```

2. **Limit Results**: Process manageable batches

```yaml
search:
  limit: 50  # Don't fetch too many
```

3. **Use Caching**: Enable model caching

```yaml
plugins:
  - name: hf_local
    config:
      cache_models: true
```

### Monitoring

Add monitoring pipes:

```yaml
- pipe_name: log_metrics
  metrics:
    - tickets_processed
    - classification_accuracy
    - processing_time
```

## Troubleshooting

### No Tickets Fetched

Check search criteria:

- Verify QueueIDs exist
- Check StateType is correct
- Ensure tickets match criteria

### Classification Fails

Check model configuration:

- Verify model name
- Ensure model is downloaded
- Check input format

### Updates Don't Apply

Verify permissions:

- API token has write access
- Queue/Priority IDs are valid
- Ticket exists and is updateable

## Next Steps

Now that you have a working pipeline:

1. **Customize**: Adapt to your specific needs
2. **Monitor**: Track performance and accuracy
3. **Refine**: Improve classification models
4. **Scale**: Increase throughput
5. **Extend**: Add custom pipes

## Related Documentation

- [Configuration Reference](../details/config_reference.md)
- [Configuration Examples](../details/configuration/examples.md)
- [Pipeline Architecture](../concepts/pipeline-architecture.md)
- [Template Rendering](../developers/template_rendering.md)
- [Troubleshooting](troubleshooting.md)
