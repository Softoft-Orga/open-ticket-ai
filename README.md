# Open Ticket AI

AI-powered automation and classification for open source ticket systems.

[![License: LGPL-2.1](https://img.shields.io/badge/License-LGPL%202.1-blue.svg)](https://www.gnu.org/licenses/lgpl-2.1)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

## Overview

Open Ticket AI is an extensible automation framework that brings AI-powered classification and routing to ticket systems. It integrates with helpdesk platforms like OTOBO, Znuny, and OTRS to automatically classify, route, and enhance tickets using machine learning models.

## Features

- 🤖 **AI-Powered Classification**: Use Hugging Face models for queue, priority, and custom classification
- 🎯 **Intelligent Routing**: Automatically route tickets based on content analysis
- 🔌 **Plugin Architecture**: Extensible design for adding new ticket systems and AI providers
- 🔄 **Workflow Automation**: Define complex automation pipelines with declarative YAML
- 🛡️ **Type-Safe**: Built with Pydantic for robust data validation
- 🧪 **Well-Tested**: Comprehensive test suite with unit and integration tests

## Quick Start

### Installation

Install Open Ticket AI:

```bash
pip install open-ticket-ai
```

Install plugins as needed:

```bash
# OTOBO/Znuny/OTRS integration
pip install open-ticket-ai-otobo-znuny-plugin

# Or install with plugin extras
pip install open-ticket-ai[otobo-znuny]
```

### Configuration

Create a configuration file (e.g., `config.yml`):

```yaml
open_ticket_ai:
  defs:
    - id: "my_ticket_system"
      use: "open_ticket_ai_otobo_znuny_plugin:OTOBOZnunyTicketSystemService"
      base_url: "https://your-otobo-instance.com/otobo/nph-genericinterface.pl"
      password: "{{ env.OTOBO_PASSWORD }}"

  orchestrator:
    - run_every_milli_seconds: 60000
      pipe:
        id: ticket-classifier
        steps:
          - id: fetch_tickets
            use: "open_ticket_ai.base:FetchTicketsPipe"
            injects: { ticket_system: "my_ticket_system" }
          
          - id: classify
            use: "open_ticket_ai_hf_local:HFLocalTextClassificationPipe"
            model: "your-model-name"
            prompt: "{{ ticket.subject }} {{ ticket.body }}"
```

### Running

```bash
open-ticket-ai --config config.yml
```

## Available Plugins

### Official Plugins

| Plugin | Description | Installation |
|--------|-------------|--------------|
| **OTOBO/Znuny Plugin** | Integration with OTOBO, Znuny, and OTRS ticket systems | `pip install open-ticket-ai-otobo-znuny-plugin` |
| **HuggingFace Local** | Run classification models locally with transformers | Included in base package |

### Creating Your Own Plugin

See the [Plugin Developer Guide](docs/vitepress_docs/docs_src/en/developers/plugins.md) for instructions on creating custom plugins.

## Package Structure

This repository is organized as a monorepo:

```
open-ticket-ai/
├── src/                          # Main Open Ticket AI source code
│   ├── open_ticket_ai/          # Core framework
│   ├── open_ticket_ai_hf_local/ # HuggingFace plugin (bundled)
│   └── open_ticket_ai_otobo_znuny_plugin/  # Legacy location (backward compat)
├── packages/                     # Standalone plugin packages
│   └── open_ticket_ai_otobo_znuny_plugin/  # OTOBO/Znuny plugin (PyPI package)
├── tests/                        # Test suite
└── docs/                         # Documentation
```

## Documentation

- 📚 [Full Documentation](https://open-ticket-ai.com)
- 🚀 [Getting Started Guide](https://open-ticket-ai.com/en/guide/getting-started.html)
- 🔌 [Available Plugins](https://open-ticket-ai.com/en/guide/available-plugins.html)
- 🛠️ [Plugin Developer Guide](https://open-ticket-ai.com/en/developers/plugins.html)

## Development

### Prerequisites

- Python 3.13 or higher
- pip or uv

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Softoft-Orga/open-ticket-ai.git
   cd open-ticket-ai
   ```

2. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests:
   ```bash
   pytest
   ```

### Plugin Development

Each plugin in `packages/` is a standalone Python package that can be developed and published independently:

```bash
cd packages/open_ticket_ai_otobo_znuny_plugin
pip install -e ".[dev]"
pytest
```

See individual plugin `DEVELOPER.md` files for plugin-specific development instructions.

## Contributing

We welcome contributions! Please see our contributing guidelines for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

This project is licensed under the LGPL-2.1 License - see the [LICENSE](LICENSE) file for details.

## Support

- 🐛 [Issue Tracker](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- 💬 [Discussions](https://github.com/Softoft-Orga/open-ticket-ai/discussions)
- 📧 Email: tab@softoft.de

## Acknowledgments

Built with ❤️ by [Softoft](https://softoft.de)

Special thanks to all contributors and the open source community.
