---
title: 'Bewertung von AI Ticket Klassifikatoren: Wesentliche Metriken für die Leistung bei unausgewogenen Daten'
description: 'Meistern Sie die Bewertung von AI Klassifikatoren mit Precision, Recall, F1-Score und Confusion Matrix Analyse. Lernen Sie, warum Accuracy bei unausgewogenen Ticket-Datensätzen irreführt.'
lang: en
date: 2025-11-08
tags:
  - ai-metrics
  - model-evaluation
  - precision-recall
  - f1-score
  - imbalanced-data
  - confusion-matrix
  - classification-performance
category: Technology
draft: false
image: ../../../assets/images/statistics-reporting-ticketsystem.png
---

# Bewertung von AI Klassifikatoren mit realen Ticketdaten: Metriken, die zählen

## Einführung

Support‑Ticket‑Daten sind unordentlich und oft stark zugunsten weniger gängiger Kategorien verzerrt. Zum Beispiel könnten 80 % der Tickets mit **„general inquiry“** gekennzeichnet sein, wodurch Klassifikatoren zur Mehrheitsklasse hin voreingenommen werden. In der Praxis kann ML auf Ticketdaten für folgende Anwendungsfälle eingesetzt werden:

- **Priority prediction** (z. B. das Markieren dringender Probleme)
- **Queue or team assignment** (z. B. das Weiterleiten von Rechnungsfragen an die Finanzabteilung)
- **Intent or topic classification** (z. B. „feature request“ vs. „bug report“)

Diese Anwendungsfälle zeigen, warum die Evaluation herausfordernd ist: reale Ticket‑Datensätze sind multi‑class und multi‑label, enthalten verrauschten Text und **imbalanced classes**:contentReference[oaicite:0]{index=0}. Ein naives Modell, das immer die Mehrheitsklasse vorhersagt, kann dennoch eine hohe Accuracy erzielen, indem es seltene, aber wichtige Fälle ignoriert. Wir werden untersuchen, warum Accuracy allein irreführend ist, und die Metriken diskutieren, die wirklich zählen.

## Warum Accuracy irreführend ist

**Accuracy** ist definiert als die Gesamtzahl korrekter Vorhersagen geteilt durch alle Vorhersagen:  
$ \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} $  
In Formel‑Form: accuracy = (TP + TN)/(alle Samples). Obwohl sie einfach ist, versagt Accuracy stark bei unausgewogenen Daten. Beispiel: Wenn 80 % der Tickets zur Klasse A gehören, erreicht ein dummes Modell, das _immer_ A vorhersagt, per Default 80 % Accuracy – es ignoriert jedoch vollständig die anderen 20 % der Tickets. In extremen Fällen (z. B. 99 % vs. 1 % Klassenverteilung) liefert das immer‑vorhersagen‑der‑Mehrheit‑Modell 99 % Accuracy, obwohl kein echtes Lernen stattfindet. Kurz gesagt, eine hohe Accuracy kann einfach die Klassenverteilung widerspiegeln, nicht die tatsächliche Leistungsfähigkeit.

> **„... Accuracy ist bei unausgewogenen Datensätzen kein geeignetes Maß mehr, da sie nicht zwischen den korrekt klassifizierten Beispielen verschiedener Klassen unterscheidet. Daher kann sie zu falschen Schlussfolgerungen führen ...”.**

## Kernmetriken: Precision, Recall, F1

Um Klassifikatoren bei Imbalance zu bewerten, greifen wir auf **Precision, Recall und F1-Score** zurück, die Fehler in Minderheitsklassen fokussieren. Diese leiten sich aus der Confusion Matrix ab, z. B. für die binäre Klassifikation:

|                     | Predicted Positive  | Predicted Negative  |
| ------------------- | ------------------- | ------------------- |
| **Actual Positive** | True Positive (TP)  | False Negative (FN) |
| **Actual Negative** | False Positive (FP) | True Negative (TN)  |

Aus diesen Zählungen definieren wir:

- **Precision** = TP / (TP + FP) – Anteil der korrekt vorhergesagten Positiven.
- **Recall** = TP / (TP + FN) – Anteil der tatsächlich positiven Fälle, die gefunden wurden.
- **F1-Score** = harmonisches Mittel von Precision und Recall:  
  \[ \mathrm{F1} = \frac{2 \cdot \mathrm{TP}}{2 \cdot \mathrm{TP} + \mathrm{FP} + \mathrm{FN}}. \]

Jede Metrik hebt unterschiedliche Fehler hervor: Precision bestraft Fehlalarme (FP), während Recall verpasste Fälle (FN) bestraft. Der F1-Score balanciert beide. Zur Vollständigkeit sei erwähnt, dass Accuracy auch als \( (TP + TN) / (TP+TN+FP+FN) \) geschrieben werden kann:contentReference[oaicite:8]{index=8}, maskiert jedoch bei Imbalance Modellfehler.

In der Praxis berechnet scikit‑learn’s `classification_report` diese Werte pro Klasse. Beispiel:

reports precision, recall, F1 (and support) for each ticket class.

## Macro vs Micro Averaging

Bei Multi‑Class‑Problemen können Metriken auf verschiedene Weise gemittelt werden. **Micro‑Averaging** fasst alle Klassen zusammen, indem globale TP, FP, FN summiert werden, und berechnet dann die Metriken – gewichtet also nach dem Support jeder Klasse. **Macro‑Averaging** berechnet die Metrik für jede Klasse separat und nimmt anschließend den ungewichteten Mittelwert. Anders ausgedrückt: Macro behandelt alle Klassen gleich (seltene Klassen zählen genauso wie häufige), während Micro die Leistung auf häufigen Klassen bevorzugt. Verwenden Sie **Macro‑Averaging**, wenn Minderheitsklassen kritisch sind (z. B. das Erkennen eines seltenen dringenden Tickets), und **Micro‑Averaging**, wenn die Gesamt‑Accuracy über alle Tickets wichtiger ist.

| Averaging | How It’s Computed                                            | When to Use                                      |
| --------- | ------------------------------------------------------------ | ------------------------------------------------ |
| **Micro** | Global counts of TP, FP, FN across all classes               | Gives overall performance (favors large classes) |
| **Macro** | Average of each class’s metric (each class weighted equally) | Ensures small/rare classes count equally         |

## Multi‑Label‑Herausforderungen

Helpdesk‑Tickets tragen oft mehrere Labels gleichzeitig (z. B. ein Ticket kann sowohl ein **queue**‑ als auch ein **priority**‑Label besitzen). In Multi‑Label‑Setups kommen zusätzliche Metriken zum Einsatz:

- **Subset Accuracy** (Exact Match) – Anteil der Samples, bei denen _alle_ vorhergesagten Labels exakt mit dem wahren Label‑Set übereinstimmen. Sehr streng: ein falsches Label bedeutet Misserfolg.
- **Hamming Loss** – Anteil der einzelnen Label‑Vorhersagen, die falsch sind. Hamming Loss ist nachsichtiger: jedes Label wird unabhängig beurteilt. Ein niedriger Hamming Loss (nahe 0) ist besser.
- **Label Ranking Loss** – misst, wie viele Label‑Paare fälschlich nach Vertrauen sortiert sind. Relevant, wenn das Modell für jedes Label Scores ausgibt und wir die Reihenfolge der Labels pro Ticket benötigen.

Scikit‑learn bietet Funktionen wie `accuracy_score` (Subset Accuracy im Multi‑Label‑Modus) und `hamming_loss`. Im Allgemeinen wählt man die Metrik, die den geschäftlichen Anforderungen entspricht: Exact Match, wenn alle Labels korrekt sein müssen, oder Hamming/Ranking Loss, wenn Teil‑Korrektheit akzeptabel ist.

## Confusion Matrix in der Praxis

Eine Confusion Matrix ist oft der erste Blick auf das Verhalten eines Klassifikators. In Python können Sie sie mit scikit‑learn berechnen und darstellen:

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred, labels=classes)
print("Confusion Matrix:\n", cm)

# To visualize:
ConfusionMatrixDisplay(cm, display_labels=classes).plot()
```

Hier ist `cm[i, j]` die Anzahl der Tickets, deren wahre Klasse `i` ist, die aber als Klasse `j` vorhergesagt wurden. Beim Untersuchen einer Confusion Matrix (oder ihres Heatmaps) achten Sie auf:

- **Off-diagonal cells** – zeigen Fehlklassifikationen (welche Klassen werden am häufigsten verwechselt).
- **False positives vs false negatives** – z. B. eine hohe Zeilensumme außerhalb der Diagonale bedeutet, dass das Modell diese tatsächliche Klasse häufig verpasst (viele FNs); eine hohe Spaltensumme außerhalb der Diagonale bedeutet viele falsche Vorhersagen dieser Klasse (FPs).
- **Underrepresented classes** – Klassen mit wenigen Beispielen können fast leere Zeilen/Spalten aufweisen, was darauf hindeutet, dass das Modell sie selten korrekt vorhersagt.

Eine gründliche Analyse der Confusion Matrix hilft, gezielte Daten‑Bereinigungen oder Modell‑Anpassungen für bestimmte Ticket‑Typen vorzunehmen.

## Evaluationsstrategie für reale Ticket‑Systeme

Der Aufbau einer zuverlässigen Evaluations‑Pipeline erfordert mehr als nur die Auswahl von Metriken:

- **Clean, labeled data**: Stellen Sie sicher, dass Ihr Test‑Set repräsentativ und korrekt gelabelt ist. Entfernen Sie Duplikate oder falsch gelabelte Tickets vor der Evaluation.
- **Baseline vs Fine‑tuned**: Vergleichen Sie Ihr AI‑Modell immer mit einfachen Baselines (z. B. Majority‑Class‑Predictor oder regelbasierte Keyword‑Systeme). Messen Sie relative Verbesserungen mit den gewählten Metriken.
- **Periodic Reevaluation**: Ticket‑Trends ändern sich über die Zeit (saisonale Probleme, neue Produkte). Planen Sie regelmäßiges Retraining und Reevaluation oder ein Trigger‑System bei Data‑Drift.
- **Stakeholder Communication**: Übersetzen Sie Metriken in umsetzbare Erkenntnisse für nicht‑technische Stakeholder. Beispiel: „Recall stieg von 75 % auf 85 % für dringende Tickets, das bedeutet, wir erfassen 10 % mehr hochprioritäre Fälle automatisch.“ Nutzen Sie Diagramme (z. B. Balkendiagramme von Precision/Recall pro Klasse) und betonen Sie den geschäftlichen Nutzen (schnellere Reaktion, geringere Rückstände).

## Fazit

Zusammengefasst: **Man kann nicht verbessern, was man nicht misst**. Accuracy allein reicht bei unausgewogenen, komplexen Ticket‑Daten nicht aus. Stattdessen sollten Sie klassenweise Precision, Recall und F1 (unter Verwendung von Macro‑ bzw. Micro‑Averages nach Bedarf) verfolgen und bei Multi‑Label‑Tickets passende Metriken berücksichtigen. Beginnen Sie frühzeitig mit dem Tracking von Metriken in jeder AI‑Integration, damit Fortschritte (oder Probleme) sichtbar werden. Durch die Fokussierung auf die richtigen Metriken von Anfang an können Support‑Teams ihre Ticket‑Klassifikatoren iterativ verbessern und zuverlässigere Automatisierung liefern.

Möchten Sie diese Ideen an Ihren eigenen Daten ausprobieren? Schauen Sie sich die Plattform [Open Ticket AI Demo](https://open-ticket-ai.com) an, um mit realen Ticket‑Datensätzen und integrierten Evaluations‑Tools zu experimentieren.