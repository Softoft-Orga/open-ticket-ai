---
description: Intégrez Zendesk avec Open Ticket AI pour la classification automatisée des tickets. Créez un adaptateur Python personnalisé pour trier automatiquement les tickets par priorité via une API REST.
---
# Intégration de Zendesk avec Open Ticket AI pour la classification automatisée des tickets

Dans les flux de travail de support modernes, l'IA peut aider les agents **Zendesk** en triant automatiquement
les tickets. [Open Ticket AI](https://ticket-classification.softoft.de) (OTAI) est un outil sur site (on-premises) qui analyse les tickets entrants
et prédit leur priorité, leur file d'attente/catégorie, leurs tags, et plus encore via une API REST. En connectant OTAI à Zendesk,
les équipes de support peuvent assigner automatiquement des priorités ou des tags basés sur l'IA, améliorant ainsi le temps de réponse et la cohérence. Cet
article montre aux développeurs comment créer un **ZendeskAdapter** personnalisé pour OTAI en étendant la classe
`TicketSystemAdapter` existante et en appelant l'API REST de Zendesk.

## Architecture d'OTAI et TicketSystemAdapter

Open Ticket AI utilise une architecture de **pipeline modulaire**. Chaque ticket entrant est prétraité, passé à travers des classifieurs de file d'attente et
de priorité, et finalement renvoyé au système de tickets via un adaptateur. Le composant clé ici est le
**TicketSystemAdapter** (une classe de base abstraite) qui définit comment mettre à jour ou interroger des tickets dans un système externe.
Les adaptateurs intégrés (par exemple pour OTOBO) héritent de cette classe de base. Pour Zendesk, nous allons créer une nouvelle sous-classe.

&#x20;*Figure : Architecture d'Open Ticket AI (extraite du diagramme de classes UML). Les étapes du pipeline (prétraitement,
classification, etc.) aboutissent à un **TicketSystemAdapter**, qui envoie les mises à jour au système de tickets externe via
REST. L'extension d'OTAI avec Zendesk implique de créer une sous-classe de cet adaptateur afin que les résultats de l'IA (priorité, tags, etc.) soient
écrits dans les tickets Zendesk.*

En pratique, OTAI est configuré via YAML et repose sur l'**injection de dépendances**. Tous les composants (fetchers, classifieurs,
modificateurs, etc.) sont définis dans `config.yml` et assemblés au démarrage. La documentation note que « Les fetchers, préparateurs, services d'IA ou modificateurs personnalisés peuvent être implémentés en tant que classes Python et enregistrés via la configuration. Grâce
à l'injection de dépendances, de nouveaux composants peuvent être facilement intégrés. ». En d'autres termes, l'ajout d'un `ZendeskAdapter` est
simple : nous l'implémentons en tant que classe Python et le déclarons dans la configuration.

## Étapes pour ajouter un adaptateur Zendesk

Suivez ces étapes pour intégrer Zendesk à OTAI :

1.  **Créer une sous-classe de `TicketSystemAdapter`** : Créez une nouvelle classe d'adaptateur (par ex. `ZendeskAdapter`) qui étend la classe abstraite
    `TicketSystemAdapter`. Cette classe implémentera la manière dont OTAI lit ou écrit dans Zendesk.
2.  **Implémenter `update_ticket`** : Dans `ZendeskAdapter`, redéfinissez la
    méthode `async def update_ticket(self, ticket_id: str, data: dict)`. Cette méthode doit envoyer une requête HTTP à
    Zendesk pour mettre à jour les champs du ticket donné (par ex. priorité, tags). Par exemple, vous ferez un `PUT` vers
    `https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json` avec une charge utile JSON contenant les champs à
    mettre à jour.
3.  **(Optionnel) Implémenter les méthodes de recherche** : Vous pouvez également redéfinir `find_tickets(self, query: dict)` ou
    `find_first_ticket(self, query: dict)` si vous avez besoin de récupérer des tickets depuis Zendesk (par ex. pour obtenir de nouveaux tickets). Ces
    méthodes doivent appeler les points de terminaison GET de Zendesk (tels que `/api/v2/tickets.json` ou l'API de recherche) et retourner les données des tickets
    sous forme de dictionnaires Python.
4.  **Configurer les identifiants** : Ajoutez vos identifiants Zendesk à la configuration d'OTAI. Par exemple, stockez le **sous-domaine**,
    l'**e-mail utilisateur** et le **jeton d'API** dans `config.yml` ou des variables d'environnement. L'adaptateur peut lire ces informations depuis le
    `SystemConfig` injecté (passé dans le constructeur).
5.  **Enregistrer l'adaptateur** : Mettez à jour `config.yml` pour qu'OTAI utilise `ZendeskAdapter` comme son intégration de système de tickets.
    Le framework d'injection de dépendances (DI) d'OTAI instanciera alors votre classe avec les paramètres de configuration.

Ces étapes tirent parti de l'extensibilité d'OTAI. Le pipeline est défini dans la configuration (aucune API REST n'est nécessaire pour déclencher la
classification), donc le simple fait de brancher votre adaptateur fait en sorte que le pipeline utilise Zendesk comme système cible.

## Exemple : Implémentation de `ZendeskAdapter`

Ci-dessous se trouve une ébauche de ce à quoi l'adaptateur Python pourrait ressembler. Il s'initialise avec les valeurs de configuration et implémente
`update_ticket` en utilisant la bibliothèque `requests` de Python. Le code ci-dessous est à titre d'illustration ; vous devrez installer `requests` (ou
utiliser `httpx`/`aiohttp` pour l'asynchrone) et gérer les erreurs si nécessaire :

```python
import requests
from open_ticket_ai.src.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


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

Le constructeur de ce `ZendeskAdapter` récupère les paramètres depuis la `config` injectée. La méthode `update_ticket` construit l'URL
en utilisant le modèle standard de Zendesk et envoie une requête PUT. Dans cet exemple, nous nous authentifions avec l'authentification HTTP de base (Basic Auth) en utilisant
l'e-mail et le jeton d'API de Zendesk (par convention, le nom d'utilisateur est `user_email/token`). La charge utile (payload) encapsule les données du ticket
sous la clé `"ticket"` comme l'attend l'API de Zendesk. Après une mise à jour réussie, elle retourne le JSON du ticket mis à jour.

Vous définiriez `config.zendesk_subdomain`, `config.zendesk_user_email` et `config.zendesk_api_token` dans
`config.yml`. Par exemple :

```yaml
ticket_system_integration:
    adapter: open_ticket_ai.src.ce.ticket_system_integration.zendesk_adapter.ZendeskAdapter
    zendesk_subdomain: "mycompany"
    zendesk_user_email: "agent@mycompany.com"
    zendesk_api_token: "ABCD1234TOKEN"
```

Ceci indique à OTAI d'utiliser `ZendeskAdapter`. L'injection de dépendances d'OTAI construira alors votre adaptateur avec ces valeurs.

## Appeler l'API REST de Zendesk

La clé de l'adaptateur est de faire des requêtes HTTP vers les points de terminaison de l'API de Zendesk. Comme montré ci-dessus, l'adaptateur d'OTAI appelle des URL
comme `https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json`. Selon la documentation de Zendesk, la mise à jour d'un ticket
requiert un PUT vers cette URL avec un corps JSON (par exemple, `{"ticket": {"priority": "high", "tags": ["urgent"]}}` si vous
voulez définir la priorité et les tags). Dans le script d'exemple ci-dessus, `requests.put(url, json=payload, auth=auth)` s'en charge.

Pour être complet, vous pouvez également implémenter la création de tickets (`requests.post(...)`) ou d'autres appels API. Mais pour
la classification, seule la **mise à jour des tickets existants** est généralement nécessaire (pour réécrire les champs prédits par l'IA). Assurez-vous
que le jeton d'API Zendesk dispose des autorisations nécessaires et que vous avez activé « Accès par jeton » (Token Access) dans l'administration de Zendesk.

Si vous souhaitez également récupérer des tickets depuis Zendesk (par exemple, pour trouver les tickets nouvellement créés à traiter), utilisez les API de liste ou de recherche de Zendesk.
Par exemple, vous pourriez faire un GET sur `/api/v2/tickets.json` pour paginer à travers les tickets, ou utiliser
`/api/v2/search.json?query=type:ticket status:new` pour trouver tous les nouveaux tickets. Retournez le JSON à OTAI sous forme de liste de
dictionnaires de tickets depuis `find_tickets()`.

## Pipeline et utilisation

Avec le `ZendeskAdapter` en place, l'exécution d'OTAI l'intégrera de manière transparente dans le pipeline. Par exemple, après
avoir configuré vos modèles d'IA (prédicteurs de file d'attente et de priorité), le démarrage du planificateur d'OTAI (par ex.
`python -m open_ticket_ai.src.ce.main start`) déclenchera le pipeline. OTAI utilisera votre adaptateur comme étape finale de
« modificateur » : après que l'IA a inféré les attributs pour chaque ticket, il appelle `ZendeskAdapter.update_ticket` pour appliquer ces
attributs à Zendesk. L'ensemble du processus reste transparent pour OTAI – il sait seulement qu'il appelle `update_ticket`
sur une classe d'adaptateur.

Comme les composants d'OTAI sont définis en YAML, vous pouvez configurer la fréquence à laquelle il récupère ou vérifie les tickets et comment il
applique les mises à jour. La documentation pour les développeurs souligne que tous les composants sont enfichables via la configuration et l'injection de dépendances (DI). Ainsi, une fois que votre adaptateur est implémenté et connecté dans `config.yml`, aucune autre modification de code n'est nécessaire pour inclure Zendesk dans le flux de tickets.