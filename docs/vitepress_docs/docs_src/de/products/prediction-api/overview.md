---
description: Kostenlose deutsche API zur Vorhersage von Queue und Priorität für Support-Tickets.
  Einfache Integration mit OTOBO, Znuny und Zammad. Keine Authentifizierung erforderlich.
---
# 🇩🇪 Deutsche Ticket-Klassifizierungs-API (kostenlos)

Sagen Sie **Queue** und **Priorität** für **deutschsprachige** Support-Tickets mit einem einzigen HTTP-Aufruf voraus.
Diese API ist **kostenlos** und ideal für Integrationen mit **OTOBO**, **Znuny**, **Zammad** oder benutzerdefinierten Helpdesks.

> **Sprachunterstützung:** Optimiert für **deutsche** Texte (Betreff + Inhalt).
> Ein englisches Modell ist in Entwicklung und wird in Kürze veröffentlicht.

## Probieren Sie es aus!

<OTAIPredictionDemo/>

## 📍 Endpunkt

**Methode:** `POST`
**URL:** `https://open-ticket-ai.com/api/german_prediction/v1/classify`
**Header:** `Content-Type: application/json`

### Request-Body

```json
{
    "subject": "VPN Verbindungsproblem",
    "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
}
````

### Beispiel-Antwort

```json
{
    "queue": "IT & Technology/Network Infrastructure",
    "queue_conf": 0.94,
    "priority": "high",
    "priority_conf": 0.88
}
```

> `queue_conf` und `priority_conf` sind Konfidenzwerte (`0.0–1.0`).

---

## 🚀 Schnellstart

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

Die API kann eine der folgenden **Queue-Bezeichnungen** zurückgeben:
    <AccordionItem title="Vollständige Queue-Liste" open>
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

## ⚡ Prioritäten

Die API sagt eine der folgenden **Prioritätsstufen** voraus:

| Priorität | Numerisch |
|-----------|-----------|
| very\_low | 0         |
| low       | 1         |
| medium    | 2         |
| high      | 3         |
| critical  | 4         |

---

## 🔌 Integrationsideen

* **OTOBO / Znuny**: Rufen Sie die API bei der Ticketerstellung auf, um Queue + Priorität vorauszufüllen.
* **Benutzerdefinierter Helpdesk**: Führen Sie es in Ihrer Eingangs-Pipeline vor dem Routing/den SLAs aus.
* **Automatisierung**: Eskalieren Sie `critical`-Tickets automatisch oder leiten Sie Sicherheitsvorfälle weiter.
* **Analyse**: Verfolgen Sie die Verteilung der Queues und die Entwicklung der Prioritäten im Zeitverlauf.

---

## ✅ Bewährte Methoden

* Geben Sie **prägnante, klare Betreffzeilen** und **aussagekräftige Inhalte** auf **Deutsch** an.
* Vermeiden Sie sehr lange Eingaben; bleiben Sie unter ca. 5.000 Zeichen insgesamt.
* Protokollieren und überwachen Sie die Ergebnisse, um nachgelagerte Regeln zu optimieren.

---

## ❓ Fehlerbehebung

* **400 Bad Request**: `subject` oder `body` fehlen.
* **5xx-Fehler**: Das Upstream-Modell ist vorübergehend nicht verfügbar – versuchen Sie es mit Backoff erneut.
* Sehen die Vorhersagen falsch aus? Stellen Sie sicher, dass der Text auf **Deutsch** ist und genügend Kontext enthält.

---

## 📄 Nutzungsbedingungen

* **Kostenlose** Nutzung; bitte achten Sie auf das Anfragevolumen.
* Wir können Fair-Use-Limits einführen, um den Dienst für alle stabil zu halten.
* Keine Authentifizierung erforderlich.

---