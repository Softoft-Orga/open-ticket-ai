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

* **core** – clases base, modelos de configuración y funciones de ayuda.
* **run** – contiene el pipeline para la clasificación de tickets.
* **ticket\_system\_integration** – adaptadores para diferentes sistemas de tickets.
* **main.py** – punto de entrada de la CLI que inicia el planificador (scheduler) y el orquestador.

El orquestador ejecuta `AttributePredictors` configurables, que se componen de `DataFetcher`, `DataPreparer`, `AIInferenceService` y `Modifier`. Todos los componentes se definen en `config.yml` y se validan al iniciar el programa.

Un comando de ejemplo para iniciar la aplicación:

```bash
python -m open_ticket_ai.src.ce.main start
```

## Entrenamiento de Modelos Personalizados

El entrenamiento directo a través de la aplicación no está disponible en el MVP. Se pueden especificar y utilizar modelos pre-entrenados en la configuración. Si un `model` necesita ser ajustado o creado de nuevo, esto debe hacerse fuera de la aplicación.

## Extensión

Se pueden implementar fetchers, preparers, servicios de IA o modifiers personalizados como clases de Python y registrarlos a través de la configuración. Gracias a la inyección de dependencias, los nuevos componentes se pueden integrar fácilmente.

## Cómo Añadir un Pipe Personalizado

El pipeline de procesamiento se puede extender con tus propias clases de pipe. Un pipe es una
unidad de trabajo que recibe un `PipelineContext`, lo modifica y lo devuelve. Todos
los pipes heredan de la clase base `Pipe`, que ya
implementa el mixin `Providable`.

1. **Crea un modelo de configuración** para tu pipe si necesita parámetros.
2. **Subclasea `Pipe`** e implementa el método `process`.
3. **Sobrescribe `get_provider_key()`** si quieres una clave personalizada.

El siguiente ejemplo simplificado del `AI_README` muestra un pipe de análisis de sentimiento:

```python
class SentimentPipeConfig(BaseModel):
    model_name: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"


class SentimentAnalysisPipe(Pipe, Providable):
    def __init__(self, config: SentimentPipeConfig):
        super().__init__(config)
        self.classifier = pipeline("sentiment-analysis", model=config.model_name)

    def process(self, context: PipelineContext) -> PipelineContext:
        ticket_text = context.data.get("combined_text")
        if not ticket_text:
            context.stop_pipeline()
            return context

        sentiment = self.classifier(ticket_text)[0]
        context.data["sentiment"] = sentiment["label"]
        context.data["sentiment_confidence"] = sentiment["score"]
        return context

    @classmethod
    def get_provider_key(cls) -> str:
        return "SentimentAnalysisPipe"
```

Después de implementar la `class`, regístrala en tu registro de inyección de dependencias
y haz referencia a ella en `config.yml` usando la clave de proveedor devuelta por
`get_provider_key()`.

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