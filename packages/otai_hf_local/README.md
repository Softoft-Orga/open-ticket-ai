# otai-hf-local

Hugging Face local text classification plugin for Open Ticket AI - on-premise ML ticket categorization.

## Overview

`otai-hf-local` enables local, privacy-preserving text classification using Hugging Face Transformers. Run state-of-the-art NLP models entirely on-premise for ticket categorization, priority detection, and sentiment analysis without sending data to external services.

## Features

- 🤖 **Local inference** - Run models entirely on your infrastructure
- 🔒 **Privacy-first** - No data leaves your environment
- 🎯 **Pre-trained models** - Use any Hugging Face text classification model
- ⚡ **GPU acceleration** - Optional CUDA support for faster inference
- 🎨 **Flexible pipelines** - Support for multi-label and single-label classification
- 📊 **Confidence scores** - Get prediction probabilities

## Installation

```bash
pip install otai-hf-local
```

For GPU support:

```bash
pip install otai-hf-local[gpu]
```

## Configuration

Add the plugin to your Open Ticket AI configuration:

```yaml
pipes:
  - type: hf_local
    params:
      model_name: "distilbert-base-uncased-finetuned-sst-2-english"
      device: "cpu"  # or "cuda" for GPU
      batch_size: 8
```

## Usage

### Programmatic Usage

```python
from otai_hf_local import HFLocalClassifier

# Initialize classifier
classifier = HFLocalClassifier(
    model_name="distilbert-base-uncased-finetuned-sst-2-english",
    device="cpu"
)

# Classify text
result = await classifier.classify(
    text="The server is down and users cannot login"
)

print(result.label)  # e.g., "urgent"
print(result.confidence)  # e.g., 0.95
```

### With Open Ticket AI

```python
from open_ticket_ai import OpenTicketAI

# Load configuration with HF Local pipe
app = OpenTicketAI.from_yaml("config.yml")

# Process ticket through classification pipeline
result = await app.process_ticket(ticket)
```

## Supported Models

Any Hugging Face model for text classification, including:

- **Sentiment**: `distilbert-base-uncased-finetuned-sst-2-english`
- **Zero-shot**: `facebook/bart-large-mnli`
- **Multi-label**: `joeddav/xlm-roberta-large-xnli`
- **Custom models**: Upload your fine-tuned models to Hugging Face

## Requirements

- Python 3.13 or higher
- PyTorch 2.0+
- transformers 4.52.4+
- CUDA (optional, for GPU acceleration)

## Performance

- **CPU**: ~50-200ms per classification (depends on model)
- **GPU**: ~10-50ms per classification
- **Batch processing**: Up to 10x faster with batching

## Documentation

- **Full docs**: [open-ticket-ai.com](https://open-ticket-ai.com/guide/available-plugins.html#hugging-face-local-text-classification-pipe)
- **Hugging Face**: [huggingface.co/transformers](https://huggingface.co/transformers/)

## Contributing

Contributions welcome! See the [main repository](https://github.com/Softoft-Orga/open-ticket-ai) for guidelines.

## License

LGPL-2.1-only - See [LICENSE](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/LICENSE).

## Related Packages

- [`open-ticket-ai`](https://pypi.org/project/open-ticket-ai/) - Core application
- [`otai-base`](https://pypi.org/project/otai-base/) - Base plugin framework
- [`otai-zammad`](https://pypi.org/project/otai-zammad/) - Zammad integration
- [`otai-otobo-znuny`](https://pypi.org/project/otai-otobo-znuny/) - OTOBO/Znuny integration

## Links

- **Homepage**: [open-ticket-ai.com](https://open-ticket-ai.com)
- **Repository**: [GitHub](https://github.com/Softoft-Orga/open-ticket-ai)
- **Issue Tracker**: [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- **PyPI**: [pypi.org/project/otai-hf-local](https://pypi.org/project/otai-hf-local/)
# otai-zammad

Zammad ticket system integration plugin for Open Ticket AI - automated helpdesk and ITSM workflows.

## Overview

`otai-zammad` provides seamless integration between Open Ticket AI and Zammad ticket systems. It enables automated ticket management, AI-powered classification, and intelligent workflow automation for Zammad instances.

## Features

- 🎫 **Full CRUD operations** - Create, read, update, and delete tickets
- 🔍 **Advanced search** - Query tickets with flexible search criteria
- 📝 **Article management** - Add notes and articles to tickets
- 🔄 **Real-time sync** - Keep ticket data synchronized
- 🔐 **Secure authentication** - Token-based API authentication
- 🎯 **Type-safe** - Full Pydantic v2 validation

## Installation

```bash
pip install otai-zammad
```

## Configuration

Add the plugin to your Open Ticket AI configuration:

```yaml
ticketsystem_service:
  type: zammad
  params:
    base_url: "https://your-zammad.example.com"
    access_token: "your-api-token"
    timeout: 30.0
    verify: true
```

## Usage

### Programmatic Usage

```python
from otai_zammad import ZammadTicketsystemService
from open_ticket_ai.models import UnifiedTicket, UnifiedEntity

# Initialize service
service = ZammadTicketsystemService(
    base_url="https://your-zammad.example.com",
    access_token="your-api-token"
)

# Create a ticket
ticket = await service.create_ticket(
    UnifiedTicket(
        subject="Issue with VPN",
        body="Cannot connect to VPN after update",
        queue=UnifiedEntity(name="IT Support"),
        priority=UnifiedEntity(name="2 normal"),
        customer=UnifiedEntity(name="user@example.com")
    )
)
```

### With Open Ticket AI

```python
from open_ticket_ai import OpenTicketAI

# Load configuration
app = OpenTicketAI.from_yaml("config.yml")

# Use the Zammad service
tickets = await app.ticketsystem.find_tickets(limit=10)
```

## Requirements

- Python 3.13 or higher
- Zammad instance with API access
- Valid Zammad API token

## Documentation

- **Full docs**: [open-ticket-ai.com](https://open-ticket-ai.com/en/guide/available-plugins.html)
- **Zammad API**: [docs.zammad.org](https://docs.zammad.org/en/latest/api/intro.html)

## Contributing

Contributions welcome! See the [main repository](https://github.com/Softoft-Orga/open-ticket-ai) for guidelines.

## License

LGPL-2.1-only - See [LICENSE](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/LICENSE).

## Related Packages

- [`open-ticket-ai`](https://pypi.org/project/open-ticket-ai/) - Core application
- [`otai-base`](https://pypi.org/project/otai-base/) - Base plugin framework
- [`otai-otobo-znuny`](https://pypi.org/project/otai-otobo-znuny/) - OTOBO/Znuny integration
- [`otai-hf-local`](https://pypi.org/project/otai-hf-local/) - Local AI model integration

## Links

- **Homepage**: [open-ticket-ai.com](https://open-ticket-ai.com)
- **Repository**: [GitHub](https://github.com/Softoft-Orga/open-ticket-ai)
- **Issue Tracker**: [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- **PyPI**: [pypi.org/project/otai-zammad](https://pypi.org/project/otai-zammad/)

