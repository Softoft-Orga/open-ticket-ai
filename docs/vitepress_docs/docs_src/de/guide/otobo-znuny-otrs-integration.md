---
description: Erfahren Sie, wie Sie Python-Anwendungen mit OTOBO, Znuny und OTRS über eine asynchrone Client-Bibliothek integrieren. Diese Anleitung bietet schrittweise Anweisungen und Codebeispiele für die Verwaltung von Helpdesk-Tickets über die REST-API, einschließlich Erstellen, Suchen, Aktualisieren und Abrufen des Ticket-Verlaufs.
---

# OTOBO Znuny OTRS Integrationsanleitung

Für die Integration in OTOBO, Znuny oder OTRS verwenden wir unsere otobo Python Client-Bibliothek.

## Python OTOBO Client-Bibliothek

Ein asynchroner Python-Client zur Interaktion mit der OTOBO REST API. Entwickelt mit `httpx` und `pydantic` für Typsicherheit und einfache Bedienung.

### Funktionen

* **Asynchrone** HTTP-Anfragen mit `httpx.AsyncClient`
* **Pydantic**-Modelle zur Validierung von Anfrage- und Antwortdaten
* Vollständige CRUD-Operationen für Tickets:

  * `TicketCreate`
  * `TicketSearch`
  * `TicketGet`
  * `TicketUpdate`
  * `TicketHistoryGet`
* **Fehlerbehandlung** über `OTOBOError` für API-Fehler
* Hilfsmethode `search_and_get`, um Suchergebnisse mit einem detaillierten Abruf zu kombinieren

### Installation

Installation von PyPI:

```bash
pip install otobo
```

### Schnellstart

#### OTOBO Webservices einrichten:

Erstellen Sie einen neuen Web-Service in OTOBO mit der folgenden Konfiguration:
Siehe Installationsanleitung.

#### Einen neuen Agenten erstellen

Erstellen Sie einen neuen Otobo-Agenten mit einem sicheren Passwort und geben Sie ihm die Berechtigungen, die für die gewünschte Aufgabe erforderlich sind.


#### 1. Den Client konfigurieren

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

#### 2. Den Client initialisieren

```python
import logging
from otobo import OTOBOClient

logging.basicConfig(level=logging.INFO)


client = OTOBOClient(config)
```

#### 3. Ein Ticket erstellen

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

#### 4. Tickets suchen und abrufen

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

#### 5. Ein Ticket aktualisieren

```python
from otobo import TicketUpdateParams

update_params = TicketUpdateParams(
    TicketID=response.TicketID,
    Ticket={"State": "closed"}
)
await client.update_ticket(update_params)
```

#### 6. Ticket-Verlauf abrufen

```python
from otobo import TicketHistoryParams

history_params = TicketHistoryParams(TicketID=str(response.TicketID))
history_res = await client.get_ticket_history(history_params)
print(history_res.History)
```

#### 7. Kombinierte Suche und Abruf

```python
from otobo import FullTicketSearchResponse

full_res: FullTicketSearchResponse = await client.search_and_get(search_params)
```