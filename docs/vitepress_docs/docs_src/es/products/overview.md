---
description: 'Descubre la suite de Open Ticket AI: un clasificador on-prem, una API
  alojada, un generador de datos sintéticos y modelos públicos para automatizar tu
  flujo de trabajo de tickets de soporte.'
pageClass: full-page
---
# Resumen de Productos

Usa esta página para ver qué está disponible hoy, qué está alojado por nosotros y qué vendrá después.
**Open Ticket AI** es el producto principal on-prem; los **models** y las **APIs** son complementos opcionales.

## De un vistazo

<Table>
    <Row>
      <C header>Producto</C>
      <C header>Qué es</C>
      <C header>Estado</C>
      <C header>Enlaces</C>
    </Row>
    <Row>
      <C><strong>Open Ticket AI (On-Prem/Producto Principal)</strong></C>
      <C>Clasificador de tickets local y de código abierto (colas y prioridad) integrado mediante pipelines/adaptadores.</C>
      <C>✅ Disponible</C>
      <C><Link to="/">Resumen</Link></C>
    </Row>
    <Row>
      <C><strong>API de Predicción Alojada (Alemán)</strong></C>
      <C>API HTTP para clasificar colas y prioridad usando nuestro modelo base público en alemán (alojado por nosotros).</C>
      <C>✅ Gratis por ahora</C>
      <C><Link to="/products/prediction-api/overview">Docs de la API</Link></C>
    </Row>
    <Row>
      <C><strong>Modelos Base Públicos (Alemán)</strong></C>
      <C>Modelos base para cola/prioridad publicados en Hugging Face para usuarios sin datos propios.</C>
      <C>✅ Disponible</C>
      <C>Ver enlaces en los <Link to="/products/prediction-api/overview">Docs de la API</Link></C>
    </Row>
    <Row>
      <C><strong>Generador de Datos Sintéticos</strong></C>
      <C>Herramienta de Python para crear conjuntos de datos de tickets sintéticos multilingües; planeado como LGPL.</C>
      <C>✅ Disponible</C>
      <C><Link to="/products/synthetic-data/synthetic-data-generation">Generador</Link></C>
    </Row>
    <Row>
      <C><strong>Conjuntos de Datos de Tickets (v5, v4, v3)</strong></C>
      <C>Conjuntos de datos sintéticos creados con nuestro generador (foco en EN/DE en v5/v4; más idiomas en v3).</C>
      <C>✅ Disponible</C>
      <C><Link to="/products/synthetic-data/ticket-dataset">Dataset</Link></C>
    </Row>
    <Row>
      <C><strong>Modelo de Predicción en Inglés</strong></C>
      <C>Modelo base para cola/prioridad en EN.</C>
      <C>🚧 Próximamente</C>
      <C>(se añadirá aquí)</C>
    </Row>
    <Row>
      <C><strong>Idiomas y Atributos Adicionales</strong></C>
      <C>Modelos para otros idiomas; predicciones para etiquetas, asignado; respuesta inicial opcional.</C>
      <C>🧭 Explorando</C>
      <C>(roadmap)</C>
    </Row>
    <Row>
      <C><strong>UI Web para el Generador de Datos</strong></C>
      <C>UI de navegador sobre el generador para usuarios no técnicos.</C>
      <C>🧭 Explorando</C>
      <C>(roadmap)</C>
    </Row>
</Table>

> **Nota sobre precios:** La **API de Predicción en Alemán** alojada es actualmente gratuita. Si la demanda eleva demasiado los costos de infraestructura, podríamos introducir límites de tasa o precios. **Open Ticket AI** on-prem sigue siendo de código abierto y local.

---

## Open Ticket AI (On-Prem/Producto Principal)

- Funciona localmente; se integra con Znuny/OTRS/OTOBO mediante adaptadores.
- Clasifica **Cola** y **Prioridad** en tickets entrantes; arquitectura de pipeline extensible.
- Combina bien con nuestro **Generador de Datos Sintéticos** para un arranque en frío o para el balanceo de clases.

**Más información:**
[Resumen](../index.md)

---

## API de Predicción Alojada y Modelos Base Públicos (Alemán)

- Para equipos **sin datos propios** donde las **colas/prioridades base** se ajustan razonablemente bien.
- Usa el modelo en **Alemán** a través de nuestra API alojada (**gratis por ahora**).
- Los modelos son **públicos en Hugging Face**; también puedes auto-alojarlos o afinarlos.

**Empieza aquí:** [API de Predicción](./prediction-api/overview.md)

---

## Generador de Datos Sintéticos

- Herramienta de Python para crear conjuntos de datos de tickets realistas y etiquetados (asunto, cuerpo, cola, prioridad, tipo, etiquetas, idioma, primera respuesta).
- Lanzamiento planeado bajo **LGPL**; envía un correo para acceso o modificaciones a: **sales@softoft.de**.

**Detalles:** [Generación de Datos Sintéticos](./synthetic-data/synthetic-data-generation.md)

---

## Conjuntos de Datos de Tickets

- Múltiples versiones disponibles:
    - **v5 / v4:** EN y DE, las más grandes y diversas.
    - **v3:** más idiomas (p. ej., FR/ES/PT), más pequeñas.
- Ideal para bootstrapping, benchmarking y experimentos multilingües.

**Explorar:** [Tickets de Soporte al Cliente Multilingües](./synthetic-data/ticket-dataset.md)

---

## Roadmap

- Modelo base en **Inglés** para cola/prioridad (alojado y descargable).
- Modelos opcionales para **otros idiomas**.
- Atributos adicionales: generación de **etiquetas**, **asignado** y **primera respuesta**.
- Prototipo temprano de una **interfaz web** para el generador de datos.

---

## FAQ

**¿La API es parte de Open Ticket AI?**
No. **Open Ticket AI** se ejecuta localmente. La **API de Predicción** es un servicio alojado separado que utiliza nuestros modelos públicos.

**¿Puedo usar mi propia taxonomía?**
Sí. Entrena localmente con tus datos, o pídenos que generemos datos sintéticos que reflejen tus colas/prioridades.

**¿Soporte y Servicios?**
Ofrecemos suscripciones de soporte e integraciones personalizadas. Contacta con **sales@softoft.de**.