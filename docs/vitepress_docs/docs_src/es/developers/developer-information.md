---
description: Guía para desarrolladores del clasificador de tickets ATC on-premise. Aprenda a configurar con YAML, ejecutar desde la CLI y extender con componentes y adaptadores de Python personalizados.
title: Información para Desarrolladores
---
# Información para Desarrolladores de ATC Community Edition

## Descripción General

ATC Community Edition es una solución on-premise para la clasificación automatizada de tickets de soporte. La versión MVP actual se controla mediante un archivo de configuración YAML y se inicia a través de la CLI. No hay una API REST para cargar datos de entrenamiento o para iniciar una ejecución de entrenamiento.

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

El entrenamiento directo a través de la aplicación no se proporciona en el MVP. Se pueden especificar y utilizar modelos preentrenados en la configuración. Si un modelo necesita ser ajustado o creado de nuevo, esto debe hacerse fuera de la aplicación.

## Extensión

Se pueden implementar fetchers, preparers, servicios de IA o modifiers personalizados como clases de Python y registrarlos a través de la configuración. Gracias a la inyección de dependencias, los nuevos componentes se pueden integrar fácilmente.

## Cómo Añadir un Pipe Personalizado

El pipeline de procesamiento se puede extender con sus propias clases de pipe. Un pipe es una unidad de trabajo que recibe un `PipelineContext`, lo modifica y lo devuelve. Todos los pipes heredan de la clase base `Pipe`, que ya implementa el mixin `Providable`.

1. **Cree un modelo de configuración** para su pipe si necesita parámetros.
2. **Subclase de `Pipe`** e implemente el método `process`.
3. **Sobrescriba `get_provider_key()`** si desea una clave personalizada.

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

Después de implementar la clase, regístrela en su registro de inyección de dependencias y haga referencia a ella en `config.yml` utilizando la clave de proveedor (provider key) devuelta por `get_provider_key()`.

## Cómo Integrar un Nuevo Sistema de Tickets

Para conectar otro sistema de help desk, implemente un nuevo adaptador que herede de `TicketSystemAdapter`. El adaptador realiza la conversión entre la API externa y los modelos unificados del proyecto.

1. **Cree una clase de adaptador**, p. ej., `FreshdeskAdapter(TicketSystemAdapter)`.
2. **Implemente todos los métodos abstractos**:
    - `find_tickets`
    - `find_first_ticket`
    - `create_ticket`
    - `update_ticket`
    - `add_note`
3. **Traduzca los datos** desde y hacia los modelos `UnifiedTicket` y `UnifiedNote`.
4. **Proporcione un modelo de configuración** para las credenciales o la configuración de la API.
5. **Registre el adaptador** en `create_registry.py` para que pueda ser instanciado desde la configuración YAML.

Una vez registrado, especifique el adaptador en la sección `system` de `config.yml` y el orquestador lo usará para comunicarse con el sistema de tickets.

## Resumen

ATC Community Edition ofrece un flujo de trabajo ejecutado localmente para la clasificación automática de tickets en su versión MVP. Toda la configuración se gestiona a través de archivos YAML; no hay una API REST disponible. Se deben utilizar procesos o scripts externos para el entrenamiento.