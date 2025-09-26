---
description: Ajusta un modelo de IA con los datos de tus tickets para una clasificación precisa y automatizada.
  Esta guía muestra cómo preparar datasets y entrenar con Hugging Face o una API REST.
---
# Cómo ajustar un modelo de IA con tus propios datos de tickets

El ajuste fino (fine-tuning) de un modelo de IA con tus propios datos de tickets es una forma poderosa de personalizar la clasificación de tickets para tu organización. Al entrenar un modelo con tickets de soporte etiquetados, le enseñas el lenguaje y las categorías específicas de tu dominio. Este proceso generalmente implica preparar un dataset (a menudo un archivo CSV o JSON de tickets y etiquetas), elegir o crear etiquetas (como departamentos o niveles de prioridad) y luego entrenar un modelo como un clasificador basado en Transformers con esos datos. Puedes usar herramientas como la biblioteca Transformer de Hugging Face para entrenar modelos localmente, o usar una solución dedicada como **Open Ticket AI (ATC)**, que proporciona una API REST on-premise para la clasificación de tickets. En cualquier caso, te beneficias del aprendizaje por transferencia (transfer learning): un modelo preentrenado (p. ej., BERT, DistilBERT o RoBERTa) se adapta a las categorías de tus tickets, mejorando enormemente la precisión en comparación con un modelo genérico.

Los flujos de trabajo modernos de clasificación de texto siguen estos pasos de alto nivel:

* **Recopilar y etiquetar datos:** Reúne tickets históricos y asígnales las categorías (colas) o prioridades correctas. Cada ticket debe tener un campo de texto y al menos una etiqueta.
* **Formatear el dataset:** Guarda estos datos etiquetados en un formato estructurado (CSV o JSON). Por ejemplo, un CSV podría tener las columnas `"text"`, `"label"`.
* **Dividir en entrenamiento/prueba:** Reserva una porción para validación/prueba para evaluar el rendimiento.
* **Ajustar el modelo:** Usa una biblioteca como Hugging Face Transformers, o nuestra API de Open Ticket AI, para entrenar un modelo de clasificación con los datos.
* **Evaluar y desplegar:** Verifica la precisión (o F1) en los datos de prueba y luego usa el modelo entrenado para clasificar nuevos tickets.

Los lectores con conocimientos técnicos pueden seguir estos pasos en detalle. Los ejemplos a continuación ilustran cómo preparar datos de tickets y ajustar un modelo usando **Hugging Face Transformers**, así como la forma en que nuestra solución Open Ticket AI soporta este flujo de trabajo a través de llamadas a la API. A lo largo del texto, asumimos categorías de tickets comunes (p. ej., “Facturación”, “Soporte Técnico”) y etiquetas de prioridad, pero tus etiquetas pueden ser cualquier cosa relevante para tu sistema.

## Preparando tus datos de tickets

Primero, reúne un conjunto representativo de tickets pasados y etiquétalos según tu esquema de clasificación. Las etiquetas podrían ser departamentos (como **Soporte Técnico**, **Atención al Cliente**, **Facturación**, etc.) o niveles de prioridad (p. ej., **Bajo**, **Medio**, **Alto**). Por ejemplo, el dataset de tickets de Softoft incluye categorías como *Soporte Técnico*, *Facturación y Pagos*, *Soporte de TI* y *Consulta General*. Un modelo de ejemplo de Hugging Face usa etiquetas como *Pregunta de Facturación*, *Solicitud de Característica*, *Consulta General* y *Problema Técnico*. Define las categorías que tengan sentido para tu flujo de trabajo.

Organiza los datos en formato CSV o JSON. Cada registro debe contener el texto del ticket y su etiqueta. Por ejemplo, un CSV podría verse así:

```
text,label
"My printer will not connect to WiFi",Hardware,  # Example ticket text and its category
"I need help accessing my account",Account
```

Si incluyes prioridades o múltiples etiquetas, podrías añadir más columnas (p. ej., `priority`). La estructura exacta es flexible, siempre que mapees claramente cada texto de ticket a su(s) etiqueta(s). Es común tener una columna para el contenido del ticket (p. ej., `"text"` o `"ticket_text"`) y una columna para la etiqueta.

Es posible que necesites limpiar y preprocesar el texto ligeramente (p. ej., eliminar firmas, etiquetas HTML o anonimizar datos), pero en muchos casos el texto crudo del ticket funciona bien como entrada para los modelos modernos de NLP. Finalmente, divide los datos etiquetados en un conjunto de entrenamiento y un conjunto de validación/prueba (por ejemplo, 80% entrenamiento / 20% prueba). Esta división te permite medir qué tan bien generaliza el modelo ajustado.

## Etiquetado de tickets

Las etiquetas consistentes y precisas son cruciales. Asegúrate de que cada ticket esté correctamente asignado a una de tus categorías elegidas. Esto puede hacerse manualmente por el personal de soporte o utilizando metadatos de tickets existentes si están disponibles. A menudo, las organizaciones etiquetan los tickets por *cola* o departamento, y a veces también por *prioridad*. Por ejemplo, el dataset de tickets de correo electrónico de Softoft categoriza los tickets tanto por departamento (cola) como por prioridad. La prioridad puede ser útil si quieres entrenar un modelo para predecir la urgencia: p. ej., `Low`, `Medium`, `Critical`. En muchas configuraciones, podrías entrenar un modelo para la clasificación de departamentos y otro para la clasificación de prioridades.

Cualquiera que sea tu esquema, asegúrate de tener un conjunto finito de valores de etiqueta. En un CSV, podrías tener:

```
text,label,priority
"System crash when saving file","Technical Support","High"
"Request to change billing address","Billing","Low"
```

Este ejemplo tiene dos columnas de etiquetas: una para la categoría y otra para la prioridad. Para simplificar, en los siguientes ejemplos asumimos una tarea de clasificación de etiqueta única (una columna de etiqueta).

**Consejos clave para el etiquetado:**

* Define los nombres de tus etiquetas claramente. Por ejemplo, *Soporte Técnico* vs *Soporte de TI* vs *Problema de Hardware* – evita la superposición ambigua.
* Si los tickets a menudo pertenecen a múltiples categorías, podrías considerar la clasificación multietiqueta (asignar múltiples etiquetas) o dividirlo en modelos separados.
* Usa un formato consistente (misma ortografía, mayúsculas/minúsculas) para las etiquetas en tu dataset.

Al final de este paso, deberías tener un archivo de dataset etiquetado (CSV o JSON) con los textos de los tickets y sus etiquetas, listo para el modelo.

## Ajuste fino con Hugging Face Transformers

Una de las formas más flexibles de ajustar un clasificador de texto es usando la biblioteca [Hugging Face Transformers](https://huggingface.co/transformers/). Esto te permite partir de un modelo de lenguaje preentrenado (como BERT o RoBERTa) y entrenarlo más a fondo con tu dataset de tickets específico. Los pasos principales son: tokenizar el texto, configurar un `Trainer` y llamar a `train()`.

1. **Cargar el dataset:** Usa `datasets` o `pandas` para cargar tu CSV/JSON. Por ejemplo, la biblioteca `datasets` de Hugging Face puede leer un CSV directamente:

   ```python
   from datasets import load_dataset
   dataset = load_dataset("csv", data_files={
       "train": "tickets_train.csv",
       "validation": "tickets_val.csv"
   })
   # Assuming 'text' is the column with ticket content, and 'label' is the category column.
   ```

2. **Tokenizar el texto:** Los transformers preentrenados requieren una entrada tokenizada. Carga un tokenizador (p. ej., DistilBERT) y aplícalo a tu texto:

   ```python
   from transformers import AutoTokenizer
   tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

   def preprocess_function(examples):
       # Tokenize the texts (this will produce input_ids, attention_mask, etc.)
       return tokenizer(examples["text"], truncation=True, padding="max_length")

   tokenized_datasets = dataset.map(preprocess_function, batched=True)
   ```

   Esto sigue el ejemplo de Hugging Face: primero carga el tokenizador DistilBERT, luego usa `Dataset.map` para tokenizar todos los textos en lotes. El resultado (`tokenized_datasets`) contiene los IDs de entrada y las máscaras de atención, listos para el modelo.

3. **Cargar el modelo:** Elige un modelo preentrenado y especifica el número de etiquetas. Por ejemplo, para ajustar DistilBERT para clasificación:

   ```python
   from transformers import AutoModelForSequenceClassification
   num_labels = 4  # set this to the number of your categories
   model = AutoModelForSequenceClassification.from_pretrained(
       "distilbert-base-uncased", num_labels=num_labels
   )
   ```

   Esto coincide con el ejemplo de clasificación de secuencias de Hugging Face, donde el modelo se carga con `num_labels` igual al número de clases en tu dataset.

4. **Establecer argumentos de entrenamiento y el Trainer:** Define los hiperparámetros con `TrainingArguments`, luego crea un `Trainer` con tu modelo y los datos tokenizados:

   ```python
   from transformers import TrainingArguments, Trainer
   training_args = TrainingArguments(
       output_dir="./ticket_model",
       num_train_epochs=3,
       per_device_train_batch_size=8,
       per_device_eval_batch_size=8,
       learning_rate=2e-5,
       evaluation_strategy="epoch"
   )
   trainer = Trainer(
       model=model,
       args=training_args,
       train_dataset=tokenized_datasets["train"],
       eval_dataset=tokenized_datasets["validation"],
       tokenizer=tokenizer
   )
   ```

   Esto refleja la guía de Hugging Face: después de configurar `TrainingArguments` (para el directorio de salida, épocas, tamaño de lote, etc.), instanciamos `Trainer` con el modelo, los datasets, el tokenizador y los argumentos de entrenamiento.

5. **Entrenar el modelo:** Llama a `trainer.train()` para iniciar el ajuste fino. Esto se ejecutará durante el número de épocas especificado, evaluando periódicamente en el conjunto de validación si se proporciona.

   ```python
   trainer.train()
   ```

   Según la documentación, este único comando inicia el ajuste fino. El entrenamiento puede tardar de minutos a horas dependiendo del tamaño de los datos y del hardware (se recomienda una GPU para datasets grandes).

6. **Evaluar y guardar:** Después del entrenamiento, evalúa el modelo en tu conjunto de prueba para verificar la precisión u otras métricas. Luego guarda el modelo ajustado y el tokenizador:

   ```python
   trainer.evaluate()
   model.save_pretrained("fine_tuned_ticket_model")
   tokenizer.save_pretrained("fine_tuned_ticket_model")
   ```

   Más tarde puedes recargar este modelo con `AutoModelForSequenceClassification.from_pretrained("fine_tuned_ticket_model")`.

Una vez entrenado, puedes usar el modelo para la inferencia. Por ejemplo, la API `pipeline` de Hugging Face lo hace fácil:

```python
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
results = classifier("Please reset my password and clear my cache.")
print(results)
```

Esto mostrará la etiqueta predicha y la confianza para el nuevo texto del ticket. Como demuestran los ejemplos de Hugging Face, la abstracción `pipeline("text-classification")` te permite clasificar rápidamente nuevos textos de tickets con el modelo ajustado.

## Usando Open Ticket AI (ATC de Softoft) para entrenamiento e inferencia

Nuestro sistema **Open Ticket AI** (también conocido como ATC – AI Ticket Classification) proporciona una solución on-premise, en contenedores Docker, con una API REST que puede ingerir tus datos de tickets etiquetados y entrenar modelos automáticamente. Esto significa que puedes mantener todos los datos de forma local y aun así aprovechar el potente ML. La API de ATC tiene endpoints para subir datos, iniciar el entrenamiento y clasificar tickets.

* **Subir datos de entrenamiento:** Envía tu CSV de tickets etiquetados al endpoint `/api/v1/train-data`. La API espera un payload CSV (`Content-Type: text/csv`) que contenga tus datos de entrenamiento. Por ejemplo, usando `requests` de Python:

  ```python
  import requests
  url = "http://localhost:8080/api/v1/train-data"
  headers = {"Content-Type": "text/csv"}
  with open("tickets_labeled.csv", "rb") as f:
      res = requests.post(url, headers=headers, data=f)
  print(res.status_code, res.text)
  ```

  Esto corresponde a la API “Train Data” en la documentación de ATC. Una respuesta exitosa significa que los datos han sido recibidos.

* **Iniciar el entrenamiento del modelo:** Después de subir los datos, inicia el entrenamiento llamando a `/api/v1/train` (no se necesita cuerpo de solicitud). En la práctica:

  ```bash
  curl -X POST http://localhost:8080/api/v1/train
  ```

  O en Python:

  ```python
  train_res = requests.post("http://localhost:8080/api/v1/train")
  print(train_res.status_code, train_res.text)
  ```

  Esto coincide con el ejemplo de la documentación para desarrolladores, que muestra que un simple POST inicia el entrenamiento. El servicio entrenará el modelo con los datos subidos (utiliza su propio pipeline de entrenamiento internamente, posiblemente basado en modelos Transformer similares). El entrenamiento se ejecuta en tu servidor y el modelo se guarda localmente cuando termina.

* **Clasificar nuevos tickets:** Una vez que el entrenamiento está completo, usa el endpoint `/api/v1/classify` para obtener predicciones para nuevos textos de tickets. Envía un payload JSON con el campo `"ticket_data"` que contenga el texto del ticket. Por ejemplo:

  ```python
  ticket_text = "My laptop overheats when I launch the app"
  res = requests.post(
      "http://localhost:8080/api/v1/classify",
      json={"ticket_data": ticket_text}
  )
  print(res.json())  # e.g. {"predicted_label": "Hardware Issue", "confidence": 0.95}
  ```

  La documentación de ATC muestra un ejemplo similar con `curl` para la clasificación. La respuesta típicamente incluirá la categoría predicha (y posiblemente la confianza).

Usar la API REST de Open Ticket AI integra el flujo de entrenamiento en tus propios sistemas. Puedes automatizar las subidas y las ejecuciones de entrenamiento (p. ej., entrenamiento nocturno o entrenamiento con datos nuevos), y luego usar el endpoint de clasificación en tu flujo de trabajo de tickets. Como todo se ejecuta on-premise, el contenido sensible de los tickets nunca sale de tus servidores.

## Ejemplo de código Python

A continuación se muestra un ejemplo consolidado que ilustra ambos flujos de trabajo:

```python
# Example: Fine-tuning with Hugging Face
from transformers import AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
from datasets import load_dataset

# Load and split your CSV dataset
dataset = load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


# Tokenize
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")


tokenized = dataset.map(preprocess, batched=True)

# Load model
num_labels = 5  # e.g., number of ticket categories
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=num_labels
    )

# Set up Trainer
training_args = TrainingArguments(
    output_dir="./model_out", num_train_epochs=3, per_device_train_batch_size=8
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    tokenizer=tokenizer
)
trainer.train()
trainer.evaluate()
model.save_pretrained("fine_tuned_ticket_model")
tokenizer.save_pretrained("fine_tuned_ticket_model")

# Use the model for classification
from transformers import pipeline

classifier = pipeline("text-classification", model="fine_tuned_ticket_model")
print(classifier("Example: The app crashes when I try to open it"))

# Example: Using Open Ticket AI API
import requests

# Upload data (CSV)
with open("tickets_labeled.csv", "rb") as data_file:
    res = requests.post(
        "http://localhost:8080/api/v1/train-data",
        headers={"Content-Type": "text/csv"},
        data=data_file
        )
    print("Upload status:", res.status_code)
# Trigger training
train_res = requests.post("http://localhost:8080/api/v1/train")
print("Training status:", train_res.status_code)
# Classify new ticket
res = requests.post(
    "http://localhost:8080/api/v1/classify",
    json={"ticket_data": "Cannot log into account"}
    )
print("Prediction:", res.json())
```

Este script demuestra ambos métodos: el pipeline de ajuste fino de Hugging Face y las llamadas REST a Open Ticket AI. Carga y tokeniza un dataset CSV, ajusta un clasificador DistilBERT y luego lo utiliza a través de un pipeline. También muestra cómo hacer POST de los mismos datos a la API de ATC para iniciar el entrenamiento/clasificación.

## Conclusión

El ajuste fino de un modelo de IA con tus propios datos de tickets permite una clasificación de tickets altamente precisa y personalizada. Al etiquetar tickets pasados y entrenar un modelo como un Transformer, aprovechas el aprendizaje por transferencia y el conocimiento del dominio. Ya sea que uses las APIs de Python de Hugging Face o una solución llave en mano como Open Ticket AI (el servicio de clasificación on-premise de Softoft), el flujo de trabajo es similar: prepara los datos etiquetados, entrena con ellos y luego usa el modelo entrenado para hacer predicciones.

Hemos mostrado cómo estructurar tu dataset CSV/JSON, usar la API `Trainer` de Hugging Face para el ajuste fino, y usar la API REST de Open Ticket AI para el entrenamiento e inferencia on-premise. La documentación de Hugging Face proporciona una guía detallada sobre el uso de tokenizadores y el `Trainer`, y las tarjetas de modelo de ejemplo ilustran cómo se aplican los modelos de clasificación al enrutamiento de tickets. Con estas herramientas, puedes iterar rápidamente: prueba diferentes modelos preentrenados (p. ej., BERT, RoBERTa, o incluso modelos específicos del dominio), experimenta con hiperparámetros y mide el rendimiento en tu conjunto de prueba.

Siguiendo estos pasos, tu sistema de soporte puede enrutar automáticamente los tickets al equipo correcto, marcar problemas urgentes y ahorrar a tu personal incontables horas de clasificación manual. Esta profunda integración de NLP en tu flujo de trabajo de tickets es ahora accesible con bibliotecas y APIs modernas – solo necesitas proporcionar tus datos y etiquetas.