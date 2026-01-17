---
title: 'Labeln von 10.000 Tickets effizient: KI-gestützte halbautomatisierte Strategien, die skalieren'
description: 'Meistern Sie effizientes Ticket-Labeln im großen Maßstab mithilfe von GPT-gestützter Zero-Shot-Klassifizierung, Label Studio-Workflows und bewährten Annotationsmethoden, die den manuellen Aufwand um 80 % reduzieren.'
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

# Labeln von 10.000 Tickets effizient: halbautomatisierte Labeling-Strategien

Das manuelle Labeln von tausenden Support‑Tickets ist zeitaufwendig und teuer. Ein **halbautomatisierter Workflow** nutzt große Sprachmodelle (LLMs) wie GPT, um Tickets **vorab zu labeln** (mit Zero‑Shot/Few‑Shot‑Prompts) und anschließend menschliche Annotatoren die **Überprüfung und Korrektur** dieser Labels durchführen zu lassen. Dieser hybride Ansatz reduziert den Annotierungsaufwand drastisch: In einer Fallstudie wurde festgestellt, dass von GPT erzeugte „Pre‑Annotations“ _„good enough to help us speed up the labeling process“_. In der Praxis können _minimale Labels_ des Modells Zeit und Kosten der Annotation senken. In diesem Artikel erklären wir, wie man eine solche Pipeline einrichtet, zeigen Python‑Beispiele (unter Verwendung von GPT via OpenRouter oder OpenAI) und diskutieren Werkzeuge wie Label Studio für die Überprüfung.

## Verwendung von GPT für Zero‑Shot/Few‑Shot‑Vor‑Labeling

Moderne LLMs können Text mit **null oder wenigen Beispielen** klassifizieren. Beim Zero‑Shot‑Labeling weist das Modell Kategorien zu, ohne explizit auf Ticket‑Daten trainiert zu sein. Wie ein Tutorial formuliert: _„Zero‑Shot learning allows models to classify new instances without labeled examples“_. In der Praxis erstellen Sie einen Prompt, der GPT anweist, ein Ticket zu taggen. Zum Beispiel:

```text
Ticket: "Cannot login to account."
Classify this ticket into one of {Bug, Feature Request, Question}.
```

Das Modell antwortet dann mit einem Label. Few‑Shot‑Labeling fügt dem Prompt ein paar Beispiele hinzu, um die Genauigkeit zu erhöhen. Das bedeutet, dass wir anfängliche Labels **direkt über die API** erzeugen können, ohne ein Modell zu trainieren.

> **Tipp:** Verwenden Sie einen strukturierten Prompt oder fordern Sie JSON‑Ausgabe an, um das Parsen zu erleichtern. Zum Beispiel:
>
> ```
> Ticket: "Password reset email bounced."
> Respond in JSON like {"category": "..."}.
> ```
>
> Dies erleichtert die Integration der Antwort in Ihre Pipeline.

## Automatisiertes Vor‑Labeling mit AI‑APIs

Sie können AI‑APIs wie OpenAI oder OpenRouter verwenden, um Tickets automatisch vorab zu labeln, bevor sie von Menschen geprüft werden. Der Prozess umfasst:

1. Durchlaufen Ihrer Ticket‑Liste
2. Senden des Ticket‑Texts an ein AI‑Modell mit einem Klassifizierungs‑Prompt
3. Speichern der vorhergesagten Kategorie als Vor‑Label
4. Menschliche Prüfer verifizieren und korrigieren die Vor‑Labels

Dieser Ansatz reduziert die manuelle Label‑Zeit erheblich, während die Qualität durch menschliche Aufsicht erhalten bleibt. OpenRouter bietet eine einheitliche API, die mit mehreren AI‑Anbietern (OpenAI, Anthropic Claude, Google PaLM usw.) funktioniert und es Ihnen ermöglicht, zwischen Modellen zu wechseln oder Fallback‑Optionen für hohe Verfügbarkeit zu nutzen.

## Integration von Vor‑Labels in Labeling‑Tools

Sobald GPT Labels erzeugt, besteht der nächste Schritt darin, **sie in eine Labeling‑Oberfläche** für die menschliche Überprüfung zu importieren. Eine beliebte Open‑Source‑Lösung ist [Label Studio](https://labelstud.io). Label Studio unterstützt das Importieren von Modell‑Vorhersagen als „Pre‑Annotations“ zusammen mit den Daten. Annotatoren sehen das vorgeschlagene Label und müssen nur Fehler korrigieren, nicht von Grund auf labeln. Tatsächlich _„verlagert das Team die zeitintensive Aufgabe des Daten‑Labelns in den deutlich effizienteren Prozess des Prüfens und Verfeinerns der vorläufigen Labels“_.

Label Studio bietet sogar ein ML‑Backend: Sie können einen kleinen Server mit der Klasse `LabelStudioMLBase` schreiben, der für jede Aufgabe GPT aufruft. In ihrem Tutorial zeigt Label Studio, wie GPT‑4‑Aufrufe in dieser Klasse gewrappt werden, um Vorhersagen on‑the‑fly zurückzugeben. Alternativ können Sie eine JSON‑Datei mit Vorhersagen importieren. Das erforderliche JSON‑Format enthält ein `data`‑Feld (der Ticket‑Text) und ein `predictions`‑Array (das jedes Label enthält). Zum Beispiel (vereinfacht):

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

Nach dem Import zeigt Label Studio jedes Ticket mit dem vom Modell vorab ausgefüllten Label an. Die Aufgabe des Annotators ist **Überprüfung und Korrektur**. Dieser halbautomatisierte Workflow hat sich als erfolgreich erwiesen: Ein Beispiel von Kili Technology zeigte das Laden eines GPT‑vor‑gelabelten Datensatzes und bemerkte _“we have successfully pre-annotated our dataset”_ und dass dieser Ansatz _“has the potential to save us a lot of time”_. In der Praxis liegt die Genauigkeit von GPT beim Labeln bei etwa 80–90 %, sodass Menschen nur die verbleibenden 10–20 % korrigieren.

## Werkzeuge und Workflow‑Schritte

Zusammengefasst sieht eine typische halbautomatisierte Labeling‑Pipeline folgendermaßen aus:

- **Bereiten Sie den Ticket‑Datensatz vor.** Exportieren Sie Ihre 10.000 unlabeled Tickets (z. B. als JSON oder CSV).
- **Generieren Sie Vor‑Labels via LLM.** Führen Sie Code (wie oben) aus, der GPT‑4 (oder ein anderes Modell via OpenRouter) aufruft, um jedes Ticket zu klassifizieren. Speichern Sie die Antworten.
- **Importieren Sie Vorhersagen in ein Labeling‑Tool.** Verwenden Sie Label Studio (oder Ähnliches), um Tickets zu laden und jedes mit dem von GPT erzeugten Label (der „prediction“) zu verknüpfen. Die Label‑Studio‑Dokumentation erklärt, wie man Vorhersagen mit Ihren Daten importiert.
- **Menschliche Überprüfung.** Annotatoren gehen die Tickets in Label Studio durch, akzeptieren oder korrigieren die Labels. Das ist viel schneller als das Labeln von Grund auf. Die Oberfläche von Label Studio hebt den Modellvorschlag für jede Aufgabe hervor, sodass die Aufgabe zu einer schnellen Validierung wird.
- **Exportieren Sie die finalen Labels.** Nach der Überprüfung exportieren Sie die korrigierten Annotations für das Modell‑Training oder Analysen.

Wichtige öffentliche Werkzeuge, die diesen Ansatz unterstützen, umfassen:

- **OpenRouter** – ein einheitliches LLM‑API‑Gateway (openrouter.ai). Es ermöglicht ein einfaches Wechseln zwischen GPT‑4, Anthropic Claude, Google PaLM usw. Sie können sogar eine Fallback‑Liste in einem API‑Aufruf angeben.
- **OpenAI API (GPT‑4/3.5)** – die Kern‑Engine zur Generierung von Labels mit Zero‑Shot/Few‑Shot‑Prompts.
- **Label Studio** – eine Open‑Source‑Daten‑Labeling‑UI. Sie unterstützt das Importieren von Vorhersagen und hat ein ML‑Backend, um Modelle aufzurufen.
- **Doccano** – ein einfacheres Open‑Source‑Tool für Textannotation (Klassifikation, NER usw.). Es hat keine integrierte LLM‑Integration, aber Sie können dennoch GPT offline nutzen, um Labels zu generieren und sie als Anfangsoptionen zu laden.
- **Snorkel/Programmatic Labeling** – für einige regelbasierte oder schwache‑Supervisions‑Fälle können Werkzeuge wie Snorkel LLM‑Labels ergänzen, aber moderne LLMs decken oft viele Fälle bereits ab.

## Beispiel für Dummy‑Ticket‑Daten

Zur Veranschaulichung, hier ein paar _Dummy‑Ticket‑Daten_, mit denen Sie arbeiten könnten:

```python
tickets = [
    {"id": 101, "text": "Error 500 when saving profile", "label": None},
    {"id": 102, "text": "How do I change my subscription plan?", "label": None},
    {"id": 103, "text": "Feature request: dark mode in settings", "label": None},
    {"id": 104, "text": "Application crashes on startup", "label": None},
]
```

Sie könnten jedes `ticket['text']` an GPT mit einem Prompt wie folgt senden:

```text
Ticket: "Error 500 when saving profile."
Classify this issue as one of {Bug, Feature, Question}.
```

Angenommen, GPT gibt jeweils `"Bug"`, `"Question"`, `"Feature"`, `"Bug"` zurück. Nach der Schleife könnte `tickets` so aussehen:

```python
[
    {'id': 101, 'text': 'Error 500 when saving profile', 'label': 'Bug'},
    {'id': 102, 'text': 'How do I change my subscription plan?', 'label': 'Question'},
    {'id': 103, 'text': 'Feature request: dark mode in settings', 'label': 'Feature'},
    {'id': 104, 'text': 'Application crashes on startup', 'label': 'Bug'},
]
```

Diese Labels würden dann in die Review‑Oberfläche geladen. Selbst wenn einige falsch sind (z. B. könnte GPT einen kniffligen Bug als Feature markieren), muss der Annotator sie nur _korrigieren_, anstatt von Grund auf zu beginnen. Empirisch erreichen von GPT erzeugte Labels häufig etwa 80–90 % Genauigkeit, sodass das Review viel schneller ist als vollständiges Labeln.

## Ergebnisse und Erkenntnisse

Der halbautomatisierte Ansatz skaliert gut. In einem großen Projekt müssen menschliche Annotatoren möglicherweise nur ein paar hundert oder tausend Labels korrigieren statt 10.000. Wie das Kili‑Tutorial nach dem Ausführen von GPT‑Vor‑Labels feststellte: _“Great! We have successfully pre-annotated our dataset. Looks like this solution has the potential to save us a lot of time in future projects.”_. Mit anderen Worten, LLMs wirken als Kraftverstärker. Auch wenn das Modell nicht zu 100 % korrekt ist, **„speeds up the labeling process“** indem es den Großteil der Arbeit übernimmt.

**Best Practices:** Verwenden Sie eine niedrige Temperatur (z. B. 0,0–0,3) für konsistente Labels und geben Sie klare Anweisungen oder eine kleine Liste von Beispielen. Überwachen Sie GPT‑Fehler: Möglicherweise müssen Sie Prompts anpassen oder ein paar Shot‑Beispiele für unterperformende Kategorien hinzufügen. Halten Sie den Prompt einfach (z. B. „Classify the ticket text into A, B, or C“). Sie können auch mehrere Tickets in einem API‑Aufruf stapeln, wenn Modell und API dies zulassen, um Kosten zu sparen. Und immer menschliche Überprüfung einbeziehen – das gewährleistet hohe Qualität und fängt LLM‑Fehler oder Drift ab.

## Fazit

Halbautomatisiertes Labeln mit GPT und Werkzeugen wie OpenRouter und Label Studio ist eine leistungsstarke Strategie, um große Text‑Datensätze schnell zu labeln. Durch **Vor‑Labeln von 10.000 Tickets mit einem LLM und anschließendes Review** können Unternehmen ihre KI‑Workflows mit minimalen Anfangsdaten schnell starten. Dieser Ansatz reduziert Kosten und Zeit drastisch, während die Qualität durch menschliche Aufsicht gewährleistet bleibt. Wie ein Implementierungs‑Guide feststellt, verlagert das Verschieben des Workflows von _„data labeling“_ zu _„reviewing and refining“_ von LLM‑generierten Labels _„significantly accelerates your workflow.“_. Kurz gesagt, die Kombination von GPT‑basierter Vor‑Annotation mit einer benutzerfreundlichen UI (Label Studio, Doccano usw.) hilft Software‑/AI‑Teams, massive Ticket‑Datensätze effizient und genau zu labeln.