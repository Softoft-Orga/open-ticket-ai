---
description: Free German API to predict Queue and Priority for support tickets. Easy
  integration with OTOBO, Znuny, and Zammad. No authentication required.
---

# 🇩🇪 German Ticket Classification API (Free)

Predict **Queue** and **Priority** for **German-language** support tickets with a single HTTP call.
This API is **free** to use and ideal for integrations with **OTOBO**, **Znuny**, **Zammad**, or custom helpdesks.

> **Language Support:** Optimized for **German** texts (subject + body).
> English Model is in development, will be realeased soon.

## Try it out!

<OTAIPredictionDemo/>

## 📍 Endpoint

**Method:** `POST`
**URL:** `https://open-ticket-ai.com/api/german_prediction/v1/classify`
**Headers:** `Content-Type: application/json`

### Request body

```json
{
    "subject": "VPN Verbindungsproblem",
    "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
}
````

### Example response

```json
{
    "queue": "IT & Technology/Network Infrastructure",
    "queue_conf": 0.94,
    "priority": "high",
    "priority_conf": 0.88
}
```

> `queue_conf` and `priority_conf` are confidence scores (`0.0–1.0`).

---

## 🚀 Quick Start

### cURL

```bash
curl -X POST "https://open-ticket-ai.com/api/german_prediction/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{
        "subject": "VPN Verbindungsproblem",
        "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
      }'
```

### JavaScript (Node.js / Browser)

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

## 🎯 Queues

The API may return any of the following **queue labels**:
<AccordionItem title="Full Queue List" open>
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

## ⚡ Priorities

The API predicts one of the following **priority levels**:

| Priority  | Numeric |
|-----------|---------|
| very\_low | 0       |
| low       | 1       |
| medium    | 2       |
| high      | 3       |
| critical  | 4       |

---

## 🔌 Integration Ideas

* **OTOBO / Znuny**: Call the API on ticket creation to pre-fill Queue + Priority.
* **Custom Helpdesk**: Run it in your intake pipeline before routing/SLAs.
* **Automation**: Auto-escalate `critical` tickets or route security incidents.
* **Analytics**: Track queue distribution & priority trends over time.

---

## ✅ Best Practices

* Provide **concise, clear subjects** and **descriptive bodies** in **German**.
* Avoid very long inputs; keep under \~5,000 characters combined.
* Log and monitor results to fine-tune downstream rules.

---

## ❓ Troubleshooting

* **400 Bad Request**: `subject` or `body` missing.
* **5xx errors**: Upstream model temporarily unavailable — retry with backoff.
* Predictions look off? Ensure the text is **German** and contains enough context.

---

## 📄 Terms

* **Free** to use; please be mindful of request volume.
* We may introduce fair-use limits to keep the service healthy for everyone.
* No authentication required.

---
