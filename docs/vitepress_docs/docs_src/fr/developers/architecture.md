---
description: Découvrez l'architecture d'Open Ticket AI. Apprenez comment son pipeline de données modulaire et ses modèles Hugging Face permettent une classification et un routage intelligents des tickets.
layout: page
pageClass: full-page
title: Aperçu de l'architecture d'Open Ticket AI
---
# Aperçu de l'architecture

Open Ticket AI repose sur un moteur d'exécution modulaire qui traite les tickets de support via des pipelines configurables. Chaque pipeline combine des « pipes » réutilisables qui récupèrent les données, exécutent des modèles Hugging Face et renvoient les résultats vers les systèmes externes.

## Vue d'ensemble du système

- **Noyau auto-hébergé** : s'exécute comme un service Python qui charge la configuration, enregistre les services et supervise l'exécution des pipelines.
- **Services injectés** : adaptateurs, modèles et utilitaires sont fournis par un conteneur d'inversion de contrôle afin que les pipes ne demandent que ce dont ils ont besoin.
- **Pipelines composables** : la configuration YAML décrit quels pipes s'exécutent, dans quel ordre, ainsi que les clauses conditionnelles `when`.
- **Contexte partagé d'exécution** : les résultats intermédiaires sont stockés dans un objet de contexte pour que les étapes suivantes puissent réutiliser les sorties précédentes sans recalcul.

## Composants principaux

### Orchestrateur de pipeline
L'orchestrateur charge la configuration du pipeline actif, rend les modèles Jinja2 et instancie chaque pipe à la volée. Il respecte les conditions `when`, itère sur les étapes et persiste l'état des pipes dans le contexte partagé.

### Pipes
Les pipes encapsulent une unité de travail — récupération de tickets, classification de texte, mise à jour de métadonnées ou journalisation. Ils sont sans état entre deux exécutions ; chaque run reçoit de nouvelles entrées de l'orchestrateur et écrit ses résultats dans le contexte pour les étapes aval.

### Services
Les capacités réutilisables (clients HTTP, pipelines Hugging Face, stockages) vivent dans le conteneur de services. Les pipes demandent ces services avec `get_instance`, ce qui centralise l'infrastructure et facilite son remplacement ou son extension.

### Adaptateurs de systèmes de tickets
Les adaptateurs assurent la traduction entre Open Ticket AI et les plateformes de helpdesk externes. Les pipes de collecte s'appuient sur un adaptateur pour charger les tickets, tandis que les pipes de mise à jour utilisent le même adaptateur pour appliquer les changements de file, de priorité ou de commentaire sur le système distant.

### Modèles de machine learning
Les prédictions de file et de priorité sont produites par des modèles Hugging Face exécutés dans des pipes dédiés. Ces pipes alimentent les entrées depuis le contexte, exécutent le modèle puis enrichissent le contexte avec des prédictions structurées consommées par les étapes suivantes.

## Flux de traitement de bout en bout

1. L'orchestrateur initialise les services et le contexte d'exécution, puis sélectionne le pipeline configuré.
2. Un pipe de collecte utilise un adaptateur pour récupérer les tickets concernés et les stocker dans le contexte.
3. Des pipes de prétraitement nettoient et normalisent le texte du ticket pour la consommation par les modèles.
4. Des pipes de classification exécutent les modèles Hugging Face pour prédire la file, la priorité ou les étiquettes.
5. Des pipes de post-traitement consolident les prédictions, appliquent des règles métier et préparent les charges utiles de mise à jour.
6. Des pipes de mise à jour rappellent l'adaptateur afin d'écrire les résultats (changement de file, de priorité, notes internes) sur le ticket d'origine.

## Étendre la plateforme

- **Ajouter un nouvel adaptateur** : implémentez l'interface d'adaptateur pour une autre plateforme de tickets et enregistrez-la dans le conteneur de services.
- **Personnaliser les pipelines** : composez de nouvelles combinaisons de pipes en YAML en utilisant des clauses `when` pour piloter les étapes optionnelles.
- **Introduire de nouvelles intelligences** : créez des pipes de modèles supplémentaires ou des processeurs basés sur des règles qui lisent et écrivent dans le contexte partagé.

Cette architecture découple la logique de classification des intégrations, ce qui permet aux équipes d'adapter le pipeline à leurs flux de travail sans modifier le runtime central.
