---
title: 'Evaluating AI Ticket Classifiers: Essential Metrics for Imbalanced Data Performance'
description: 'Master AI classifier evaluation with precision, recall, F1-score, and confusion matrix analysis. Learn why accuracy misleads on imbalanced ticket datasets.'
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

# Bewertung von KI-Klassifikatoren mit echten Ticket-Daten: Die entscheidenden Metriken

## Einleitung

Support-Ticket-Daten sind unübersichtlich und oft stark zugunsten weniger häufiger Kategorien verzerrt. Beispielsweise könnten 80 % der Tickets als **"Allgemeine Anfrage"** gekennzeichnet sein, wodurch Klassifikatoren auf die Mehrheitsklasse voreingenommen werden. In der Praxis kann ML für Ticket-Daten verwendet werden für:

- **Prioritätsvorhersage** (z. B. Markierung dringender Probleme)
- **Warteschlangen- oder Teamzuweisung** (z. B. Weiterleitung von Abrechnungsfragen an die Finanzabteilung)
- **Absichts- oder Themenklassifikation** (z. B. "Feature-Request" vs. "Bug-Report")

Diese Anwendungsfälle zeigen, warum die Evaluation herausfordernd ist: Reale Ticket-Datensätze sind mehrklassig und mehrfach gelabelt, mit verrauschtem Text und **ungleichmäßigen Klassen**:contentReference[oaicite:0]{index=0}. Ein naives Modell, das immer die Mehrheitsklasse vorhersagt, kann dennoch eine hohe Genauigkeit erzielen, indem es seltene, aber wichtige Fälle ignoriert. Wir werden untersuchen, warum die Genauigkeit allein irreführend ist und die Metriken besprechen, die wirklich zählen.

## Warum Genauigkeit irreführend ist

**Genauigkeit (Accuracy)** ist definiert als die Anzahl der korrekten Vorhersagen geteilt durch alle Vorhersagen:
$ \text{Genauigkeit} = \frac{TP + TN}{TP + TN + FP + FN} $
In Formelausdrücken: Genauigkeit = (TP + TN)/(alle Stichproben). Obwohl einfach, versagt die Genauigkeit bei unausgewogenen Daten dramatisch. Wenn beispielsweise 80 % der Tickets zur Klasse A gehören, erreicht ein einfältiger Klassifikator, der _immer_ A vorhersagt, standardmäßig 80 % Genauigkeit – ignoriert dabei aber die anderen 20 % der Tickets vollständig. In Extremfällen (z. B. 99 % vs. 1 % Klassenaufteilung) ergibt die ständige Vorhersage der Mehrheitsklasse 99 % Genauigkeit, obwohl kein echtes Lernen stattfindet. Kurz gesagt, eine hohe Genauigkeit kann einfach die Klassenverteilung widerspiegeln, nicht die tatsächliche Leistung.

> \*\*"... Genauigkeit ist kein geeignetes Maß mehr [für unausgewogene Datensätze], da sie nicht zwischen der Anzahl korrekt klassifizierter Beispiele verschiedener Klassen unterscheidet. Daher kann sie zu falschen Schlussfolgerungen führen ...".

## Kernmetriken: Präzision, Trefferquote, F1

Um Klassifikatoren bei unausgewogenen Daten zu bewerten, verlassen wir uns auf **Präzision, Trefferquote (Recall) und den F1-Score**, die sich auf Fehler in Minderheitsklassen konzentrieren. Diese leiten sich aus der Konfusionsmatrix ab, z. B. für binäre Klassifikation:

|                         | Vorhergesagt Positiv | Vorhergesagt Negativ |
| ----------------------- | -------------------- | -------------------- |
| **Tatsächlich Positiv** | True Positive (TP)   | False Negative (FN)  |
| **Tatsächlich Negativ** | False Positive (FP)  | True Negative (TN)   |

Aus diesen Werten definieren wir:

- **Präzision** = TP / (TP + FP) – Anteil der vorhergesagten Positivfälle, die korrekt sind:
- **Trefferquote (Recall)** = TP / (TP + FN) – Anteil der tatsächlichen Positivfälle, die gefunden wurden:
- **F1-Score** = harmonisches Mittel aus Präzision und Trefferquote:
  \[ \mathrm{F1} = \frac{2 \cdot \mathrm{TP}}{2 \cdot \mathrm{TP} + \mathrm{FP} + \mathrm{FN}}. \]

Jede Metrik hebt unterschiedliche Fehler hervor: Präzision bestraft Fehlalarme (FP), während Trefferquote Verpasste (FN) bestraft. Der F1-Score balanciert beide. Der Vollständigkeit halber sei angemerkt, dass Genauigkeit auch als \( (TP + TN) / (TP+TN+FP+FN) \) geschrieben werden kann:contentReference[oaicite:8]{index=8}, aber bei unausgewogenen Daten verschleiert sie Modellfehler.

In der Praxis berechnet scikit-learns `classification_report` diese Werte pro Klasse. Zum Beispiel:

gibt Präzision, Trefferquote, F1 (und Support) für jede Ticket-Klasse aus.

## Makro- vs. Mikro-Mittelung

Bei Mehrklassenproblemen können Metriken auf verschiedene Arten gemittelt werden. **Mikro-Mittelung** fasst alle Klassen zusammen, indem globale TP, FP, FN summiert und dann Metriken berechnet werden – effektiv gewichtet nach der Häufigkeit jeder Klasse. **Makro-Mittelung** berechnet die Metrik für jede Klasse separat und bildet dann den ungewichteten Durchschnitt. Mit anderen Worten, Makro behandelt alle Klassen gleich (seltene Klassen zählen also genauso viel wie häufige), während Mikro die Leistung bei häufigen Klassen bevorzugt. Verwenden Sie **Makro-Mittelung**, wenn Minderheitsklassen kritisch sind (z. B. Erkennung eines seltenen dringenden Tickets), und **Mikro-Mittelung**, wenn die Gesamtgenauigkeit über alle Tickets wichtiger ist.

| Mittelung | Wie sie berechnet wird                                              | Wann zu verwenden                                        |
| --------- | ------------------------------------------------------------------- | -------------------------------------------------------- |
| **Mikro** | Globale Zählungen von TP, FP, FN über alle Klassen                  | Gibt Gesamtleistung wieder (bevorzugt große Klassen)     |
| **Makro** | Durchschnitt der Metrik jeder Klasse (jede Klasse gleich gewichtet) | Stellt sicher, dass kleine/seltene Klassen gleich zählen |

## Herausforderungen bei Mehrfach-Labels

Helpdesk-Tickets tragen oft mehrere Labels gleichzeitig (z. B. kann ein Ticket sowohl ein **Warteschlangen-** als auch ein **Prioritäts-**Label haben). Bei Mehrfach-Label-Setups gelten zusätzliche Metriken:

- **Teilmengen-Genauigkeit (Exact Match)** – Anteil der Stichproben, bei denen _alle_ vorhergesagten Labels genau mit der wahren Menge der Labels übereinstimmen. Dies ist sehr streng: Ein falsches Label bedeutet Fehler.
- **Hamming-Verlust** – der Anteil der einzelnen Label-Vorhersagen, die falsch sind. Hamming-Verlust ist nachsichtiger: Jedes Label wird unabhängig beurteilt. Ein niedrigerer Hamming-Verlust (nahe 0) ist besser.
- **Label-Ranking-Verlust** – misst, wie viele Label-Paare durch das Vertrauen falsch geordnet sind. Er ist relevant, wenn das Modell für jedes Label Scores ausgibt und wir uns um die Rangfolge der Labels für jedes Ticket kümmern.

Scikit-learn bietet Funktionen wie `accuracy_score` (Teilmengen-Genauigkeit im Mehrfach-Label-Modus) und `hamming_loss`. Im Allgemeinen wählt man die Metrik, die den Geschäftsanforderungen entspricht: Exact Match, wenn alle Labels korrekt sein müssen, oder Hamming/Ranking-Verlust, wenn teilweise Korrektheit akzeptabel ist.

## Konfusionsmatrix in der Praxis

Eine Konfusionsmatrix ist oft der erste Blick auf das Verhalten eines Klassifikators. In Python können Sie sie mit scikit-learn berechnen und anzeigen:

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred, labels=classes)
print("Konfusionsmatrix:\n", cm)

# Zur Visualisierung:
ConfusionMatrixDisplay(cm, display_labels=classes).plot()
```

Hier ist `cm[i, j]` die Anzahl der Tickets, deren wahre Klasse `i` ist, aber als Klasse `j` vorhergesagt wurden. Bei der Betrachtung einer Konfusionsmatrix (oder ihrer Heatmap) achten Sie auf:

- **Nicht-diagonale Zellen** – diese zeigen Fehlklassifikationen an (welche Klassen am häufigsten verwechselt werden).
- **Falsch Positive vs. Falsch Negative** – z. B. eine hohe Zeilensumme außerhalb der Diagonale bedeutet, dass das Modell diese tatsächliche Klasse häufig verpasst hat (viele FNs); eine hohe Spaltensumme außerhalb der Diagonale bedeutet viele falsche Vorhersagen dieser Klasse (FPs).
- **Unterrepräsentierte Klassen** – Klassen mit wenigen Beispielen können als fast leere Zeilen/Spalten erscheinen, was darauf hindeutet, dass das Modell sie selten korrekt vorhersagt.

Die richtige Analyse der Konfusionsmatrix hilft, Datenbereinigung oder Modellanpassungen für bestimmte Tickettypen gezielt anzugehen.

## Evaluationsstrategie für echte Ticketsysteme

Der Aufbau einer zuverlässigen Evaluationspipeline erfordert mehr als nur die Auswahl von Metriken:

- **Saubere, gelabelte Daten**: Stellen Sie sicher, dass Ihr Testset repräsentativ und korrekt gelabelt ist. Entfernen Sie Duplikate oder falsch gelabelte Tickets vor der Evaluation.
- **Baseline vs. Feinabgestimmt**: Vergleichen Sie Ihr KI-Modell immer mit einfachen Baselines (z. B. Mehrheitsklassen-Prädiktor oder Keyword-Regelsysteme). Messen Sie relative Verbesserungen mit den gewählten Metriken.
- **Periodische Neubewertung**: Ticket-Trends ändern sich im Laufe der Zeit (saisonale Probleme, neue Produkte). Planen Sie, das Modell regelmäßig neu zu trainieren und zu bewerten oder bei Datenverschiebung auszulösen.
- **Kommunikation mit Stakeholdern**: Übersetzen Sie Metriken in umsetzbare Erkenntnisse für nicht-technische Stakeholder. Zum Beispiel: "Die Trefferquote für dringende Tickets stieg von 75 % auf 85 %, was bedeutet, dass wir 10 % mehr hochprioritäre Probleme automatisch erfassen." Verwenden Sie Diagramme (z. B. Balkendiagramme von Präzision/Trefferquote pro Klasse) und betonen Sie die geschäftliche Auswirkung (schnellere Antwort, reduzierte Rückstände).

## Fazit

Zusammenfassend gilt: **Was man nicht misst, kann man nicht verbessern**. Genauigkeit allein reicht nicht für unausgewogene, komplexe Ticket-Daten aus. Verfolgen Sie stattdessen klassenweise Präzision, Trefferquote und F1 (unter Verwendung von Makro-/Mikro-Mittelungen nach Bedarf) und ziehen Sie Mehrfach-Label-Metriken in Betracht, wenn Ihre Tickets mehrere Annotationen haben. Beginnen Sie die Metrikverfolgung früh in jeder KI-Integration, damit Gewinne (oder Probleme) sichtbar werden. Durch die Konzentration auf die richtigen Metriken von Anfang an können Support-Teams ihre Ticket-Klassifikatoren iterativ verbessern und zuverlässigere Automatisierung liefern.

Möchten Sie diese Ideen mit Ihren eigenen Daten ausprobieren? Besuchen Sie die [Open Ticket AI Demo](https://open-ticket-ai.com) Plattform, um mit echten Ticket-Datensätzen und integrierten Evaluierungswerkzeugen zu experimentieren.
