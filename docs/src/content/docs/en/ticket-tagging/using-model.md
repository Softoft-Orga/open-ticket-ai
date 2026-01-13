---
title: Using Model
description: "Configure, deploy, and use classification models for automated ticket tagging and categorization."
lang: en
nav:
  group: Ticket Tagging
  order: 3
---
# Using Model

Learn how to configure, deploy, and use classification models for automated ticket tagging.

## Overview

Open Ticket AI supports multiple model sources and types for ticket classification:

- **HuggingFace Models**: Pre-trained and fine-tuned transformers
- **Custom Models**: Your own trained models
- **Ensemble Models**: Combine multiple models for better accuracy

## Model Selection

### Pre-trained Models

Start with pre-trained models for quick deployment:

```yaml
# Using a general-purpose model
services:
  hf_local:
    use: "hf-local:HFClassificationService"
    params:
      api_token: "{{ get_env('OTAI_HF_TOKEN') }}"

orchestrator:
  steps:
    - id: classify
      use: "base:ClassificationPipe"
      injects: { classification_service: "hf_local" }
      params:
        text: "{{ ticket.subject }} {{ ticket.body }}"
        model_name: "distilbert-base-uncased-finetuned-sst-2-english"
```

**Advantages**:
- Quick to deploy
- No training required
- Works out-of-the-box

**Disadvantages**:
- May not match your specific use case
- Lower accuracy for domain-specific tickets
- Generic categories

### Fine-tuned Models

Use domain-specific fine-tuned models:

```yaml
orchestrator:
  steps:
    - id: classify_queue
      use: "base:ClassificationPipe"
      injects: { classification_service: "hf_local" }
      params:
        text: "{{ ticket.subject }} {{ ticket.body }}"
        model_name: "softoft/EHS_Queue_Prediction"
```

**Advantages**:
- Higher accuracy for your domain
- Understands your terminology
- Matches your taxonomy

**Disadvantages**:
- Requires training data
- Takes time to fine-tune
- May need periodic retraining

### Model Comparison

| Model Type | Accuracy | Setup Time | Cost | Best For |
|------------|----------|------------|------|----------|
| Pre-trained | 60-75% | Minutes | Low | Quick start, testing |
| Fine-tuned | 80-95% | Days-Weeks | Medium | Production use |
| Custom | 85-98% | Weeks-Months | High | Specialized needs |
| Ensemble | 90-99% | Weeks | High | Maximum accuracy |

## Configuration

### Basic Configuration

Minimal setup for classification:

```yaml
open_ticket_ai:
  api_version: ">=1.0.0"
  
  services:
    hf_local:
      use: "hf-local:HFClassificationService"
      params:
        api_token: "{{ get_env('OTAI_HF_TOKEN') }}"
  
  orchestrator:
    use: "base:SimpleSequentialOrchestrator"
    params:
      steps:
        - id: runner
          use: "base:SimpleSequentialRunner"
          params:
            on:
              id: "interval"
              use: "base:IntervalTrigger"
              params:
                interval: "PT60S"  # Run every 60 seconds
            run:
              id: "pipeline"
              use: "base:CompositePipe"
              params:
                steps:
                  - id: fetch
                    use: "base:FetchTicketsPipe"
                    injects: { ticket_system: "otobo_znuny" }
                    params:
                      ticket_search_criteria:
                        queue: { name: "Inbox" }
                        state: { name: "new" }
                        limit: 10
                  
                  - id: classify
                    use: "base:ClassificationPipe"
                    injects: { classification_service: "hf_local" }
                    params:
                      text: "{{ get_pipe_result('fetch','fetched_tickets')[0]['subject'] }}"
                      model_name: "distilbert-base-uncased"
```

### Advanced Configuration

Multi-label classification with confidence thresholds:

```yaml
steps:
  - id: classify_category
    use: "base:ClassificationPipe"
    injects: { classification_service: "hf_local" }
    params:
      text: "{{ ticket.subject }} {{ ticket.body }}"
      model_name: "your-org/ticket-category-classifier"
      options:
        top_k: 3  # Return top 3 predictions
        threshold: 0.7  # Minimum confidence threshold
  
  - id: classify_priority
    use: "base:ClassificationPipe"
    injects: { classification_service: "hf_local" }
    params:
      text: "{{ ticket.subject }} {{ ticket.body }}"
      model_name: "your-org/ticket-priority-classifier"
  
  - id: select_category
    use: "base:ExpressionPipe"
    params:
      expression: >
        {{
          get_pipe_result('classify_category', 'label')
          if get_pipe_result('classify_category', 'confidence') >= 0.8
          else 'Unclassified'
        }}
```

## Model Loading

### Local Model Loading

Models are automatically downloaded and cached:

```yaml
services:
  hf_local:
    use: "hf-local:HFClassificationService"
    params:
      api_token: "{{ get_env('OTAI_HF_TOKEN') }}"
      cache_dir: "/app/models"  # Optional: specify cache location
```

**First Run**:
- Model downloaded from HuggingFace
- Cached locally (5-10 seconds for small models, 30-60s for large)
- Ready for inference

**Subsequent Runs**:
- Model loaded from cache
- Fast startup (1-5 seconds)

### Model Cache Management

```bash
# Check cache size
du -sh /app/models

# Clear cache (requires restart)
rm -rf /app/models/*

# Pre-download model
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

## Text Preprocessing

### Combining Fields

Improve accuracy by combining multiple ticket fields:

```yaml
params:
  text: "{{ ticket.subject }} {{ ticket.body }}"
```

**With Priority**:
```yaml
params:
  text: "Priority: {{ ticket.priority }}. Subject: {{ ticket.subject }}. Body: {{ ticket.body }}"
```

**With Metadata**:
```yaml
params:
  text: >
    Queue: {{ ticket.queue }}.
    Type: {{ ticket.type }}.
    Subject: {{ ticket.subject }}.
    Description: {{ ticket.body }}
```

### Text Cleaning

Clean input text for better results:

```yaml
- id: clean_text
  use: "base:ExpressionPipe"
  params:
    expression: >
      {{
        (ticket.subject + ' ' + ticket.body)
        | replace('\n', ' ')
        | replace('\r', ' ')
        | trim
      }}

- id: classify
  use: "base:ClassificationPipe"
  params:
    text: "{{ get_pipe_result('clean_text') }}"
    model_name: "your-model"
```

## Confidence Thresholds

### Setting Thresholds

Use confidence scores to ensure quality:

```yaml
- id: classify
  use: "base:ClassificationPipe"
  params:
    text: "{{ ticket.subject }}"
    model_name: "your-model"

- id: final_category
  use: "base:ExpressionPipe"
  params:
    expression: >
      {{
        get_pipe_result('classify', 'label')
        if get_pipe_result('classify', 'confidence') >= 0.8
        else 'Manual Review Required'
      }}
```

### Confidence-Based Routing

Route differently based on confidence:

```yaml
- id: update_ticket
  use: "base:UpdateTicketPipe"
  params:
    ticket_id: "{{ ticket.id }}"
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

### Threshold Guidelines

| Confidence | Action | Use Case |
|------------|--------|----------|
| >0.95 | Auto-assign | High certainty classifications |
| 0.80-0.95 | Auto-assign with flag | Standard classifications |
| 0.60-0.80 | Suggest to agent | Low certainty - needs review |
| <0.60 | Manual classification | Too uncertain |

## Multi-Label Classification

Classify tickets into multiple categories:

```yaml
- id: classify_multiple
  use: "base:ClassificationPipe"
  injects: { classification_service: "hf_local" }
  params:
    text: "{{ ticket.subject }} {{ ticket.body }}"
    model_name: "your-org/multi-label-classifier"
    options:
      top_k: 5
      threshold: 0.6

- id: apply_tags
  use: "base:ExpressionPipe"
  params:
    expression: >
      {{
        get_pipe_result('classify_multiple', 'labels')
        | selectattr('confidence', '>=', 0.7)
        | map(attribute='label')
        | list
      }}
```

## Model Performance

### Monitoring Predictions

Track model performance:

```yaml
- id: classify
  use: "base:ClassificationPipe"
  params:
    text: "{{ ticket.subject }}"
    model_name: "your-model"

- id: log_prediction
  use: "base:LogPipe"
  params:
    message: >
      Classified ticket {{ ticket.id }}:
      Label: {{ get_pipe_result('classify', 'label') }}
      Confidence: {{ get_pipe_result('classify', 'confidence') }}
```

### Metrics to Track

Monitor these metrics:

- **Confidence Distribution**: Are most predictions high confidence?
- **Category Distribution**: Is any category over/under-represented?
- **Manual Overrides**: How often do agents change the classification?
- **Processing Time**: How long does classification take?

### Performance Analysis

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

## Troubleshooting

### Model Not Loading

**Error**: `Model 'xyz' not found`

**Solutions**:
1. Verify model name is correct
2. Check HuggingFace token is valid
3. Ensure model is public or you have access
4. Check internet connectivity

```bash
# Test model access
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

### Low Accuracy

**Symptoms**: Classifications often incorrect

**Solutions**:
1. Use a fine-tuned model for your domain
2. Combine more ticket fields in input text
3. Increase training data if using custom model
4. Adjust confidence threshold
5. Consider ensemble approach

### Slow Classification

**Symptoms**: High latency, slow processing

**Solutions**:
1. Use smaller model variant (e.g., DistilBERT vs BERT)
2. Enable GPU acceleration
3. Reduce input text length
4. Increase hardware resources
5. Implement batch processing

### High Memory Usage

**Error**: `OOM (Out of Memory)`

**Solutions**:
1. Use smaller model
2. Increase container memory limit
3. Reduce batch size
4. Clear model cache periodically

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

- Start with a small, fast model for testing
- Monitor confidence scores continuously
- Set appropriate confidence thresholds
- Combine multiple ticket fields for better context
- Fine-tune models on your data for production
- Track and analyze misclassifications
- Implement fallback for low-confidence predictions

### DON'T ❌

- Deploy without testing on representative data
- Ignore low confidence predictions
- Use overly complex models unnecessarily
- Skip performance monitoring
- Auto-assign tickets with <70% confidence without review
- Forget to update models as ticket patterns change

## Example Workflows

### Simple Queue Classification

```yaml
- id: classify_queue
  use: "base:ClassificationPipe"
  injects: { classification_service: "hf_local" }
  params:
    text: "{{ ticket.subject }} {{ ticket.body }}"
    model_name: "softoft/EHS_Queue_Prediction"

- id: update_queue
  use: "base:UpdateTicketPipe"
  injects: { ticket_system: "otobo_znuny" }
  params:
    ticket_id: "{{ ticket.id }}"
    updated_ticket:
      queue:
        name: "{{ get_pipe_result('classify_queue', 'label') }}"
```

### Priority Detection with Fallback

```yaml
- id: detect_priority
  use: "base:ClassificationPipe"
  params:
    text: "{{ ticket.subject }}"
    model_name: "your-org/priority-classifier"

- id: final_priority
  use: "base:ExpressionPipe"
  params:
    expression: >
      {{
        get_pipe_result('detect_priority', 'label')
        if get_pipe_result('detect_priority', 'confidence') >= 0.75
        else 'Normal'
      }}

- id: update_priority
  use: "base:UpdateTicketPipe"
  params:
    ticket_id: "{{ ticket.id }}"
    updated_ticket:
      priority:
        name: "{{ get_pipe_result('final_priority') }}"
```

## Next Steps

After configuring your model:

1. **Test Classifications**: Validate on sample tickets
2. **Set Confidence Thresholds**: Based on your risk tolerance
3. **Monitor Performance**: Track accuracy and adjust
4. **Fine-tune Model**: Improve with your data
5. **Scale Deployment**: Process more tickets

## Related Documentation

- [Taxonomy Design](taxonomy-design.md) - Design your classification categories
- [Tag Mapping](tag-mapping.md) - Map classifications to ticket fields
- [Hardware Sizing](hardware-sizing.md) - Infrastructure requirements
