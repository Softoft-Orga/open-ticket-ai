---
description: API allemande gratuite pour prédire la file d'attente et la priorité des tickets de support. Intégration facile avec OTOBO, Znuny et Zammad. Aucune authentification requise.
---
# 🇩🇪 API de Classification de Tickets Allemands (Gratuite)

Prédisez la **File d'attente** et la **Priorité** pour les tickets de support en **langue allemande** avec un seul appel HTTP.
Cette API est **gratuite** et idéale pour les intégrations avec **OTOBO**, **Znuny**, **Zammad**, ou des services d'assistance personnalisés.

> **Support linguistique :** Optimisé pour les textes en **allemand** (sujet + corps).
> Un modèle anglais est en cours de développement et sera bientôt disponible.

## Essayez-la !

<OTAIPredictionDemo/>

## 📍 Point d'accès (Endpoint)

**Méthode :** `POST`
**URL :** `https://open-ticket-ai.com/api/german_prediction/v1/classify`
**En-têtes :** `Content-Type: application/json`

### Corps de la requête

```json
{
    "subject": "VPN Verbindungsproblem",
    "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
}
````

### Exemple de réponse

```json
{
    "queue": "IT & Technology/Network Infrastructure",
    "queue_conf": 0.94,
    "priority": "high",
    "priority_conf": 0.88
}
```

> `queue_conf` et `priority_conf` sont des scores de confiance (`0.0–1.0`).

---

## 🚀 Démarrage rapide

### cURL

```bash
curl -X POST "https://open-ticket-ai.com/api/german_prediction/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{
        "subject": "VPN Verbindungsproblem",
        "body": "Kann nach dem Update keine Verbindung zum Unternehmens-VPN herstellen. Vor dem letzten Update funktionierte es einwandfrei."
      }'
```

### JavaScript (Node.js / Navigateur)

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

## 🎯 Files d'attente

L'API peut retourner l'une des **étiquettes de file d'attente** suivantes :
    <AccordionItem title="Liste complète des files d'attente" open>
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

## ⚡ Priorités

L'API prédit l'un des **niveaux de priorité** suivants :

| Priorité  | Numérique |
|-----------|-----------|
| very\_low | 0         |
| low       | 1         |
| medium    | 2         |
| high      | 3         |
| critical  | 4         |

---

## 🔌 Idées d'intégration

* **OTOBO / Znuny** : Appelez l'API lors de la création d'un ticket pour pré-remplir la file d'attente et la priorité.
* **Service d'assistance personnalisé** : Exécutez-le dans votre pipeline de réception avant le routage/les SLA.
* **Automatisation** : Escaladez automatiquement les tickets `critical` ou routez les incidents de sécurité.
* **Analytique** : Suivez la distribution des files d'attente et les tendances de priorité dans le temps.

---

## ✅ Bonnes pratiques

* Fournissez des **sujets concis et clairs** et des **corps descriptifs** en **allemand**.
* Évitez les entrées très longues ; restez en dessous de ~5 000 caractères combinés.
* Enregistrez et surveillez les résultats pour affiner les règles en aval.

---

## ❓ Dépannage

* **400 Bad Request** : `subject` ou `body` manquant.
* **Erreurs 5xx** : Le `model` en amont est temporairement indisponible — réessayez avec un backoff.
* Les prédictions semblent incorrectes ? Assurez-vous que le texte est en **allemand** et contient suffisamment de contexte.

---

## 📄 Conditions

* Utilisation **gratuite** ; veuillez faire attention au volume de requêtes.
* Nous pourrions introduire des limites d'utilisation équitable pour maintenir le service fonctionnel pour tout le monde.
* Aucune authentification requise.

---