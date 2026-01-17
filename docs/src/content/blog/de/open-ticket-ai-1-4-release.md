---
title: 'Open Ticket AI 1.4 Release: Produktionsbereite KI-Automatisierung für moderne Helpdesks'
description: 'Entdecken Sie Open Ticket AI 1.4 – die erste Produktionsveröffentlichung mit Enterprise-Plugins, flexiblen Pipelines, Jinja2-Konfiguration und nahtloser Docker-Bereitstellung für OTOBO, Znuny und Zammad.'
lang: en
date: 2025-10-30
tags:
  - product-release
  - version-1-4
  - plugin-architecture
  - docker-deployment
  - huggingface-integration
  - production-ready
category: Product Update
draft: false
image: ../../../assets/images/laptop-ai-ticketsystem.png
---

# Open Ticket AI 1.4: Die erste große Produktionsveröffentlichung

Open Ticket AI 1.4 ist da und markiert die **erste große produktionsbereite Veröffentlichung**! Diese Version bringt Enterprise-Grade-Funktionen, ein ausgereiftes Plugin‑Ökosystem und die Flexibilität, Ihre Ticket‑System‑Workflows wie nie zuvor zu automatisieren. Holen Sie sich die vollständige Veröffentlichung auf [GitHub](https://github.com/Softoft-Orga/open-ticket-ai/releases/tag/v1.4.1).

![Open Ticket AI Release Version 1.4](https://softoft.sirv.com/open-ticket-ai/Open-Ticket-AI-Release-Version-1.png)

## Demo ansehen!

Dieses Demo zeigt das OTOBO Ticketsystem mit OTAI‑Konfiguration, das Queue und Priority basierend auf dem Ticketinhalt klassifiziert. Sie können sich über den folgenden Link anmelden!

:::caution German Models!
Deutsche Modelle!
:::

[OTOBO Queue Priority Demo](https://otobo-demo.open-ticket-ai.com/otobo/customer.pl?Action=Login;User=otai;Password=otai)

Example!

Subject: "DRINGEND! Wohnung in Mainzer Straße 8 Heizung kaputt;"
Text: "Hallo,
meine Heizung in der Wohnung in der Mainzer Straße 8 funktioniert nicht. Bitte um schnelle Hilfe!
dringend!
Die Heizungsrohre sind kalt und es ist sehr kalt in der Wohnung. Vielen Dank!
Mit freundlichen Grüßen,
Max Mustermann
"

[Queue Priority - Test Ticket](https://otobo-demo.open-ticket-ai.com/otobo/customer.pl?Action=CustomerTicketMessage;Subject=DRINGEND!%20Wohnung%20in%20Mainzer%20Stra%C3%9Fe%208%20Heizung%20kaputt;Body=Hallo,%20meine%20Heizung%20in%20der%20Wohnung%20in%20der%20Mainzer%20Stra%C3%9Fe%208%20funktioniert%20nicht.%20Bitte%20um%20schnelle%20Hilfe!%20dringend!%20Die%20Heizungsrohre%20sind%20kalt%20und%20es%20ist%20sehr%20kalt%20in%20der%20Wohnung.%20Vielen%20Dank!%20Mit%20freundlichen%20Gr%C3%BC%C3%9Fen,%20Max%20Mustermann)

Dies sind nur Testmodelle. Sie können jedes gewünschte Modell mit Open Ticket AI verwenden! Es funktioniert mit Huggingface‑Modellen

interesting models:
OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract
oliverguhr/german-sentiment-bert
siebert/sentiment-roberta-large-english
distilbert/distilbert-base-uncased-finetuned-sst-2-english

Oft ist es besser, eigene Modelle mit eigenen Daten zu trainieren. Dann müssen Sie diese zu huggingface_hub veröffentlichen, das Modell und HF_TOKEN in der config.yml ändern und OTAI neu starten.

## Was Open Ticket AI 1.4 bietet

### Leistungsstarke Plugin-Architektur

Installieren Sie nur die Funktionen, die Sie benötigen, über ein **modulares Plugin‑System**. Plugins erweitern Open Ticket AI mit benutzerdefinierten Ticket‑System‑Integrationen, ML‑Modellen und Verarbeitungslogik – alles ohne den Kerncode zu berühren.

- **OTOBO/Znuny Plugin** (`otai-otobo-znuny`): Verbindet sich mit OTOBO-, Znuny- und OTRS‑Ticket‑Systemen
- **HuggingFace Local Plugin** (`otai-hf-local`): Führt ML‑Klassifizierungsmodelle auf Ihrer eigenen Infrastruktur aus

**Wie es funktioniert:** Plugins sind Standard‑Python‑Pakete, die über Entry Points entdeckt werden. Installieren Sie sie mit `uv add otai-otobo-znuny`, referenzieren Sie sie in Ihrer config und Sie sind bereit. Weitere Informationen finden Sie in der Dokumentation zum [Plugin System](../users/plugins.mdx).

### Flexibles Pipeline‑System

Erstellen Sie anspruchsvolle Automatisierungs‑Workflows mit **sequentieller Pipe‑Ausführung**:

- **Simple Pipes**: Tickets abrufen, Inhalt klassifizieren, Felder aktualisieren, Notizen hinzufügen
- **Expression Pipes**: Dynamische bedingte Logik mit Jinja2‑Templates
- **Composite Pipes**: Pipelines verschachteln für mehrstufige Orchestrierung

Jede Pipe erhält Kontext von vorherigen Schritten, führt ihre Aufgabe aus und leitet die Ergebnisse weiter. Lesen Sie die vollständige Anleitung im [Pipe System](../users/pipeline.mdx).

### Dynamische Konfiguration mit Template‑Rendering

Konfigurieren Sie alles mit **YAML + Jinja2** für maximale Flexibilität:

<div v-pre>

- Umgebungsvariablen referenzieren: `{{ get_env('API_KEY') }}`
- Pipe‑Ergebnisse abrufen: `{{ get_pipe_result('fetch', 'tickets') }}`
- Bedingte Parameter basierend auf dem Laufzeitzustand
- Typ‑sichere Konfigurations‑Schemas

</div>

Services werden einmal definiert und über Dependency Injection in mehreren Pipes wiederverwendet. Weitere Details finden Sie unter [Configuration & Template Rendering](../users/config_rendering.mdx).

### Einfache Installation

Der einfachste Weg, Open Ticket AI auf Ihrem Server einzurichten, ist die Verwendung von **Docker Compose**:

**1. Create `compose.yml`:**

```yaml
services:
  open-ticket-ai:
    image: openticketai/engine:latest
    restart: 'unless-stopped'
    environment:
      OTAI_TS_PASSWORD: '${OTAI_TS_PASSWORD}'
    volumes:
      - ./config.yml:/app/config.yml:ro
```

**2. Erstellen Sie Ihre `config.yml`** (siehe [Configuration Guide](../users/config_rendering.mdx))

**3. Starten Sie den Service:**

```bash
docker compose up -d
```

**4. Sie müssen außerdem das Ticketsystem einrichten**

#### Alternative: Installation mit pip/uv

Für lokale Entwicklung oder benutzerdefinierte Deployments:

:::code-group

```bash title="uv (Recommended)"
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Open Ticket AI with all plugins
uv pip install open-ticket-ai[all]

# Or install plugins individually
uv pip install open-ticket-ai
uv pip install otai-otobo-znuny otai-hf-local
```

```bash title="pip"
# Install Open Ticket AI with all plugins
pip install open-ticket-ai[all]

# Or install plugins individually
pip install open-ticket-ai
pip install otai-otobo-znuny otai-hf-local
```

:::

Siehe die vollständige [Installation Guide](../guides/installation.md) für Systemanforderungen und Deploy‑Optionen.

---

## Für Plugin‑Entwickler: Erstellen und Monetarisieren

Open Ticket AI 1.4 befähigt Entwickler, **kommerzielle Plugins zu erstellen und zu verkaufen** mit voller Lizenzfreiheit. Es gibt noch keinen Marktplatz, aber die Grundlage ist bereit.

### Freiheit bei der Plugin‑Entwicklung

- **Keine Lizenzbeschränkungen**: Wählen Sie Ihr eigenes Lizenzmodell
- **Kommerzielle Plugins verkaufen**: Monetarisieren Sie Ihre Erweiterungen, wie Sie möchten
- **Vollständige Dokumentation**: Komplettleitfaden unter [Plugin Development](../developers/plugin_development.mdx)
- **Community‑Sichtbarkeit**: Ihr Plugin kann auf unserer [Plugins](../users/plugins.mdx)-Seite gelistet werden

### Zukünftiger Marktplatz

Obwohl es heute keinen offiziellen Marktplatz gibt, bauen wir darauf hin:

- **Plugin‑Listings**: Bereits auf der Dokumentationsseite verfügbar
- **Discovery‑Seite**: Demnächst mit Suche, Kategorien und Bewertungen
- **Community‑Showcase**: Beliebte und trendige Plugins hervorheben

Beginnen Sie jetzt mit dem Aufbau, und Ihr Plugin wird bereit sein, wenn der Marktplatz startet!

---

## Technische Highlights

- **Python 3.14**: Moderne Typ‑Hints, Leistungsverbesserungen
- **Dependency Injection**: Saubere Architektur mit dem Injector‑Framework
- **Entry‑Point‑Erkennung**: Standard‑Python‑Packaging für das Laden von Plugins
- **API‑Kompatibilitäts‑Validierung**: Plugins und Kern‑Versionen werden zur Laufzeit geprüft
- **Umfassende Tests**: Vollständige Testabdeckung mit pytest

Open Ticket AI 1.4 ist produktionsbereit, erweiterbar und für die Zukunft gebaut. Installieren Sie es noch heute, automatisieren Sie Ihre Workflows und werden Sie Teil des wachsenden Plugin‑Ökosystems!