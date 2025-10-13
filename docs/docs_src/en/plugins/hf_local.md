---
description: HuggingFace Local plugin for Open Ticket AI enabling local ML model inference with GPU acceleration and model caching from HuggingFace Hub.
---

# HuggingFace Local Plugin

The HuggingFace Local plugin enables local ML model inference using models from the HuggingFace Hub.

## Overview

This plugin provides:
- Local model inference
- Support for various model types
- Model caching
- GPU acceleration (if available)

## Model Loading and Caching

Models are:
1. Downloaded from HuggingFace Hub
2. Cached locally for reuse
3. Loaded into memory on first use
4. Shared across pipeline executions

## Supported Model Types

### Text Classification
- Queue classification
- Priority classification
- Sentiment analysis
- Multi-label classification

### Text Generation
- Ticket summarization
- Response generation
- Text completion

### Named Entity Recognition
- Extract entities from tickets
- Custom entity types

## Configuration Examples

### Basic Classification

```yaml
plugins:
  - name: hf_local
    config:
      model_name: "bert-base-uncased"
      task: "text-classification"
      cache_dir: "./models"

pipes:
  - pipe_name: classify_with_hf
    model_name: "bert-base-uncased"
```

### GPU Acceleration

```yaml
plugins:
  - name: hf_local
    config:
      device: "cuda"  # Use GPU
      model_name: "roberta-large"
```

### Custom Model

```yaml
plugins:
  - name: hf_local
    config:
      model_name: "./my-custom-model"
      local: true
```

## Performance Considerations

### Memory Usage
- Models consume significant RAM
- Consider model size vs. accuracy trade-offs
- Use quantization for large models

### Inference Speed
- First inference is slower (model loading)
- Subsequent inferences are faster (cached)
- Batch processing improves throughput

### GPU vs CPU
- GPU significantly faster for large models
- CPU sufficient for smaller models
- Consider deployment environment

## Configuration Reference

### Required Settings
- `model_name`: HuggingFace model identifier or local path

### Optional Settings
- `device`: "cpu" or "cuda" (default: "cpu")
- `cache_dir`: Model cache directory (default: "~/.cache/huggingface")
- `batch_size`: Batch size for inference (default: 1)
- `max_length`: Maximum sequence length (default: 512)

## Troubleshooting

### Model Download Issues
- Check internet connectivity
- Verify HuggingFace Hub access
- Check disk space for cache

### Out of Memory
- Reduce batch size
- Use smaller model
- Enable CPU offloading

### Slow Inference
- Enable GPU if available
- Increase batch size
- Use distilled model variants

## Related Documentation

- [Plugin System](plugin_system.md)
- [Plugin Development](../developers/plugin_development.md)
- [Configuration Examples](../details/configuration/examples.md)
