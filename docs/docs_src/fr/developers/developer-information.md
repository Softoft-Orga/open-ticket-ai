---
description: Guide du développeur pour le classifieur de tickets ATC sur site. Apprenez
  à configurer avec YAML, à exécuter depuis le CLI, et à étendre avec des composants
  et adaptateurs Python personnalisés.
title: Informations pour les développeurs
---
# Informations pour les développeurs de l'ATC Community Edition

## Aperçu

L'ATC Community Edition est une solution sur site (on-premise) pour la classification automatisée des tickets de support. La version MVP actuelle est contrôlée via un fichier de configuration YAML et démarrée via le CLI. Il n'y a pas d'API REST pour téléverser des données d'entraînement ou déclencher une session d'entraînement.

## Architecture logicielle

L'application se compose essentiellement des paquets suivants :

* **core** – modèles de configuration, utilitaires d'injection de dépendances, moteur de pipeline et rendu de templates.
* **base** – implémentations de pipes réutilisables (par ex. récupération/mise à jour de tickets et pipes composites).
* **hf_local** – pipes d'inférence HuggingFace fournies en exemples.
* **ticket\_system\_integration** – adaptateurs pour différents systèmes de tickets.
* **main.py** – point d'entrée CLI qui relie injecteur, planificateur et orchestrateur.

L'orchestrateur exécute désormais des graphes de `Pipe` décrits en YAML. Les définitions sont assemblées à partir de `defs` réutilisables, rendues avec le contexte courant, puis résolues à l'exécution via le conteneur d'injection de dépendances. Chaque entrée du planning précise quel arbre de pipes doit s'exécuter et à quel intervalle l'orchestrateur le déclenche.

Un exemple de commande pour démarrer l'application :

```bash
python -m open_ticket_ai.src.ce.main start
```

## Architecture du pipeline

Le pipeline d'exécution est décrit en YAML. `RawOpenTicketAIConfig` regroupe les plugins, la configuration globale, les `defs` réutilisables et le planning `orchestrator` qui indique quelles pipes doivent s'exécuter et à quel intervalle. Au démarrage, le conteneur d'injection de dépendances charge ce fichier, instancie les services singletons définis dans `defs` et les enregistre dans le `UnifiedRegistry`. Les pipes et les templates peuvent ensuite référencer ces services par identifiant.

Chaque entrée du pipeline est normalisée en `RegisterableConfig` avec un `id`, la classe ciblée dans `use`, des `steps` optionnels et des métadonnées d'orchestration telles que `_if` et `depends_on`. À l'exécution, la configuration est rendue avec le `Context` courant, ce qui permet aux expressions Jinja2 (par exemple `get_pipe_result('classify', 'label')`) de réutiliser les résultats précédents. Les expressions `if:` activent ou désactivent une pipe pour un run donné et `depends_on` garantit qu'une pipe n'est lancée qu'après le succès de ses dépendances.

Le `Context` conserve deux dictionnaires : `pipes` stocke pour chaque étape un `PipeResult` (success/failed/message/data) et `config` expose la configuration rendue pour l'entrée de planning active. Les pipes lisent ce contexte, exécutent leur logique dans la méthode asynchrone `_process()` et renvoient des données qui deviennent `PipeResult.data`. Les pipes et templates suivants peuvent ainsi détecter des erreurs ou réutiliser des données.

Le champ `orchestrator` de la YAML est une liste d'entrées de planning. Chaque entrée fournit `run_every_milli_seconds` et une définition `pipe` qui peut être une pipe composite avec des `steps` imbriqués. Le planificateur parcourt cette liste, déclenche les exécutions lorsque les intervalles expirent et remet à l'orchestrateur un `Context` neuf initialisé avec la configuration correspondante.

## Entraînement de modèles personnalisés

L'entraînement direct via l'application n'est pas fourni dans le MVP. Des modèles pré-entraînés peuvent être spécifiés et utilisés dans la configuration. Si un modèle doit être ajusté ou nouvellement créé, cela doit être fait en dehors de l'application.

## Extension

Des fetchers, preparers, services d'IA ou modifiers personnalisés peuvent être implémentés en tant que classes Python et enregistrés via la configuration. Grâce à l'injection de dépendances, de nouveaux composants peuvent être facilement intégrés.

## Comment ajouter un pipe personnalisé

Le pipeline de traitement peut être enrichi avec vos propres classes de pipe. Un pipe est une unité de travail qui exploite le `Context`, consulte les `PipeResult` déjà stockés et produit un nouveau `PipeResult` avec des données et indicateurs de succès à jour.

1. **Définissez éventuellement un modèle de configuration** pour les paramètres du pipe.
2. **Héritez de `Pipe`** et implémentez la méthode asynchrone `_process()`.
3. **Retournez un dictionnaire** au format `PipeResult` (ou utilisez `PipeResult(...).model_dump()`).

L'exemple simplifié suivant illustre un pipe d'analyse de sentiment HuggingFace exécuté localement :

```python
from typing import Any

from pydantic import BaseModel
from transformers import pipeline

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class SentimentPipeConfig(BaseModel):
    model_name: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    text: str


class SentimentAnalysisPipe(Pipe):
    def __init__(self, config: dict[str, Any]):
        super().__init__(pipe_params)
        self.cfg = SentimentPipeConfig(**pipe_params)
        self.classifier = pipeline("sentiment-analysis", model=self.cfg.model_name)

    async def _process(self) -> dict[str, Any]:
        if not self.cfg.text:
            return PipeResult(success=False, failed=True, message="Aucun texte disponible", data={}).model_dump()

        sentiment = self.classifier(self.cfg.text)[0]
        return PipeResult(
            success=True,
            failed=False,
            data={
                "label": sentiment["label"],
                "confidence": sentiment["score"],
            },
        ).model_dump()
```

Après implémentation, enregistrez la classe dans `open_ticket_ai.defs` (ou `infrastructure.pipe_classes`) afin que la pipeline YAML puisse la référencer via son `id`. Comme l'orchestrateur rend la configuration avec Jinja2, il est possible d'inclure des expressions réutilisant des variables d'environnement ou les résultats de pipes précédentes.

## Comment intégrer un nouveau système de tickets

Pour connecter un autre système de help desk, implémentez un nouvel adaptateur qui hérite de
`TicketSystemAdapter`. L'adaptateur effectue la conversion entre l'API externe et les
modèles unifiés du projet.

1. **Créez une classe d'adaptateur**, par ex. `FreshdeskAdapter(TicketSystemAdapter)`.
2. **Implémentez toutes les méthodes abstraites** :
    - `find_tickets`
    - `find_first_ticket`
    - `create_ticket`
    - `update_ticket`
    - `add_note`
3. **Traduisez les données** vers et depuis les modèles `UnifiedTicket` et `UnifiedNote`.
4. **Fournissez un modèle de configuration** pour les identifiants ou les paramètres de l'API.
5. **Enregistrez l'adaptateur** dans `create_registry.py` afin qu'il puisse être instancié
   à partir de la configuration YAML.

Une fois enregistré, spécifiez l'adaptateur dans la section `system` de `config.yml` et
l'orchestrateur l'utilisera pour communiquer avec le système de tickets.

## Exemples de Configuration

Pour vous aider à démarrer rapidement, nous avons créé une collection d'exemples de configuration prêts à l'emploi
démontrant divers cas d'utilisation. Ces exemples se trouvent dans le répertoire `docs/config_examples/`.

### Exemples Disponibles

1. **L'IA Ajoute une Note au Ticket** (`add_note_when_in_queue.yml`)
   - Ajout automatique de notes générées par l'IA aux tickets dans des files spécifiques
   - Cas d'utilisation : Ajouter des analyses ou des suggestions aux tickets en révision

2. **Création Conditionnelle de Ticket** (`create_ticket_on_condition.yml`)
   - Création automatique de nouveaux tickets en fonction de conditions détectées
   - Cas d'utilisation : Créer automatiquement des tickets d'escalade pour les problèmes urgents

3. **Classification de File** (`queue_classification.yml`)
   - Acheminement des tickets vers les files appropriées via analyse IA
   - Cas d'utilisation : Routage automatique par département (IT, RH, Finance, etc.)

4. **Classification de Priorité** (`priority_classification.yml`)
   - Attribution de niveaux de priorité basée sur l'analyse d'urgence des tickets
   - Cas d'utilisation : S'assurer que les problèmes critiques reçoivent une attention immédiate

5. **Workflow Complet** (`complete_workflow.yml`)
   - Exemple complet combinant plusieurs opérations IA
   - Cas d'utilisation : Automatisation complète avec classification, notes et gestion des erreurs

### Utilisation des Exemples

Chaque exemple comprend :
- Configuration complète avec toutes les sections requises
- Commentaires détaillés expliquant chaque étape
- Paramètres personnalisables pour votre environnement
- Meilleures pratiques pour la gestion des erreurs et les mécanismes de repli

Pour utiliser un exemple :
1. Parcourez les exemples dans `docs/config_examples/`
2. Copiez la configuration pertinente dans votre `config.yml`
3. Mettez à jour les variables d'environnement et personnalisez les paramètres
4. Testez d'abord avec un sous-ensemble limité de tickets

Pour plus de détails, consultez le [README dans le répertoire config_examples](../../config_examples/README.md).

## Résumé

L'ATC Community Edition offre un flux de travail exécuté localement pour la classification automatique des tickets dans sa version MVP. Tous les paramètres sont gérés via des fichiers YAML ; aucune API REST n'est disponible. Des processus ou des scripts externes doivent être utilisés pour l'entraînement.