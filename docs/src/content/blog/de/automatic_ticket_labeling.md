---
title: '10.000 Tickets effizient labeln: KI-gestützte halbautomatische Strategien, die skalieren'
description: 'Meistern Sie effizientes Ticket-Labeling im großen Maßstab mit GPT-gestützter Zero-Shot-Klassifikation, Label Studio-Workflows und bewährten Annotationstechniken, die den manuellen Aufwand um 80 % reduzieren.'
lang: de
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

# 10.000 Tickets effizient labeln: Halbautomatische Labeling-Strategien

Tausende Support-Tickets manuell zu labeln ist zeitaufwändig und teuer. Ein **halbautomatisierter Workflow** nutzt große Sprachmodelle (LLMs) wie GPT, um Tickets **vorzulabeln** (mit Zero-Shot-/Few-Shot-Prompts), und setzt dann menschliche Annotatoren ein, um diese Labels zu **überprüfen und zu korrigieren**. Dieser hybride Ansatz reduziert den Annotationsaufwand drastisch: Eine Fallstudie fand beispielsweise heraus, dass GPT-generierte "Vorannotationen" _"gut genug waren, um unseren Labeling-Prozess zu beschleunigen"_. In der Praxis können *minimale Labels* vom Modell Zeit und Kosten der Annotation reduzieren. In diesem Artikel erklären wir, wie man eine solche Pipeline einrichtet, zeigen Python-Beispiele (mit GPT über OpenRouter oder OpenAI) und diskutieren Tools wie Label Studio für die Überprüfung.

## GPT für Zero-Shot-/Few-Shot-Vorlabeling nutzen

Moderne LLMs können Text mit **null oder wenigen Beispielen** klassifizieren. Beim Zero-Shot-Labeling weist das Modell Kategorien zu, ohne explizit auf Ticketdaten trainiert worden zu sein. Wie ein Tutorial es ausdrückt: _"Zero-Shot Learning ermöglicht es Modellen, neue Instanzen ohne gelabelte Beispiele zu klassifizieren"_. In der Praxis erstellen Sie einen Prompt, der GPT anweist, ein Ticket zu taggen. Zum Beispiel:

```text
Ticket: "Cannot login to account."
Classify this ticket into one of {Bug, Feature Request, Question}.
```

Das Modell antwortet dann mit einem Label. Few-Shot-Labeling fügt dem Prompt ein paar Beispiele hinzu, um die Genauigkeit zu verbessern. Das bedeutet, wir können initiale Labels **direkt über die API** generieren, ohne jegliches Modelltraining.

> **Tipp:** Verwenden Sie einen strukturierten Prompt oder fordern Sie JSON-Ausgabe an, um das Parsen zu erleichtern. Zum Beispiel:
>
> ```
> Ticket: "Password reset email bounced."
> Respond in JSON like {"category": "..."}.
> ```
>
> Dies hilft, die Antwort in Ihre Pipeline zu integrieren.

## Automatisiertes Vorlabeling mit KI-APIs

Sie können KI-APIs wie OpenAI oder OpenRouter verwenden, um Tickets automatisch vorzulabeln, bevor sie von Menschen überprüft werden. Der Prozess umfasst:

1. Durchlaufen Ihrer Ticketliste
2. Senden jedes Tickettexts an ein KI-Modell mit einem Klassifikationsprompt
3. Speichern der vorhergesagten Kategorie als Vorlabel
4. Überprüfung und Korrektur der Vorlabels durch menschliche Reviewer

Dieser Ansatz reduziert die manuelle Labeling-Zeit erheblich, während die Qualität durch menschliche Aufsicht erhalten bleibt. OpenRouter bietet eine einheitliche API, die mit mehreren KI-Anbietern (OpenAI, Anthropic Claude, Google PaLM, etc.) funktioniert, sodass Sie zwischen Modellen wechseln oder Fallback-Optionen für hohe Verfügbarkeit nutzen können.

## Integration von Vorlabels mit Labeling-Tools

Sobald GPT Labels generiert hat, besteht der nächste Schritt darin, **sie in eine Labeling-Oberfläche zu importieren** für die menschliche Überprüfung. Eine beliebte Open-Source-Lösung ist [Label Studio](https://labelstud.io). Label Studio unterstützt den Import von Modellvorhersagen als "Vorannotationen" zusammen mit den Daten. Annotatoren sehen das vorgeschlagene Label und müssen nur Fehler korrigieren, nicht von Grund auf neu labeln. Effektiv wechselt das Team _"von der zeitintensiven Aufgabe des Datenlabelings zum weitaus effizienteren Prozess der Überprüfung und Verfeinerung der vorläufigen Labels"_.

Label Studio bietet sogar ein ML-Backend: Sie können einen kleinen Server schreiben, der die Klasse `LabelStudioMLBase` verwendet und GPT für jede Aufgabe aufruft. In ihrem Tutorial zeigt Label Studio, wie GPT-4-Aufrufe in dieser Klasse gekapselt werden, um Vorhersagen on-the-fly zurückzugeben. Alternativ können Sie eine JSON-Datei mit Vorhersagen importieren. Das erforderliche JSON-Format hat ein `data`-Feld (der Tickettext) und ein `predictions`-Array (das jedes Label enthält). Zum Beispiel (vereinfacht):

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

Nach dem Import zeigt Label Studio jedes Ticket mit dem vorausgefüllten Label des Modells an. Die Aufgabe des Annotators ist es, **zu überprüfen und zu korrigieren**. Dieser halbautomatisierte Workflow hat sich als gut funktionierend erwiesen: Ein Kili Technology-Beispiel demonstrierte das Laden eines GPT-vorgelabelten Datensatzes und stellte fest, _"we have successfully pre-annotated our dataset"_ und dass dieser Ansatz _"has the potential to save us a lot of time"_. In der Praxis liegt die Genauigkeit von GPT beim Labeling bei etwa \~80–90 %, was bedeutet, dass Menschen nur die verbleibenden 10–20 % korrigieren müssen.

## Tools und Workflow-Schritte

Zusammenfassend sieht eine typische halbautomatisierte Labeling-Pipeline so aus:

- **Bereiten Sie den Ticket-Datensatz vor.** Exportieren Sie Ihre 10.000 ungelabelten Tickets (z.B. als JSON oder CSV).
- **Generieren Sie Vorlabels via LLM.** Führen Sie Code (wie oben) aus, der GPT-4 (oder ein anderes Modell über OpenRouter) aufruft, um jedes Ticket zu klassifizieren. Speichern Sie die Antworten.
- **Importieren Sie Vorhersagen in ein Labeling-Tool.** Verwenden Sie Label Studio (oder ähnliches), um Tickets zu laden und jedes mit dem GPT-generierten Label (der "Vorhersage") zu verknüpfen. Die Label Studio-Dokumentation erklärt, wie man Vorhersagen mit Ihren Daten importiert.
- **Menschliche Überprüfung.** Annotatoren gehen die Tickets in Label Studio durch, akzeptieren oder korrigieren die Labels. Dies ist viel schneller als das Labeling von Grund auf. Die Oberfläche von Label Studio hebt die Modellvorschläge für jede Aufgabe hervor, sodass die Aufgabe zur schnellen Validierung wird.
- **Exportieren Sie die finalen Labels.** Nach der Überprüfung exportieren Sie die korrigierten Annotationen für das Modelltraining oder die Analyse.

Wichtige öffentliche Tools, die diesen Ansatz unterstützen, sind:

- **OpenRouter** – ein einheitliches LLM-API-Gateway (openrouter.ai). Es ermöglicht Ihnen, einfach zwischen GPT-4, Anthropic Claude, Google PaLM usw. zu wechseln. Sie können sogar eine Fallback-Liste in einem API-Aufruf angeben.
- **OpenAI API (GPT-4/3.5)** – die Kern-Engine zur Generierung von Labels mit Zero-/Few-Shot-Prompts.
- **Label Studio** – eine Open-Source-Datenlabeling-UI. Es unterstützt den Import von Vorhersagen und hat ein ML-Backend, um Modelle aufzurufen.
- **Doccano** – ein einfacheres Open-Source-Tool für Textannotation (Klassifikation, NER, etc.). Es hat keine eingebaute LLM-Integration, aber Sie können GPT offline verwenden, um Labels zu generieren und sie als initiale Auswahl zu laden.
- **Snorkel/Programmatic Labeling** – für einige regelbasierte oder Weak-Supervision-Fälle können Tools wie Snorkel LLM-Labels ergänzen, aber moderne LLMs decken oft viele Fälle out-of-the-box ab.

## Beispiel mit Dummy-Ticket-Daten

Zur Veranschaulichung hier einige *Dummy-Ticket-Daten*, mit denen Sie arbeiten könnten:

```python
tickets = [
    {"id": 101, "text": "Error 500 when saving profile", "label": None},
    {"id": 102, "text": "How do I change my subscription plan?", "label": None},
    {"id": 103, "text": "Feature request: dark mode in settings", "label": None},
    {"id": 104, "text": "Application crashes on startup", "label": None},
]
```

Sie könnten jeden `ticket['text']` an GPT mit einem Prompt wie diesem füttern:

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

Diese Labels würden dann in die Überprüfungsoberfläche geladen werden. Selbst wenn einige falsch sind (z.B. könnte GPT einen kniffligen Bug als Feature falsch labeln), muss der Annotator sie nur *korrigieren*, anstatt von Grund auf zu beginnen. Empirisch erreichen GPT-generierte Labels oft eine Genauigkeit von \~80–90 %, sodass die Überprüfung viel schneller ist als vollständiges Labeling.

## Ergebnisse und Erkenntnisse

Der halbautomatisierte Ansatz skaliert gut. In einem großen Projekt müssen menschliche Annotatoren möglicherweise nur ein paar hundert oder tausend Labels korrigieren, anstatt 10.000. Wie das Kili-Tutorial nach dem Ausführen von GPT-Vorlabels feststellte: _"Great! We have successfully pre-annotated our dataset. Looks like this solution has the potential to save us a lot of time in future projects."_. Mit anderen Worten dienen LLMs als Kraftmultiplikator. Auch wenn das Modell nicht zu 100 % korrekt ist, **"beschleunigt es den Labeling-Prozess"**, indem es den Großteil der Arbeit erledigt.

**Best Practices:** Verwenden Sie eine niedrige Temperature (z.B. 0.0–0.3) für konsistente Labels und geben Sie klare Anweisungen oder eine kleine Liste von Beispielen. Überwachen Sie die Fehler von GPT: Möglicherweise müssen Sie Prompts anpassen oder Few-Shot-Beispiele für unterperformende Kategorien hinzufügen. Halten Sie den Prompt einfach (z.B. "Classify the ticket text into A, B, or C"). Sie können auch mehrere Tickets in einem API-Aufruf bündeln, wenn Modell und API dies erlauben, um Kosten zu sparen. Und schließen Sie immer eine menschliche Überprüfung ein – dies stellt hohe Qualität sicher und fängt alle LLM-Fehler oder -Abweichungen auf.

## Fazit

Halbautomatisches Labeling mit GPT und Tools wie OpenRouter und Label Studio ist eine leistungsstarke Strategie, um große Textdatensätze schnell zu labeln. Indem Sie **10.000 Tickets mit einem LLM vorlabeln und dann überprüfen**, können Unternehmen ihre KI-Workflows mit minimalen initialen Daten beschleunigen. Dieser Ansatz senkt Kosten und Zeit dramatisch, während die Qualität durch menschliche Aufsicht gewährleistet bleibt. Wie ein Implementierungsleitfaden feststellt, beschleunigt die Verlagerung des Workflows von _"data labeling"_ zum _"reviewing and refining"_ von LLM-generierten Labels _"significantly accelerates your workflow."_. Kurz gesagt hilft die Kombination von GPT-basierter Vorannotation mit einer benutzerfreundlichen UI (Label Studio, Doccano, etc.) Software-/KI-Teams dabei, massive Ticket-Datensätze effizient und genau zu labeln.