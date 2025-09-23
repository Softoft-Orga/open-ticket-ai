---
description: API gratuita en alemán para predecir Cola y Prioridad para tickets de soporte. Fácil
  integración con OTOBO, Znuny y Zammad. No requiere autenticación.
---
# 🇩🇪 API de Clasificación de Tickets en Alemán (Gratuita)

Predice la **Cola** y la **Prioridad** para tickets de soporte en **idioma alemán** con una única llamada HTTP.
Esta API es de uso **gratuito** e ideal para integraciones con **OTOBO**, **Znuny**, **Zammad** o sistemas de helpdesk personalizados.

> **Soporte de Idiomas:** Optimizado para textos en **alemán** (asunto + cuerpo).
> El modelo en inglés está en desarrollo y se lanzará pronto.

## ¡Pruébalo!

<OTAIPredictionDemo/>

## 📍 Endpoint

**Método:** `POST`
**URL:** `https://open-ticket-ai.com/api/german_prediction/v1/classify`
**Cabeceras:** `Content-Type: application/json`

### Cuerpo de la solicitud

```json
{
    "subject": "VPN Verbindungsproblem",
    "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
}
````

### Ejemplo de respuesta

```json
{
    "queue": "IT & Technology/Network Infrastructure",
    "queue_conf": 0.94,
    "priority": "high",
    "priority_conf": 0.88
}
```

> `queue_conf` y `priority_conf` son puntuaciones de confianza (`0.0–1.0`).

---

## 🚀 Inicio Rápido

### cURL

```bash
curl -X POST "https://open-ticket-ai.com/api/german_prediction/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{
        "subject": "VPN Verbindungsproblem",
        "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
      }'
```

### JavaScript (Node.js / Navegador)

```js
const res = await fetch("https://open-ticket-ai.com/api/german_prediction/v1/classify", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
        subject: "VPN Verbindungsproblem",
        body: "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
    })
});
const data = await res.json();
console.log(data);
```

### Python

```python
import requests

payload = {
    "subject": "VPN Verbindungsproblem",
    "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
}

r = requests.post(
    "https://open-ticket-ai.com/api/german_prediction/v1/classify",
    json=payload,
    timeout=30
)

print(r.json())
```

---

## 🎯 Colas

La API puede devolver cualquiera de las siguientes **etiquetas de cola**:
    <AccordionItem title="Lista Completa de Colas" open>
        <ul>
            <li>Arts &amp; Entertainment/Movies</li>
            <li>Arts &amp; Entertainment/Music</li>
            <li>Autos &amp; Vehicles/Maintenance</li>
            <li>Autos &amp; Vehicles/Sales</li>
            <li>Beauty &amp; Fitness/Cosmetics</li>
            <li>Beauty &amp; Fitness/Fitness Training</li>
            <li>Books &amp; Literature/Fiction</li>
            <li>Books &amp; Literature/Non-Fiction</li>
            <li>Business &amp; Industrial/Manufacturing</li>
            <li>Finance/Investments</li>
            <li>Finance/Personal Finance</li>
            <li>Food &amp; Drink/Groceries</li>
            <li>Food &amp; Drink/Restaurants</li>
            <li>Games</li>
            <li>Health/Medical Services</li>
            <li>Health/Mental Health</li>
            <li>Hobbies &amp; Leisure/Collectibles</li>
            <li>Hobbies &amp; Leisure/Crafts</li>
            <li>Home &amp; Garden/Home Improvement</li>
            <li>Home &amp; Garden/Landscaping</li>
            <li>IT &amp; Technology/Hardware Support</li>
            <li>IT &amp; Technology/Network Infrastructure</li>
            <li>IT &amp; Technology/Security Operations</li>
            <li>IT &amp; Technology/Software Development</li>
            <li>Jobs &amp; Education/Online Courses</li>
            <li>Jobs &amp; Education/Recruitment</li>
            <li>Law &amp; Government/Government Services</li>
            <li>Law &amp; Government/Legal Advice</li>
            <li>News</li>
            <li>Online Communities/Forums</li>
            <li>Online Communities/Social Networks</li>
            <li>People &amp; Society/Culture &amp; Society</li>
            <li>Pets &amp; Animals/Pet Services</li>
            <li>Pets &amp; Animals/Veterinary Care</li>
            <li>Real Estate</li>
            <li>Science/Environmental Science</li>
            <li>Science/Research</li>
            <li>Shopping/E-commerce</li>
            <li>Shopping/Retail Stores</li>
            <li>Sports</li>
            <li>Travel &amp; Transportation/Air Travel</li>
            <li>Travel &amp; Transportation/Land Travel</li>
        </ul>
    </AccordionItem>

---

## ⚡ Prioridades

La API predice uno de los siguientes **niveles de prioridad**:

| Prioridad | Numérico |
|-----------|----------|
| very\_low | 0        |
| low       | 1        |
| medium    | 2        |
| high      | 3        |
| critical  | 4        |

---

## 🔌 Ideas de Integración

* **OTOBO / Znuny**: Llama a la API al crear un ticket para pre-rellenar la Cola y la Prioridad.
* **Helpdesk Personalizado**: Ejecútalo en tu pipeline de entrada antes del enrutamiento/SLAs.
* **Automatización**: Escala automáticamente los tickets `critical` o enruta los incidentes de seguridad.
* **Analíticas**: Realiza un seguimiento de la distribución de colas y las tendencias de prioridad a lo largo del tiempo.

---

## ✅ Mejores Prácticas

* Proporciona **asuntos concisos y claros** y **cuerpos descriptivos** en **alemán**.
* Evita entradas muy largas; mantenlas por debajo de ~5,000 caracteres combinados.
* Registra y monitorea los resultados para ajustar las reglas posteriores.

---

## ❓ Solución de Problemas

* **400 Bad Request**: Falta `subject` o `body`.
* **Errores 5xx**: El modelo upstream no está disponible temporalmente — reintenta con un backoff exponencial.
* ¿Las predicciones parecen incorrectas? Asegúrate de que el texto esté en **alemán** y contenga suficiente contexto.

---

## 📄 Términos

* Uso **gratuito**; por favor, ten en cuenta el volumen de solicitudes.
* Podríamos introducir límites de uso justo para mantener el servicio saludable para todos.
* No se requiere autenticación.

---