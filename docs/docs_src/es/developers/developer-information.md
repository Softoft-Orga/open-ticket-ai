---
description: Guía de desarrollo para el clasificador de tickets ATC on-premise. Aprende
  a configurar con YAML, ejecutar desde la CLI y extender con componentes y adaptadores
  de Python personalizados.
title: Información para Desarrolladores
---
# Información para Desarrolladores de ATC Community Edition

## Resumen General

ATC Community Edition es una solución on-premise para la clasificación automatizada de tickets de soporte. La versión MVP actual se controla a través de un archivo de configuración YAML y se inicia mediante la CLI. No existe una API REST para cargar datos de entrenamiento o para iniciar una ejecución de entrenamiento.

## Arquitectura del Software

La aplicación consta esencialmente de los siguientes paquetes:

* **core** – modelos de configuración, utilidades de inyección de dependencias, el motor de la pipeline y el renderizado de plantillas.
* **base** – implementaciones reutilizables de pipes (por ejemplo, obtención/actualización de tickets y pipes compuestas).
* **hf_local** – pipes de inferencia con HuggingFace incluidas como ejemplos.
* **ticket\_system\_integration** – adaptadores para diferentes sistemas de tickets.
* **main.py** – punto de entrada de la CLI que conecta inyector, planificador y orquestador.

El orquestador ahora ejecuta grafos de `Pipe` definidos en YAML. Las definiciones se componen a partir de `defs` reutilizables, se renderizan con el alcance actual y se resuelven en tiempo de ejecución a través del contenedor de inyección de dependencias. Cada entrada del calendario indica qué árbol de pipes debe ejecutarse y con qué frecuencia debe dispararlo el orquestador.

Un comando de ejemplo para iniciar la aplicación:

```bash
python -m open_ticket_ai.src.ce.main start
```

## Arquitectura de la Pipeline

La pipeline en tiempo de ejecución se describe en YAML. `RawOpenTicketAIConfig` agrupa plugins, configuración global, `defs` reutilizables y el calendario `orchestrator` que indica qué pipes deben ejecutarse y en qué intervalo. Al arrancar, el contenedor de inyección de dependencias carga este archivo, crea servicios singleton definidos en `defs` y los registra en el `UnifiedRegistry`. Las pipes y las plantillas pueden referenciar estos servicios por ID.

Cada entrada de la pipeline se normaliza como un `RegisterableConfig` con un `id`, la clase objetivo en `use`, `steps` opcionales y metadatos de orquestación como `_if` y `depends_on`. En tiempo de ejecución la configuración se renderiza contra el `Context` actual, de modo que las expresiones Jinja2 (por ejemplo `get_pipe_result('classify', 'label')`) pueden reutilizar resultados previos. Las expresiones `if:` activan o desactivan pipes por ejecución y `depends_on` garantiza que una pipe solo se ejecute tras el éxito de sus dependencias.

El `Context` mantiene dos diccionarios: `pipes` almacena el `PipeResult` (success/failed/message/data) de cada paso y `params` expone la configuración renderizada para la entrada del calendario activa. Las pipes leen este contexto, realizan su trabajo dentro del método asíncrono `_process()` y devuelven datos que se guardan como `PipeResult.data`. Así, las pipes y plantillas posteriores pueden reaccionar ante errores o reutilizar resultados.

El campo `orchestrator` en YAML es una lista de entradas de calendario. Cada entrada define `run_every_milli_seconds` y una definición `pipe` que puede ser una pipe compuesta con `steps` anidados. El planificador recorre esta lista, dispara ejecuciones cuando vence cada intervalo y entrega al orquestador un `Context` nuevo inicializado con la configuración del calendario.

## Entrenamiento de Modelos Personalizados

El entrenamiento directo a través de la aplicación no está disponible en el MVP. Se pueden especificar y utilizar modelos pre-entrenados en la configuración. Si un `model` necesita ser ajustado o creado de nuevo, esto debe hacerse fuera de la aplicación.

## Extensión

Se pueden implementar fetchers, preparers, servicios de IA o modifiers personalizados como clases de Python y registrarlos a través de la configuración. Gracias a la inyección de dependencias, los nuevos componentes se pueden integrar fácilmente.

## Cómo Añadir un Pipe Personalizado

El pipeline de procesamiento se puede ampliar con clases de pipe propias. Un pipe es una unidad de trabajo que utiliza el `Context`, consulta `PipeResult` almacenados previamente y produce un nuevo `PipeResult` con datos y estado actualizados.

1. **Define (si lo necesitas) un modelo de configuración** para los parámetros del pipe.
2. **Hereda de `Pipe`** e implementa el método asíncrono `_process()`.
3. **Devuelve un diccionario** con el formato de `PipeResult` (o usa `PipeResult(...).model_dump()`).

El siguiente ejemplo simplificado muestra un pipe de análisis de sentimiento con HuggingFace ejecutándose localmente:

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
            return PipeResult(success=False, failed=True, message="No hay texto disponible", data={}).model_dump()

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

Después de implementarla, regístrala dentro de `open_ticket_ai.defs` (o en `infrastructure.pipe_classes`) para que la pipeline en YAML pueda referenciarla por su `id`. Gracias a que el orquestador renderiza la configuración con Jinja2, puedes incluir expresiones que reutilicen variables de entorno o resultados de pipes anteriores.

## Cómo Integrar un Nuevo Sistema de Tickets

Para conectar otro sistema de help desk, implementa un nuevo adaptador que herede de
`TicketSystemAdapter`. El adaptador convierte entre la API externa y los
modelos unificados del proyecto.

1. **Crea una clase de adaptador**, por ejemplo, `FreshdeskAdapter(TicketSystemAdapter)`.
2. **Implementa todos los métodos abstractos**:
    - `find_tickets`
    - `find_first_ticket`
    - `create_ticket`
    - `update_ticket`
    - `add_note`
3. **Traduce los datos** desde y hacia los modelos `UnifiedTicket` y `UnifiedNote`.
4. **Proporciona un modelo de configuración** para las credenciales o la configuración de la API.
5. **Registra el adaptador** en `create_registry.py` para que pueda ser instanciado
   desde la configuración YAML.

Una vez registrado, especifica el adaptador en la sección `system` de `config.yml` y
el orquestador lo usará para comunicarse con el sistema de tickets.

## Ejemplos de Configuración

Para ayudarte a comenzar rápidamente, hemos creado una colección de ejemplos de configuración listos para usar
que demuestran varios casos de uso. Estos ejemplos se encuentran en el directorio `docs/config_examples/`.

### Ejemplos Disponibles

1. **IA Añade Nota al Ticket** (`add_note_when_in_queue.yml`)
   - Añade automáticamente notas generadas por IA a tickets en colas específicas
   - Caso de uso: Agregar análisis o sugerencias a tickets en revisión

2. **Creación Condicional de Ticket** (`create_ticket_on_condition.yml`)
   - Crea automáticamente nuevos tickets basándose en condiciones detectadas
   - Caso de uso: Auto-crear tickets de escalación para problemas urgentes

3. **Clasificación de Cola** (`queue_classification.yml`)
   - Enruta tickets a colas apropiadas mediante análisis de IA
   - Caso de uso: Enrutamiento automático por departamento (IT, RRHH, Finanzas, etc.)

4. **Clasificación de Prioridad** (`priority_classification.yml`)
   - Asigna niveles de prioridad basados en análisis de urgencia del ticket
   - Caso de uso: Asegurar que los problemas críticos reciban atención inmediata

5. **Flujo de Trabajo Completo** (`complete_workflow.yml`)
   - Ejemplo completo que combina múltiples operaciones de IA
   - Caso de uso: Automatización completa con clasificación, notas y manejo de errores

### Uso de los Ejemplos

Cada ejemplo incluye:
- Configuración completa con todas las secciones requeridas
- Comentarios detallados explicando cada paso
- Parámetros personalizables para tu entorno
- Mejores prácticas para manejo de errores y mecanismos de respaldo

Para usar un ejemplo:
1. Explora los ejemplos en `docs/config_examples/`
2. Copia la configuración relevante a tu `config.yml`
3. Actualiza las variables de entorno y personaliza la configuración
4. Prueba primero con un subconjunto limitado de tickets

Para más detalles, consulta el [README en el directorio config_examples](../../config_examples/README.md).

## Resumen

ATC Community Edition ofrece un flujo de trabajo ejecutado localmente para la clasificación automática de tickets en su versión MVP. Todas las configuraciones se gestionan a través de archivos YAML; no hay una API REST disponible. Se deben utilizar procesos o scripts externos para el entrenamiento.