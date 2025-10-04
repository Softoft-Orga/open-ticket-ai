---
title: Référence du pipeline
description: Comprenez la structure YAML qui pilote l'orchestrateur, les pipes et les définitions réutilisables d'OpenTicketAI.
---

# Référence du pipeline

OpenTicketAI se configure entièrement via YAML. Cette page décrit l'organisation de la configuration, la manière dont les ancres et les
réutilisations fonctionnent, ainsi que la façon dont l'orchestrateur transforme ces données en instances de `Pipe` et en objets `PipeResult`
pendant l'exécution.

## Structure principale

Toutes les options sont regroupées sous la clé `open_ticket_ai`. Le schéma correspond à `RawOpenTicketAIConfig` et se divise en quatre sections :

- **`plugins`** – modules Python optionnels importés avant la création des pipes.
- **`general_config`** – paramètres globaux (logging, catalogue `pipe_classes` défini via des ancres YAML réutilisables).
- **`defs`** – définitions réutilisables (services, pipes composites, ensembles de paramètres) pouvant être fusionnées dans les pipes planifiées via
  `<<: *ancre`.
- **`orchestrator`** – tableau d'entrées de planning. Chaque élément précise `run_every_milli_seconds` et la `pipe` (souvent une définition composite
  tirée de `defs`) qui doit être lancée à cet intervalle.

```yaml
open_ticket_ai:
  plugins: []
  general_config:
    pipe_classes:
      - &ticket_fetch_pipe
        use: "open_ticket_ai.base:FetchTicketsPipe"
  defs:
    - &default_ticket_fetcher
      <<: *ticket_fetch_pipe
      injects:
        ticket_system: "otobo_znuny"
  orchestrator:
    - run_every_milli_seconds: 10000
      pipe:
        <<: *default_ticket_fetcher
        ticket_search_criteria:
          state.name: "new"
```

## Définitions réutilisables et ancres

Les ancres YAML sont centrales dans OpenTicketAI :

- Définissez un bloc une seule fois (ex. `&ticket_classifier`) puis réutilisez-le avec `<<: *ticket_classifier` où cela est nécessaire.
- Les ancres peuvent se combiner. `PipeFactory.resolve_config` fusionne la configuration parente avec les substitutions des enfants, si bien que les
  enfants ne décrivent que les différences.
- Les éléments de `defs` peuvent contenir des `steps` imbriqués, d'autres ancres ou des dépendances injectées. Lorsqu'ils sont référencés dans
  l'orchestrateur, ils s'étendent en arbre de pipes complet.

## Champs d'une configuration de pipe

Chaque pipe (y compris les étapes imbriquées) est validé sous forme de `RegisterableConfig`/`RenderedPipeConfig`. Champs essentiels :

- `id` – identifiant unique du pipe. S'il est absent, un UUID est généré ; il est toutefois recommandé d'en fournir un afin d'utiliser
  `get_pipe_result('mon_id', 'value')` dans les templates.
- `use` – chemin d'import (`module:Classe`) résolu par `PipeFactory`.
- `injects` – correspondance entre paramètres de constructeur et identifiants présents dans `defs`. Les références sont résolues avant
  l'instanciation.
- `steps` – pour une pipe composite, liste ordonnée de pipes enfants exécutées séquentiellement.
- `if` – expression Jinja2 facultative rendue en booléen. La valeur est stockée dans `_if` au sein de `RenderedPipeConfig`; si elle vaut `False`, la
  pipe est ignorée.
- `depends_on` – chaîne ou liste d'identifiants de pipes qui doivent avoir réussi (`PipeResult.success == True`) avant d'exécuter la pipe.
- Champs supplémentaires – valeurs arbitraires exposées comme attributs de la configuration rendue et utilisables par la pipe.

## Modèle d'exécution

1. L'orchestrateur sélectionne l'entrée de planning dont l'intervalle `run_every_milli_seconds` vient d'expirer.
2. La définition `pipe` correspondante est rendue avec un `Context` vierge (`context.config` contient l'entrée de planning, `context.pipes` est vide).
3. Pour chaque pipe ou étape :
   - L'expression `_if` est évaluée ; si elle vaut `False`, la pipe est passée.
   - Les dépendances listées dans `depends_on` sont vérifiées en consultant les valeurs `PipeResult.success` déjà enregistrées.
   - `PipeFactory` localise la classe indiquée dans `use`, injecte les dépendances définies par `injects` et appelle la méthode asynchrone `process()`
     de la pipe (qui attend en interne `_process()`).
   - Le résultat est encapsulé dans un `PipeResult` (`success`, `failed`, `message`, `data`) et sauvegardé dans `context.pipes[id]`.
4. Les fonctions utilitaires disponibles dans les templates (`get_pipe_result`, `has_failed`, etc.) consultent `context.pipes` pour fournir les résultats
   précédents aux étapes suivantes.
5. Les pipes composites fusionnent les résultats de leurs enfants via `PipeResult.union`, offrant ainsi un unique état de succès/échec et des données
   agrégées.

## Utilisation de `PipeResult`

Chaque état sauvegardé est un `PipeResult` (voir `open_ticket_ai.core.pipeline.pipe_config`). Pour vos propres pipes :

- Retournez un dictionnaire que `PipeResult.model_validate` peut interpréter, ou instanciez `PipeResult(...)` puis appelez `.model_dump()`.
- Placez les informations à réutiliser dans `data`.
- Renseignez `success`/`failed` et `message` afin que les templates puissent appliquer une logique conditionnelle.

## Conseils de planification

- Les entrées d'`orchestrator` sont indépendantes ; chacune s'exécute avec un `Context` neuf.
- Il est possible de dupliquer une définition composite pour plusieurs entrées et de n'en modifier que les paramètres (critères de recherche, seuils, etc.).
- Les intervalles sont exprimés en millisecondes ; `run_every_milli_seconds: 60000` équivaut à environ une exécution par minute.

Grâce à cette structure, vous pouvez composer des flux de traitement de tickets complexes sans modifier le code Python : ajustez simplement la YAML et
laissez l'orchestrateur reconstruire le pipeline à l'exécution.
