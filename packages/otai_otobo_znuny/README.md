# otai-otobo-znuny

OTOBO and Znuny (OTRS fork) ticket system integration plugin for Open Ticket AI - automated helpdesk workflows.

## Overview

`otai-otobo-znuny` provides comprehensive integration between Open Ticket AI and OTOBO/Znuny ticket systems. It supports both OTOBO and Znuny (formerly OTRS) instances, enabling automated ticket management and intelligent workflow automation.

## Features

- 🎫 **Full CRUD operations** - Create, read, update, and delete tickets
- 🔍 **Ticket search** - Query tickets across queues and states
- 📝 **Article management** - Add notes and articles to tickets
- 🔄 **Dual compatibility** - Works with both OTOBO and Znuny
- 🔐 **Secure authentication** - Session-based or token authentication
- 🎯 **Type-safe** - Full Pydantic v2 validation

## Installation

```bash
pip install otai-otobo-znuny
```

## Configuration

Add the plugin to your Open Ticket AI configuration:

```yaml
ticketsystem_service:
  type: otobo_znuny
  params:
    webservice_url: "https://your-otobo.example.com/otrs/nph-genericinterface.pl/Webservice/GenericTicketConnectorREST"
    username: "api-user"
    password: "api-password"
```

## Usage

### Programmatic Usage

```python
from otai_otobo_znuny import OTOBOZnunyTicketsystemService
from open_ticket_ai.models import UnifiedTicket, UnifiedEntity

# Initialize service
service = OTOBOZnunyTicketsystemService(
    webservice_url="https://your-otobo.example.com/otrs/nph-genericinterface.pl/Webservice/GenericTicketConnectorREST",
    username="api-user",
    password="api-password"
)

# Create a ticket
ticket = await service.create_ticket(
    UnifiedTicket(
        subject="System Error",
        body="Database connection failed",
        queue=UnifiedEntity(name="System::Database"),
        priority=UnifiedEntity(name="3 normal"),
        customer=UnifiedEntity(name="admin@example.com")
    )
)
```

### With Open Ticket AI

```python
from open_ticket_ai import OpenTicketAI

# Load configuration
app = OpenTicketAI.from_yaml("config.yml")

# Use the OTOBO/Znuny service
tickets = await app.ticketsystem.find_tickets(limit=10)
```

## Requirements

- Python 3.13 or higher
- OTOBO or Znuny instance with REST webservice configured
- Valid API credentials

## Documentation

- **Full docs**: [open-ticket-ai.com](https://open-ticket-ai.com/en/guide/available-plugins.html)
- **OTOBO docs**: [doc.otobo.org](https://doc.otobo.org/)
- **Znuny docs**: [doc.znuny.org](https://doc.znuny.org/)

## Contributing

Contributions welcome! See the [main repository](https://github.com/Softoft-Orga/open-ticket-ai) for guidelines.

## License

LGPL-2.1-only - See [LICENSE](https://github.com/Softoft-Orga/open-ticket-ai/blob/main/LICENSE).

## Related Packages

- [`open-ticket-ai`](https://pypi.org/project/open-ticket-ai/) - Core application
- [`otai-base`](https://pypi.org/project/otai-base/) - Base plugin framework
- [`otai-zammad`](https://pypi.org/project/otai-zammad/) - Zammad integration
- [`otai-hf-local`](https://pypi.org/project/otai-hf-local/) - Local AI model integration

## Links

- **Homepage**: [open-ticket-ai.com](https://open-ticket-ai.com)
- **Repository**: [GitHub](https://github.com/Softoft-Orga/open-ticket-ai)
- **Issue Tracker**: [GitHub Issues](https://github.com/Softoft-Orga/open-ticket-ai/issues)
- **PyPI**: [pypi.org/project/otai-otobo-znuny](https://pypi.org/project/otai-otobo-znuny/)

