---
description: Learn to integrate OpenTicketAI with Zammad for on-premise AI ticket
  classification. Use the REST API to fetch, classify, and update ticket queues &
  priorities.
---
# Integrating OpenTicketAI with Zammad for Automated Ticket Classification

OpenTicketAI is an on-premise **AI ticket classifier** that automates categorization, routing, and prioritization of support tickets. To integrate it with Zammad, we implement a **ZammadAdapter** that extends OpenTicketAI’s `TicketSystemAdapter` interface. This adapter uses Zammad’s REST API to *fetch* tickets from Zammad, *run them through OpenTicketAI’s pipeline*, and *update* the ticket (queue, priority, comments) based on the AI predictions. The key components are illustrated in the architecture: OpenTicketAI’s **AdapterFactory** creates the appropriate adapter (e.g. ZammadAdapter) to communicate via REST with the ticket system. The pipeline fetches tickets, classifies them, and finally the ticket system adapter updates Zammad via its API.

OpenTicketAI’s architecture uses a modular pipeline where each ticket is processed by a series of pipes. The final *Ticket System Adapter* stage applies updates (queue, priority, notes) to the external system via REST API. In practice, you register your `ZammadAdapter` in the dependency-injection configuration so that the **BasicTicketFetcher** pipe uses it to load tickets, and the **GenericTicketUpdater** pipe uses it to apply updates.

## OpenTicketAI Pipeline Overview

OpenTicketAI runs in a *pipeline* that transforms ticket data step by step. A simplified flow is:

1. **Preprocessor** – merge/clean `subject` and `body`.
2. **Transformer / Tokenizer** – prepare text for AI.
3. **Queue Classifier** – predicts target queue/group.
4. **Priority Classifier** – predicts priority level.
5. **Postprocessor** – applies thresholds, chooses actions.
6. **Ticket System Adapter** – updates the ticket in Zammad via REST API.

Each stage takes a `PipelineContext` object (containing `ticket_id` and a `data` dict) and enriches it. For example, after the classifiers run, the context’s `data` might have keys like `new_queue`, `new_priority`, or an `article` (comment) to add. The **GenericTicketUpdater** pipe then looks for an `update_data` entry in the context and calls the adapter to apply those fields to the ticket. This design makes it easy to add new steps (e.g. a pseudonymization pipe) or to customize the update logic. The orchestrator manages these *AttributePredictors* (fetcher, preparer, AI service, modifier) based on YAML config.

## TicketSystemAdapter and ZammadAdapter

OpenTicketAI defines an abstract base class `TicketSystemAdapter` that all integrations must extend. It declares core methods like:

* `async update_ticket(ticket_id: str, data: dict) -> dict | None`: **Update** a ticket’s fields (e.g. queue, priority, add note). Must handle partial updates and return the updated ticket object.
* `async find_tickets(query: dict) -> list[dict]`: **Search** for tickets matching a query. The query format is adapter-specific, but this should return a list of matching tickets.
* `async find_first_ticket(query: dict) -> dict | None`: Convenience to return only the first match.

A **ZammadAdapter** will subclass this and implement these methods using Zammad’s API. It will typically hold configuration (base URL, credentials) injected via a `SystemConfig`. For example:

```python
from open_ticket_ai.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
import httpx


class ZammadAdapter(TicketSystemAdapter):
    def __init__(self, config):
        super().__init__(config)
        # Assume config.zammad contains URL and auth info
        self.base_url = config.zammad.base_url.rstrip('/')
        self.auth = (config.zammad.user, config.zammad.password)

    async def find_tickets(self, query: dict) -> list[dict]:
        # Use Zammad search API (e.g. full-text search or filters).
        async with httpx.AsyncClient(auth=self.auth) as client:
            params = {"query": query.get("search", "")}
            res = await client.get(f"{self.base_url}/api/v1/tickets/search", params=params)
            res.raise_for_status()
            return res.json()  # list of matching tickets (each as dict)

    async def find_first_ticket(self, query: dict) -> dict | None:
        tickets = await self.find_tickets(query)
        return tickets[0] if tickets else None

    async def update_ticket(self, ticket_id: str, data: dict) -> dict | None:
        # Send PUT to update the ticket. Data can include 'group', 'priority', etc.
        url = f"{self.base_url}/api/v1/tickets/{ticket_id}"
        async with httpx.AsyncClient(auth=self.auth) as client:
            res = await client.put(url, json=data)
            if res.status_code == 200:
                return res.json()  # updated ticket object
            return None
```

*Citation:* The base class requires these methods. In this example we use `httpx.AsyncClient` (since the methods are async), but you could similarly use `requests` in a synchronous context. For instance, fetching all tickets might be as simple as `requests.get(f"{base_url}/api/v1/tickets", auth=(user, pwd))`.

### Fetching Tickets from Zammad

Zammad’s REST API provides endpoints to list and search tickets. A simple way to fetch recent or matching tickets is via:

* **List All (paginated)**: `GET /api/v1/tickets` returns an array of ticket objects.
* **Search**: `GET /api/v1/tickets/search?query=...` supports full-text or field queries, returning matching tickets in JSON form (and `expand=true` can resolve related fields).

Your `find_tickets` implementation can use these. For example, to filter by state or subject:

```python
async with httpx.AsyncClient(auth=self.auth) as client:
    res = await client.get(f"{base_url}/api/v1/tickets/search", params={"query": "state:open OR state:new"})
    res.raise_for_status()
    tickets = res.json()  # a list of dicts
```

Then wrap or return those in the format OpenTicketAI expects (a list of ticket dicts). The `BasicTicketFetcher` pipe will call this using the ticket ID from the `PipelineContext` to load a ticket before processing.

### Updating Zammad Tickets

After classification, we update Zammad using its **Update Ticket** API. Zammad supports changing fields like group (queue) and priority, and even adding an internal note or article in one call. For example, the following payload (sent via `PUT /api/v1/tickets/{id}`) sets a new group and priority and appends an internal article:

```json
{
  "group": "Sales",
  "state": "open",
  "priority": "3 high",
  "article": {
    "subject": "AI Insight",
    "body": "Sentiment analysis: negative tone detected.",
    "internal": true
  }
}
```

This would reassign the ticket to the “Sales” group, set it to high priority, and attach a new note (internal comment) with AI insights. In code, our `update_ticket` could do:

```python
await client.put(f"{base_url}/api/v1/tickets/{ticket_id}", json={
    "group": new_queue,
    "priority": f"{priority_level} {priority_label}",
    "article": {
        "subject": "Auto-classified Ticket",
        "body": f"Queue={new_queue}, Priority={priority_label}",
        "internal": True
    }
})
```

The response will be the full updated ticket JSON if status 200. If you only need to post a comment or note, include the `article` block as above. Alternatively, smaller updates (like just setting a note) can use the ticket “note” field or a separate articles endpoint, but the bundled `article` in the PUT is convenient.

## Pipeline Integration in OpenTicketAI

To wire this into OpenTicketAI’s pipeline, you add **pipes** in `config.yml`. For example:

* **BasicTicketFetcher**: configured with `ticket_system: ZammadAdapter`. It calls `find_tickets`/`find_first_ticket` and populates `context.data` with the ticket fields.
* **Preparer**: e.g. `SubjectBodyPreparer` to combine subject/body text.
* **AI Inference Services**: your custom queue/priority classifiers (e.g. a HuggingFace model).
* **GenericTicketUpdater**: configured with `ticket_system: ZammadAdapter`. It looks for `context.data["update_data"]` after inference and calls `update_ticket`.

For example, a custom pipe might do:

```python
class QueuePriorityPredictor(Pipe):
    def process(self, context: PipelineContext) -> PipelineContext:
        subject = context.data.get("subject", "")
        body = context.data.get("body", "")
        queue_pred = my_queue_model.predict(subject + body)
        prio_pred = my_prio_model.predict(subject + body)
        # Prepare update data for Zammad
        context.data['update_data'] = {
            "group": queue_pred.group_name,
            "priority": f"{prio_pred.score} {prio_pred.label}",
            "article": {
                "subject": "AI Classification",
                "body": f"Assigned to {queue_pred.group_name}, Priority={prio_pred.label}",
                "internal": True
            }
        }
        return context
```

This sets up the `update_data` that GenericTicketUpdater will use.

Finally, the **AdapterFactory** (configured via DI) ensures that `ticket_system: Zammad` creates an instance of your `ZammadAdapter` class, injecting the base URL and auth from `config.yml`. The **GenericTicketUpdater** pipe then calls `await adapter.update_ticket(id, update_data)`, applying your AI-driven changes.

## Enhancements: Classification, Pseudonymization, and Notes

Beyond basic queue/priority, OpenTicketAI offers features to enrich the Zammad integration:

* **Queue & Priority Classification:** You can train custom models for specific Zammad queues or priority schemes. The predicted values map to Zammad’s groups and priorities (for example, the priority API uses `"priority": "2 normal"` format). By adjusting thresholds in the **postprocessor**, you can also automatically drop low-confidence predictions or escalate tickets.

* **Pseudonymization Connectors:** To protect user privacy, you can insert a custom *pipeline pipe* before inference that **pseudonymizes** or masks sensitive data (e.g. names, emails) in the ticket text. This could use regex or external services to replace PII with tokens. The masked text is then classified, and the original ticket is updated, ensuring no sensitive content leaves your system.

* **Note/Article Creation:** You can leverage Zammad’s article API to log AI insights or sentiment. As shown above, include an `article` in the update payload to add comments. Alternatively, you could configure a separate **note-creation pipe** that, regardless of updating queue/priority, always appends a ticket note with model confidence scores or sentiment analysis. These notes help agents understand *why* a decision was made.

Each enhancement fits naturally into the pipeline and is automatically applied by the GenericTicketUpdater via the adapter. For example, after running a sentiment analysis pipe, you might do:

```python
context.data['update_data'] = {
    "article": {
        "subject": "Sentiment Score",
        "body": f"Sentiment polarity: {sentiment_score}",
        "internal": True,
    },
}
```

Then the adapter will POST it as an article to Zammad.

## Benefits for Zammad Ticket Automation

With this integration, Zammad gains on-premise AI-powered automation. Incoming tickets can be auto-assigned to the correct queue and given a preliminary priority, freeing support teams to focus on urgent issues. Because OpenTicketAI runs locally, sensitive ticket data stays in-house (important for compliance). This **Zammad AI integration** turns manual triage into a streamlined process: you maintain full control and customization (via config and custom models) while leveraging OpenTicketAI’s pipeline.

In summary, implementing a **ZammadAdapter** involves subclassing `TicketSystemAdapter` and wiring it into OpenTicketAI’s pipeline. The adapter uses Zammad’s API for ticket CRUD operations (e.g. `GET /tickets` and `PUT /tickets/{id}`). Once configured, OpenTicketAI will continuously fetch tickets, run them through your AI model stack, and update Zammad with predicted queue, priority, and any notes. This **ticket system AI** integration empowers Zammad with automated classification and routing, realizing the vision of an on-premise AI ticket classifier for enterprise support teams.

**Sources:** Zammad REST API docs; OpenTicketAI developer docs.
