---
description: Apprenez à intégrer OpenTicketAI avec Zammad pour la classification de tickets par IA sur site. Utilisez l'API REST pour récupérer, classifier et mettre à jour les files d'attente et les priorités des tickets.
---
# Intégration d'OpenTicketAI avec Zammad pour la classification automatisée de tickets

OpenTicketAI est un **classifieur de tickets par IA** sur site (on-premise) qui automatise la catégorisation, le routage et la priorisation des tickets de support. Pour l'intégrer avec Zammad, nous implémentons un **ZammadAdapter** qui étend l'interface `TicketSystemAdapter` d'OpenTicketAI. Cet adaptateur utilise l'API REST de Zammad pour *récupérer* les tickets de Zammad, les *traiter via le pipeline d'OpenTicketAI*, et *mettre à jour* le ticket (file d'attente, priorité, commentaires) en fonction des prédictions de l'IA. Les composants clés sont illustrés dans l'architecture : l'**AdapterFactory** d'OpenTicketAI crée l'adaptateur approprié (par exemple, ZammadAdapter) pour communiquer via REST avec le système de tickets. Le pipeline récupère les tickets, les classifie, et enfin l'adaptateur du système de tickets met à jour Zammad via son API.

L'architecture d'OpenTicketAI utilise un pipeline modulaire où chaque ticket est traité par une série de pipes. L'étape finale du *Ticket System Adapter* applique les mises à jour (file d'attente, priorité, notes) au système externe via l'API REST. En pratique, vous enregistrez votre `ZammadAdapter` dans la configuration d'injection de dépendances afin que le pipe **BasicTicketFetcher** l'utilise pour charger les tickets, et que le pipe **GenericTicketUpdater** l'utilise pour appliquer les mises à jour.

## Aperçu du pipeline OpenTicketAI

OpenTicketAI s'exécute dans un *pipeline* qui transforme les données des tickets étape par étape. Un flux simplifié est :

1.  **Préprocesseur** – fusionne/nettoie `subject` et `body`.
2.  **Transformeur / Tokenizer** – prépare le texte pour l'IA.
3.  **Classifieur de file d'attente** – prédit la file d'attente/le groupe cible.
4.  **Classifieur de priorité** – prédit le niveau de priorité.
5.  **Post-processeur** – applique des seuils, choisit des actions.
6.  **Adaptateur de système de tickets** – met à jour le ticket dans Zammad via l'API REST.

Chaque étape prend un objet `PipelineContext` (contenant `ticket_id` et un dictionnaire `data`) et l'enrichit. Par exemple, après l'exécution des classifieurs, le `data` du contexte peut contenir des clés comme `new_queue`, `new_priority`, ou un `article` (commentaire) à ajouter. Le pipe **GenericTicketUpdater** recherche ensuite une entrée `update_data` dans le contexte et appelle l'adaptateur pour appliquer ces champs au ticket. Cette conception facilite l'ajout de nouvelles étapes (par exemple, un pipe de pseudonymisation) ou la personnalisation de la logique de mise à jour. L'orchestrateur gère ces *AttributePredictors* (récupérateur, préparateur, service d'IA, modificateur) en se basant sur la configuration YAML.

## TicketSystemAdapter et ZammadAdapter

OpenTicketAI définit une `class` de base abstraite `TicketSystemAdapter` que toutes les intégrations doivent étendre. Elle déclare des méthodes de base comme :

*   `async update_ticket(ticket_id: str, data: dict) -> dict | None`: **Mettre à jour** les champs d'un ticket (ex: file d'attente, priorité, ajout de note). Doit gérer les mises à jour partielles et retourner l'objet ticket mis à jour.
*   `async find_tickets(query: dict) -> list[dict]`: **Rechercher** des tickets correspondant à une requête. Le format de la requête est spécifique à l'adaptateur, mais cette méthode doit retourner une liste des tickets correspondants.
*   `async find_first_ticket(query: dict) -> dict | None`: Raccourci pour ne retourner que le premier résultat.

Un **ZammadAdapter** héritera de cette `class` et implémentera ces méthodes en utilisant l'API de Zammad. Il contiendra généralement la configuration (URL de base, identifiants) injectée via un `SystemConfig`. Par exemple :

```python
from open_ticket_ai.src.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
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

*Citation :* La `class` de base requiert ces méthodes. Dans cet exemple, nous utilisons `httpx.AsyncClient` (car les méthodes sont `async`), mais vous pourriez de la même manière utiliser `requests` dans un contexte synchrone. Par exemple, récupérer tous les tickets pourrait être aussi simple que `requests.get(f"{base_url}/api/v1/tickets", auth=(user, pwd))`.

### Récupération des tickets depuis Zammad

L'API REST de Zammad fournit des points de terminaison (endpoints) pour lister et rechercher des tickets. Un moyen simple de récupérer les tickets récents ou correspondants est via :

*   **Lister tout (paginé)** : `GET /api/v1/tickets` retourne un tableau d'objets ticket.
*   **Recherche** : `GET /api/v1/tickets/search?query=...` prend en charge les recherches en texte intégral ou par champ, retournant les tickets correspondants au format JSON (et `expand=true` peut résoudre les champs liés).

Votre implémentation de `find_tickets` peut les utiliser. Par exemple, pour filtrer par état ou sujet :

```python
async with httpx.AsyncClient(auth=self.auth) as client:
    res = await client.get(f"{base_url}/api/v1/tickets/search", params={"query": "state:open OR state:new"})
    res.raise_for_status()
    tickets = res.json()  # a list of dicts
```

Ensuite, encapsulez ou retournez-les dans le format attendu par OpenTicketAI (une liste de dictionnaires de tickets). Le pipe `BasicTicketFetcher` appellera cette méthode en utilisant l'ID du ticket depuis le `PipelineContext` pour charger un ticket avant son traitement.

### Mise à jour des tickets Zammad

Après la classification, nous mettons à jour Zammad en utilisant son **API de mise à jour de ticket**. Zammad permet de modifier des champs comme le groupe (file d'attente) et la priorité, et même d'ajouter une note interne ou un article en un seul appel. Par exemple, la charge utile (payload) suivante (envoyée via `PUT /api/v1/tickets/{id}`) définit un nouveau groupe et une nouvelle priorité, et ajoute un article interne :

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

Cela réassignerait le ticket au groupe « Ventes », le définirait en haute priorité, et y attacherait une nouvelle note (commentaire interne) avec les informations de l'IA. En code, notre `update_ticket` pourrait faire :

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

La réponse sera le JSON complet du ticket mis à jour si le statut est 200. Si vous avez seulement besoin de poster un commentaire ou une note, incluez le bloc `article` comme ci-dessus. Alternativement, des mises à jour plus petites (comme simplement définir une note) peuvent utiliser le champ « note » du ticket ou un point de terminaison d'articles séparé, mais l'`article` groupé dans le PUT est pratique.

## Intégration du pipeline dans OpenTicketAI

Pour connecter cela au pipeline d'OpenTicketAI, vous ajoutez des **pipes** dans `config.yml`. Par exemple :

*   **BasicTicketFetcher** : configuré avec `ticket_system: ZammadAdapter`. Il appelle `find_tickets`/`find_first_ticket` et remplit `context.data` avec les champs du ticket.
*   **Preparer** : par exemple, `SubjectBodyPreparer` pour combiner le texte du sujet et du corps.
*   **Services d'inférence IA** : vos classifieurs de file d'attente/priorité personnalisés (par exemple, un `model` HuggingFace).
*   **GenericTicketUpdater** : configuré avec `ticket_system: ZammadAdapter`. Il recherche `context.data["update_data"]` après l'inférence et appelle `update_ticket`.

Par exemple, un pipe personnalisé pourrait faire :

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

Ceci prépare le `update_data` que GenericTicketUpdater utilisera.

Enfin, l'**AdapterFactory** (configurée via DI) s'assure que `ticket_system: Zammad` crée une instance de votre `class` `ZammadAdapter`, en injectant l'URL de base et l'authentification depuis `config.yml`. Le pipe **GenericTicketUpdater** appelle ensuite `await adapter.update_ticket(id, update_data)`, appliquant vos modifications pilotées par l'IA.

## Améliorations : Classification, Pseudonymisation et Notes

Au-delà de la file d'attente/priorité de base, OpenTicketAI offre des fonctionnalités pour enrichir l'intégration Zammad :

*   **Classification de file d'attente & priorité :** Vous pouvez entraîner des `model`s personnalisés pour des files d'attente ou des schémas de priorité Zammad spécifiques. Les valeurs prédites correspondent aux groupes et priorités de Zammad (par exemple, l'API de priorité utilise le format `"priority": "2 normal"`). En ajustant les seuils dans le **post-processeur**, vous pouvez également rejeter automatiquement les prédictions à faible confiance ou escalader des tickets.

*   **Connecteurs de pseudonymisation :** Pour protéger la vie privée des utilisateurs, vous pouvez insérer un *pipe de pipeline* personnalisé avant l'inférence qui **pseudonymise** ou masque les données sensibles (par exemple, noms, e-mails) dans le texte du ticket. Cela pourrait utiliser des regex ou des services externes pour remplacer les PII (informations personnelles identifiables) par des jetons. Le texte masqué est ensuite classifié, et le ticket original est mis à jour, garantissant qu'aucun contenu sensible ne quitte votre système.

*   **Création de note/article :** Vous pouvez tirer parti de l'API d'articles de Zammad pour enregistrer les informations de l'IA ou l'analyse de sentiment. Comme montré ci-dessus, incluez un `article` dans la charge utile de mise à jour pour ajouter des commentaires. Alternativement, vous pourriez configurer un **pipe de création de note** séparé qui, indépendamment de la mise à jour de la file d'attente/priorité, ajoute toujours une note au ticket avec les scores de confiance du `model` ou l'analyse de sentiment. Ces notes aident les agents à comprendre *pourquoi* une décision a été prise.

Chaque amélioration s'intègre naturellement dans le pipeline et est automatiquement appliquée par le GenericTicketUpdater via l'adaptateur. Par exemple, après avoir exécuté un pipe d'analyse de sentiment, vous pourriez faire :

```python
context.data['update_data'] = {
    "article": {
        "subject": "Sentiment Score",
        "body": f"Sentiment polarity: {sentiment_score}",
        "internal": True,
    },
}
```

Ensuite, l'adaptateur le publiera (POST) en tant qu'article sur Zammad.

## Avantages pour l'automatisation des tickets Zammad

Avec cette intégration, Zammad bénéficie d'une automatisation sur site (on-premise) alimentée par l'IA. Les tickets entrants peuvent être automatiquement assignés à la bonne file d'attente et recevoir une priorité préliminaire, libérant ainsi les équipes de support pour se concentrer sur les problèmes urgents. Comme OpenTicketAI s'exécute localement, les données sensibles des tickets restent en interne (ce qui est important pour la conformité). Cette **intégration IA pour Zammad** transforme le tri manuel en un processus rationalisé : vous conservez un contrôle total et une personnalisation complète (via la configuration et les `model`s personnalisés) tout en tirant parti du pipeline d'OpenTicketAI.

En résumé, l'implémentation d'un **ZammadAdapter** implique de sous-classer `TicketSystemAdapter` et de le connecter au pipeline d'OpenTicketAI. L'adaptateur utilise l'API de Zammad pour les opérations CRUD sur les tickets (par exemple, `GET /tickets` et `PUT /tickets/{id}`). Une fois configuré, OpenTicketAI récupérera continuellement les tickets, les traitera via votre pile de `model`s d'IA, et mettra à jour Zammad avec la file d'attente, la priorité et les notes prédites. Cette intégration **IA pour système de tickets** dote Zammad de capacités de classification et de routage automatisés, concrétisant la vision d'un classifieur de tickets par IA sur site pour les équipes de support d'entreprise.

**Sources :** Documentation de l'API REST de Zammad ; Documentation pour les développeurs d'OpenTicketAI.