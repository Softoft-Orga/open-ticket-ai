---
description: 'Entdecken Sie die Suite von Open Ticket AI: ein On-Premises-Klassifikator, eine gehostete API,
  ein Generator für synthetische Daten und öffentliche Modelle zur Automatisierung Ihres Support-Ticket-Workflows.'
pageClass: full-page
---
# Produktübersicht

Auf dieser Seite sehen Sie, was heute verfügbar ist, was von uns gehostet wird und was als Nächstes geplant ist.
**Open Ticket AI** ist das Flaggschiff-Produkt für den On-Premises-Einsatz; **Models** und **APIs** sind optionale Add-ons.

## Auf einen Blick

<Table>
    <Row>
      <C header>Produkt</C>
      <C header>Beschreibung</C>
      <C header>Status</C>
      <C header>Links</C>
    </Row>
    <Row>
      <C><strong>Open Ticket AI (On-Premises/Hauptprodukt)</strong></C>
      <C>Lokaler, Open-Source-Ticket-Klassifikator (Queues & Priorität), integriert über Pipelines/Adapter.</C>
      <C>✅ Verfügbar</C>
      <C><Link to="/">Übersicht</Link></C>
    </Row>
    <Row>
      <C><strong>Gehostete Prediction API (Deutsch)</strong></C>
      <C>HTTP API zur Klassifizierung von Queue & Priorität unter Verwendung unseres öffentlichen deutschen Basis-Modells (von uns gehostet).</C>
      <C>✅ Derzeit kostenlos</C>
      <C><Link to="/products/prediction-api/overview">API-Doku</Link></C>
    </Row>
    <Row>
      <C><strong>Öffentliche Basis-Modelle (Deutsch)</strong></C>
      <C>Basis-Modelle für Queue/Priorität, veröffentlicht auf Hugging Face für Nutzer ohne eigene Daten.</C>
      <C>✅ Verfügbar</C>
      <C>Siehe Links in der <Link to="/products/prediction-api/overview">API-Doku</Link></C>
    </Row>
    <Row>
      <C><strong>Generator für synthetische Daten</strong></C>
      <C>Python-Tool zur Erstellung mehrsprachiger synthetischer Ticket-Datensätze; LGPL geplant.</C>
      <C>✅ Verfügbar</C>
      <C><Link to="/products/synthetic-data/synthetic-data-generation">Generator</Link></C>
    </Row>
    <Row>
      <C><strong>Ticket-Datensätze (v5, v4, v3)</strong></C>
      <C>Synthetische Datensätze, erstellt mit unserem Generator (Fokus auf EN/DE in v5/v4; mehr Sprachen in v3).</C>
      <C>✅ Verfügbar</C>
      <C><Link to="/products/synthetic-data/ticket-dataset">Datensatz</Link></C>
    </Row>
    <Row>
      <C><strong>Englisches Prediction Model</strong></C>
      <C>Basis-Modell für EN Queue/Priorität.</C>
      <C>🚧 Bald verfügbar</C>
      <C>(wird hier hinzugefügt)</C>
    </Row>
    <Row>
      <C><strong>Zusätzliche Sprachen & Attribute</strong></C>
      <C>Modelle für andere Sprachen; Vorhersagen für Tags, Bearbeiter; optionale Erstantwort.</C>
      <C>🧭 In Planung</C>
      <C>(Roadmap)</C>
    </Row>
    <Row>
      <C><strong>Web-UI für den Datengenerator</strong></C>
      <C>Browser-UI auf Basis des Generators für nicht-technische Benutzer.</C>
      <C>🧭 In Planung</C>
      <C>(Roadmap)</C>
    </Row>
</Table>

> **Hinweis zur Preisgestaltung:** Die gehostete **German Prediction API** ist derzeit kostenlos. Sollte die Nachfrage die Infrastrukturkosten zu stark erhöhen, werden wir möglicherweise Ratenbegrenzungen oder Preise einführen. Die On-Premises-Version von **Open Ticket AI** bleibt Open-Source und lokal.

---

## Open Ticket AI (On-Premises/Hauptprodukt)

- Läuft lokal; Integration mit Znuny/OTRS/OTOBO über Adapter.
- Klassifiziert **Queue** & **Priorität** bei eingehenden Tickets; erweiterbare Pipeline-Architektur.
- Lässt sich gut mit unserem **Generator für synthetische Daten** für den Kaltstart oder das Class-Balancing kombinieren.

**Mehr erfahren:**
[Übersicht](../index.md)

---

## Gehostete Prediction API & öffentliche Basis-Modelle (Deutsch)

- Für Teams **ohne eigene Daten**, bei denen die **Basis-Queues/Prioritäten** gut passen.
- Nutzen Sie das **deutsche** Model über unsere gehostete API (**derzeit kostenlos**).
- Die Modelle sind **öffentlich auf Hugging Face** verfügbar; Sie können sie auch selbst hosten oder feintunen.

**Hier starten:** [Prediction API](./prediction-api/overview.md)

---

## Generator für synthetische Daten

- Python-Tool zur Erstellung realistischer, gelabelter Ticket-Datensätze (Betreff, Text, Queue, Priorität, Typ, Tags, Sprache, Erstantwort).
- Geplante **LGPL**-Veröffentlichung; für Zugriff oder Anpassungen senden Sie eine E-Mail an: **sales@softoft.de**.

**Details:** [Generierung synthetischer Daten](./synthetic-data/synthetic-data-generation.md)

---

## Ticket-Datensätze

- Mehrere Versionen verfügbar:
    - **v5 / v4:** EN & DE, die größten und vielfältigsten.
    - **v3:** mehr Sprachen (z.B. FR/ES/PT), kleiner.
- Ideal für Bootstrapping, Benchmarking und mehrsprachige Experimente.

**Durchsuchen:** [Mehrsprachige Kundensupport-Tickets](./synthetic-data/ticket-dataset.md)

---

## Roadmap

- **Englisches** Basis-Modell für Queue/Priorität (gehostet & zum Download).
- Optionale Modelle für **andere Sprachen**.
- Zusätzliche Attribute: **Tags**, **Bearbeiter** und Generierung von **Erstantworten**.
- Früher Prototyp einer **Web-Oberfläche** für den Datengenerator.

---

## FAQ

**Ist die API Teil von Open Ticket AI?**
Nein. **Open Ticket AI** läuft lokal. Die **Prediction API** ist ein separater, gehosteter Dienst, der unsere öffentlichen Modelle verwendet.

**Kann ich meine eigene Taxonomie verwenden?**
Ja. Trainieren Sie lokal mit Ihren Daten oder beauftragen Sie uns, synthetische Daten zu generieren, die Ihre Queues/Prioritäten widerspiegeln.

**Support & Dienstleistungen?**
Wir bieten Support-Abonnements und individuelle Integrationen an. Kontaktieren Sie **sales@softoft.de**.