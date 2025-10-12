# Configuration Examples

Overview of available configuration examples demonstrating different use cases and patterns.

## Available Examples

All examples are available in the `docs/raw_en_docs/config_examples/` directory.

### Queue Classification Example

Automatically route tickets to appropriate queues based on content.

**File**: `queue_classification.yml`

**Use Case**: 
- Classify incoming tickets by department
- Route to correct queue automatically
- Reduce manual triage time

**Key Features**:
- ML-based queue classification
- Confidence thresholds
- Fallback queue for low confidence

### Priority Classification Example

Assign priority levels to tickets based on urgency indicators.

**File**: `priority_classification.yml`

**Use Case**:
- Identify urgent tickets automatically
- Set priority based on keywords and patterns
- Escalate high-priority issues

**Key Features**:
- Priority prediction
- Keyword-based rules
- SLA-aware classification

### Complete Workflow Example

End-to-end ticket processing workflow.

**File**: `complete_workflow.yml`

**Use Case**:
- Full ticket lifecycle automation
- Combine multiple classification steps
- Add notes and notifications

**Key Features**:
- Multi-step pipeline
- Queue and priority classification
- Automatic note addition
- Error handling

### Conditional Processing Example

Execute pipes based on conditions.

**File**: `add_note_when_in_queue.yml`

**Use Case**:
- Conditional logic in pipelines
- Queue-specific processing
- Dynamic behavior based on ticket properties

**Key Features**:
- `if` conditions on pipes
- Template expressions
- Context-aware execution

### Custom Pipe Examples

Creating and using custom pipes.

**Key Features**:
- Custom business logic
- Service injection
- Configuration patterns

## Example Structure

Each example follows this structure:

```yaml
# Plugin configuration
plugins:
  - name: required_plugin
    config: {}

# Pipeline definition
orchestrator:
  pipelines:
    - name: example_pipeline
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: step1
        - pipe_name: step2
```

## Using Examples

### 1. Copy Example

```bash
cp docs/raw_en_docs/config_examples/queue_classification.yml config.yml
```

### 2. Set Environment Variables

```bash
export OTOBO_API_TOKEN="your-token"
export OTOBO_BASE_URL="https://your-instance.com"
```

### 3. Customize Configuration

Edit the configuration file to match your requirements:
- Update queue IDs
- Modify search criteria
- Adjust intervals

### 4. Run

```bash
open-ticket-ai run --config config.yml
```

## Quick Reference

See [QUICK_REFERENCE.md](../../config_examples/QUICK_REFERENCE.md) for a comparison table of all examples.

## Combining Examples

You can combine patterns from multiple examples:

```yaml
orchestrator:
  pipelines:
    # Queue classification from example 1
    - name: classify_queues
      run_every_milli_seconds: 60000
      pipes:
        - pipe_name: fetch_tickets
        - pipe_name: classify_queue
    
    # Priority classification from example 2
    - name: classify_priority
      run_every_milli_seconds: 120000
      pipes:
        - pipe_name: fetch_tickets
        - pipe_name: classify_priority
```

## Example-Specific Documentation

Each example includes:
- **README**: Overview and use case
- **Configuration file**: Complete working configuration
- **Sidecar file**: Detailed pipe-by-pipe documentation
- **Environment variables**: Required variables

## Testing Examples

Test examples before production:

```bash
# Dry run mode
open-ticket-ai run --config config.yml --dry-run

# Test with limited data
open-ticket-ai run --config config.yml --limit 10
```

## Related Documentation

- [Configuration Schema](config_schema.md)
- [Configuration Structure](config_structure.md)
- [Quick Start Guide](../../guides/quick_start.md)
- [First Pipeline Tutorial](../../guides/first_pipeline.md)
