# Open Ticket AI OTOBO/Znuny Plugin

OTOBO/Znuny/OTRS ticket system integration plugin for Open Ticket AI.

## Overview

This plugin enables Open Ticket AI to connect to OTOBO, Znuny, and legacy OTRS ticketing systems via their GenericInterface REST API. It provides a unified interface for searching, fetching, updating tickets, and adding notes.

## Features

- Search and fetch tickets from OTOBO/Znuny/OTRS
- Update ticket fields (queue, priority, etc.)
- Add notes/articles to tickets
- Unified ticket model for seamless integration with Open Ticket AI pipelines
- Interactive CLI setup wizard for easy configuration

## Installation

Install from PyPI:

```bash
pip install open-ticket-ai-otobo-znuny-plugin
```

## Quick Start

The plugin includes an interactive CLI setup wizard to help you get started:

```bash
otai otobo-znuny setup
```

This will guide you through:
- Entering your OTOBO/Znuny instance URL
- Configuring web service details
- Testing the connection (optional)
- Generating a configuration file

### Non-interactive Setup

You can also provide all options via command-line flags:

```bash
otai otobo-znuny setup \
  --base-url "https://your-otobo.com/otrs" \
  --webservice-name "OpenTicketAI" \
  --username "open_ticket_ai" \
  --password "your-password" \
  --verify-connection \
  --output-config config.yml
```

## Prerequisites

1. A running OTOBO/Znuny/OTRS instance with GenericInterface enabled
2. A dedicated web service configured for Open Ticket AI
3. An agent user with appropriate permissions:
   - Search tickets
   - Read ticket details
   - Update tickets
   - Add articles/notes

## Configuration

Add the plugin to your Open Ticket AI configuration:

```yaml
open_ticket_ai:
  defs:
    - id: "otobo_znuny"
      use: "open_ticket_ai_otobo_znuny_plugin:OTOBOZnunyTicketSystemService"
      base_url: "https://your-otobo-instance.com/otobo/nph-genericinterface.pl"
      webservice_name: "OpenTicketAI"
      username: "open_ticket_ai"
      password: "{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}"
      operation_urls:
        ticket-search: "ticket-search"
        ticket-get: "ticket-get"
        ticket-update: "ticket-update"
```

### Configuration Parameters

- **base_url**: Base URL of your OTOBO/Znuny GenericInterface endpoint
- **webservice_name**: Name of the web service configured in OTOBO/Znuny (default: "OpenTicketAI")
- **username**: Agent username for authentication (default: "open_ticket_ai")
- **password**: Agent password (use environment variable substitution for security)
- **operation_urls**: Mapping of operations to their endpoint paths

## Usage in Pipelines

### Fetch Tickets

```yaml
- id: ticket_fetcher
  use: "open_ticket_ai.base:FetchTicketsPipe"
  injects: { ticket_system: "otobo_znuny" }
  ticket_search_criteria:
    queue.name: "MyQueue"
    limit: 10
```

### Update Ticket

```yaml
- id: update_ticket
  use: "open_ticket_ai.base:UpdateTicketsPipe"
  injects: { ticket_system: "otobo_znuny" }
  ticket_id: "{{ config.ticket.id }}"
  updated_ticket:
    queue:
      name: "NewQueue"
    priority:
      name: "high"
```

### Add Note

```yaml
- id: add_note
  use: "open_ticket_ai.base:AddNoteTicketsPipe"
  injects: { ticket_system: "otobo_znuny" }
  ticket_id: "{{ config.ticket.id }}"
  note:
    subject: "Classification Result"
    body: "Ticket was automatically classified."
```

## Runtime Behavior

- **Initialization**: On startup, the service instantiates the OTOBO/Znuny client, authenticates via GenericInterface, and keeps the session ready for subsequent requests.
- **Fetching Tickets**: Search criteria (queue, limit, etc.) are translated to OTOBO search payloads and returned as unified tickets.
- **Updating & Notes**: Updates build a `TicketUpdate` request and can optionally append a new article, enabling both field changes and audit notes in one operation.

## Development

### Running Tests

```bash
pytest tests/
```

### Building the Package

```bash
python -m build
```

## License

LGPL-2.1-only

## Links

- [Open Ticket AI Homepage](https://open-ticket-ai.com)
- [Documentation](https://open-ticket-ai.com/en/guide/available-plugins.html)
- [GitHub Repository](https://github.com/Softoft-Orga/open-ticket-ai)

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/Softoft-Orga/open-ticket-ai).
