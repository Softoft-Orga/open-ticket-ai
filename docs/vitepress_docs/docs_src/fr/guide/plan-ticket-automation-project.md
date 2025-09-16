---
aside: false
description: "Planifiez votre projet d'automatisation de tickets. Choisissez le bon\
  \ parcours en fonction de vos données (étiquetées, non étiquetées ou inexistantes)\
  \ pour un entraînement, un déploiement et un support rapides."
pageClass: full-page
---
# Planificateur d'Automatisation de Tickets — Choisissez Votre Meilleur Parcours

Modernisez rapidement le routage des tickets, quel que soit votre point de départ. Ce planificateur vous aide à choisir le parcours adapté à la réalité de vos données : beaucoup de tickets étiquetés, beaucoup de tickets non étiquetés, ou presque aucune donnée. Chaque parcours aboutit à un package de services concret avec des livrables et des KPIs clairs, vous permettant de passer de l'idée au pilote, puis à la production, sans incertitude.

**À qui s'adresse ce guide :** Aux équipes IT/service utilisant Znuny/OTRS/OTOBO (ou similaire) qui souhaitent des prédictions fiables pour les files d'attente, les priorités ou les tags, que ce soit sur site ou via une API hébergée.

**Ce que vous obtiendrez :** un flux de décision court, 4 parcours actionnables (A–D), des modules complémentaires (multilingue, attributs supplémentaires), des critères/métriques pour savoir quand vous êtes prêt, et une checklist de préparation des données.

**Comment utiliser cette page**

* Commencez par la vue d'ensemble et répondez à trois questions : **Données étiquetées ? → Non étiquetées ? → Rapide ?**
* Cliquez sur la case du **Flux A/B/C/D** pour accéder à ses étapes, livrables et KPIs.
* Utilisez les **modules complémentaires** si vous avez besoin de plusieurs langues ou de plus de sorties (tags, personne assignée, première réponse).
* Maintenez des **critères** stricts (score F1 par classe + KPIs métier) pour que les pilotes se traduisent par une confiance en production.

Continuez maintenant avec le diagramme de vue d'ensemble et les flux détaillés ci-dessous.
Parfait — voici une description plus complète que vous pouvez ajouter sous vos diagrammes. Je l'ai gardée facile à parcourir tout en ajoutant des conseils concrets et des seuils pour que les lecteurs puissent choisir un flux en toute confiance.

Compris — je vais conserver vos nouveaux diagrammes courts et ajouter un texte explicatif clair et concis pour chaque section afin que l'article soit complet tout en restant facile à parcourir.

---

## 0) Vue d'ensemble

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  S((Start)) --> Q1{Labeled?}
  Q1 -- Yes --> A0[Flow A]
  Q1 -- No --> Q2{Unlabeled?}
  Q2 -- Yes --> B0[Flow B]
  Q2 -- No --> Q3{Fast?}
  Q3 -- Yes --> D0[Flow D]
  Q3 -- No --> C0[Flow C]

click A0 "#flow-a-many-labeled" "Flow A"
click B0 "#flow-b-many-unlabeled" "Flow B"
click C0 "#flow-c-few-or-no-tickets" "Flow C"
click D0 "#flow-d-quick-start-hosted-api" "Flow D"
```

**Comment utiliser cette vue d'ensemble :**
Commencez en haut, répondez aux questions et suivez la branche jusqu'au flux qui vous correspond. Cliquez sur un flux pour voir ses détails.

---

## <a id="flow-a-many-labeled"></a> Flux A — Beaucoup de tickets étiquetés

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Audit/Tax] --> B[Train]
  B --> C[Eval]
  C --> D[On-Prem]
  D --> E[Pilot]
  E --> F[Support]
```

**Quand choisir ce parcours :**

* Vous avez déjà des **milliers de tickets avec des étiquettes de file d'attente, de priorité ou de tag**.
* Vous voulez un modèle **entraîné sur mesure** pour une précision maximale.

**Que se passe-t-il dans ce flux :**

1. **Audit/Taxonomie** — Vérifier la qualité des étiquettes, l'équilibre des classes et la nomenclature.
2. **Entraînement** — Affiner le modèle de classification avec vos données.
3. **Évaluation** — Mesurer la précision, le rappel et le score F1 par classe.
4. **Sur site** — Déployer dans votre propre infrastructure.
5. **Pilote** — Tester en production avec supervision.
6. **Support** — Itérer et ré-entraîner si nécessaire.

**Package recommandé :** Affinage + Installation sur site.

---

## <a id="flow-b-many-unlabeled"></a> Flux B — Beaucoup de tickets non étiquetés

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Ingest] --> B[Auto-Label]
  B --> C[QC]
  C --> D{OK?}
  D -- No --> B
  D -- Yes --> E[Train]
  E --> F[Eval]
  F --> G[On-Prem]
  G --> H[Support]
```

**Quand choisir ce parcours :**

* Vous disposez de **grandes archives de tickets historiques** mais sans étiquettes.
* Vous pouvez allouer du temps de revue humaine pour les contrôles de qualité.

**Que se passe-t-il dans ce flux :**

1. **Ingestion** — Collecter les tickets de votre système.
2. **Étiquetage auto.** — Utiliser l'étiquetage automatique assisté par LLM.
3. **Contrôle Qualité (QC)** — Vérifier et corriger des échantillons.
4. **OK ?** — Boucler jusqu'à ce que la qualité atteigne le seuil requis.
5. **Entraînement** — Affiner avec l'ensemble de données préparé.
6. **Éval / Sur site / Support** — Identique au Flux A.

**Package recommandé :** Étiquetage automatique + Affinage.

---

## <a id="flow-c-few-or-no-tickets"></a> Flux C — Peu ou pas de tickets

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Define Tax] --> B[Synth Data]
  B --> C[Baseline]
  C --> D[Eval]
  D --> E{Pilot}
  E -- API --> H[Hosted DE]
  E -- Local --> I[On-Prem]
  H --> J[Collect]
  I --> J
  J --> K[Fine-Tune]
  K --> L[Prod/Support]
```

**Quand choisir ce parcours :**

* Vous partez de **zéro** ou avez trop peu de tickets pour un entraînement.
* Vous voulez une solution de **démarrage à froid** pour une mise en production rapide.

**Que se passe-t-il dans ce flux :**

1. **Définir Taxonomie** — Décider des files d'attente, des priorités, du ton.
2. **Données synthétiques** — Générer des tickets réalistes (DE/EN).
3. **Modèle de base** — Entraîner un modèle initial sur les données synthétiques.
4. **Évaluation** — Vérifier les performances avant le déploiement.
5. **Pilote** — Choisir l'API hébergée pour la vitesse ou l'installation sur site pour le contrôle.
6. **Collecte** — Rassembler les vrais tickets pendant la phase pilote.
7. **Affinage** — Fusionner les données réelles et synthétiques.
8. **Prod/Support** — Mettre en production avec des itérations continues.

**Package recommandé :** Démarrage à froid synthétique.

---

## <a id="flow-d-quick-start-hosted-api"></a> Flux D — Démarrage rapide via l'API hébergée

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
    A[Use API DE] --> B[Measure]
    B --> C{Tax OK?}
    C -- Yes --> D[Scale/Support]
    C -- No --> E[Auto/Synth - Train]
    E --> F[On-Prem]
```

**Quand choisir ce parcours :**

* Vous avez besoin de **résultats immédiats**.
* Vous voulez essayer l'automatisation sans entraînement préalable.

**Que se passe-t-il dans ce flux :**

1. **Utiliser l'API DE** — Classification instantanée via le modèle allemand hébergé.
2. **Mesurer** — Suivre l'impact sur le routage, les SLA et le backlog.
3. **Taxonomie OK ?** — Si satisfait, augmentez l'utilisation ; sinon, passez au Flux B ou C pour l'entraînement.

**Package recommandé :** Pilote API hébergée → Affinage (optionnel).

---

## Modules complémentaires optionnels

### Extension multilingue

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[More langs?] --> B{Hist per lang?}
  B -- Yes --> C[Auto-Label]
  B -- No --> D[Synth]
  C --> E[Train Multi]
  D --> E
  E --> F[Pilot/Eval]
```

Ajoutez le support pour des langues supplémentaires via l'étiquetage automatique multilingue ou la génération synthétique, puis entraînez et évaluez par langue.

---

### Attributs supplémentaires

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Add tags/assignee/FAA] --> B[Extend labels/gen]
  B --> C[Multi-task/Chain]
  C --> D[Deploy]
```

Prédisez plus que les files d'attente/priorités — par ex., les tags, la personne assignée ou le temps de première réponse — en étendant l'étiquetage et en entraînant un modèle multi-tâches.