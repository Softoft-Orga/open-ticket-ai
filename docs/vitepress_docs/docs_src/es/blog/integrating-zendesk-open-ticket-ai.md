---
description: Integra Zendesk con Open Ticket AI para la clasificación automatizada de tickets. Construye un adaptador de Python personalizado para clasificar automáticamente los tickets por prioridad a través de la API REST.
---
# Integración de Zendesk con Open Ticket AI para la Clasificación Automatizada de Tickets

En los flujos de trabajo de soporte modernos, la IA puede ayudar a los agentes de **Zendesk** clasificando automáticamente los tickets. [Open Ticket AI](https://ticket-classification.softoft.de) (OTAI) es una herramienta on-premises que analiza los tickets entrantes y predice su prioridad, cola/categoría, etiquetas y más a través de una API REST. Al conectar OTAI a Zendesk, los equipos de soporte pueden asignar prioridades o etiquetas automáticamente basándose en la IA, mejorando el tiempo de respuesta y la consistencia. Este artículo muestra a los desarrolladores cómo construir un **ZendeskAdapter** personalizado para OTAI extendiendo la clase existente `TicketSystemAdapter` y llamando a la API REST de Zendesk.

## Arquitectura de OTAI y TicketSystemAdapter

Open Ticket AI utiliza una arquitectura de **pipeline modular**. Cada ticket entrante es preprocesado, pasa a través de clasificadores de cola y prioridad, y finalmente se envía de vuelta al sistema de tickets a través de un adaptador. El componente clave aquí es el **TicketSystemAdapter** (una clase base abstracta) que define cómo actualizar o consultar tickets en un sistema externo. Los adaptadores incorporados (por ejemplo, para OTOBO) heredan de esta clase base. Para Zendesk, crearemos una nueva subclase.

&#x20;*Figura: Arquitectura de Open Ticket AI (extraída del diagrama de clases UML). Las etapas del pipeline (preprocesamiento, clasificación, etc.) culminan en un **TicketSystemAdapter**, que envía actualizaciones al sistema de tickets externo a través de REST. Extender OTAI con Zendesk implica crear una subclase de este adaptador para que los resultados de la IA (prioridad, etiquetas, etc.) se escriban en los tickets de Zendesk.*

En la práctica, OTAI se configura a través de YAML y se basa en la **inyección de dependencias**. Todos los componentes (fetchers, clasificadores, modificadores, etc.) se definen en `config.yml` y se ensamblan al inicio. La documentación señala que “Los fetchers, preparers, servicios de IA o modificadores personalizados pueden implementarse como clases de Python y registrarse a través de la configuración. Gracias a la inyección de dependencias, los nuevos componentes se pueden integrar fácilmente.”. En otras palabras, agregar un `ZendeskAdapter` es sencillo: lo implementamos como una clase de Python y lo declaramos en la configuración.

## Pasos para Añadir un Adaptador de Zendesk

Sigue estos pasos para integrar Zendesk en OTAI:

1. **Crear una subclase de `TicketSystemAdapter`**: Crea una nueva clase de adaptador (p. ej., `ZendeskAdapter`) que extienda la clase abstracta `TicketSystemAdapter`. Esta clase implementará cómo OTAI lee o escribe en Zendesk.
2. **Implementar `update_ticket`**: En `ZendeskAdapter`, sobrescribe el método `async def update_ticket(self, ticket_id: str, data: dict)`. Este método debe enviar una solicitud HTTP a Zendesk para actualizar los campos del ticket dado (p. ej., prioridad, etiquetas). Por ejemplo, harás un `PUT` a `https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json` con un payload JSON que contenga los campos a actualizar.
3. **(Opcional) Implementar métodos de búsqueda**: También puedes sobrescribir `find_tickets(self, query: dict)` o `find_first_ticket(self, query: dict)` si necesitas obtener tickets de Zendesk (p. ej., para obtener nuevos tickets). Estos métodos deben llamar a los endpoints GET de Zendesk (como `/api/v2/tickets.json` o la API de búsqueda) y devolver los datos de los tickets como diccionarios de Python.
4. **Configurar Credenciales**: Añade tus credenciales de Zendesk a la configuración de OTAI. Por ejemplo, guarda el **subdominio**, el **email de usuario** y el **token de API** en `config.yml` o en variables de entorno. El adaptador puede leer estos valores desde el `SystemConfig` inyectado (pasado en el constructor).
5. **Registrar el Adaptador**: Actualiza `config.yml` para que OTAI use `ZendeskAdapter` como su integración con el sistema de tickets. El framework de inyección de dependencias (DI) de OTAI instanciará tu clase con los parámetros de configuración.

Estos pasos aprovechan la extensibilidad de OTAI. El pipeline se define en la configuración (no se necesita REST para activar la clasificación), por lo que simplemente conectar tu adaptador hace que el pipeline use Zendesk como sistema de destino.

## Ejemplo: Implementación de `ZendeskAdapter`

A continuación se muestra un borrador de cómo podría ser el adaptador de Python. Se inicializa con valores de configuración e implementa `update_ticket` usando la librería `requests` de Python. El siguiente código es ilustrativo; necesitarás instalar `requests` (o usar `httpx`/`aiohttp` para operaciones asíncronas) y manejar los errores según sea necesario:

```python
import requests
from open_ticket_ai.src.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter


class ZendeskAdapter(TicketSystemAdapter):
    def __init__(self, params):
        super().__init__(params)
        # Read Zendesk settings from config (defined in config.yml)
        self.subdomain = params.zendesk_subdomain
        self.user_email = params.zendesk_user_email
        self.api_token = params.zendesk_api_token

    async def update_ticket(self, ticket_id: str, data: dict) -> dict | None:
        """
        Update a Zendesk ticket with the provided data (dict of fields).
        Uses Zendesk Tickets API to apply changes.
        """
        url = f"https://{self.subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json"
        # Zendesk expects a JSON object with "ticket": { ...fields... }
        payload = {"ticket": data}
        auth = (f"{self.user_email}/token", self.api_token)
        response = requests.put(url, json=payload, auth=auth)
        if response.status_code == 200:
            return response.json().get("ticket")
        else:
            # Log or handle errors (e.g., invalid ID or auth)
            return None

    async def find_tickets(self, query: dict) -> list[dict]:
        """
        (Optional) Search for tickets. Query could include filtering criteria.
        This example uses Zendesk's search endpoint.
        """
        query_str = query.get("query", "")  # e.g. "status<solved"
        url = f"https://{self.subdomain}.zendesk.com/api/v2/search.json?query={query_str}"
        auth = (f"{self.user_email}/token", self.api_token)
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
```

El constructor de este `ZendeskAdapter` extrae la configuración del `config` inyectado. El método `update_ticket` construye la URL usando el patrón estándar de Zendesk y envía una solicitud PUT. En este ejemplo, nos autenticamos con autenticación básica HTTP usando el email y el token de API de Zendesk (por convención, el nombre de usuario es `user_email/token`). El payload envuelve los datos del ticket bajo la clave `"ticket"` como espera la API de Zendesk. Tras una actualización exitosa, devuelve el JSON del ticket actualizado.

Definirías `params.zendesk_subdomain`, `params.zendesk_user_email` y `params.zendesk_api_token` en `config.yml`. Por ejemplo:

```yaml
ticket_system_integration:
    adapter: open_ticket_ai.src.ce.ticket_system_integration.zendesk_adapter.ZendeskAdapter
    zendesk_subdomain: "mycompany"
    zendesk_user_email: "agent@mycompany.com"
    zendesk_api_token: "ABCD1234TOKEN"
```

Esto le indica a OTAI que use `ZendeskAdapter`. La inyección de dependencias de OTAI construirá entonces tu adaptador con estos valores.

## Llamando a la API REST de Zendesk

La clave del adaptador es hacer solicitudes HTTP a los endpoints de la API de Zendesk. Como se mostró anteriormente, el adaptador de OTAI llama a URLs como `https://{subdomain}.zendesk.com/api/v2/tickets/{ticket_id}.json`. Según la documentación de Zendesk, actualizar un ticket requiere un PUT a esa URL con un cuerpo JSON (por ejemplo, `{"ticket": {"priority": "high", "tags": ["urgent"]}}` si quieres establecer la prioridad y las etiquetas). En el script de ejemplo anterior, `requests.put(url, json=payload, auth=auth)` se encarga de esto.

Para que sea más completo, también puedes implementar la creación de tickets (`requests.post(...)`) u otras llamadas a la API. Pero para la clasificación, normalmente solo se necesita **actualizar los tickets existentes** (para escribir los campos predichos por la IA). Asegúrate de que el token de la API de Zendesk tenga los permisos necesarios y de que hayas habilitado el “Acceso por token” en el panel de administración de Zendesk.

Si también quieres obtener tickets de Zendesk (por ejemplo, para encontrar tickets recién creados para procesar), usa las APIs de listado o búsqueda de Zendesk. Por ejemplo, podrías hacer un GET a `/api/v2/tickets.json` para paginar a través de los tickets, o usar `/api/v2/search.json?query=type:ticket status:new` para encontrar todos los tickets nuevos. Devuelve el JSON a OTAI como una lista de diccionarios de tickets desde `find_tickets()`.

## Pipeline y Uso

Con el `ZendeskAdapter` implementado, la ejecución de OTAI lo incorporará sin problemas en el pipeline. Por ejemplo, después de configurar tus modelos de IA (predictores de cola y prioridad), iniciar el planificador de OTAI (p. ej., `python -m open_ticket_ai.src.ce.main start`) activará el pipeline. OTAI usará tu adaptador como el paso final de “modificador”: después de que la IA infiera los atributos para cada ticket, llama a `ZendeskAdapter.update_ticket` para aplicar esos atributos de vuelta en Zendesk. Todo el proceso permanece transparente para OTAI: solo sabe que está llamando a `update_ticket` en una clase de adaptador.

Debido a que los componentes de OTAI se definen en YAML, puedes configurar con qué frecuencia obtiene o comprueba los tickets y cómo aplica las actualizaciones. La documentación para desarrolladores enfatiza que todos los componentes son conectables a través de la configuración y la inyección de dependencias (DI). Así que una vez que tu adaptador esté implementado y conectado en `config.yml`, no se necesitan más cambios en el código para incluir a Zendesk en el flujo de tickets.