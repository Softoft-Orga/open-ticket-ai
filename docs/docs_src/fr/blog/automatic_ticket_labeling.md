---
description: Gagnez du temps en étiquetant des milliers de tickets. Découvrez un flux de travail semi-automatisé utilisant GPT pour le pré-étiquetage zero-shot et Label Studio pour une révision efficace.
---
# Étiquetage efficace de 10 000 tickets : Stratégies d'étiquetage semi-automatisé

L'étiquetage manuel de milliers de tickets de support est long et coûteux. Un **flux de travail semi-automatisé** tire parti des grands modèles de langage (LLM) comme GPT pour **pré-étiqueter** les tickets (en utilisant des prompts zero-shot/few-shot), puis fait appel à des annotateurs humains pour **réviser et corriger** ces étiquettes.
Cette approche hybride réduit considérablement l'effort d'annotation : par exemple, une étude de cas a révélé que les « pré-annotations » générées par GPT étaient *« suffisamment bonnes pour nous aider à accélérer le processus d'étiquetage »*. En
pratique, des *étiquettes minimales* provenant du modèle peuvent réduire le temps et le coût de l'annotation. Dans cet article, nous expliquons comment mettre en place un tel pipeline, montrons des exemples en Python (utilisant GPT via OpenRouter ou OpenAI), et discutons d'outils comme Label Studio pour la révision.

## Utiliser GPT pour le pré-étiquetage Zero-Shot/Few-Shot

Les LLM modernes peuvent classifier du texte avec **zéro ou quelques exemples**. Dans l'étiquetage zero-shot, le modèle attribue des catégories sans avoir été explicitement entraîné sur les données des tickets. Comme le dit un tutoriel :
*« L'apprentissage zero-shot permet aux modèles de classifier de nouvelles instances sans exemples étiquetés »*. En
pratique, vous rédigez un prompt demandant à GPT d'étiqueter un ticket. Par exemple :

```text
Ticket: "Cannot login to account."
Classify this ticket into one of {Bug, Feature Request, Question}.
```

Le modèle répond alors avec une étiquette. L'étiquetage few-shot ajoute quelques exemples dans le prompt pour améliorer la précision. Cela signifie que nous pouvons générer des étiquettes initiales **directement via l'API** sans aucun entraînement de modèle.

> **Astuce :** Utilisez un prompt structuré ou demandez une sortie JSON pour faciliter l'analyse. Par exemple :
>
> ```
> Ticket: "Password reset email bounced."
> Respond in JSON like {"category": "..."}.
> ```
>
> Cela aide à intégrer la réponse dans votre pipeline.

## Exemple : Code Python pour le pré-étiquetage

Voici un exemple en Python utilisant l'API d'OpenAI via la bibliothèque `openai`. Il parcourt une liste de tickets factices, demande à GPT-4 de classifier chaque ticket, et enregistre la catégorie. (Vous pouvez également
utiliser [OpenRouter](https://openrouter.ai) de manière similaire en définissant
`base_url="https://openrouter.ai/api/v1"` et en modifiant le paramètre `model`.)

```python
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"
tickets = [
    {"id": 1, "text": "User cannot login to account", "category": None},
    {"id": 2, "text": "Error 404 when uploading file", "category": None},
    {"id": 3, "text": "Request to add dark mode feature", "category": None},
    {"id": 4, "text": "Payment declined on checkout", "category": None},
]
categories = ["Bug", "Feature Request", "Question"]

for ticket in tickets:
    prompt = f"Ticket: \"{ticket['text']}\". Classify it as one of {categories}."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    # Extract the category from GPT's reply
    ticket["category"] = response.choices[0].message.content.strip()

print(tickets)
```

Après avoir exécuté ce code, `tickets` pourrait devenir :

```python
[
    {'id': 1, 'text': 'User cannot login to account', 'category': 'Bug'},
    {'id': 2, 'text': 'Error 404 when uploading file', 'category': 'Bug'},
    {'id': 3, 'text': 'Request to add dark mode feature', 'category': 'Feature Request'},
    {'id': 4, 'text': 'Payment declined on checkout', 'category': 'Bug'}
]
```

Ce sont des **pré-étiquettes** que des réviseurs humains vérifieront. Notez comment OpenRouter facilite le changement de modèles : en changeant `model="openai/gpt-4"` pour un autre fournisseur (par exemple, Claude ou un modèle plus léger), le même code fonctionne. En fait, l'API unifiée d'OpenRouter vous permet d'essayer plusieurs fournisseurs ou d'utiliser des modèles de secours si l'un d'eux est indisponible. Par exemple :

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY",
)
client.chat.completions.create(
    model="openai/gpt-4o",  # try GPT-4 first
    extra_body={"models": ["anthropic/claude-3.5-sonnet", "google/palm-2"]},
    messages=[{"role": "user", "content": "Ticket: 'Login page error'. Classify it."}]
)
```

Ceci utilisera GPT-4 s'il est disponible, sinon se rabattra sur Claude ou PaLM comme indiqué dans la documentation d'OpenRouter. Une telle flexibilité est utile pour les entreprises nécessitant une haute disponibilité ou souhaitant comparer des modèles.

## Intégration des pré-étiquettes avec les outils d'étiquetage

Une fois que GPT a généré les étiquettes, l'étape suivante consiste à **les importer dans une interface d'étiquetage** pour une révision humaine. Une solution open-source populaire est [Label Studio](https://labelstud.io). Label Studio prend en charge l'importation des prédictions du modèle en tant que « pré-annotations » à côté des données. Les annotateurs voient l'étiquette suggérée et n'ont qu'à corriger les erreurs, pas à étiqueter de zéro. En effet, l'équipe *« passe de la tâche fastidieuse d'étiquetage des données au processus beaucoup plus efficace de révision et d'affinage des étiquettes préliminaires »*.

Label Studio propose même un backend ML : vous pouvez écrire un petit serveur utilisant la `class` `LabelStudioMLBase` qui appelle GPT pour chaque tâche. Dans leur tutoriel, Label Studio montre comment encapsuler les appels à GPT-4 dans cette `class` pour retourner des prédictions à la volée. Alternativement, vous pouvez importer un fichier JSON de prédictions. Le format JSON requis a un champ `data` (le texte du ticket) et un tableau `predictions` (contenant chaque étiquette). Par exemple (simplifié) :

```json
[
    {
        "data": {
            "text": "User cannot login to account"
        },
        "predictions": [
            {
                "result": [
                    {
                        "value": {
                            "choices": [
                                {
                                    "text": "Bug"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    },
    {
        "data": {
            "text": "Add dark mode to settings"
        },
        "predictions": [
            {
                "result": [
                    {
                        "value": {
                            "choices": [
                                {
                                    "text": "Feature Request"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
]
```

Après l'importation, Label Studio affichera chaque ticket avec l'étiquette du modèle pré-remplie. Le travail de l'annotateur est de **réviser et corriger**. Ce flux de travail semi-automatisé a prouvé son efficacité : un exemple de Kili Technology a démontré le chargement d'un jeu de données pré-étiqueté par GPT et a noté *« nous avons réussi à pré-annoter notre jeu de données »* et que cette approche *« a le potentiel de nous faire gagner beaucoup de temps »*. En pratique, la précision de GPT pour l'étiquetage peut être d'environ 80 à 90 %, ce qui signifie que les humains ne corrigent que les 10 à 20 % restants.

## Outils et étapes du flux de travail

Pour résumer, un pipeline d'étiquetage semi-automatisé typique ressemble à ceci :

* **Préparez le jeu de données de tickets.** Exportez vos 10 000 tickets non étiquetés (par exemple, en JSON ou CSV).
* **Générez des pré-étiquettes via un LLM.** Exécutez du code (comme ci-dessus) appelant GPT-4 (ou un autre `model` via OpenRouter) pour classifier chaque ticket. Enregistrez les réponses.
* **Importez les prédictions dans un outil d'étiquetage.** Utilisez Label Studio (ou un outil similaire) pour charger les tickets et associer chacun à l'étiquette générée par GPT (la « prédiction »). La documentation de Label Studio explique comment importer les prédictions avec vos données.
* **Révision humaine.** Les annotateurs parcourent les tickets dans Label Studio, acceptant ou corrigeant les étiquettes. C'est beaucoup plus rapide que d'étiqueter à partir de zéro. L'interface de Label Studio met en évidence la suggestion du modèle pour chaque tâche, transformant ainsi la tâche en une validation rapide.
* **Exportez les étiquettes finales.** Une fois révisées, exportez les annotations corrigées pour l'entraînement de modèles ou l'analyse.

Les principaux outils publics qui prennent en charge cette approche incluent :

* **OpenRouter** – une passerelle d'API LLM unifiée (openrouter.ai). Elle vous permet de basculer facilement entre GPT-4, Anthropic Claude, Google PaLM, etc. Vous pouvez même spécifier une liste de secours dans un seul appel API.
* **API OpenAI (GPT-4/3.5)** – le moteur principal pour générer des étiquettes avec des prompts zero/few-shot.
* **Label Studio** – une interface utilisateur (UI) d'étiquetage de données open-source. Elle prend en charge l'importation de prédictions et dispose d'un backend ML pour appeler des modèles.
* **Doccano** – un outil open-source plus simple pour l'annotation de texte (classification, NER, etc.). Il n'a pas d'intégration LLM intégrée, mais vous pouvez toujours utiliser GPT hors ligne pour générer des étiquettes et les charger comme choix initiaux.
* **Snorkel/Étiquetage programmatique** – pour certains cas basés sur des règles ou de supervision faible, des outils comme Snorkel peuvent compléter les étiquettes LLM, mais les LLM modernes couvrent souvent de nombreux cas d'emblée.

## Exemple de données de tickets factices

Pour illustrer, voici quelques *données de tickets factices* avec lesquelles vous pourriez travailler :

```python
tickets = [
    {"id": 101, "text": "Error 500 when saving profile", "label": None},
    {"id": 102, "text": "How do I change my subscription plan?", "label": None},
    {"id": 103, "text": "Feature request: dark mode in settings", "label": None},
    {"id": 104, "text": "Application crashes on startup", "label": None},
]
```

Vous pourriez fournir chaque `ticket['text']` à GPT avec un prompt comme :

```text
Ticket: "Error 500 when saving profile."
Classify this issue as one of {Bug, Feature, Question}.
```

Supposons que GPT retourne respectivement `"Bug"`, `"Question"`, `"Feature"`, `"Bug"`. Après la boucle, `tickets` pourrait être :

```python
[
    {'id': 101, 'text': 'Error 500 when saving profile', 'label': 'Bug'},
    {'id': 102, 'text': 'How do I change my subscription plan?', 'label': 'Question'},
    {'id': 103, 'text': 'Feature request: dark mode in settings', 'label': 'Feature'},
    {'id': 104, 'text': 'Application crashes on startup', 'label': 'Bug'},
]
```

Ces étiquettes seraient ensuite chargées dans l'interface de révision. Même si certaines sont incorrectes (par exemple, GPT pourrait mal étiqueter un bug complexe comme une fonctionnalité), l'annotateur n'a qu'à les *corriger* au lieu de partir de zéro. Empiriquement, les étiquettes générées par GPT atteignent souvent une précision d'environ 80 à 90 %, donc la révision est beaucoup plus rapide que l'étiquetage complet.

## Résultats et points à retenir

L'approche semi-automatisée s'adapte bien à l'échelle. Dans un grand projet, les annotateurs humains pourraient n'avoir besoin de corriger que quelques centaines ou milliers d'étiquettes au lieu de 10 000. Comme l'a observé le tutoriel de Kili après avoir exécuté les pré-étiquettes GPT : *« Super ! Nous avons réussi à pré-annoter notre jeu de données. Il semble que cette solution ait le potentiel de nous faire gagner beaucoup de temps dans les projets futurs. »*. En d'autres termes, les LLM agissent comme un multiplicateur de force. Même si le modèle n'est pas correct à 100 %, il **« accélère le processus d'étiquetage »** en effectuant la majeure partie du travail.

**Bonnes pratiques :** Utilisez une température basse (par exemple, 0.0–0.3) pour des étiquettes cohérentes, et fournissez des instructions claires ou une petite liste d'exemples. Surveillez les erreurs de GPT : vous devrez peut-être ajuster les prompts ou ajouter quelques exemples (few-shot) pour les catégories peu performantes. Gardez le prompt simple (par exemple, « Classifiez le texte du ticket en A, B ou C »). Vous pouvez également traiter plusieurs tickets par lots dans un seul appel API si le `model` et l'API le permettent, pour réduire les coûts. Et incluez toujours une révision humaine – cela garantit une haute qualité et détecte les erreurs ou la dérive du LLM.

## Conclusion

L'étiquetage semi-automatisé avec GPT et des outils comme OpenRouter et Label Studio est une stratégie puissante pour étiqueter rapidement de grands jeux de données textuelles. En **pré-étiquetant 10 000 tickets avec un LLM puis en les révisant**, les entreprises peuvent lancer leurs flux de travail d'IA avec un minimum de données initiales. Cette approche réduit considérablement les coûts et le temps tout en garantissant la qualité grâce à la supervision humaine. Comme le note un guide de mise en œuvre, le passage d'un flux de travail de *« l'étiquetage de données »* à la *« révision et l'affinage »* des étiquettes générées par le LLM *« accélère considérablement votre flux de travail. »*. En bref, combiner la pré-annotation basée sur GPT avec une interface utilisateur conviviale (Label Studio, Doccano, etc.) aide les équipes de logiciels/IA à étiqueter des jeux de données de tickets massifs de manière efficace et précise.