---
description: Integrate Zendesk with Open Ticket AI for automated ticket classification.
  Build a custom Python adapter to auto-triage tickets by priority via REST API.
---
# Integrating Zendesk with Open Ticket AI for Automated Ticket Classification

In modern support workflows, AI can help **Zendesk** agents by auto-triaging
tickets. [Open Ticket AI](https://ticket-classification.softoft.de) (OTAI) is an on-premises tool that analyzes incoming
tickets and predicts their priority, queue/category, tags, and more via a REST API. By plugging OTAI into Zendesk,
support teams can automatically assign priorities or tags based on AI, improving response time and consistency. This
article shows developers how to build a custom **ZendeskAdapter** for OTAI by extending the existing
`TicketSystemAdapter` and calling the Zendesk REST API.

## OTAI Architecture and TicketSystemAdapter

Open Ticket AI uses a **modular pipeline** architecture. Each incoming ticket is preprocessed, passed through queue and
priority classifiers, and finally sent back to the ticketing system via an adapter. The key component here is the *
*TicketSystemAdapter** (an abstract base class) which defines how to update or query tickets in an external system.
Built-in adapters (e.g. for OTOBO) inherit from this base class. For Zendesk, we'll create a new subclass.

&#x20;*Figure: Open Ticket AI’s architecture (extracted from the UML class diagram). The pipeline stages (preprocessing,
classification, etc.) culminate in a **TicketSystemAdapter**, which sends updates to the external ticket system via
REST. Extending OTAI with Zendesk involves subclassing this adapter so that AI results (priority, tags, etc.) are
written into Zendesk tickets.*

In practice, OTAI is configured via YAML and relies on **dependency injection**. All components (fetchers, classifiers,
modifiers, etc.) are defined in `config.yml` and assembled at startup. The documentation notes that “Custom fetchers,
preparers, AI services, or modifiers can be implemented as Python classes and registered via the configuration. Thanks
to dependency injection, new components can be easily integrated.”. In other words, adding a `ZendeskAdapter` is
straightforward: we implement it as a Python class and declare it in the config.

## Steps to Add a Zendesk Adapter

Follow these steps to integrate Zendesk into OTAI:

1. **Subclass `TicketSystemAdapter`**: Create a new adapter class (e.g. `ZendeskAdapter`) that extends the abstract
   `TicketSystemAdapter`. This class will implement how OTAI reads from or writes to Zendesk.
2. **Implement `update_ticket`**: In `ZendeskAdapter`, override the
   `async def update_ticket(self, ticket_id: str, data: dict)` method. This method should send an HTTP request to
   Zendesk to update the given ticket’s fields (e.g. priority, tags). For example, you will `PUT` to
   `https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json` with a JSON payload containing the fields to
   update.
3. **(Optional) Implement search methods**: You can also override `find_tickets(self, query: dict)` or
   `find_first_ticket(self, query: dict)` if you need to fetch tickets from Zendesk (e.g. to get new tickets). These
   methods should call Zendesk’s GET endpoints (such as `/api/v2/tickets.json` or the search API) and return ticket data
   as Python dictionaries.
4. **Configure Credentials**: Add your Zendesk credentials to OTAI’s configuration. For example, store the **subdomain
   **, **user email**, and **API token** in `config.yml` or environment variables. The adapter can read these from the
   injected `SystemConfig` (passed in the constructor).
5. **Register the Adapter**: Update `config.yml` so that OTAI uses `ZendeskAdapter` as its ticket system integration.
   OTAI’s DI framework will then instantiate your class with the config parameters.

These steps leverage OTAI’s extensibility. The pipeline is defined in config (no REST needed for triggering
classification), so simply plugging in your adapter makes the pipeline use Zendesk as the target system.

## Example: Implementing `ZendeskAdapter`

Below is a sketch of what the Python adapter might look like. It initializes with config values and implements
`update_ticket` using Python’s `requests` library. The code below is illustrative; you’ll need to install `requests` (or
use `httpx`/`aiohttp` for async) and handle errors as needed:

```python
import requests
from open_ticket_ai.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


class ZendeskAdapter(TicketSystemAdapter):
    def __init__(self, config):
        super().__init__(config)
        # Read Zendesk settings from config (defined in config.yml)
        self.subdomain = config.zendesk_subdomain
        self.user_email = config.zendesk_user_email
        self.api_token = config.zendesk_api_token

    async def update_ticket(self, ticket_id: str, data: dict) -> dict | None:
        """
        Update a Zendesk ticket with the provided data (dict of fields).
        Uses Zendesk Tickets API to apply changes.
        """
        url = f"https://{self.subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json"
        # Zendesk expects a JSON object with "ticket": { ...fields... }
        payload = {"ticket": data}
        auth = (f"{self.user_email}/token", self.api_token)
        response = requests.put(url, json=payload, auth=auth)
        if response.status_code == 200:
            return response.json().get("ticket")
        else:
            # Log or handle errors (e.g., invalid ID or auth)
            return None

    async def find_tickets(self, query: dict) -> list[dict]:
        """
        (Optional) Search for tickets. Query could include filtering criteria.
        This example uses Zendesk's search endpoint.
        """
        query_str = query.get("query", "")  # e.g. "status<solved"
        url = f"https://{self.subdomain}.zendesk.com/api/v2/search.json?query={query_str}"
        auth = (f"{self.user_email}/token", self.api_token)
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
```

This `ZendeskAdapter` constructor pulls settings from the injected `config`. The `update_ticket` method builds the URL
using the standard Zendesk pattern and sends a PUT request. In this example, we authenticate with HTTP Basic Auth using
the Zendesk email and API token (by convention, the username is `user_email/token`). The payload wraps the ticket data
under the `"ticket"` key as Zendesk’s API expects. After a successful update, it returns the updated ticket JSON.

You would define `config.zendesk_subdomain`, `config.zendesk_user_email`, and `config.zendesk_api_token` in
`config.yml`. For example:

```yaml
ticket_system_integration:
    adapter: open_ticket_ai.src.ce.ticket_system_integration.zendesk_adapter.ZendeskAdapter
    zendesk_subdomain: "mycompany"
    zendesk_user_email: "agent@mycompany.com"
    zendesk_api_token: "ABCD1234TOKEN"
```

This tells OTAI to use `ZendeskAdapter`. OTAI’s dependency injection will then construct your adapter with these values.

## Calling the Zendesk REST API

The key to the adapter is making HTTP requests to Zendesk’s API endpoints. As shown above, OTAI’s adapter calls URLs
like `https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json`. According to Zendesk’s docs, updating a ticket
requires a PUT to that URL with a JSON body (for example, `{"ticket": {"priority": "high", "tags": ["urgent"]}}` if you
want to set priority and tags). In the example script above, `requests.put(url, json=payload, auth=auth)` handles this.

For completeness, you may also implement ticket creation (`requests.post(...)`) or other API calls. But for
classification, usually only **updating existing tickets** is needed (to write back the AI’s predicted fields). Ensure
that the Zendesk API token has the necessary permissions, and that you set “Token Access” enabled in Zendesk Admin.

If you also want to fetch tickets from Zendesk (for example, to find newly created tickets to process), use Zendesk’s
list or search APIs. For instance, you could GET `/api/v2/tickets.json` to page through tickets, or use
`/api/v2/search.json?query=type:ticket status:new` to find all new tickets. Return the JSON to OTAI as a list of ticket
dicts from `find_tickets()`.

## Pipeline and Usage

With the `ZendeskAdapter` in place, running OTAI will incorporate it seamlessly into the pipeline. For example, after
setting up your AI models (queue and priority predictors), starting OTAI’s scheduler (e.g.
`python -m open_ticket_ai.src.ce.main start`) will trigger the pipeline. OTAI will use your adapter as the final
“modifier” step: after the AI infers attributes for each ticket, it calls `ZendeskAdapter.update_ticket` to apply those
attributes back to Zendesk. The whole process remains transparent to OTAI – it only knows it’s calling `update_ticket`
on an adapter class.

Because OTAI’s components are defined in YAML, you can configure how often it fetches or checks for tickets and how it
applies updates. The developer docs emphasize that all components are pluggable via config and DI. So once your adapter
is implemented and wired up in `config.yml`, no further code changes are needed to include Zendesk in the ticket flow.
