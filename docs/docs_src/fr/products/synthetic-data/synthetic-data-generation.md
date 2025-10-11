---
description: Générez des jeux de données synthétiques multilingues de tickets de support
  client avec notre outil Python. Comprend un pipeline graphique, des assistants
  IA, des champs riches et un suivi des coûts.
---
# Génération de données synthétiques pour les tickets de support

Créez des jeux de données de tickets de support multilingues de haute quality pour la classification, le routage et l'automatisation des réponses.
Cette page décrit notre **Générateur de données synthétiques** basé sur Python et le jeu de données public que nous avons créé avec. Elle explique également comment le générateur soutient le flux d'entraînement d'**Open Ticket AI** et nos services commerciaux de génération de données.

::: info

- **Objectif :** Générer des tickets réalistes (sujet, corps, file d'attente, priorité, type, tags, langue et une première réponse d'agent IA).
- **Langues :** DE, EN, FR, ES, PT.
- **Pipeline :** Graphe de « nœuds » IA configurables (thème → e-mail → tags → paraphrase → traduction → réponse).
- **Modèles :** Fonctionne avec OpenAI, OpenRouter, Together… (GPT-4, Qwen, LLaMA, etc.).
- **Contrôles :** CLI intégrée, modes dev/prod, suivi des coûts et des tokens avec résumés monétaires.
- **Licence :** Publication prévue sous licence **LGPL**.
- **Besoin de l'outil ou de modifications personnalisées ?** → **sales@softoft.de**
:::

## Ce qu'il génère

- **Champs principaux :** `ticket_id`, `subject`, `body`
- **Étiquettes de classification :** `type` (Incident/Request/Problem/Change), `queue` (ex. Support Technique, Facturation, RH), `priority` (Low/Medium/High)
- **Langue :** `language` (DE/EN/FR/ES/PT)
- **Tags :** 4 à 8 tags de domaine/thème par ticket
- **Réponse de l'agent :** un message de **première réponse** rédigé par un assistant IA

Un exemple d'enregistrement (CSV) :

```csv
ticket_id,subject,body,language,type,queue,priority,tags,first_response
8934012332184,"VPN verbindet nicht","Seit dem Update keine Verbindung…","DE","Incident","IT / Security","High","vpn,update,remote-access,windows","Hallo! Bitte öffnen Sie die VPN-App…"
```

> Les ID sont garantis uniques dans une plage de 12 à 13 chiffres, ce qui simplifie les jointures et les fusions entre les exécutions.

## Comment ça marche (en bref)

Le générateur utilise un **pipeline basé sur un graphe** de petits « nœuds » testables. Chemin typique :

```
Thème → Brouillon de sujet → Brouillon de corps d'e-mail → Tagging → Paraphrase → Traduction → Première réponse
```

Vous pouvez réorganiser les nœuds, supprimer des étapes ou ajouter les vôtres. Chaque « assistant » est configurable (prompts système/utilisateur, modèle/fournisseur, limites). Cela signifie que vous pouvez rapidement produire des tickets spécifiques à un domaine (par ex., RH, santé, commerce de détail, secteur public) sans réécrire de code.

## Flexibilité des modèles et des fournisseurs

Apportez vos LLMs préférés :

*   **Fournisseurs :** OpenAI, OpenRouter, Together (et d'autres via des adaptateurs)
*   **Modèles :** `class` GPT-4, Qwen, LLaMA, etc.
*   Changez les prompts par nœud pour augmenter la diversité et contrôler le ton, la terminologie et la structure.

## Suivi des coûts et de l'utilisation (intégré)

*   **Comptabilité des tokens et des coûts par exécution** (entrée vs. sortie) par `model`
*   **Seuils configurables** qui avertissent/errent si une seule exécution dépasse une limite de coût
*   **Résumés monétaires** (par ex., USD, EUR) pour une budgétisation claire
*   **Modes Dev vs. Prod** pour basculer entre de petites exécutions de test et des constructions complètes de jeux de données

## Démarrage rapide

Lancez une tâche de génération de jeu de données avec la CLI intégrée :

```bash
python -m ticket_generator
```

Idées de configuration minimale (pseudocode) :

```python
# config/config.py (example)
RUN = {
    "rows": 10_000,  # total examples
    "batch_size": 50,  # lower for cheap dev runs
    "languages": ["DE", "EN", "FR", "ES", "PT"],
    "timezone": "Europe/Berlin",
    "pipeline": [
        "topic_node",
        "email_draft_node",
        "tagging_node",
        "paraphrase_node",
        "translate_node",
        "first_response_node"
    ],
    "models": {
        "default": {
            "provider": "openai",
            "name": "gpt-4o-mini",
            "max_tokens": 800
        }
    },
    "cost_limits": {
        "warn": 0.001,  # USD per single assistant run
        "error": 0.01
    }
}
```

> En pratique, vous ajusterez les prompts, choisirez différents modèles par nœud et ajouterez des tables de randomisation spécifiques au domaine (files d'attente, priorités, types d'entreprise, etc.).

## Schéma de sortie

Colonnes courantes que vous verrez dans nos exportations CSV/Parquet générées :

*   `ticket_id` (chaîne de 12–13 chiffres)
*   `subject`, `body`
*   `language` (DE/EN/FR/ES/PT)
*   `type` ∈ (Incident, Request, Problem, Change)
*   `queue` (spécifique au domaine, ex. *Support Technique*, *Facturation*, *RH*)
*   `priority` ∈ (Low, Medium, High)
*   `tags` (tableau/liste de 4–8)
*   `first_response` (réponse de l'agent)

## Exemple de jeu de données sur Kaggle

Nous avons utilisé ce générateur pour construire le jeu de données public **Multilingual Customer Support Tickets**, incluant **priorités, files d'attente, types, tags et types d'entreprise**, idéal pour l'entraînement de modèles de classification et de priorisation de tickets.
➡️ Kaggle : **Multilingual Customer Support Tickets**

*   Inclut plusieurs langues et toutes les étiquettes listées ci-dessus
*   Des notebooks communautaires démontrent des cas d'usage de classification et de routage

## Comment cela soutient Open Ticket AI

**Open Ticket AI** classifie la **file d'attente** (`queue`) et la **priorité** (`priority`) des tickets entrants. Les données synthétiques sont inestimables lorsque vous avez :

*   Un historique étiqueté **inexistant ou limité**
*   Des données **sensibles** qui ne peuvent pas quitter votre infrastructure
*   Un besoin de classes **équilibrées** (par ex., files d'attente/priorités rares)
*   Une couverture **multilingue** dès le premier jour

Nous utilisons régulièrement le générateur pour :

1.  amorcer l'entraînement des modèles,
2.  équilibrer les classes à longue traîne, et
3.  simuler des opérations multilingues.
    Si vous souhaitez que nous générions des jeux de données sur mesure (votre domaine/files d'attente/priorités/tags, vos langues), nous le proposons en tant que **service**.

\::: tip Services
Besoin de données synthétiques spécifiques à votre domaine pour votre service d'assistance ? Nous concevrons des prompts, des nœuds et des tables de randomisation pour votre secteur, les intégrerons à votre pipeline de données et livrerons des fichiers CSV/Parquet prêts pour l'entraînement et l'évaluation.
**Contact :** [sales@softoft.de](mailto:sales@softoft.de)
\:::

## Licence et disponibilité

*   La publication du **Générateur de données synthétiques** est prévue sous licence **LGPL**.
*   Si vous souhaitez un accès anticipé, une licence privée ou des modifications/extensions personnalisées, **envoyez un e-mail à `sales@softoft.de`** et nous nous en occuperons for vous.

---

### FAQ

**Le jeu de données est-il « réel » ou « synthétique » ?**
Entièrement synthétique, produit par un pipeline LLM configurable.

**Puis-je ajouter mes propres champs (par ex., *Unité commerciale*, *Impact*, *Urgence*) ?**
Oui, en étendant les tables de randomisation et en ajoutant un nœud pour émettre les champs.

**Puis-je contrôler le style et le ton ?**
Absolument. Les prompts sont définis par nœud, vous pouvez donc imposer le ton, la formalité, les régionalismes et la terminologie.

**Comment maîtriser les coûts ?**
Utilisez le mode dev (petites `rows`, `max_tokens` plus bas), les seuils de coût et des modèles moins chers pour les premières itérations. Passez à votre mélange de modèles préféré une fois que les résultats sont corrects.