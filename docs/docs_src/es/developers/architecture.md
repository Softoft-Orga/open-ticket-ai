---
description: Aprenda sobre la arquitectura de Open Ticket AI. Descubra cómo su canal de datos modular y los modelos de Hugging Face potencian la clasificación y el enrutamiento inteligente de tickets.
layout: page
pageClass: full-page
title: Resumen de la Arquitectura de Open Ticket AI
---
# Resumen de la Arquitectura

Open Ticket AI se basa en un motor de ejecución modular que procesa los tickets de soporte mediante pipelines configurables. Cada pipeline combina «pipes» reutilizables que recuperan datos, ejecutan modelos de Hugging Face y envían los resultados de vuelta a los sistemas externos.

## Visión general del sistema

- **Núcleo autoalojado**: Se ejecuta como un servicio de Python que carga la configuración, registra los servicios y supervisa la ejecución del pipeline.
- **Servicios inyectados**: Los adaptadores, modelos y utilidades se proporcionan a través de un contenedor de inversión de control para que cada pipe solicite solo lo que necesita.
- **Pipelines componibles**: La configuración YAML describe qué pipes se ejecutan, en qué orden y con qué cláusulas condicionales `when`.
- **Contexto de ejecución compartido**: Los resultados intermedios se guardan en un objeto de contexto, de modo que los pasos posteriores pueden reutilizar salidas previas sin recalcularlas.

## Componentes principales

### Orquestador del pipeline
El orquestador carga la configuración del pipeline activo, renderiza cualquier plantilla de Jinja2 e instancia cada pipe justo a tiempo. Respeta las condiciones `when`, recorre los pasos y persiste el estado de cada pipe en el contexto compartido.

### Pipes
Los pipes encapsulan una unidad de trabajo —como recuperar tickets, clasificar texto, actualizar metadatos o registrar telemetría—. Son sin estado entre ejecuciones; cada ejecución recibe entradas nuevas del orquestador y escribe sus resultados en el contexto para los pasos posteriores.

### Servicios
Las capacidades reutilizables (clientes HTTP, pipelines de Hugging Face, backends de almacenamiento) viven en el contenedor de servicios. Los pipes solicitan servicios con `get_instance`, lo que centraliza la infraestructura y facilita su sustitución o ampliación.

### Adaptadores de sistemas de tickets
Los adaptadores traducen entre Open Ticket AI y las plataformas de helpdesk externas. Los pipes de obtención utilizan un adaptador para cargar tickets, mientras que los pipes de actualización usan el mismo adaptador para aplicar cambios de cola, prioridad o comentarios en el sistema remoto.

### Modelos de aprendizaje automático
Las predicciones de cola y prioridad se generan mediante modelos de Hugging Face que se ejecutan en pipes dedicados. Estos pipes alimentan entradas desde el contexto, ejecutan el modelo y enriquecen el contexto con predicciones estructuradas que consumen los pasos siguientes.

## Flujo de procesamiento de extremo a extremo

1. El orquestador inicializa los servicios y el contexto de ejecución y, después, selecciona el pipeline configurado.
2. Un pipe de obtención utiliza un adaptador de sistema de tickets para recuperar los tickets pertinentes y almacenarlos en el contexto.
3. Los pipes de preprocesamiento limpian y normalizan el texto del ticket para que lo consuman los modelos.
4. Los pipes de clasificación ejecutan modelos de Hugging Face para predecir asignaciones de cola, prioridades o etiquetas.
5. Los pipes de posprocesamiento consolidan las predicciones, aplican reglas de negocio y preparan las cargas útiles de actualización.
6. Los pipes de actualización vuelven a llamar al adaptador del sistema de tickets para escribir los resultados (cambios de cola, actualizaciones de prioridad, notas internas) en el ticket original.

## Ampliar la plataforma

- **Añadir un nuevo adaptador**: Implemente la interfaz de adaptador para otra plataforma de tickets y regístrela en el contenedor de servicios.
- **Personalizar los pipelines**: Combine nuevas secuencias de pipes en YAML y utilice cláusulas `when` para controlar los pasos opcionales.
- **Introducir nueva inteligencia**: Cree pipes de modelos adicionales o procesadores basados en reglas que lean y escriban en el contexto compartido.

Esta arquitectura desacopla la lógica de clasificación de las integraciones, lo que permite a los equipos adaptar el pipeline a sus flujos de trabajo sin modificar el runtime central.
