---
description: Integrate on-premise Open Ticket AI with Freshdesk for automated ticket
  classification. Learn to create a custom Python adapter to update tickets via the
  REST API.
---
# Freshdesk AI Integration with Open Ticket AI

Open Ticket AI (OTAI) is a local, on-premise **ticket classification** system (also called ATC Community Edition) that automates support ticket categorization and routing. Freshdesk is a popular cloud-based customer support platform with its own AI tools, offering ticketing, workflows and reporting. By writing a custom *TicketSystemAdapter*, you can integrate OTAI with Freshdesk and update Freshdesk tickets automatically via its REST API. This unlocks AI-driven ticket triage within the Freshdesk environment. In the Open Ticket AI pipeline, the final stage is a **TicketSystemAdapter** that applies AI predictions to the ticket system via REST calls. To extend OTAI for Freshdesk, you implement a `FreshdeskAdapter` that subclasses `TicketSystemAdapter` and implements methods to query and update tickets in Freshdesk.

&#x20;*Figure: UML class diagram from the Open Ticket AI architecture. The abstract `TicketSystemAdapter` class provides a base for system-specific adapters (e.g. an OTOBOAdapter) that connect to external ticket systems.* The OTAI architecture is modular: incoming tickets go through NLP classifiers and a **TicketSystemAdapter** then writes the results back to the ticket system. The documentation explains that `TicketSystemAdapter` is an abstract base class “that all concrete ticket system adapters must implement” to interact with different ticket platforms. Subclasses must implement three core async methods: `update_ticket(ticket_id, data)`, `find_tickets(query)`, and `find_first_ticket(query)`. In practice, you would create a new Python class, e.g. `class FreshdeskAdapter(TicketSystemAdapter)`, and override those methods. For example:

```python
import aiohttp

from open_ticket_ai.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


class FreshdeskAdapter(TicketSystemAdapter):
    async def update_ticket(self, ticket_id: str, data: dict) -> dict:
        # Construct Freshdesk API URL for updating a ticket
        base = f"https://{self.config.freshdesk_domain}.freshdesk.com"
        url = f"{base}/api/v2/tickets/{ticket_id}"
        auth = aiohttp.BasicAuth(self.config.freshdesk_api_key, password="X")
        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.put(url, json=data) as resp:
                return await resp.json()

    async def find_tickets(self, query: dict) -> list[dict]:
        # Use Freshdesk List Tickets or Search API to retrieve tickets matching query
        base = f"https://{self.config.freshdesk_domain}.freshdesk.com"
        params = {k: v for k, v in query.items()}
        url = f"{base}/api/v2/tickets"
        async with aiohttp.ClientSession(
                auth=aiohttp.BasicAuth(self.config.freshdesk_api_key, password="X"),
        ) as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()
                return data.get('tickets', [])

    async def find_first_ticket(self, query: dict) -> dict:
        tickets = await self.find_tickets(query)
        return tickets[0] if tickets else None
```

The code above shows a simple **FreshdeskAdapter**. It pulls the Freshdesk domain (the company name) and API key from the OTAI configuration (`self.config`) that is injected at runtime. It then uses Python’s `aiohttp` for async HTTP calls. The `update_ticket` method issues a PUT to `https://<domain>.freshdesk.com/api/v2/tickets/<id>` with the JSON payload of fields to change. The `find_tickets` method uses GET on `/api/v2/tickets` with query params (or you could call `/api/v2/search/tickets` for more complex searches). The Freshdesk API requires basic auth: your API key (from your Freshdesk profile) is used as the username and any password (often just “X”) as the password.

**Key Steps to Integrate Freshdesk:**

* *Configure API access:* Log into Freshdesk and get your **API key** from the profile (this key is used to authenticate API requests). Also note your Freshdesk domain (the subdomain in your Freshdesk URL).
* *Implement the Adapter:* Create a class `FreshdeskAdapter` extending `TicketSystemAdapter` and implement `update_ticket`, `find_tickets`, and `find_first_ticket`. In these methods, use Freshdesk’s REST API endpoints (e.g. `GET /api/v2/tickets` and `PUT /api/v2/tickets/{id}`).
* *Configure OTAI:* Update the OTAI `config.yml` to include the `FreshdeskAdapter` and its settings (such as `freshdesk_domain` and `freshdesk_api_key`). Thanks to OTAI’s dependency-injection setup, the new adapter will be loaded at runtime.
* *Run Classification:* Start Open Ticket AI (e.g. via `python -m open_ticket_ai.src.ce.main start`). As new tickets are fetched, the pipeline will classify them and then call your `FreshdeskAdapter.update_ticket(...)` to write the predicted queue or priority back into Freshdesk.

Using this custom adapter, Freshdesk tickets flow through the OTAI pipeline just like any other ticket system. Once OTAI assigns a queue ID or priority, the `update_ticket` call will push that back to Freshdesk via its API. This allows Freshdesk users to leverage OTAI’s AI models for *automated ticket classification* while still working inside the Freshdesk platform. Freshdesk’s flexible REST API (which supports searching, listing, creating and updating tickets) makes this integration straightforward. By following the OTAI adapter pattern and the Freshdesk API conventions, developers can seamlessly embed AI-driven ticket triage into Freshdesk without relying on proprietary cloud AI – keeping all data local if desired.

**References:** Open Ticket AI’s documentation explains its adapter architecture and `TicketSystemAdapter` interface. The OTAI architecture overview shows the adapter step in the pipeline. Freshdesk’s API guide and developer blogs document how to authenticate (with an API key) and call ticket endpoints. Together, these sources outline the steps for building a custom Freshdesk integration.
