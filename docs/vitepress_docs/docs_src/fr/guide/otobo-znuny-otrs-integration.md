---
description: Apprenez à intégrer des applications Python avec OTOBO, Znuny et OTRS en utilisant
  une bibliothèque client asynchrone. Ce guide fournit des instructions étape par étape et
  des exemples de code pour gérer les tickets de helpdesk via l'API REST, y compris la création,
  la recherche, la mise à jour et la récupération de l'historique des tickets.
---

# Guide d'Intégration OTOBO Znuny OTRS

Pour l'intégration avec OTOBO, Znuny ou OTRS, nous utilisons notre bibliothèque client Python otobo.

## Bibliothèque Client Python OTOBO

Un client Python asynchrone pour interagir avec l'API REST d'OTOBO. Conçu avec `httpx` et `pydantic` pour la sécurité des types
et la facilité d'utilisation.

### Fonctionnalités

*   Requêtes HTTP **asynchrones** utilisant `httpx.AsyncClient`
*   Modèles **Pydantic** pour la validation des données de requête et de réponse
*   Opérations CRUD complètes pour les tickets :

    *   `TicketCreate`
    *   `TicketSearch`
    *   `TicketGet`
    *   `TicketUpdate`
    *   `TicketHistoryGet`
*   **Gestion des erreurs** via `OTOBOError` pour les erreurs de l'API
*   Méthode utilitaire `search_and_get` pour combiner les résultats de recherche avec une récupération détaillée

### Installation

Installer depuis PyPI :

```bash
pip install otobo
```

### Démarrage Rapide

#### Configuration des Webservices OTOBO :

Créez un nouveau web service dans OTOBO avec la configuration suivante :
Voir le Guide d'Installation.

#### Créer un nouvel Agent

Créez un nouvel agent Otobo avec un mot de passe sécurisé et donnez-lui les permissions nécessaires pour ce que vous voulez accomplir.


#### 1. Configurer le client

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

#### 2. Initialiser le client

```python
import logging
from otobo import OTOBOClient

logging.basicConfig(level=logging.INFO)


client = OTOBOClient(config)
```

#### 3. Créer un ticket

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

#### 4. Rechercher et récupérer des tickets

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

#### 5. Mettre à jour un ticket

```python
from otobo import TicketUpdateParams

update_params = TicketUpdateParams(
    TicketID=response.TicketID,
    Ticket={"State": "closed"}
)
await client.update_ticket(update_params)
```

#### 6. Obtenir l'historique d'un ticket

```python
from otobo import TicketHistoryParams

history_params = TicketHistoryParams(TicketID=str(response.TicketID))
history_res = await client.get_ticket_history(history_params)
print(history_res.History)
```

#### 7. Recherche et récupération combinées

```python
from otobo import FullTicketSearchResponse

full_res: FullTicketSearchResponse = await client.search_and_get(search_params)
```