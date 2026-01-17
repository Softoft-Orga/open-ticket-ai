---
title: 'Evaluierung von KI-Ticket-Klassifizierern: Wesentliche Metriken für die Leistung bei unausgewogenen Daten'
description: 'Meistern Sie die Evaluierung von KI-Klassifizierern mit Präzision, Recall, F1-Score und Konfusionsmatrix-Analyse. Erfahren Sie, warum Genauigkeit bei unausgewogenen Ticket-Datensätzen irreführend ist.'
lang: de
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

# Evaluierung von KI-Klassifizierern anhand realer Ticket-Daten: Die Metriken, die zählen

## Einleitung

Support-Ticket-Daten sind unordentlich und oft stark auf einige wenige häufige Kategorien verzerrt. Beispielsweise könnten 80 % der Tickets als **"Allgemeine Anfrage"** gekennzeichnet sein, was Klassifizierer zur Mehrheitsklasse verzerrt. In der Praxis kann ML bei Ticket-Daten für Folgendes verwendet werden:

- **Prioritätsvorhersage** (z. B. Kennzeichnung dringender Probleme)
- **Queue- oder Teamzuweisung** (z. B. Weiterleitung von Abrechnungsfragen an die Finanzabteilung)
- **Absichts- oder Themenklassifizierung** (z. B. "Feature-Anfrage" vs. "Bug-Report")

Diese Anwendungsfälle zeigen, warum die Evaluierung herausfordernd ist: Reale Ticket-Datensätze sind mehrklassig und mehrfach gekennzeichnet, mit verrauschtem Text und **unausgewogenen Klassen**:contentReference[oaicite:0]{index=0}. Ein naives Modell, das immer die Mehrheitsklasse vorhersagt, kann dennoch eine hohe Genauigkeit erzielen, indem es seltene, aber wichtige Fälle ignoriert. Wir werden untersuchen, warum Genauigkeit allein irreführend ist, und die Metriken diskutieren, die wirklich zählen.

## Warum Genauigkeit irreführend ist

**Genauigkeit** ist definiert als die Gesamtzahl der korrekten Vorhersagen über alle Vorhersagen:
$ \text{Genauigkeit} = \frac{TP + TN}{TP + TN + FP + FN} $
In Formelausdrücken: Genauigkeit = (TP + TN)/(alle Stichproben). Obwohl einfach, versagt die Genauigkeit bei unausgewogenen Daten stark. Wenn beispielsweise 80 % der Tickets zur Klasse A gehören, erreicht ein einfacher Klassifizierer, der _immer_ A vorhersagt, standardmäßig 80 % Genauigkeit – ignoriert jedoch die anderen 20 % der Tickets vollständig. In extremen Fällen (z. B. 99 % vs. 1 % Klassenaufteilung) ergibt die ständige Vorhersage der Mehrheit 99 % Genauigkeit, obwohl kein echtes Lernen stattfindet. Kurz gesagt, eine hohe Genauigkeit kann einfach die Klassenverteilung widerspiegeln, nicht die tatsächliche Leistung.

> \*\*"... Genauigkeit ist kein geeignetes Maß mehr [für unausgewogene Datensätze], da sie nicht zwischen den Zahlen korrekt klassifizierter Beispiele verschiedener Klassen unterscheidet. Daher kann sie zu fehlerhaften Schlussfolgerungen führen ...".

## Kernmetriken: Präzision, Recall, F1

Um Klassifizierer bei Unausgewogenheit zu evaluieren, verlassen wir uns auf **Präzision, Recall und F1-Score**, die sich auf Fehler in Minderheitsklassen konzentrieren. Diese werden aus der Konfusionsmatrix abgeleitet, z. B. für binäre Klassifikation:

|                         | Vorhergesagt Positiv | Vorhergesagt Negativ |
| ----------------------- | -------------------- | -------------------- |
| **Tatsächlich Positiv** | True Positive (TP)   | False Negative (FN)  |
| **Tatsächlich Negativ** | False Positive (FP)  | True Negative (TN)   |

Aus diesen Zählungen definieren wir:

- **Präzision** = TP / (TP + FP) – Anteil der vorhergesagten Positivfälle, die korrekt sind:
- **Recall** = TP / (TP + FN) – Anteil der tatsächlichen Positivfälle, die gefunden wurden:
- **F1-Score** = harmonisches Mittel aus Präzision und Recall:
  \[ \mathrm{F1} = \frac{2 \cdot \mathrm{TP}}{2 \cdot \mathrm{TP} + \mathrm{FP} + \mathrm{FN}}. \]

Jede Metrik hebt unterschiedliche Fehler hervor: Präzision bestraft Fehlalarme (FP), während Recall verpasste Fälle (FN) bestraft. Der F1-Score balanciert beide. Der Vollständigkeit halber sei angemerkt, dass Genauigkeit auch als \( (TP + TN) / (TP+TN+FP+FN) \):contentReference[oaicite:8]{index=8} geschrieben werden kann, aber bei unausgewogenen Daten verdeckt sie Modellfehler.

In der Praxis berechnet scikit-learns `classification_report` diese pro Klasse. Zum Beispiel:

berichtet Präzision, Recall, F1 (und Support) für jede Ticketklasse.

## Makro- vs. Mikro-Mittelung

Bei Mehrklassenproblemen können Metriken auf unterschiedliche Weise gemittelt werden. **Mikro-Mittelung** fasst alle Klassen zusammen, indem globale TP, FP, FN summiert werden, und berechnet dann die Metriken – effektiv gewichtet nach dem Support jeder Klasse. **Makro-Mittelung** berechnet die Metrik für jede Klasse separat und nimmt dann den ungewichteten Durchschnitt. Mit anderen Worten, Makro behandelt alle Klassen gleich (seltene Klassen zählen also genauso viel wie häufige), während Mikro die Leistung bei häufigen Klassen bevorzugt. Verwenden Sie **Makro-Mittelung**, wenn Minderheitsklassen kritisch sind (z. B. Erkennung eines seltenen dringenden Tickets), und **Mikro-Mittelung**, wenn die Gesamtgenauigkeit über alle Tickets wichtiger ist.

| Mittelung | Wie sie berechnet wird                                              | Wann zu verwenden                                        |
| --------- | ------------------------------------------------------------------- | -------------------------------------------------------- |
| **Mikro** | Globale Zählungen von TP, FP, FN über alle Klassen                  | Gibt Gesamtleistung an (bevorzugt große Klassen)         |
| **Makro** | Durchschnitt der Metrik jeder Klasse (jede Klasse gleich gewichtet) | Stellt sicher, dass kleine/seltene Klassen gleich zählen |

## Herausforderungen bei Multi-Label

Helpdesk-Tickets haben oft mehrere Labels gleichzeitig (z. B. könnte ein Ticket sowohl ein **Queue-** als auch ein **Prioritäts-**Label haben). Bei Multi-Label-Setups gelten zusätzliche Metriken:

- **Subset-Genauigkeit** (Exakte Übereinstimmung) – Anteil der Stichproben, bei denen _alle_ vorhergesagten Labels genau mit der wahren Menge der Labels übereinstimmen. Dies ist sehr streng: Ein falsches Label bedeutet Fehler.
- **Hamming-Verlust** – der Anteil der einzelnen Label-Vorhersagen, die falsch sind. Hamming-Verlust ist nachsichtiger: Jedes Label wird unabhängig beurteilt. Ein niedrigerer Hamming-Verlust (nahe 0) ist besser.
- **Label-Ranking-Verlust** – misst, wie viele Label-Paare durch das Konfidenzniveau falsch geordnet sind. Dies ist relevant, wenn das Modell für jedes Label Scores ausgibt und wir uns um die Rangfolge der Labels für jedes Ticket kümmern.

Scikit-learn bietet Funktionen wie `accuracy_score` (Subset-Genauigkeit im Multi-Label-Modus) und `hamming_loss`. Im Allgemeinen wählt man die Metrik, die den Geschäftsanforderungen entspricht: Exakte Übereinstimmung, wenn alle Labels korrekt sein müssen, oder Hamming-/Ranking-Verlust, wenn teilweise Korrektheit akzeptabel ist.

## Konfusionsmatrix in der Praxis

Eine Konfusionsmatrix ist oft der erste Blick auf das Verhalten eines Klassifizierers. In Python können Sie sie mit scikit-learn berechnen und anzeigen:

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred, labels=classes)
print("Konfusionsmatrix:\n", cm)

# Zur Visualisierung:
ConfusionMatrixDisplay(cm, display_labels=classes).plot()
```

Hier ist `cm[i, j]` die Anzahl der Tickets, deren wahre Klasse `i` ist, aber als Klasse `j` vorhergesagt wurden. Bei der Betrachtung einer Konfusionsmatrix (oder ihrer Heatmap) achten Sie auf:

- **Zellen außerhalb der Diagonale** – diese zeigen Fehlklassifizierungen an (welche Klassen am häufigsten verwechselt werden).
- **False Positives vs. False Negatives** – z. B. eine hohe Zeilensumme außerhalb der Diagonale bedeutet, dass das Modell diese tatsächliche Klasse häufig verpasst hat (viele FNs); eine hohe Spaltensumme außerhalb der Diagonale bedeutet viele falsche Vorhersagen dieser Klasse (FPs).
- **Unterrepräsentierte Klassen** – Klassen mit wenigen Beispielen können als fast leere Zeilen/Spalten erscheinen, was darauf hindeutet, dass das Modell sie selten korrekt vorhersagt.

Eine ordnungsgemäße Analyse der Konfusionsmatrix hilft, Datenbereinigung oder Modellanpassungen für bestimmte Tickettypen gezielt anzugehen.

## Evaluierungsstrategie für reale Ticketsysteme

Der Aufbau einer zuverlässigen Evaluierungspipeline erfordert mehr als nur die Auswahl von Metriken:

- **Saubere, gelabelte Daten**: Stellen Sie sicher, dass Ihr Testset repräsentativ und genau gelabelt ist. Entfernen Sie Duplikate oder falsch gelabelte Tickets vor der Evaluierung.
- **Baseline vs. Feinabgestimmt**: Vergleichen Sie Ihr KI-Modell immer mit einfachen Baselines (z. B. Mehrheitsklassen-Vorhersager oder Keyword-Regelsysteme). Messen Sie relative Verbesserungen mit den gewählten Metriken.
- **Periodische Neubewertung**: Ticket-Trends ändern sich im Laufe der Zeit (saisonale Probleme, neue Produkte). Planen Sie, das Modell regelmäßig neu zu trainieren und zu evaluieren oder bei Daten-Drift auszulösen.
- **Kommunikation mit Stakeholdern**: Übersetzen Sie Metriken in umsetzbare Erkenntnisse für nicht-technische Stakeholder. Zum Beispiel: "Der Recall für dringende Tickets stieg von 75 % auf 85 %, was bedeutet, dass wir 10 % mehr hochprioritäre Probleme automatisch erfassen." Verwenden Sie Diagramme (z. B. Balkendiagramme von Präzision/Recall pro Klasse) und betonen Sie die geschäftliche Auswirkung (schnellere Reaktion, reduzierte Rückstände).

## Fazit

Zusammenfassend gilt: **Man kann nicht verbessern, was man nicht misst**. Genauigkeit allein reicht nicht für unausgewogene, komplexe Ticketdaten aus. Verfolgen Sie stattdessen klassenweise Präzision, Recall und F1 (unter Verwendung von Makro-/Mikro-Mittelung je nach Bedarf) und berücksichtigen Sie Multi-Label-Metriken, wenn Ihre Tickets mehrere Annotationen haben. Beginnen Sie frühzeitig in jeder KI-Integration mit der Metrikverfolgung, damit Gewinne (oder Probleme) sichtbar werden. Indem Support-Teams von Anfang an die richtigen Metriken fokussieren, können sie ihre Ticket-Klassifizierer iterativ verbessern und zuverlässigere Automatisierung liefern.

Möchten Sie diese Ideen an Ihren eigenen Daten ausprobieren? Besuchen Sie die [Open Ticket AI Demo](https://open-ticket-ai.com)-Plattform, um mit realen Ticket-Datensätzen und integrierten Evaluierungswerkzeugen zu experimentieren.
