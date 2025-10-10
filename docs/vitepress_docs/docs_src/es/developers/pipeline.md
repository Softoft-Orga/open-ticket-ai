---
title: Referencia de la Pipeline
description: Comprende la estructura YAML que gobierna el orquestador, los pipes y las definiciones reutilizables de OpenTicketAI.
---

# Referencia de la Pipeline

OpenTicketAI se configura íntegramente con YAML. Esta referencia explica cómo se organiza la configuración, cómo funcionan los anclajes
(anchors) y las definiciones reutilizables, y cómo el orquestador transforma todo ello en instancias de `Pipe` y objetos `PipeResult`
en tiempo de ejecución.

## Disposición principal

Toda la configuración vive bajo la clave `open_ticket_ai`. El esquema coincide con `RawOpenTicketAIConfig` y se divide en cuatro secciones:

- **`plugins`** – módulos Python opcionales que se importan antes de crear pipes.
- **`general_config`** – ajustes globales como el logging y `pipe_classes` (catálogo de plantillas de pipe referenciadas mediante anclas YAML).
- **`defs`** – definiciones reutilizables (servicios, pipes compuestas, conjuntos de parámetros) que pueden mezclarse en pipes programadas con
  `<<: *ancla`.
- **`orchestrator`** – una matriz de entradas de calendario. Cada elemento declara `run_every_milli_seconds` y la `pipe` (normalmente una
  definición compuesta de `defs`) que debe ejecutarse con esa cadencia.

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

## Definiciones reutilizables y anclajes

OpenTicketAI hace un uso intensivo de los anclajes de YAML:

- Define un bloque una sola vez (por ejemplo `&ticket_classifier`) y mézclalo donde lo necesites con `<<: *ticket_classifier`.
- Los anclajes se pueden combinar. `PipeFactory.resolve_config` fusiona la configuración padre con las sustituciones del hijo, de modo que los
  hijos solo declaran las diferencias.
- Las definiciones en `defs` pueden incluir `steps` anidados, otros anclajes o dependencias inyectadas. Cuando el orquestador las referencia,
  se expanden a un árbol de pipes completo.

## Campos de configuración de un pipe

Cada pipe (incluidos los pasos anidados) se valida como `RegisterableConfig`/`RenderedPipeConfig`. Los campos más relevantes son:

- `id` – identificador único del pipe. Si se omite se genera un UUID, pero es recomendable fijarlo para poder usar `get_pipe_result('tu_id', 'value')`.
- `use` – ruta de importación (`módulo:Clase`) que `PipeFactory` resuelve.
- `injects` – mapeo entre parámetros del constructor e IDs definidos en `defs`. Se resuelven antes de instanciar la clase.
- `steps` – en pipes compuestas, lista ordenada de pipes hijas que se ejecutan de manera secuencial.
- `if` – expresión opcional de Jinja2 que se renderiza a booleano. El resultado se guarda como `_if` en `RenderedPipeConfig`; si es `False`, la
  pipe se omite.
- `depends_on` – cadena o lista de IDs de pipes que deben haber finalizado con éxito (`PipeResult.success == True`) antes de ejecutar la pipe.
- Campos adicionales – valores arbitrarios que quedan disponibles como atributos de la configuración renderizada y que la pipe puede consumir.

## Modelo de ejecución

1. El orquestador elige la siguiente entrada cuyo intervalo `run_every_milli_seconds` haya expirado.
2. La definición `pipe` asociada se renderiza con un `Context` nuevo (`context.params` contiene la entrada de calendario; `context.pipes` comienza vacío).
3. Para cada pipe o paso:
   - Se evalúa la expresión `_if`. Si es falsa, se salta la pipe.
   - Se comprueban las dependencias listadas en `depends_on` revisando los valores `PipeResult.success` anteriores.
   - `PipeFactory` localiza la clase indicada en `use`, inyecta las dependencias de `injects` y ejecuta el método asíncrono `process()` (que
     internamente espera a `_process()`).
   - El valor devuelto se encapsula en un `PipeResult` (`success`, `failed`, `message`, `data`) y se almacena en `context.pipes[id]`.
4. Las funciones auxiliares disponibles en las plantillas (`get_pipe_result`, `has_failed`, etc.) leen de `context.pipes`, exponiendo resultados
   anteriores a los pasos posteriores.
5. Las pipes compuestas fusionan los resultados de sus hijos mediante `PipeResult.union` para ofrecer un único estado de éxito/fracaso y datos combinados.

## Uso de `PipeResult`

Cada estado guardado es un `PipeResult` (consulta `open_ticket_ai.core.pipeline.pipe_config`). Al crear pipes personalizadas:

- Devuelve un diccionario compatible con `PipeResult.model_validate`, o instancia `PipeResult(...)` y llama a `.model_dump()`.
- Coloca los datos que quieras reutilizar en el campo `data`.
- Ajusta `success`/`failed` y `message` según corresponda para que las plantillas tomen decisiones condicionales.

## Consejos de programación

- Las entradas de `orchestrator` son independientes; cada ejecución recibe un `Context` limpio.
- Puedes definir varias entradas que reutilicen la misma definición compuesta y solo cambien parámetros (por ejemplo, criterios de búsqueda o umbrales).
- Los intervalos se expresan en milisegundos; `run_every_milli_seconds: 60000` significa aproximadamente una ejecución por minuto.

Con esta estructura puedes diseñar flujos de trabajo complejos para tickets sin tocar el código Python: modifica la YAML y deja que el
orquestador reconstruya la pipeline en tiempo de ejecución.
