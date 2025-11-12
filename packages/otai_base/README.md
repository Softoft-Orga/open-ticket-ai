# otai-base

Base package with core implementations for Open Ticket AI - ticket system automation and AI integration.

## Overview

`otai-base` provides foundational abstractions and utilities for building Open Ticket AI plugins. It includes:

- **Core data models** using Pydantic v2 for type-safe ticket system operations
- **Plugin interfaces** for extending Open Ticket AI with custom ticket system integrations
- **Template rendering** with Jinja2 for dynamic content generation
- **Unified ticket abstractions** for working across multiple ticket systems

## Installation

```bash
pip install otai-base
```

For development:

```bash
pip install otai-base[dev]
```

## Usage

### Creating a Plugin

```python
from otai_base.base_plugin import BasePlugin

class MyTicketSystemPlugin(BasePlugin):
    name = "my-ticket-system"

    # Implement plugin interface methods
```

### Using Core Models

```python
from otai_base.models import UnifiedTicket, UnifiedEntity

ticket = UnifiedTicket(
    subject="Example Ticket",
    body="Ticket description",
    queue=UnifiedEntity(name="Support"),
    priority=UnifiedEntity(name="High"),
)
```

## Features

- 🎯 **Type-safe** - Full type hints and Pydantic validation
- 🔌 **Extensible** - Plugin system for custom integrations
- 🎨 **Template support** - Jinja2 integration for dynamic content
- 🔄 **Unified interface** - Work with multiple ticket systems using a single API
- 🐍 **Modern Python** - Requires Python 3.13+

## Documentation

Full documentation is available at [open-ticket-ai.com](https://open-ticket-ai.com).

## Requirements

- Python 3.13 or higher
- Pydantic 2.11.7+
- Jinja2 3.1.0+

## Contributing

Contributions are welcome! Please see the [main repository](https://github.com/Softoft-Orga/open-ticket-ai) for contribution guidelines.

## License

LGPL-2.1-only - See [LICENSE](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/LICENSE) for details.

## Related Packages

- [`open-ticket-ai`](https://pypi.org/project/open-ticket-ai/) - Core application
- [`otai-zammad`](https://pypi.org/project/otai-zammad/) - Zammad integration
- [`otai-otobo-znuny`](https://pypi.org/project/otai-otobo-znuny/) - OTOBO/Znuny integration
- [`otai-hf-local`](https://pypi.org/project/otai-hf-local/) - Local AI model integration

## Links

- **Homepage**: [open-ticket-ai.com](https://open-ticket-ai.com)
- **Repository**: [GitHub](https://github.com/Softoft-Orga/open-ticket-ai)
- **Issue Tracker**: [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- **PyPI**: [pypi.org/project/otai-base](https://pypi.org/project/otai-base/)

