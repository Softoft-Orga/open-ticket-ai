---
description: Entraînez des modèles de file d'attente, de priorité et de type avec nos
  tickets de support client multilingues synthétiques. Inclut des champs riches et
  plusieurs versions. Disponible sur Kaggle.
---
# Tickets de support client multilingues (synthétiques)

Un jeu de données **entièrement synthétique** pour l'entraînement et l'évaluation de modèles de service d'assistance tels que la classification de **file d'attente**, de **priorité** et de **type**, ainsi que pour le pré-entraînement d'aide à la réponse.
Créé avec notre **générateur de données synthétiques** Python et publié sur **Kaggle**.

* **Kaggle :** [Jeu de données de tickets](https://www.kaggle.com/datasets/tobiasbueck/multilingual-customer-support-tickets/data)
* [Génération de données synthétiques](synthetic-data-generation.md) (prévu en **LGPL**)
* **Besoin de données personnalisées ou de l'outil ?** [sales@softoft.de](mailto:sales@softoft.de)

---

## Aperçu des versions

![Diagramme réseau des versions du jeu de données](/images/network_diagram.svg)

| Version | Langues                       | Taille (relative) | Remarques                                                                     |
|--------:|-------------------------------|-------------------|-------------------------------------------------------------------------------|
|  **v5** | **EN, DE**                    | La plus grande    | Taxonomie/équilibrage les plus récents et affinés ; se concentre sur la qualité EN/DE. |
|  **v4** | **EN, DE**                    | Grande            | Similaire à l'orientation de la v5 ; prompts et distributions légèrement plus anciens. |
|  **v3** | EN, DE, **+ autres (FR/ES/PT)** | Plus petite       | Pipeline plus ancien ; plus de langues mais un contenu globalement moins diversifié. |

> Les anciennes versions incluent **plus de langues** mais sont généralement **plus petites** et **moins diversifiées**.
> Les versions les plus récentes (**v5**, **v4**) mettent l'accent sur la qualité et l'échelle **EN/DE**.

### Quelle version devrais-je utiliser ?

* **Entraînement de modèles de production EN/DE** → commencez avec la **v5** (ou la **v4** si vous avez besoin d'un ensemble plus ancien comparable).
* **Recherche sur plusieurs langues** → **v3** (plus petite, mais inclut plus de localisations).

---

## Fichiers et nommage

Vous trouverez des exports CSV par version (exemples) :

```
dataset-tickets-multi-lang-4-20k.csv
dataset-tickets-multi-lang3-4k.csv
dataset-tickets-german_normalized.csv
```

---

## Schéma

Chaque ticket inclut un texte principal ainsi que des étiquettes utilisées par **Open Ticket AI**.

| Colonne             | Description                                          |
|---------------------|------------------------------------------------------|
| `subject`           | L'objet de l'e-mail du client                        |
| `body`              | Le corps de l'e-mail du client                       |
| `answer`            | La première réponse de l'agent (générée par IA)      |
| `type`              | Type de ticket (ex: Incident, Demande, Problème, …)  |
| `queue`             | File d'attente cible (ex: Support Technique, Facturation) |
| `priority`          | Priorité (ex: basse, moyenne, haute)                 |
| `language`          | Langue du ticket (ex: `en`, `de`, …)                 |
| `version`           | Version du jeu de données (métadonnées)              |
| `tag_1`, `tag_2`, … | Un ou plusieurs tags thématiques (peut être `null` par endroits) |

### Extraits des données

* **de (Incident / Support Technique / haute)**
  *Objet :* Wesentlicher Sicherheitsvorfall
  *Corps (extrait) :* „…ich möchte einen gravierenden Sicherheitsvorfall melden…“
  *Réponse (extrait) :* „Vielen Dank für die Meldung…“

* **en (Incident / Support Technique / haute)**
  *Objet :* Account Disruption
  *Corps (extrait) :* “I am writing to report a significant problem with the centralized account…”
  *Réponse (extrait) :* “We are aware of the outage…”

* **en (Demande / Retours et Échanges / moyenne)**
  *Objet :* Query About Smart Home System Integration Features
  *Corps (extrait) :* “I am reaching out to request details about…”
  *Réponse (extrait) :* “Our products support…”

---

## Tour d'horizon visuel

![Nuage de mots des objets de tickets](/images/word_cloud.png)

![Tags les plus utilisés](/images/tags.png)

![Distributions pour la file d'attente, la priorité, la langue, le type](/images/basic_distribution.png)

---

## Utilisation prévue et limitations

**Utilisation prévue :**

* Entraînement de modèles à froid pour **file d'attente/priorité/type**
* Expériences d'équilibrage de classes
* Benchmarking multilingue (utilisez la **v3** si vous avez besoin de FR/ES/PT)

**Limitations :**

* Les distributions synthétiques peuvent différer de votre trafic de production. Validez toujours sur un petit échantillon réel et anonymisé avant le déploiement.

---

## Comment charger et vérifications rapides

```python
import pandas as pd

df = pd.read_csv("dataset-tickets-multi-lang-4-20k.csv")  # ou la version de votre choix

# Vérifications de base
print(df.language.value_counts())
print(df.queue.value_counts().head())

# Préparer un texte simple pour la classification
X = (df["subject"].fillna("") + "\n\n" + df["body"].fillna("")).astype(str)
y = df["queue"].astype(str)
```

---

## Relation avec Open Ticket AI

Ce jeu de données reflète les étiquettes que **Open Ticket AI** prédit sur les tickets entrants (**file d'attente**, **priorité**, **type**, **tags**).
Utilisez-le pour **amorcer** l'entraînement et l'évaluation ; déployez votre modèle avec **Open Ticket AI** une fois que vous êtes satisfait des métriques.

* [Générateur de données synthétiques](synthetic-data-generation.md)
* [API de prédiction (hébergée)](../prediction-api/overview.md)

---

## Licence et citation

* Jeu de données : veuillez ajouter ici la licence de données de votre choix (par ex., **CC BY 4.0**).
* Générateur : prévu en **LGPL**. Pour un accès ou des personnalisations : **[sales@softoft.de](mailto:sales@softoft.de)**.

**Citation suggérée :**

> Bueck, T. (2025). *Multilingual Customer Support Tickets (Synthetic)*. Kaggle Dataset.
> Generated with the Open Ticket AI Synthetic Data Generator.

---

## Changelog (vue d'ensemble)

* **v5 :** EN/DE uniquement ; plus grand ensemble ; taxonomie et équilibrage améliorés.
* **v4 :** EN/DE ; grand ; ensemble de prompts plus ancien.
* **v3 :** Plus petit ; inclut des langues supplémentaires (FR/ES/PT), pipeline plus ancien.