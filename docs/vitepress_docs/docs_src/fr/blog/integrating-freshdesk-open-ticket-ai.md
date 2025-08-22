---
description: Intégrez Open Ticket AI sur site (on-premise) avec Freshdesk pour la
  classification automatisée des tickets. Apprenez à créer un adaptateur Python personnalisé
  pour mettre à jour les tickets via l'API REST.
---
# Intégration de l'IA Freshdesk avec Open Ticket AI

Open Ticket AI (OTAI) est un système local, sur site (on-premise), de **classification de tickets** (également appelé ATC Community Edition) qui automatise la catégorisation et le routage des tickets de support. Freshdesk est une plateforme populaire de support client basée sur le cloud, dotée de ses propres outils d'IA, qui propose la gestion de tickets, des workflows et des rapports. En écrivant un *TicketSystemAdapter* personnalisé, vous pouvez intégrer OTAI avec Freshdesk et mettre à jour les tickets Freshdesk automatiquement via son API REST. Cela permet un tri de tickets piloté par l'IA au sein de l'environnement Freshdesk. Dans le pipeline d'Open Ticket AI, l'étape finale est un **TicketSystemAdapter** qui applique les prédictions de l'IA au système de tickets via des appels REST. Pour étendre OTAI à Freshdesk, vous implémentez un `FreshdeskAdapter` qui est une sous-classe de `TicketSystemAdapter` et qui met en œuvre des méthodes pour interroger et mettre à jour les tickets dans Freshdesk.

&#x20;*Figure : Diagramme de classes UML de l'architecture d'Open Ticket AI. La classe abstraite `TicketSystemAdapter` fournit une base pour les adaptateurs spécifiques à un système (par exemple, un OTOBOAdapter) qui se connectent à des systèmes de tickets externes.* L'architecture d'OTAI est modulaire : les tickets entrants passent par des classifieurs NLP et un **TicketSystemAdapter** écrit ensuite les résultats dans le système de tickets. La documentation explique que `TicketSystemAdapter` est une classe de base abstraite « que tous les adaptateurs de système de tickets concrets doivent implémenter » pour interagir avec différentes plateformes de tickets. Les sous-classes doivent implémenter trois méthodes `async` principales : `update_ticket(ticket_id, data)`, `find_tickets(query)`, et `find_first_ticket(query)`. En pratique, vous créeriez une nouvelle `class` Python, par exemple `class FreshdeskAdapter(TicketSystemAdapter)`, et surchargeriez ces méthodes. Par exemple :

```python
import aiohttp

from open_ticket_ai.src.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


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

Le code ci-dessus montre un **FreshdeskAdapter** simple. Il récupère le domaine Freshdesk (le nom de l'entreprise) et la clé d'API depuis la configuration d'OTAI (`self.config`) qui est injectée à l'exécution. Il utilise ensuite `aiohttp` de Python pour les appels HTTP `async`. La méthode `update_ticket` émet une requête PUT vers `https://<domain>.freshdesk.com/api/v2/tickets/<id>` avec la charge utile JSON des champs à modifier. La méthode `find_tickets` utilise GET sur `/api/v2/tickets` avec des paramètres de requête (ou vous pourriez appeler `/api/v2/search/tickets` pour des recherches plus complexes). L'API Freshdesk nécessite une authentification de base (basic auth) : votre clé d'API (depuis votre profil Freshdesk) est utilisée comme nom d'utilisateur et n'importe quel mot de passe (souvent juste « X ») comme mot de passe.

**Étapes clés pour intégrer Freshdesk :**

* *Configurer l'accès à l'API :* Connectez-vous à Freshdesk et récupérez votre **clé d'API** depuis votre profil (cette clé est utilisée pour authentifier les requêtes API). Notez également votre domaine Freshdesk (le sous-domaine dans votre URL Freshdesk).
* *Implémenter l'adaptateur :* Créez une `class` `FreshdeskAdapter` qui étend `TicketSystemAdapter` et implémentez `update_ticket`, `find_tickets`, et `find_first_ticket`. Dans ces méthodes, utilisez les points de terminaison de l'API REST de Freshdesk (par ex. `GET /api/v2/tickets` et `PUT /api/v2/tickets/{id}`).
* *Configurer OTAI :* Mettez à jour le fichier `config.yml` d'OTAI pour inclure le `FreshdeskAdapter` et ses paramètres (tels que `freshdesk_domain` et `freshdesk_api_key`). Grâce au système d'injection de dépendances d'OTAI, le nouvel adaptateur sera chargé à l'exécution.
* *Lancer la classification :* Démarrez Open Ticket AI (par ex. via `python -m open_ticket_ai.src.ce.main start`). Au fur et à mesure que de nouveaux tickets sont récupérés, le pipeline les classifiera puis appellera votre `FreshdeskAdapter.update_ticket(...)` pour réécrire la file d'attente ou la priorité prédite dans Freshdesk.

En utilisant cet adaptateur personnalisé, les tickets Freshdesk transitent par le pipeline d'OTAI comme n'importe quel autre système de tickets. Une fois qu'OTAI a attribué un ID de file d'attente ou une priorité, l'appel `update_ticket` renverra cette information à Freshdesk via son API. Cela permet aux utilisateurs de Freshdesk de tirer parti des modèles d'IA d'OTAI pour la *classification automatisée des tickets* tout en continuant à travailler sur la plateforme Freshdesk. L'API REST flexible de Freshdesk (qui prend en charge la recherche, le listage, la création et la mise à jour des tickets) rend cette intégration simple. En suivant le modèle d'adaptateur d'OTAI et les conventions de l'API Freshdesk, les développeurs peuvent intégrer de manière transparente le tri de tickets piloté par l'IA dans Freshdesk sans dépendre d'une IA propriétaire sur le cloud – en gardant toutes les données en local si désiré.

**Références :** La documentation d'Open Ticket AI explique son architecture d'adaptateur et l'interface `TicketSystemAdapter`. L'aperçu de l'architecture d'OTAI montre l'étape de l'adaptateur dans le pipeline. Le guide de l'API et les blogs pour développeurs de Freshdesk documentent comment s'authentifier (avec une clé d'API) et appeler les points de terminaison des tickets. Ensemble, ces sources décrivent les étapes pour construire une intégration Freshdesk personnalisée.