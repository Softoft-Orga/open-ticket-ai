---
description: Ahorra tiempo etiquetando miles de tickets. Aprende un flujo de trabajo semiautomatizado
  usando GPT para el pre-etiquetado zero-shot y Label Studio para una revisión eficiente.
---
# Etiquetado Eficiente de 10,000 Tickets: Estrategias de Etiquetado Semiautomatizado

Etiquetar miles de tickets de soporte manualmente consume mucho tiempo y es costoso. Un **flujo de trabajo semiautomatizado** aprovecha los modelos de lenguaje grandes (LLMs) como GPT para **pre-etiquetar** tickets (usando prompts zero-shot/few-shot) y luego utiliza anotadores humanos para **revisar y corregir** esas etiquetas.
Este enfoque híbrido reduce drásticamente el esfuerzo de anotación: por ejemplo, un caso de estudio encontró que las "pre-anotaciones" generadas por GPT eran *“lo suficientemente buenas como para ayudarnos a acelerar el proceso de etiquetado”*. En
la práctica, las *etiquetas mínimas* del modelo pueden reducir el tiempo y el costo de la anotación. En este artículo explicamos cómo configurar una pipeline de este tipo, mostramos ejemplos en Python (usando GPT a través de OpenRouter u OpenAI)
y discutimos herramientas como Label Studio para la revisión.

## Uso de GPT para Pre-etiquetado Zero-Shot/Few-Shot

Los LLMs modernos pueden clasificar texto con **cero o pocos ejemplos**. En el etiquetado zero-shot, el modelo
asigna categorías sin haber sido entrenado explícitamente con datos de tickets. Como lo expresa un tutorial:
*“El aprendizaje zero-shot permite a los modelos clasificar nuevas instancias sin ejemplos etiquetados”*. En
la práctica, se elabora un prompt que instruye a GPT para que etiquete un ticket. Por ejemplo:

```text
Ticket: "Cannot login to account."
Classify this ticket into one of {Bug, Feature Request, Question}.
```

El modelo responde entonces con una etiqueta. El etiquetado few-shot añade un par de ejemplos en el prompt para
mejorar la precisión. Esto significa que podemos generar etiquetas iniciales **directamente a través de la API** sin ningún
entrenamiento del modelo.

> **Consejo:** Usa un prompt estructurado o solicita una salida en JSON para facilitar el análisis. Por ejemplo:
>
> ```
> Ticket: "Password reset email bounced."
> Respond in JSON like {"category": "..."}.
> ```
>
> Esto ayuda a integrar la respuesta en tu pipeline.

## Ejemplo: Código Python para Pre-etiquetado

A continuación se muestra un ejemplo en Python que utiliza la API de OpenAI a través de la librería `openai`. Recorre una lista de tickets de prueba, le pide a GPT-4 que clasifique cada ticket y registra la categoría. (También puedes
usar [OpenRouter](https://openrouter.ai) de manera similar estableciendo
`base_url="https://openrouter.ai/api/v1"` y cambiando el parámetro `model`.)

```python
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"
tickets = [
    {"id": 1, "text": "User cannot login to account", "category": None},
    {"id": 2, "text": "Error 404 when uploading file", "category": None},
    {"id": 3, "text": "Request to add dark mode feature", "category": None},
    {"id": 4, "text": "Payment declined on checkout", "category": None},
]
categories = ["Bug", "Feature Request", "Question"]

for ticket in tickets:
    prompt = f"Ticket: \"{ticket['text']}\". Classify it as one of {categories}."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    # Extract the category from GPT's reply
    ticket["category"] = response.choices[0].message.content.strip()

print(tickets)
```

Después de ejecutar esto, `tickets` podría convertirse en:

```python
[
    {'id': 1, 'text': 'User cannot login to account', 'category': 'Bug'},
    {'id': 2, 'text': 'Error 404 when uploading file', 'category': 'Bug'},
    {'id': 3, 'text': 'Request to add dark mode feature', 'category': 'Feature Request'},
    {'id': 4, 'text': 'Payment declined on checkout', 'category': 'Bug'}
]
```

Estas son **pre-etiquetas** que los revisores humanos verificarán. Observa cómo OpenRouter facilita el cambio de modelos:
al cambiar `model="openai/gpt-4"` a otro proveedor (p. ej. Claude o un modelo más ligero), el
mismo código funciona. De hecho, la API unificada de OpenRouter te permite probar múltiples proveedores o usar modelos de respaldo
si uno está caído. Por ejemplo:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY",
)
client.chat.completions.create(
    model="openai/gpt-4o",  # try GPT-4 first
    extra_body={"models": ["anthropic/claude-3.5-sonnet", "google/palm-2"]},
    messages=[{"role": "user", "content": "Ticket: 'Login page error'. Classify it."}]
)
```

Esto usará GPT-4 si está disponible; de lo contrario, recurrirá a Claude o PaLM como se muestra en la documentación de OpenRouter.
Dicha flexibilidad es útil para empresas que necesitan alta disponibilidad o que comparan modelos.

## Integración de Pre-etiquetas con Herramientas de Etiquetado

Una vez que GPT genera las etiquetas, el siguiente paso es **importarlas a una interfaz de etiquetado** para la revisión humana.
Una solución popular de código abierto es [Label Studio](https://labelstud.io). Label Studio
admite la importación de predicciones del modelo como "pre-anotaciones" junto con los datos. Los anotadores ven la
etiqueta sugerida y solo necesitan corregir los errores, no etiquetar desde cero. En efecto, el equipo
*“pasa de la tarea intensiva en tiempo de etiquetado de datos al proceso mucho más eficiente de
revisar y refinar las etiquetas preliminares”*.

Label Studio incluso ofrece un backend de ML: puedes escribir un pequeño servidor usando la
`class` `LabelStudioMLBase` que llama a GPT para cada tarea. En su tutorial, Label Studio muestra
cómo envolver las llamadas a GPT-4 en esta `class` para devolver predicciones sobre la marcha. Alternativamente, puedes importar un archivo JSON de
predicciones. El formato JSON requerido tiene un campo `data` (el texto del ticket) y un array `predictions`
(que contiene cada etiqueta). Por ejemplo (simplificado):

```json
[
    {
        "data": {
            "text": "User cannot login to account"
        },
        "predictions": [
            {
                "result": [
                    {
                        "value": {
                            "choices": [
                                {
                                    "text": "Bug"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    },
    {
        "data": {
            "text": "Add dark mode to settings"
        },
        "predictions": [
            {
                "result": [
                    {
                        "value": {
                            "choices": [
                                {
                                    "text": "Feature Request"
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
]
```

Después de importar, Label Studio mostrará cada ticket con la etiqueta del modelo pre-rellenada. El
trabajo del anotador es **revisar y corregir**. Se ha demostrado que este flujo de trabajo semiautomatizado funciona
bien: un ejemplo de Kili Technology demostró la carga de un dataset pre-etiquetado con GPT y señaló *“hemos
pre-anotado nuestro dataset con éxito”* y que este enfoque *“tiene el potencial de ahorrarnos mucho
de tiempo”*. En la práctica, la precisión de GPT en el etiquetado puede ser de ~80–90%, lo que significa que los humanos solo corrigen
el 10–20% restante.

## Herramientas y Pasos del Flujo de Trabajo

Para resumir, una pipeline típica de etiquetado semiautomatizado se ve así:

* **Prepara el dataset de tickets.** Exporta tus 10,000 tickets sin etiquetar (p. ej. como JSON o CSV).
* **Genera pre-etiquetas a través de un LLM.** Ejecuta código (como el anterior) que llame a GPT-4 (u otro modelo a través de
  OpenRouter) para clasificar cada ticket. Guarda las respuestas.
* **Importa las predicciones a una herramienta de etiquetado.** Usa Label Studio (o similar) para cargar los tickets y
  asociar cada uno con la etiqueta generada por GPT (la “predicción”). La documentación de Label Studio explica cómo
  importar predicciones con tus datos.
* **Revisión humana.** Los anotadores revisan los tickets en Label Studio, aceptando o corrigiendo las
  etiquetas. Esto es mucho más rápido que etiquetar desde cero. La interfaz de Label Studio resalta la
  sugerencia del modelo para cada tarea, por lo que la tarea se convierte en una validación rápida.
* **Exporta las etiquetas finales.** Una vez revisadas, exporta las anotaciones corregidas para el entrenamiento de modelos o
  para análisis.

Las principales herramientas públicas que soportan este enfoque incluyen:

* **OpenRouter** – una puerta de enlace de API de LLM unificada (openrouter.ai). Te permite cambiar fácilmente entre
  GPT-4, Anthropic Claude, Google PaLM, etc. Incluso puedes especificar una lista de respaldo en una sola llamada a la API.
* **OpenAI API (GPT-4/3.5)** – el motor principal para generar etiquetas con prompts zero/few-shot.
* **Label Studio** – una UI de etiquetado de datos de código abierto. Admite la importación de predicciones y tiene un
  backend de ML para llamar a modelos.
* **Doccano** – una herramienta de código abierto más simple para la anotación de texto (clasificación, NER, etc.). No
  tiene integración nativa con LLM, pero aún puedes usar GPT offline para generar etiquetas y cargarlas
  como opciones iniciales.
* **Snorkel/Etiquetado Programático** – para algunos casos basados en reglas o de supervisión débil, herramientas como
  Snorkel pueden complementar las etiquetas de LLM, pero los LLMs modernos a menudo cubren muchos casos de forma nativa.

## Ejemplo de Datos de Tickets de Prueba

Para ilustrar, aquí hay algunos *datos de tickets de prueba* con los que podrías trabajar:

```python
tickets = [
    {"id": 101, "text": "Error 500 when saving profile", "label": None},
    {"id": 102, "text": "How do I change my subscription plan?", "label": None},
    {"id": 103, "text": "Feature request: dark mode in settings", "label": None},
    {"id": 104, "text": "Application crashes on startup", "label": None},
]
```

Podrías pasar cada `ticket['text']` a GPT con un prompt como:

```text
Ticket: "Error 500 when saving profile."
Classify this issue as one of {Bug, Feature, Question}.
```

Supongamos que GPT devuelve `"Bug"`, `"Question"`, `"Feature"`, `"Bug"` respectivamente. Después del bucle,
`tickets` podría ser:

```python
[
    {'id': 101, 'text': 'Error 500 when saving profile', 'label': 'Bug'},
    {'id': 102, 'text': 'How do I change my subscription plan?', 'label': 'Question'},
    {'id': 103, 'text': 'Feature request: dark mode in settings', 'label': 'Feature'},
    {'id': 104, 'text': 'Application crashes on startup', 'label': 'Bug'},
]
```

Estas etiquetas se cargarían luego en la interfaz de revisión. Incluso si algunas son incorrectas (p. ej., GPT podría
etiquetar erróneamente un bug complicado como una feature), el anotador solo necesita *corregirlas* en lugar de empezar
de cero. Empíricamente, las etiquetas generadas por GPT a menudo alcanzan una precisión de ~80–90%, por lo que la revisión es mucho
más rápida que el etiquetado completo.

## Resultados y Conclusiones Clave

El enfoque semiautomatizado escala bien. En un proyecto grande, los anotadores humanos podrían necesitar corregir
solo unos pocos cientos o miles de etiquetas en lugar de 10,000. Como observó el tutorial de Kili después de ejecutar las pre-etiquetas de GPT:
*“¡Genial! Hemos pre-anotado nuestro dataset con éxito. Parece que esta solución tiene
el potencial de ahorrarnos mucho tiempo en proyectos futuros.”*. En otras palabras, los LLMs sirven como un
multiplicador de fuerza. Aunque el modelo no es 100% correcto, **“acelera el proceso de etiquetado”** al
hacer la mayor parte del trabajo.

**Mejores prácticas:** Usa una temperatura baja (p. ej. 0.0–0.3) para obtener etiquetas consistentes y proporciona instrucciones
claras o una pequeña lista de ejemplos. Monitorea los errores de GPT: es posible que necesites ajustar los prompts o
agregar algunos ejemplos few-shot para las categorías con bajo rendimiento. Mantén el prompt simple (p. ej., “Clasifica el
texto del ticket en A, B o C”). También puedes agrupar múltiples tickets en una sola llamada a la API si el modelo y
la API lo permiten, para ahorrar costos. Y siempre incluye la revisión humana: esto asegura una alta calidad y detecta
cualquier error o deriva del LLM.

## Conclusión

El etiquetado semiautomatizado con GPT y herramientas como OpenRouter y Label Studio es una estrategia poderosa
para etiquetar rápidamente grandes datasets de texto. Al **pre-etiquetar 10,000 tickets con un LLM y luego
revisarlos**, las empresas pueden poner en marcha sus flujos de trabajo de IA con datos iniciales mínimos. Este enfoque
reduce drásticamente los costos y el tiempo, al tiempo que garantiza la calidad mediante la supervisión humana. Como señala
una guía de implementación, cambiar el flujo de trabajo de *“etiquetado de datos”* a *“revisión y refinamiento”*
de las etiquetas generadas por el LLM *“acelera significativamente tu flujo de trabajo.”*. En resumen, combinar
la pre-anotación basada en GPT con una UI amigable (Label Studio, Doccano, etc.) ayuda a los equipos de
software/IA a etiquetar datasets masivos de tickets de manera eficiente y precisa.