---
description: Integrate Python with OTOBO, Znuny, & OTRS using an async client library.
  This guide provides code examples for managing helpdesk tickets via REST API.
---

# OTOBO Znuny OTRS Integration Guide

For the Integration into OTOBO, Znuny or OTRS, we are using our otobo python client library

## Python OTOBO Client Library

An asynchronous Python client for interacting with the OTOBO REST API. Built with `httpx` and `pydantic` for type safety
and ease of use.

### Features

* **Asynchronous** HTTP requests using `httpx.AsyncClient`
* **Pydantic** models for request and response data validation
* Full CRUD operations for tickets:

    * `TicketCreate`
    * `TicketSearch`
    * `TicketGet`
    * `TicketUpdate`
    * `TicketHistoryGet`
* **Error handling** via `OTOBOError` for API errors
* Utility method `search_and_get` to combine search results with detailed retrieval

### Installation

Install from PyPI:

```bash
pip install otobo
```

### Quickstart

#### Setup OTOBO Webservices:

Create a new web service in OTOBO with the following configuration:
See Installation Guide.

#### Create a new Agent

Create a new Otobo Agent with a secure password and give it the permissions needed for the thing you want to accomplish.

#### 1. Configure the client

```python
from otobo import TicketOperation, OTOBOClientConfig
from otobo import AuthData

config = OTOBOClientConfig(
    base_url="https://your-otobo-server/nph-genericinterface.pl",
    service="OTOBO",
    auth=AuthData(UserLogin="user1", Password="SecurePassword"),
    operations={
        TicketOperation.CREATE.value: "ticket",
        TicketOperation.SEARCH.value: "ticket/search",
        TicketOperation.GET.value: "ticket/get",
        TicketOperation.UPDATE.value: "ticket",
        TicketOperation.HISTORY_GET.value: "ticket/history",
    }
)
```

#### 2. Initialize the client

```python
import logging
from otobo import OTOBOClient

logging.basicConfig(level=logging.INFO)


client = OTOBOClient(config)
```

#### 3. Create a ticket

```python
from otobo import (TicketOperation, OTOBOClientConfig, AuthData, TicketSearchParams, TicketCreateParams,
                   TicketHistoryParams, TicketUpdateParams, \
                   TicketGetParams, OTOBOClient, OTOBOTicketCreateResponse)

payload = TicketCreateParams(
    Ticket={
        "Title": "New Order",
        "Queue": "Sales",
        "State": "new",
        "Priority": "3 normal",
        "CustomerUser": "customer@example.com"
    },
    Article={
        "Subject": "Product Inquiry",
        "Body": "Please send pricing details...",
        "MimeType": "text/plain"
    }
)

response: OTOBOTicketCreateResponse = await client.create_ticket(payload)
print(response.TicketID, response.TicketNumber)
```

#### 4. Search and retrieve tickets

```python
from otobo import TicketSearchParams, TicketGetParams

search_params = TicketSearchParams(Title="%Order%")
search_res = await client.search_tickets(search_params)
ids = search_res.TicketID

for ticket_id in ids:
    get_params = TicketGetParams(TicketID=ticket_id, AllArticles=1)
    details = await client.get_ticket(get_params)
    print(details.Ticket[0])
```

#### 5. Update a ticket

```python
from otobo import TicketUpdateParams

update_params = TicketUpdateParams(
    TicketID=response.TicketID,
    Ticket={"State": "closed"}
)
await client.update_ticket(update_params)
```

#### 6. Get ticket history

```python
from otobo import TicketHistoryParams

history_params = TicketHistoryParams(TicketID=str(response.TicketID))
history_res = await client.get_ticket_history(history_params)
print(history_res.History)
```

#### 7. Combined search and get

```python
from otobo import FullTicketSearchResponse

full_res: FullTicketSearchResponse = await client.search_and_get(search_params)
```
