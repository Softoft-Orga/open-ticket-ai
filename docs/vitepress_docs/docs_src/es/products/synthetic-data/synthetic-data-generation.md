---
description: Genere conjuntos de datos sintéticos multilingües de tickets de soporte al cliente con
  nuestra herramienta de Python. Incluye un pipeline de grafos, asistentes de IA, campos enriquecidos y seguimiento de costos.
---
# Generación de Datos Sintéticos para Tickets de Soporte

Cree conjuntos de datos de tickets de soporte multilingües y de alta calidad para clasificación, enrutamiento y automatización de respuestas.
Esta página describe nuestro **Generador de Datos Sintéticos** basado en Python y el conjunto de datos público que creamos con él. También
explica cómo el generador apoya el flujo de trabajo de entrenamiento de **Open Ticket AI** y nuestros servicios comerciales de generación de
datos.

::: info

- **Propósito:** Generar tickets realistas (asunto, cuerpo, cola, prioridad, tipo, etiquetas, idioma y una primera respuesta de un agente de IA).
- **Idiomas:** DE, EN, FR, ES, PT.
- **Pipeline:** Grafo de “nodos” de IA configurables (tema → correo electrónico → etiquetas → parafraseo → traducción → respuesta).
- **Modelos:** Funciona con OpenAI, OpenRouter, Together… (GPT-4, Qwen, LLaMA, etc.).
- **Controles:** CLI integrada, modos dev/prod, seguimiento de costos y tokens con resúmenes de divisas.
- **Licencia:** Lanzamiento planeado bajo **LGPL**.
- **¿Necesita la herramienta o modificaciones personalizadas?** → **sales@softoft.de**
:::

## Qué genera

- **Campos principales:** `ticket_id`, `subject`, `body`
- **Etiquetas de clasificación:** `type` (Incidente/Solicitud/Problema/Cambio), `queue` (p. ej., Soporte Técnico, Facturación, RRHH),
  `priority` (Baja/Media/Alta)
- **Idioma:** `language` (DE/EN/FR/ES/PT)
- **Etiquetas:** 4–8 etiquetas de dominio/tema por ticket
- **Respuesta del agente:** un mensaje de **primera respuesta** redactado por un asistente de IA

Un registro de ejemplo (CSV):

```csv
ticket_id,subject,body,language,type,queue,priority,tags,first_response
8934012332184,"VPN verbindet nicht","Seit dem Update keine Verbindung…","DE","Incident","IT / Security","High","vpn,update,remote-access,windows","Hallo! Bitte öffnen Sie die VPN-App…"
```

> Se garantiza que los ID son únicos en un rango de 12 a 13 dígitos, lo que simplifica las uniones (joins) y fusiones (merges) entre ejecuciones.

## Cómo funciona (en resumen)

El generador utiliza un **pipeline basado en grafos** de “nodos” pequeños y comprobables. Ruta típica:

```
Tema → Borrador de asunto → Borrador de cuerpo de correo → Etiquetado → Parafraseo → Traducción → Primera respuesta
```

Puede reordenar los nodos, eliminar pasos o añadir los suyos propios. Cada “asistente” es configurable (prompts de sistema/usuario,
modelo/proveedor, límites). Esto significa que puede producir rápidamente tickets específicos de un dominio (p. ej., RRHH, sanidad, retail,
sector público) sin reescribir código.

## Flexibilidad de modelos y proveedores

Utilice sus LLMs preferidos:

* **Proveedores:** OpenAI, OpenRouter, Together (y otros a través de adaptadores)
* **Modelos:** clase GPT-4, Qwen, LLaMA, etc.
* Intercambie los prompts por nodo para aumentar la diversidad y controlar el tono, la terminología y la estructura.

## Seguimiento de costos y uso (integrado)

* **Contabilidad de tokens y costos por ejecución** (entrada vs. salida) por modelo
* **Umbrales configurables** que advierten/fallan si una sola ejecución supera un límite de costo
* **Resúmenes de divisas** (p. ej., USD, EUR) para una presupuestación clara
* **Modos Dev vs. Prod** para cambiar entre pequeñas ejecuciones de prueba y compilaciones completas de conjuntos de datos

## Inicio rápido

Ejecute un trabajo de generación de conjuntos de datos con la CLI integrada:

```bash
python -m ticket_generator
```

Ideas de configuración mínima (pseudocódigo):

```python
# config/config.py (example)
RUN = {
    "rows": 10_000,  # total examples
    "batch_size": 50,  # lower for cheap dev runs
    "languages": ["DE", "EN", "FR", "ES", "PT"],
    "timezone": "Europe/Berlin",
    "pipeline": [
        "topic_node",
        "email_draft_node",
        "tagging_node",
        "paraphrase_node",
        "translate_node",
        "first_response_node"
    ],
    "models": {
        "default": {
            "provider": "openai",
            "name": "gpt-4o-mini",
            "max_tokens": 800
        }
    },
    "cost_limits": {
        "warn": 0.001,  # USD per single assistant run
        "error": 0.01
    }
}
```

> En la práctica, ajustará los prompts, elegirá diferentes modelos por nodo y agregará tablas de aleatorización específicas del dominio (
> colas, prioridades, tipos de negocio, etc.).

## Esquema de salida

Columnas comunes que verá en nuestras exportaciones generadas en CSV/Parquet:

* `ticket_id` (cadena de 12–13 dígitos)
* `subject`, `body`
* `language` (DE/EN/FR/ES/PT)
* `type` ∈ (Incidente, Solicitud, Problema, Cambio)
* `queue` (específico del dominio, p. ej., *Soporte Técnico*, *Facturación*, *RRHH*)
* `priority` ∈ (Baja, Media, Alta)
* `tags` (array/lista de 4–8)
* `first_response` (respuesta del agente)

## Conjunto de datos de ejemplo en Kaggle

Utilizamos este generador para construir el conjunto de datos público **Multilingual Customer Support Tickets**, que incluye **prioridades,
colas, tipos, etiquetas y tipos de negocio**, ideal para entrenar modelos de clasificación y priorización de tickets.
➡️ Kaggle: **Multilingual Customer Support Tickets**

* Incluye múltiples idiomas y todas las etiquetas mencionadas anteriormente
* Los notebooks de la comunidad demuestran casos de uso de clasificación y enrutamiento

## Cómo apoya esto a Open Ticket AI

**Open Ticket AI** clasifica la **cola** y la **prioridad** en los tickets entrantes. Los datos sintéticos son invaluables cuando se tiene:

* Un historial etiquetado **nulo o limitado**
* Datos **sensibles** que no pueden salir de su infraestructura
* La necesidad de clases **equilibradas** (p. ej., colas/prioridades poco comunes)
* Cobertura **multilingüe** desde el primer día

Usamos el generador de forma rutinaria para:

1. iniciar el entrenamiento del modelo,
2. equilibrar las clases de cola larga (long-tail), y
3. simular operaciones multilingües.
   Si desea que generemos conjuntos de datos a medida (su dominio/colas/prioridades/etiquetas, sus idiomas), lo ofrecemos como un **
   servicio**.

\::: tip Servicios
¿Necesita datos sintéticos específicos de su dominio para su servicio de asistencia? Diseñaremos prompts, nodos y tablas de aleatorización para su
industria, nos integraremos con su pipeline de datos y entregaremos archivos CSV/Parquet listos para el entrenamiento y la evaluación.
**Contacto:** [sales@softoft.de](mailto:sales@softoft.de)
\:::

## Licencia y disponibilidad

* Está previsto que el **Generador de Datos Sintéticos** se publique bajo la licencia **LGPL**.
* Si desea acceso anticipado, una licencia privada o modificaciones/extensibilidad personalizadas, **envíe un correo electrónico a `sales@softoft.de`** y
  lo configuraremos para usted.

---

### FAQ

**¿El conjunto de datos es “real” o “sintético”?**
Totalmente sintético, producido por un pipeline de LLM configurable.

**¿Puedo añadir mis propios campos (p. ej., *Unidad de Negocio*, *Impacto*, *Urgencia*)?**
Sí, amplíe las tablas de aleatorización y añada un nodo para emitir los campos.

**¿Puedo controlar el estilo y el tono?**
Por supuesto. Los prompts son por nodo, por lo que puede imponer el tono, la formalidad, los regionalismos y la terminología.

**¿Cómo mantengo los costos bajo control?**
Use el modo de desarrollo (pocas `rows`, `max_tokens` más bajos), umbrales de costo y modelos más económicos para las primeras iteraciones. Cambie a su combinación de modelos preferida una vez que los resultados parezcan correctos.