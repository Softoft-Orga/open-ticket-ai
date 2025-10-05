# open-ticket-ai-hf-local

Hugging Face local text classification plugin for Open Ticket AI.

## Installation

```bash
pip install open-ticket-ai-hf-local
```

## Overview

This package provides a pipe that executes Hugging Face sequence-classification models locally for automated ticket classification. When the pipe runs, it loads the tokenizer and model, builds a `text-classification` pipeline, and returns the top label together with its confidence score.

## Usage

### Configuration

Add the pipe to your Open Ticket AI configuration:

```yaml
open_ticket_ai:
  general_config:
    pipe_classes:
      - &ticket_classifier_pipe
        use: "open_ticket_ai_hf_local:HFLocalTextClassificationPipe"
  defs:
    - &ticket_classifier
      <<: *ticket_classifier_pipe
      model: "your-model-name"
      token: "{{ env.HUGGINGFACE_TOKEN }}"
      prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"
```

### Parameters

- `model` (str, required): The Hugging Face model name (e.g., `"softoft/EHS_Queue_V8"`)
- `token` (str, optional): Hugging Face API token for private models
- `prompt` (str, required): The text to classify (supports Jinja2 templates)

### Example

```yaml
steps:
  - id: classify_ticket
    use: "open_ticket_ai_hf_local:HFLocalTextClassificationPipe"
    model: "softoft/EHS_Queue_V8"
    token: "{{ env.HUGGINGFACE_TOKEN }}"
    prompt: "{{ data.ticket.subject }} {{ data.ticket.body }}"
```

## Features

- **Local execution**: No external API calls required
- **Model caching**: Models are cached per `(model, token)` combination to avoid reloading
- **Jinja2 templating**: Dynamic prompt construction from ticket data
- **Confidence scores**: Returns both label and confidence for each prediction

## Dependencies

- `open-ticket-ai>=1.0.0rc1`: Core Open Ticket AI framework
- `transformers[torch]~=4.52.4`: Hugging Face transformers library with PyTorch
- `pydantic~=2.11.7`: Data validation

## Development

Install development dependencies:

```bash
pip install open-ticket-ai-hf-local[dev]
```

Run tests:

```bash
pytest
```

## License

LGPL-2.1-only

## Links

- [Documentation](https://open-ticket-ai.com/guide/available-plugins.html#hugging-face-local-text-classification-pipe)
- [Repository](https://github.com/Softoft-Orga/open-ticket-ai)
- [Homepage](https://open-ticket-ai.com)
