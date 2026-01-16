---
title: 'Labeling 10,000 Tickets Efficiently: AI-Powered Semi-Automated Strategies That Scale'
description: 'Master efficient ticket labeling at scale using GPT-powered zero-shot classification, Label Studio workflows, and proven annotation techniques that reduce manual effort by 80%.'
lang: en
date: 2025-09-25
tags:
  - ai-labeling
  - data-annotation
  - gpt-classification
  - label-studio
  - zero-shot-learning
  - ml-training
  - automation-workflow
category: Tutorial
draft: false
image: ../../../assets/images/ticket-list-classified-automation.png
---

# 10.000 Tickets effizient labeln: Semi-automatisierte Labeling-Strategien

Tausende Support-Tickets manuell zu labeln ist zeitaufwändig und teuer. Ein **semi-automatisierter Workflow** nutzt große Sprachmodelle (LLMs) wie GPT, um Tickets **vorzulabeln** (mit Zero-Shot-/Few-Shot-Prompts), und setzt dann menschliche Annotatoren ein, um diese Labels zu **überprüfen und zu korrigieren**. Dieser hybride Ansatz reduziert den Annotationsaufwand drastisch: Eine Fallstudie fand beispielsweise heraus, dass GPT-generierte "Vor-Annotationen" _"gut genug waren, um unseren Labeling-Prozess zu beschleunigen"_. In der Praxis können _minimale Labels_ vom Modell Zeit und Kosten der Annotation reduzieren. In diesem Artikel erklären wir, wie man eine solche Pipeline einrichtet, zeigen Python-Beispiele (mit GPT über OpenRouter oder OpenAI) und diskutieren Tools wie Label Studio für die Überprüfung.

## GPT für Zero-Shot-/Few-Shot-Vor-Labeling nutzen

Moderne LLMs können Text mit **null oder wenigen Beispielen** klassifizieren. Beim Zero-Shot-Labeling weist das Modell Kategorien zu, ohne explizit auf Ticket-Daten trainiert worden zu sein. Wie ein Tutorial es ausdrückt: _"Zero-Shot Learning ermöglicht es Modellen, neue Instanzen ohne gelabelte Beispiele zu klassifizieren"_. In der Praxis erstellt man einen Prompt, der GPT anweist, ein Ticket zu taggen. Zum Beispiel:

```text
Ticket: "Cannot login to account."
Classify this ticket into one of {Bug, Feature Request, Question}.
```

Das Modell antwortet dann mit einem Label. Few-Shot-Labeling fügt dem Prompt ein paar Beispiele hinzu, um die Genauigkeit zu verbessern. Das bedeutet, wir können initiale Labels **direkt über die API** generieren, ohne jegliches Modell-Training.

> **Tipp:** Verwende einen strukturierten Prompt oder bitte um JSON-Ausgabe, um das Parsen zu erleichtern. Zum Beispiel:
>
> ```
> Ticket: "Password reset email bounced."
> Respond in JSON like {"category": "..."}.
> ```
>
> Dies hilft, die Antwort in deine Pipeline zu integrieren.

## Automatisiertes Vor-Labeling mit AI-APIs

Du kannst AI-APIs wie OpenAI oder OpenRouter nutzen, um Tickets automatisch vorzulabeln, bevor sie von Menschen überprüft werden. Der Prozess umfasst:

1. Durchlaufe deine Ticket-Liste
2. Sende jeden Ticket-Text an ein AI-Modell mit einem Klassifizierungs-Prompt
3. Speichere die vorhergesagte Kategorie als Vor-Label
4. Menschliche Reviewer verifizieren und korrigieren die Vor-Labels

Dieser Ansatz reduziert die manuelle Labeling-Zeit erheblich, während die Qualität durch menschliche Überwachung erhalten bleibt. OpenRouter bietet eine einheitliche API, die mit mehreren AI-Anbietern (OpenAI, Anthropic Claude, Google PaLM, etc.) funktioniert, sodass du zwischen Modellen wechseln oder Fallback-Optionen für hohe Verfügbarkeit nutzen kannst.

## Vor-Labels mit Labeling-Tools integrieren

Sobald GPT Labels generiert hat, ist der nächste Schritt, **sie in eine Labeling-Oberfläche zu importieren** für die menschliche Überprüfung. Eine beliebte Open-Source-Lösung ist [Label Studio](https://labelstud.io). Label Studio unterstützt den Import von Modellvorhersagen als "Vor-Annotationen" zusammen mit den Daten. Annotatoren sehen das vorgeschlagene Label und müssen nur Fehler korrigieren, nicht von Grund auf neu labeln. Effektiv wechselt das Team _"von der zeitintensiven Aufgabe des Daten-Labelings zum weitaus effizienteren Prozess des Überprüfens und Verfeinerns der vorläufigen Labels"_.

Label Studio bietet sogar ein ML-Backend: Du kannst einen kleinen Server schreiben, der die Klasse `LabelStudioMLBase` verwendet und GPT für jede Aufgabe aufruft. In ihrem Tutorial zeigt Label Studio, wie man GPT-4-Aufrufe in dieser Klasse kapselt, um Vorhersagen on-the-fly zurückzugeben. Alternativ kannst du eine JSON-Datei mit Vorhersagen importieren. Das erforderliche JSON-Format hat ein `data`-Feld (der Ticket-Text) und ein `predictions`-Array (das jedes Label enthält). Zum Beispiel (vereinfacht):

```json
[
  {
    "data": {
      "text": "User cannot login to account"
    },
    "predictions": [
      {
        "result": [
          {
            "value": {
              "choices": [
                {
                  "text": "Bug"
                }
              ]
            }
          }
        ]
      }
    ]
  },
  {
    "data": {
      "text": "Add dark mode to settings"
    },
    "predictions": [
      {
        "result": [
          {
            "value": {
              "choices": [
                {
                  "text": "Feature Request"
                }
              ]
            }
          }
        ]
      }
    ]
  }
]
```

Nach dem Import zeigt Label Studio jedes Ticket mit dem vorausgefüllten Label des Modells an. Die Aufgabe des Annotators ist es, **zu überprüfen und zu korrigieren**. Dieser semi-automatisierte Workflow hat sich als gut funktionierend erwiesen: Ein Kili Technology-Beispiel demonstrierte das Laden eines GPT-vorgelabelten Datensatzes und stellte fest, _"we have successfully pre-annotated our dataset"_ und dass dieser Ansatz _"has the potential to save us a lot of time"_. In der Praxis liegt die Genauigkeit von GPT beim Labeling bei etwa \~80–90 %, was bedeutet, dass Menschen nur die verbleibenden 10–20 % korrigieren müssen.

## Tools und Workflow-Schritte

Zusammenfassend sieht eine typische semi-automatisierte Labeling-Pipeline so aus:

- **Bereite den Ticket-Datensatz vor.** Exportiere deine 10.000 ungelabelten Tickets (z.B. als JSON oder CSV).
- **Generiere Vor-Labels via LLM.** Führe Code (wie oben) aus, der GPT-4 (oder ein anderes Modell über OpenRouter) aufruft, um jedes Ticket zu klassifizieren. Speichere die Antworten.
- **Importiere Vorhersagen in ein Labeling-Tool.** Verwende Label Studio (oder ähnliches), um Tickets zu laden und jedes mit dem GPT-generierten Label (der "Vorhersage") zu verknüpfen. Die Label Studio-Dokumentation erklärt, wie man Vorhersagen mit deinen Daten importiert.
- **Menschliche Überprüfung.** Annotatoren gehen die Tickets in Label Studio durch, akzeptieren oder korrigieren die Labels. Das ist viel schneller als das Labeling von Grund auf. Die Oberfläche von Label Studio hebt die Modellvorschläge für jede Aufgabe hervor, sodass die Aufgabe zur schnellen Validierung wird.
- **Exportiere finale Labels.** Nach der Überprüfung exportiere die korrigierten Annotationen für Modell-Training oder Analysen.

Wichtige öffentliche Tools, die diesen Ansatz unterstützen, sind:

- **OpenRouter** – ein einheitliches LLM-API-Gateway (openrouter.ai). Es ermöglicht dir, einfach zwischen GPT-4, Anthropic Claude, Google PaLM, etc. zu wechseln. Du kannst sogar eine Fallback-Liste in einem API-Aufruf angeben.
- **OpenAI API (GPT-4/3.5)** – die zentrale Engine zum Generieren von Labels mit Zero-/Few-Shot-Prompts.
- **Label Studio** – eine Open-Source-Daten-Labeling-UI. Es unterstützt den Import von Vorhersagen und hat ein ML-Backend, um Modelle aufzurufen.
- **Doccano** – ein einfacheres Open-Source-Tool für Text-Annotation (Klassifikation, NER, etc.). Es hat keine eingebaute LLM-Integration, aber du kannst GPT offline nutzen, um Labels zu generieren und sie als initiale Auswahl zu laden.
- **Snorkel/Programmatic Labeling** – für einige regelbasierte oder Weak-Supervision-Fälle können Tools wie Snorkel LLM-Labels ergänzen, aber moderne LLMs decken oft viele Fälle out-of-the-box ab.

## Beispiel mit Dummy-Ticket-Daten

Zur Veranschaulichung hier einige _Dummy-Ticket-Daten_, mit denen du arbeiten könntest:

```python
tickets = [
    {"id": 101, "text": "Error 500 when saving profile", "label": None},
    {"id": 102, "text": "How do I change my subscription plan?", "label": None},
    {"id": 103, "text": "Feature request: dark mode in settings", "label": None},
    {"id": 104, "text": "Application crashes on startup", "label": None},
]
```

Du könntest jeden `ticket['text']` an GPT mit einem Prompt wie diesem füttern:

```text
Ticket: "Error 500 when saving profile."
Classify this issue as one of {Bug, Feature, Question}.
```

Angenommen, GPT gibt `"Bug"`, `"Question"`, `"Feature"`, `"Bug"` zurück. Nach der Schleife könnte `tickets` so aussehen:

```python
[
    {'id': 101, 'text': 'Error 500 when saving profile', 'label': 'Bug'},
    {'id': 102, 'text': 'How do I change my subscription plan?', 'label': 'Question'},
    {'id': 103, 'text': 'Feature request: dark mode in settings', 'label': 'Feature'},
    {'id': 104, 'text': 'Application crashes on startup', 'label': 'Bug'},
]
```

Diese Labels würden dann in die Überprüfungsoberfläche geladen werden. Selbst wenn einige falsch sind (z.B. könnte GPT einen kniffligen Bug fälschlicherweise als Feature labeln), muss der Annotator sie nur _korrigieren_, anstatt von Grund auf zu beginnen. Empirisch erreichen GPT-generierte Labels oft eine Genauigkeit von \~80–90 %, daher ist die Überprüfung viel schneller als vollständiges Labeling.

## Ergebnisse und Erkenntnisse

Der semi-automatisierte Ansatz skaliert gut. In einem großen Projekt müssen menschliche Annotatoren möglicherweise nur ein paar hundert oder tausend Labels korrigieren, anstatt 10.000. Wie das Kili-Tutorial nach dem Ausführen von GPT-Vor-Labels feststellte: _"Great! We have successfully pre-annotated our dataset. Looks like this solution has the potential to save us a lot of time in future projects."_. Mit anderen Worten, LLMs dienen als Kraftmultiplikator. Auch wenn das Modell nicht 100 % korrekt ist, **"beschleunigt es den Labeling-Prozess"**, indem es den Großteil der Arbeit erledigt.

**Best Practices:** Verwende eine niedrige Temperature (z.B. 0.0–0.3) für konsistente Labels und liefere klare Anweisungen oder eine kleine Liste von Beispielen. Überwache GPTs Fehler: Möglicherweise musst du Prompts anpassen oder ein paar Few-Shot-Beispiele für unterperformende Kategorien hinzufügen. Halte den Prompt einfach (z.B. "Classify the ticket text into A, B, or C"). Du kannst auch mehrere Tickets in einem API-Aufruf bündeln, wenn Modell und API es erlauben, um Kosten zu sparen. Und schließe immer eine menschliche Überprüfung ein – dies stellt hohe Qualität sicher und fängt alle LLM-Fehler oder -Abweichungen auf.

## Fazit

Semi-automatisiertes Labeling mit GPT und Tools wie OpenRouter und Label Studio ist eine leistungsstarke Strategie, um große Textdatensätze schnell zu labeln. Indem man **10.000 Tickets mit einem LLM vorlabelt und dann überprüft**, können Unternehmen ihre AI-Workflows mit minimalen initialen Daten schnell starten. Dieser Ansatz senkt Kosten und Zeit dramatisch, während die Qualität durch menschliche Überwachung sichergestellt wird. Wie ein Implementierungsleitfaden feststellt, beschleunigt die Verlagerung des Workflows von _"data labeling"_ zum _"reviewing and refining"_ von LLM-generierten Labels _"significantly accelerates your workflow."_. Kurz gesagt, die Kombination von GPT-basierter Vor-Annotation mit einer benutzerfreundlichen UI (Label Studio, Doccano, etc.) hilft Software-/AI-Teams, massive Ticket-Datensätze effizient und genau zu labeln.
