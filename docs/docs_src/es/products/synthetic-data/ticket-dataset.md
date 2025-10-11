---
description: Entrena modelos de cola, prioridad y tipo con nuestros tickets de soporte al cliente multilingües y sintéticos. Incluye campos enriquecidos y múltiples versiones. Disponible en Kaggle.
---
# Tickets de Soporte al Cliente Multilingües (Sintéticos)

Un conjunto de datos **totalmente sintético** para entrenar y evaluar modelos de mesa de ayuda, como la clasificación de **cola**, **prioridad** y **tipo**, además del preentrenamiento para asistencia en respuestas.
Creado con nuestro **Generador de Datos Sintéticos** en Python y publicado en **Kaggle**.

* **Kaggle:** [Conjunto de datos de tickets](https://www.kaggle.com/datasets/tobiasbueck/multilingual-customer-support-tickets/data)
* [Generación de Datos Sintéticos](synthetic-data-generation.md) (planeado como **LGPL**)
* **¿Necesita datos personalizados o la herramienta?** [sales@softoft.de](mailto:sales@softoft.de)

---

## Versiones de un vistazo

![Diagrama de red de versiones del conjunto de datos](/images/network_diagram.svg)

| Versión | Idiomas                       | Tamaño (relativo) | Notas                                                                         |
|--------:|-------------------------------|-------------------|-------------------------------------------------------------------------------|
|  **v5** | **EN, DE**                    | El más grande     | La taxonomía y el balanceo más recientes y refinados; se centra en la calidad de EN/DE. |
|  **v4** | **EN, DE**                    | Grande            | Enfoque similar a v5; prompts y distribuciones ligeramente más antiguos.        |
|  **v3** | EN, DE, **+ más (FR/ES/PT)**  | Más pequeño       | Pipeline anterior; más idiomas pero contenido general menos diverso.          |

> Las versiones más antiguas incluyen **más idiomas**, pero generalmente son **más pequeñas** y **menos diversas**.
> Las versiones más recientes (**v5**, **v4**) enfatizan la calidad y la escala de **EN/DE**.

### ¿Qué versión debería usar?

* **Entrenamiento de modelos de producción EN/DE** → comienza con **v5** (o **v4** si necesitas un conjunto comparable más antiguo).
* **Investigación en múltiples idiomas** → **v3** (más pequeño, pero incluye más localizaciones).

---

## Archivos y nomenclatura

Encontrarás exportaciones CSV por versión (ejemplos):

```
dataset-tickets-multi-lang-4-20k.csv
dataset-tickets-multi-lang3-4k.csv
dataset-tickets-german_normalized.csv
```

---

## Esquema

Cada ticket incluye el texto principal más las etiquetas utilizadas por **Open Ticket AI**.

| Columna             | Descripción                                                  |
|---------------------|--------------------------------------------------------------|
| `subject`           | El asunto del correo electrónico del cliente                 |
| `body`              | El cuerpo del correo electrónico del cliente                 |
| `answer`            | La primera respuesta del agente (generada por IA)            |
| `type`              | Tipo de ticket (p. ej., Incidente, Solicitud, Problema, …)   |
| `queue`             | Cola de destino (p. ej., Soporte Técnico, Facturación)       |
| `priority`          | Prioridad (p. ej., baja, media, alta)                        |
| `language`          | Idioma del ticket (p. ej., `en`, `de`, …)                    |
| `version`           | Versión del conjunto de datos (metadatos)                    |
| `tag_1`, `tag_2`, … | Una o más etiquetas temáticas (puede ser `null` en algunos casos) |

### Fragmentos de los datos

* **de (Incidente / Soporte Técnico / alta)**
  *Asunto:* Wesentlicher Sicherheitsvorfall
  *Cuerpo (extracto):* „…ich möchte einen gravierenden Sicherheitsvorfall melden…“
  *Respuesta (extracto):* „Vielen Dank für die Meldung…“

* **en (Incidente / Soporte Técnico / alta)**
  *Asunto:* Account Disruption
  *Cuerpo (extracto):* “I am writing to report a significant problem with the centralized account…”
  *Respuesta (extracto):* “We are aware of the outage…”

* **en (Solicitud / Devoluciones y Cambios / media)**
  *Asunto:* Query About Smart Home System Integration Features
  *Cuerpo (extracto):* “I am reaching out to request details about…”
  *Respuesta (extracto):* “Our products support…”

---

## Recorrido visual

![Nube de palabras de los asuntos de los tickets](/images/word_cloud.png)

![Etiquetas más utilizadas](/images/tags.png)

![Distribuciones para cola, prioridad, idioma, tipo](/images/basic_distribution.png)

---

## Uso previsto y limitaciones

**Uso previsto:**

* Entrenamiento de modelos desde cero para **cola/prioridad/tipo**
* Experimentos de balanceo de clases
* Benchmarking multilingüe (usa **v3** si necesitas FR/ES/PT)

**Limitaciones:**

* Las distribuciones sintéticas pueden diferir del tráfico de tu entorno de producción. Valida siempre con una muestra real, pequeña y anonimizada antes del despliegue.

---

## Cómo cargar y comprobaciones rápidas

```python
import pandas as pd

df = pd.read_csv("dataset-tickets-multi-lang-4-20k.csv")  # o la versión que elijas

# Comprobaciones básicas
print(df.language.value_counts())
print(df.queue.value_counts().head())

# Preparar texto simple para clasificación
X = (df["subject"].fillna("") + "\n\n" + df["body"].fillna("")).astype(str)
y = df["queue"].astype(str)
```

---

## Relación con Open Ticket AI

Este conjunto de datos refleja las etiquetas que **Open Ticket AI** predice en los tickets entrantes (**cola**, **prioridad**, **tipo**, **etiquetas**).
Úsalo para **iniciar** el entrenamiento y la evaluación; despliega tu modelo con **Open Ticket AI** una vez que estés satisfecho con las métricas.

* [Generador de Datos Sintéticos](synthetic-data-generation.md)
* [API de Predicción (alojada)](../prediction-api/overview.md)

---

## Licencia y cita

* Conjunto de datos: por favor, añade aquí la licencia de datos que elijas (p. ej., **CC BY 4.0**).
* Generador: planeado como **LGPL**. Para acceso o personalizaciones: **[sales@softoft.de](mailto:sales@softoft.de)**.

**Cita sugerida:**

> Bueck, T. (2025). *Multilingual Customer Support Tickets (Synthetic)*. Kaggle Dataset.
> Generado con el Generador de Datos Sintéticos de Open Ticket AI.

---

## Historial de cambios (alto nivel)

* **v5:** Solo EN/DE; el conjunto más grande; taxonomía y balanceo mejorados.
* **v4:** EN/DE; grande; conjunto de prompts anterior.
* **v3:** Más pequeño; incluye idiomas adicionales (FR/ES/PT), pipeline anterior.