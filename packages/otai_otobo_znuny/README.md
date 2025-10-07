# OTOBO/Znuny Plugin for Open Ticket AI

This plugin provides integration with OTOBO and Znuny ticket systems for Open Ticket AI.

## Installation

```bash
pip install otai-otobo-znuny
```

## Configuration

The plugin requires the following configuration in your Open Ticket AI config file:

```yaml
open_ticket_ai:
  defs:
    - id: "otobo_znuny"
      use: "otai_otobo_znuny.OTOBOZnunyTicketSystemService"
      base_url: "https://your-otobo-instance.com"
      webservice_name: "OpenTicketAI"
      username: "open_ticket_ai"
      password: "{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}"
      operation_urls:
        search: "ticket-search"
        get: "ticket-get"
        update: "ticket-update"
```

## Setup

You can use the CLI to help set up the plugin:

```bash
open-ticket-ai otobo-znuny setup
```

This will guide you through the setup process and optionally generate a configuration file.

## Requirements

- Python 3.13+
- open-ticket-ai >= 1.0.0rc1
- otobo-znuny >= 1.4.0

## License

LGPL-2.1-only

## Links

- Homepage: https://open-ticket-ai.com
- Documentation: https://open-ticket-ai.com/en/guide/available-plugins.html
- Repository: https://github.com/Softoft-Orga/open-ticket-ai
