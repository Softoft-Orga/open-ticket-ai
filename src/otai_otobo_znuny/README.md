# open-ticket-ai-otobo-znuny-plugin

OTOBO/Znuny ticket system integration plugin for Open Ticket AI.

This plugin provides seamless integration with OTOBO and Znuny ticket systems.

## Installation

```bash
pip install open-ticket-ai-otobo-znuny-plugin
```

Or with Open Ticket AI extras:

```bash
pip install open-ticket-ai[otobo-znuny]
```

## Quick Setup

The plugin includes an interactive CLI setup wizard:

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

## Requirements

- Python >= 3.13
- open-ticket-ai >= 1.0.0rc1
- otobo-znuny >= 1.4.0

## Usage

This plugin integrates with the Open Ticket AI pipeline system. See the main [Open Ticket AI documentation](https://open-ticket-ai.com) for configuration examples.

After running the setup command, you'll have a configuration file that you can use with Open Ticket AI.

## OTOBO/Znuny Prerequisites

1. Create a dedicated API web service in OTOBO/Znuny
2. Create an agent with permissions to search, read, update tickets, and add articles
3. Configure the web service with the following operations:
   - `ticket-search`: Search for tickets
   - `ticket-get`: Get ticket details
   - `ticket-update`: Update ticket fields

## License

LGPL-2.1-only
