---
title: 'Open Ticket AI 1.4 Release: Production-Ready AI Automation for Modern Help Desks'
description: 'Entdecken Sie Open Ticket AI 1.4 – die erste Produktionsversion mit Enterprise-Plugins, flexiblen Pipelines, Jinja2-Konfiguration und nahtloser Docker-Bereitstellung für OTOBO, Znuny und Zammad.'
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

# Open Ticket AI 1.4: Die erste große Produktionsversion

Open Ticket AI 1.4 ist da und markiert die **erste große produktionsreife Version**! Diese Version bringt Enterprise-Features, ein ausgereiftes Plugin-Ökosystem und die Flexibilität, Ihre Ticket-System-Workflows wie nie zuvor zu automatisieren. Holen Sie sich die vollständige Version auf [GitHub](https://github.com/Softoft-Orga/open-ticket-ai/releases/tag/v1.4.1).

![Open Ticket AI Release Version 1.4](https://softoft.sirv.com/open-ticket-ai/Open-Ticket-AI-Release-Version-1.png)

## Schauen Sie sich die Demo an!

Diese Demo zeigt das OTOBO Ticketsystem mit OTAI, eingerichtet, um Queue und Priorität basierend auf dem Ticketinhalt zu klassifizieren. Sie können sich über den folgenden Link einloggen!

:::caution Deutsche Modelle!
Die Queue- und Priority-Modelle funktionieren nur für deutsche Tickets, da sie mit deutschen Daten trainiert wurden.
:::

[OTOBO Queue Priority Demo](https://otobo-demo.open-ticket-ai.com/otobo/customer.pl?Action=Login;User=otai;Password=otai)

Beispiel!

Betreff: "DRINGEND! Wohnung in Mainzer Straße 8 Heizung kaputt;"
Text: "Hallo,
meine Heizung in der Wohnung in der Mainzer Straße 8 funktioniert nicht. Bitte um schnelle Hilfe!
dringend!
Die Heizungsrohre sind kalt und es ist sehr kalt in der Wohnung. Vielen Dank!
Mit freundlichen Grüßen,
Max Mustermann
"

[Queue Priority - Test Ticket](https://otobo-demo.open-ticket-ai.com/otobo/customer.pl?Action=CustomerTicketMessage;Subject=DRINGEND!%20Wohnung%20in%20Mainzer%20Stra%C3%9Fe%208%20Heizung%20kaputt;Body=Hallo,%20meine%20Heizung%20in%20der%20Wohnung%20in%20der%20Mainzer%20Stra%C3%9Fe%208%20funktioniert%20nicht.%20Bitte%20um%20schnelle%20Hilfe!%20dringend!%20Die%20Heizungsrohre%20sind%20kalt%20und%20es%20ist%20sehr%20kalt%20in%20der%20Wohnung.%20Vielen%20Dank!%20Mit%20freundlichen%20Gr%C3%BC%C3%9Fen,%20Max%20Mustermann)

Dies sind nur Testmodelle. Sie können mit Open Ticket AI jedes beliebige Modell verwenden!
Es funktioniert mit Huggingface-Modellen.

Interessante Modelle:
OpenAlex/bert-base-multilingual-cased-finetuned-openalex-topic-classification-title-abstract
oliverguhr/german-sentiment-bert
siebert/sentiment-roberta-large-english
distilbert/distilbert-base-uncased-finetuned-sst-2-english

Oft ist es besser, eigene Modelle mit eigenen Daten zu trainieren.
Dann müssen Sie dieses auf huggingface_hub veröffentlichen, das Modell und HF_TOKEN in der config.yml ändern und OTAI neu starten.

## Was Open Ticket AI 1.4 bietet

### Leistungsstarke Plugin-Architektur

Installieren Sie nur die Funktionen, die Sie benötigen, über ein **modulares Plugin-System**. Plugins erweitern Open Ticket AI mit benutzerdefinierten Ticket-System-Integrationen, ML-Modellen und Verarbeitungslogik – alles ohne den Kerncode zu berühren.

- **OTOBO/Znuny Plugin** (`otai-otobo-znuny`): Verbindung zu OTOBO-, Znuny- und OTRS-Ticketsystemen
- **HuggingFace Local Plugin** (`otai-hf-local`): ML-Klassifikationsmodelle auf eigener Infrastruktur ausführen

**So funktioniert es:** Plugins sind Standard-Python-Pakete, die über Entry Points erkannt werden. Installieren Sie mit `uv add otai-otobo-znuny`, verweisen Sie in Ihrer Konfiguration darauf, und schon kann es losgehen. Erfahren Sie mehr in der [Plugin-System](../users/plugins.mdx)-Dokumentation.

### Flexibles Pipeline-System

Erstellen Sie anspruchsvolle Automatisierungs-Workflows mit **sequentieller Pipe-Ausführung**:

- **Simple Pipes**: Tickets abrufen, Inhalte klassifizieren, Felder aktualisieren, Notizen hinzufügen
- **Expression Pipes**: Dynamische bedingte Logik mit Jinja2-Templates
- **Composite Pipes**: Pipelines für mehrstufige Orchestrierung verschachteln

Jede Pipe erhält Kontext von vorherigen Schritten, führt ihre Aufgabe aus und gibt Ergebnisse weiter. Lesen Sie den vollständigen Leitfaden im [Pipe System](../users/pipeline.mdx).

### Dynamische Konfiguration mit Template-Rendering

Konfigurieren Sie alles mit **YAML + Jinja2** für maximale Flexibilität:

<div v-pre>

- Auf Umgebungsvariablen verweisen: `{{ get_env('API_KEY') }}`
- Auf Pipe-Ergebnisse zugreifen: `{{ get_pipe_result('fetch', 'tickets') }}`
- Bedingte Parameter basierend auf Laufzeitstatus
- Typsichere Konfigurations-Schemata

</div>

Services werden einmal definiert und über Dependency Injection in mehreren Pipes wiederverwendet.
Erkunden Sie [Configuration & Template Rendering](../users/config_rendering.mdx) für Details.

### Einfache Installation

Der einfachste Weg, Open Ticket AI auf Ihrem Server einzurichten, ist die Verwendung von **Docker Compose**:

**1. Erstellen Sie `compose.yml`:**

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

**4. Sie müssen auch das Ticketsystem einrichten**

#### Alternative: Installation mit pip/uv

Für lokale Entwicklung oder benutzerdefinierte Bereitstellungen:

:::code-group

```bash title="uv (Empfohlen)"
# Installieren Sie den uv Paketmanager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installieren Sie Open Ticket AI mit allen Plugins
uv pip install open-ticket-ai[all]

# Oder installieren Sie Plugins einzeln
uv pip install open-ticket-ai
uv pip install otai-otobo-znuny otai-hf-local
```

```bash title="pip"
# Installieren Sie Open Ticket AI mit allen Plugins
pip install open-ticket-ai[all]

# Oder installieren Sie Plugins einzeln
pip install open-ticket-ai
pip install otai-otobo-znuny otai-hf-local
```

:::

Siehe den vollständigen [Installation Guide](../guides/installation.md) für Systemanforderungen und Bereitstellungsoptionen.

---

## Für Plugin-Entwickler: Bauen und Monetarisieren

Open Ticket AI 1.4 befähigt Entwickler, **kommerzielle Plugins zu erstellen und zu verkaufen** mit vollständiger Lizenzfreiheit. Es gibt noch keinen Marketplace, aber das Fundament ist bereit.

### Plugin-Entwicklungsfreiheit

- **Keine Lizenzbeschränkungen**: Wählen Sie Ihr eigenes Lizenzmodell
- **Verkaufen Sie kommerzielle Plugins**: Monetarisieren Sie Ihre Erweiterungen, wie Sie möchten
- **Vollständige Dokumentation**: Kompletter Leitfaden unter [Plugin Development](../developers/plugin_development.mdx)
- **Community-Sichtbarkeit**: Ihr Plugin kann auf unserer [Plugins](../users/plugins.mdx)-Seite gelistet werden

### Zukünftiger Marketplace

Während es heute noch keinen offiziellen Marketplace gibt, arbeiten wir auf einen hin:

- **Plugin-Listings**: Bereits auf der Dokumentationsseite verfügbar
- **Entdeckungsseite**: Kommt bald mit Suche, Kategorien und Bewertungen
- **Community-Showcase**: Beliebte und trendige Plugins hervorheben

Fangen Sie jetzt an zu entwickeln, und Ihr Plugin ist bereit, wenn der Marketplace startet!

---

## Technische Highlights

- **Python 3.14**: Moderne Type Hints, Leistungsverbesserungen
- **Dependency Injection**: Saubere Architektur mit Injector-Framework
- **Entry Point Discovery**: Standard-Python-Packaging für Plugin-Loading
- **API-Kompatibilitätsvalidierung**: Plugin- und Core-Versionen werden zur Laufzeit geprüft
- **Umfassendes Testing**: Vollständige Testabdeckung mit pytest

---

Open Ticket AI 1.4 ist produktionsreif, erweiterbar und für die Zukunft gebaut. Installieren Sie es noch heute, automatisieren Sie Ihre Workflows und werden Sie Teil des wachsenden Plugin-Ökosystems!