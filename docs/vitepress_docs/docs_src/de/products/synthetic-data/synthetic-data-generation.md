---
description: Erstellen Sie mehrsprachige synthetische Datensätze für Kundensupport-Tickets mit unserem Python-Tool. Bietet eine Graph-Pipeline, KI-Assistenten, vielfältige Felder & Kostenverfolgung.
---
# Generierung synthetischer Daten für Support-Tickets

Erstellen Sie hochwertige, mehrsprachige Datensätze für Support-Tickets zur Klassifizierung, Weiterleitung und automatisierten Beantwortung.
Diese Seite beschreibt unseren Python-basierten **Synthetic Data Generator** und den öffentlichen Datensatz, den wir damit erstellt haben. Sie erklärt auch, wie der Generator den Trainings-Workflow von **Open Ticket AI** und unsere kommerziellen Dienstleistungen zur Datengenerierung unterstützt.

::: info

- **Zweck:** Generierung realistischer Tickets (Betreff, Inhalt, Warteschlange, Priorität, Typ, Tags, Sprache und eine erste Antwort eines KI-Agenten).
- **Sprachen:** DE, EN, FR, ES, PT.
- **Pipeline:** Graph aus konfigurierbaren KI-„Knoten“ (Thema → E-Mail → Tags → Paraphrasieren → Übersetzen → Antworten).
- **Modelle:** Funktioniert mit OpenAI, OpenRouter, Together… (GPT-4, Qwen, LLaMA, etc.).
- **Steuerung:** Integrierte CLI, Dev/Prod-Modi, Kosten- & Token-Tracking mit Währungsübersichten.
- **Lizenz:** Geplante **LGPL**-Veröffentlichung.
- **Benötigen Sie das Tool oder individuelle Anpassungen?** → **sales@softoft.de**
:::

## Was generiert wird

- **Kernfelder:** `ticket_id`, `subject`, `body`
- **Klassifizierungslabels:** `type` (Incident/Request/Problem/Change), `queue` (z. B. Technischer Support, Abrechnung, Personal), `priority` (Niedrig/Mittel/Hoch)
- **Sprache:** `language` (DE/EN/FR/ES/PT)
- **Tags:** 4–8 Domain-/Themen-Tags pro Ticket
- **Agenten-Antwort:** eine **Erstantwort**, verfasst von einem KI-Assistenten

Ein Beispieldatensatz (CSV):

```csv
ticket_id,subject,body,language,type,queue,priority,tags,first_response
8934012332184,"VPN verbindet nicht","Seit dem Update keine Verbindung…","DE","Incident","IT / Security","High","vpn,update,remote-access,windows","Hallo! Bitte öffnen Sie die VPN-App…"
```

> IDs sind garantiert eindeutig in einem 12–13-stelligen Bereich, was Joins und Merges über verschiedene Durchläufe hinweg vereinfacht.

## Funktionsweise (kurz erklärt)

Der Generator verwendet eine **graph-basierte Pipeline** aus kleinen, testbaren „Knoten“. Ein typischer Pfad ist:

```
Thema → Betreff entwerfen → E-Mail-Text entwerfen → Tagging → Paraphrasieren → Übersetzen → Erste Antwort
```

Sie können Knoten neu anordnen, Schritte entfernen oder eigene hinzufügen. Jeder „Assistent“ ist konfigurierbar (System-/Benutzer-Prompts, Modell/Anbieter, Limits). Das bedeutet, dass Sie schnell domänenspezifische Tickets (z. B. für Personalwesen, Gesundheitswesen, Einzelhandel, öffentlichen Sektor) erstellen können, ohne Code umschreiben zu müssen.

## Flexibilität bei Modellen & Anbietern

Nutzen Sie Ihre bevorzugten LLMs:

* **Anbieter:** OpenAI, OpenRouter, Together (und andere über Adapter)
* **Modelle:** GPT-4-Klasse, Qwen, LLaMA, etc.
* Tauschen Sie Prompts pro Knoten aus, um die Vielfalt zu erhöhen und Tonalität, Terminologie und Struktur zu steuern.

## Kosten- & Nutzungsverfolgung (integriert)

* **Token- und Kostenabrechnung pro Durchlauf** (Input vs. Output) für jedes Modell
* **Konfigurierbare Schwellenwerte**, die warnen/einen Fehler auslösen, wenn ein einzelner Durchlauf ein Kostenlimit überschreitet
* **Währungsübersichten** (z. B. USD, EUR) für eine klare Budgetierung
* **Dev- vs. Prod-Modi** zum Umschalten zwischen kleinen Testläufen und der Erstellung vollständiger Datensätze

## Schnellstart

Starten Sie einen Job zur Datensatzerstellung mit der integrierten CLI:

```bash
python -m ticket_generator
```

Minimale Konfigurationsideen (Pseudocode):

```python
# config/config.py (Beispiel)
RUN = {
    "rows": 10_000,  # Gesamtanzahl der Beispiele
    "batch_size": 50,  # niedriger für günstige Entwicklungs-Durchläufe
    "languages": ["DE", "EN", "FR", "ES", "PT"],
    "timezone": "Europe/Berlin",
    "pipeline": [
        "topic_node",
        "email_draft_node",
        "tagging_node",
        "paraphrase_node",
        "translate_node",
        "first_response_node"
    ],
    "models": {
        "default": {
            "provider": "openai",
            "name": "gpt-4o-mini",
            "max_tokens": 800
        }
    },
    "cost_limits": {
        "warn": 0.001,  # USD pro einzelnem Assistenten-Durchlauf
        "error": 0.01
    }
}
```

> In der Praxis werden Sie Prompts anpassen, verschiedene Modelle pro Knoten auswählen und domänenspezifische Zufallstabellen hinzufügen (Warteschlangen, Prioritäten, Geschäftsbereiche usw.).

## Ausgabeschema

Häufige Spalten, die Sie in unseren generierten CSV/Parquet-Exporten finden werden:

* `ticket_id` (12–13-stelliger String)
* `subject`, `body`
* `language` (DE/EN/FR/ES/PT)
* `type` ∈ (Incident, Request, Problem, Change)
* `queue` (domänenspezifisch, z. B. *Technischer Support*, *Abrechnung*, *Personal*)
* `priority` ∈ (Niedrig, Mittel, Hoch)
* `tags` (Array/Liste von 4–8)
* `first_response` (Antwort des Agenten)

## Beispieldatensatz auf Kaggle

Wir haben diesen Generator verwendet, um den öffentlichen Datensatz **Multilingual Customer Support Tickets** zu erstellen. Er enthält **Prioritäten, Warteschlangen, Typen, Tags und Geschäftsbereiche** und ist ideal für das Training von Modellen zur Ticket-Klassifizierung und -Priorisierung.
➡️ Kaggle: **Multilingual Customer Support Tickets**

* Enthält mehrere Sprachen und alle oben aufgeführten Labels
* Community-Notebooks demonstrieren Anwendungsfälle für Klassifizierung und Routing

## Wie dies Open Ticket AI unterstützt

**Open Ticket AI** klassifiziert die **Warteschlange** und **Priorität** bei eingehenden Tickets. Synthetische Daten sind von unschätzbarem Wert, wenn Sie:

* **Keine oder nur begrenzte** gelabelte Verlaufsdaten haben
* **Sensible** Daten haben, die Ihre Infrastruktur nicht verlassen dürfen
* **Ausgeglichene** Klassen benötigen (z. B. für seltene Warteschlangen/Prioritäten)
* **Mehrsprachige** Abdeckung vom ersten Tag an benötigen

Wir verwenden den Generator routinemäßig, um:

1. das Modelltraining zu bootstrappen,
2. Long-Tail-Klassen auszugleichen, und
3. mehrsprachige Abläufe zu simulieren.
   Wenn Sie möchten, dass wir maßgeschneiderte Datensätze für Sie generieren (Ihre Domain/Warteschlangen/Prioritäten/Tags, Ihre Sprachen), bieten wir dies als **Dienstleistung** an.

\::: tip Dienstleistungen
Benötigen Sie domänenspezifische synthetische Daten für Ihren Helpdesk? Wir entwerfen Prompts, Knoten und Zufallstabellen für Ihre Branche, integrieren sie in Ihre Datenpipeline und liefern CSV/Parquet-Dateien, die für Training und Evaluierung bereit sind.
**Kontakt:** [sales@softoft.de](mailto:sales@softoft.de)
\:::

## Lizenzierung & Verfügbarkeit

* Die Veröffentlichung des **Synthetic Data Generator** ist unter der **LGPL** geplant.
* Wenn Sie frühen Zugriff, eine private Lizenz oder individuelle Anpassungen/Erweiterungen wünschen, **senden Sie eine E-Mail an `sales@softoft.de`**, und wir richten es für Sie ein.

---

### FAQ

**Ist der Datensatz „echt“ oder „synthetisch“?**
Vollständig synthetisch, erzeugt durch eine konfigurierbare LLM-Pipeline.

**Kann ich eigene Felder hinzufügen (z. B. *Geschäftseinheit*, *Auswirkung*, *Dringlichkeit*)?**
Ja – erweitern Sie die Zufallstabellen und fügen Sie einen Knoten hinzu, um die Felder auszugeben.

**Kann ich Stil und Tonalität steuern?**
Absolut. Prompts sind pro Knoten definiert, sodass Sie Tonalität, Formalität, Regionalismen und Terminologie erzwingen können.

**Wie halte ich die Kosten unter Kontrolle?**
Verwenden Sie den Dev-Modus (kleine `rows`, niedrigere `max_tokens`), Kostenschwellenwerte und günstigere Modelle für frühe Iterationen. Wechseln Sie zu Ihrer bevorzugten Modellmischung, sobald die Ergebnisse stimmen.