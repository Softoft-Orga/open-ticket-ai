---
description: 'Lernen Sie, KI-Ticket-Klassifikatoren auf realen, unausgeglichenen Daten zu bewerten. Entdecken Sie, warum Accuracy irreführend ist, und konzentrieren Sie sich auf die wirklich wichtigen Metriken: Precision, Recall & F1-Score.'
---
# Bewertung von KI-Klassifikatoren auf realen Ticketdaten: Die wirklich wichtigen Metriken

## Einführung

Support-Ticketdaten sind unübersichtlich und oft stark auf einige wenige gängige Kategorien konzentriert. Zum Beispiel
könnten 80 % der Tickets als **„allgemeine Anfrage“** gekennzeichnet sein, was dazu führt, dass Klassifikatoren zur Mehrheitsklasse
tendieren. In der Praxis kann ML für Ticketdaten für folgende Zwecke eingesetzt werden:

- **Prioritätsvorhersage** (z. B. Kennzeichnung dringender Probleme)
- **Warteschlangen- oder Teamzuweisung** (z. B. Weiterleitung von Abrechnungsfragen an die Finanzabteilung)
- **Absichts- oder Themenklassifizierung** (z. B. „Funktionswunsch“ vs. „Fehlerbericht“)

Diese Anwendungsfälle zeigen, warum die Bewertung eine Herausforderung darstellt: Reale Ticket-Datensätze sind Multi-Class und
Multi-Label, mit verrauschtem Text und **unausgeglichenen Klassen**:contentReference[oaicite:0]{index=0}. Ein
naives Modell, das immer die Mehrheitsklasse vorhersagt, kann dennoch eine hohe Accuracy erzielen, indem es seltene, aber wichtige Fälle ignoriert.
Wir werden untersuchen, warum Accuracy allein irreführend ist, und die Metriken besprechen, die wirklich zählen.

## Warum Accuracy irreführend ist

**Accuracy** (Genauigkeit) ist definiert als die Gesamtzahl der korrekten Vorhersagen geteilt durch alle Vorhersagen:
$ \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} $
In Formelschreibweise: Accuracy = (TP + TN)/(alle Samples). Obwohl
einfach, versagt die Accuracy bei unausgeglichenen Daten dramatisch. Wenn beispielsweise 80 % der Tickets zur Klasse A gehören,
erreicht ein simpler Klassifikator, der *immer* A vorhersagt, standardmäßig eine Accuracy von 80 % – ignoriert dabei aber die anderen 20 % der Tickets vollständig.
In Extremfällen (z. B. bei einer Klassenverteilung von 99 % zu 1 %) führt die ständige Vorhersage der Mehrheit zu einer Accuracy von 99 %,
obwohl kein echtes Lernen stattgefunden hat. Kurz gesagt, eine hohe Accuracy kann einfach die Klassenverteilung widerspiegeln, nicht die tatsächliche Leistung.

> **„… Accuracy ist kein geeignetes Maß mehr [für unausgeglichene Datensätze], da sie nicht zwischen der Anzahl der korrekt klassifizierten Beispiele verschiedener Klassen unterscheidet. Daher kann sie zu fehlerhaften Schlussfolgerungen führen …“.**

## Kernmetriken: Precision, Recall, F1

Um Klassifikatoren bei unausgeglichenen Daten zu bewerten, stützen wir uns auf **Precision, Recall und den F1-Score**, die sich auf Fehler in den Minderheitsklassen konzentrieren.
Diese werden aus der Konfusionsmatrix abgeleitet, z. B. für eine binäre Klassifizierung:

|                      | Vorhergesagt Positiv | Vorhergesagt Negativ |
|----------------------|----------------------|----------------------|
| **Tatsächlich Positiv** | Richtig Positiv (TP) | Falsch Negativ (FN)  |
| **Tatsächlich Negativ** | Falsch Positiv (FP)  | Richtig Negativ (TN) |

Aus diesen Zählungen definieren wir:

- **Precision** (Präzision) = TP / (TP + FP) – der Anteil der positiven Vorhersagen, die korrekt sind:
- **Recall** (Trefferquote) = TP / (TP + FN) – der Anteil der tatsächlich positiven Fälle, die gefunden wurden:
- **F1-Score** = das harmonische Mittel aus Precision und Recall:
  \[ \mathrm{F1} = \frac{2 \cdot \mathrm{TP}}{2 \cdot \mathrm{TP} + \mathrm{FP} + \mathrm{FN}}. \]

Jede Metrik hebt unterschiedliche Fehler hervor: Precision bestraft Fehlalarme (FP), während Recall übersehene Fälle (FN) bestraft. Der F1-Score gleicht beides aus. Der Vollständigkeit halber sei erwähnt, dass die Accuracy auch als \( (TP + TN) / (TP+TN+FP+FN) \) geschrieben werden kann:contentReference[oaicite:8]{index=8}, aber bei unausgeglichenen Daten verdeckt sie Modellfehler.

In der Praxis berechnet der `classification_report` von scikit-learn diese Werte pro Klasse. Zum Beispiel:

meldet Precision, Recall, F1 (und Support) für jede Ticket-Klasse.

## Makro- vs. Mikro-Mittelung

Bei Multi-Class-Problemen können Metriken auf unterschiedliche Weise gemittelt werden. **Mikro-Mittelung** fasst alle Klassen zusammen, indem die globalen TP, FP und FN summiert und dann die Metriken berechnet werden – was einer Gewichtung nach dem Support jeder Klasse entspricht. **Makro-Mittelung** berechnet die Metrik für jede Klasse separat und bildet dann den ungewichteten Mittelwert. Mit anderen Worten, die Makro-Mittelung behandelt alle Klassen gleich (sodass seltene Klassen genauso viel zählen wie häufige), während die Mikro-Mittelung die Leistung bei häufigen Klassen bevorzugt. Verwenden Sie die **Makro-Mittelung**, wenn Minderheitsklassen kritisch sind (z. B. das Erkennen eines seltenen, dringenden Tickets), und die **Mikro-Mittelung**, wenn die Gesamt-Accuracy über alle Tickets hinweg wichtiger ist.

| Mittelung | Berechnung                                                   | Anwendungsfall                                           |
|-----------|--------------------------------------------------------------|----------------------------------------------------------|
| **Mikro** | Globale Zählung von TP, FP, FN über alle Klassen               | Gibt die Gesamtleistung an (bevorzugt große Klassen)     |
| **Makro** | Durchschnitt der Metrik jeder Klasse (jede Klasse gleich gewichtet) | Stellt sicher, dass kleine/seltene Klassen gleich gewichtet werden |

## Multi-Label-Herausforderungen

Helpdesk-Tickets haben oft mehrere Labels gleichzeitig (z. B. könnte ein Ticket sowohl ein **Warteschlangen**- als auch ein **Prioritäts**-Label haben). In Multi-Label-Setups kommen zusätzliche Metriken zur Anwendung:

*   **Subset Accuracy** (Exakte Übereinstimmung) – der Anteil der Samples, bei denen *alle* vorhergesagten Labels exakt mit dem wahren Satz von Labels übereinstimmen. Dies ist sehr streng: Ein falsches Label bedeutet einen Fehlschlag.
*   **Hamming-Verlust** – der Anteil der einzelnen Label-Vorhersagen, die falsch sind. Der Hamming-Verlust ist nachsichtiger: Jedes Label wird unabhängig bewertet. Ein niedrigerer Hamming-Verlust (nahe 0) ist besser.
*   **Label Ranking Loss** – misst, wie viele Label-Paare nach Konfidenz falsch geordnet sind. Dies ist relevant, wenn das Modell Scores für jedes Label ausgibt und uns die Rangfolge der Labels für jedes Ticket wichtig ist.

Scikit-learn bietet Funktionen wie `accuracy_score` (Subset Accuracy im Multi-Label-Modus) und `hamming_loss`. Im Allgemeinen wählt man die Metrik, die den Geschäftsanforderungen entspricht: exakte Übereinstimmung, wenn alle Labels korrekt sein müssen, oder Hamming/Ranking Loss, wenn eine teilweise Korrektheit akzeptabel ist.

## Konfusionsmatrix in der Praxis

Eine Konfusionsmatrix ist oft der erste Blick auf das Verhalten eines Klassifikators. In Python können Sie sie mit scikit-learn berechnen und anzeigen:

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred, labels=classes)
print("Confusion Matrix:\n", cm)

# To visualize:
ConfusionMatrixDisplay(cm, display_labels=classes).plot()
```

Hier ist `cm[i, j]` die Anzahl der Tickets, deren wahre Klasse `i` ist, die aber als Klasse `j` vorhergesagt wurden.
Bei der Untersuchung einer Konfusionsmatrix (oder ihrer Heatmap) achten Sie auf:

*   **Zellen außerhalb der Diagonalen** – diese deuten auf Fehlklassifizierungen hin (welche Klassen am häufigsten verwechselt werden).
*   **Falsch Positive vs. Falsch Negative** – z. B. bedeutet eine hohe Summe einer Zeile außerhalb der Diagonalen, dass das Modell diese tatsächliche Klasse häufig übersehen hat (viele FNs); eine hohe Summe einer Spalte außerhalb der Diagonalen bedeutet viele falsche Vorhersagen dieser Klasse (FPs).
*   **Unterrepräsentierte Klassen** – Klassen mit wenigen Beispielen können als fast leere Zeilen/Spalten erscheinen, was darauf hindeutet, dass das Modell sie selten korrekt vorhersagt.

Eine sorgfältige Analyse der Konfusionsmatrix hilft dabei, die Datenbereinigung oder Modellanpassungen für bestimmte Ticket-Typen gezielt vorzunehmen.

## Evaluierungsstrategie für reale Ticketsysteme

Der Aufbau einer zuverlässigen Evaluierungspipeline erfordert mehr als nur die Auswahl von Metriken:

*   **Saubere, gelabelte Daten**: Stellen Sie sicher, dass Ihr Testdatensatz repräsentativ und korrekt gelabelt ist. Entfernen Sie Duplikate oder falsch gelabelte Tickets vor der Bewertung.
*   **Baseline vs. feinabgestimmtes Modell**: Vergleichen Sie Ihr KI-Modell immer mit einfachen Baselines (z. B. einem Mehrheitsklassen-Prädiktor oder regelbasierten Keyword-Systemen). Messen Sie relative Verbesserungen mit den gewählten Metriken.
*   **Regelmäßige Neubewertung**: Ticket-Trends ändern sich im Laufe der Zeit (saisonale Probleme, neue Produkte). Planen Sie, das Modell regelmäßig neu zu trainieren und zu bewerten oder dies bei Datendrift auszulösen.
*   **Kommunikation mit Stakeholdern**: Übersetzen Sie Metriken in handlungsorientierte Erkenntnisse für nicht-technische Stakeholder. Zum Beispiel: „Der Recall für dringende Tickets stieg von 75 % auf 85 %, was bedeutet, dass wir 10 % mehr hochpriore Probleme automatisch erkennen.“ Verwenden Sie Diagramme (z. B. Balkendiagramme für Precision/Recall pro Klasse) und betonen Sie die geschäftlichen Auswirkungen (schnellere Reaktion, reduzierte Rückstände).

## Fazit

Zusammenfassend lässt sich sagen: **Was man nicht misst, kann man nicht verbessern**. Accuracy allein reicht für unausgeglichene, komplexe Ticketdaten nicht aus. Verfolgen Sie stattdessen klassenweise Precision, Recall und F1 (unter Verwendung von Makro-/Mikro-Mittelwerten, wo angebracht) und ziehen Sie Multi-Label-Metriken in Betracht, wenn Ihre Tickets mehrere Annotationen haben. Beginnen Sie frühzeitig mit der Verfolgung von Metriken bei jeder KI-Integration, damit Gewinne (oder Probleme) sichtbar werden. Indem sich Support-Teams vom ersten Tag an auf die richtigen Metriken konzentrieren, können sie ihre Ticket-Klassifikatoren iterativ verbessern und eine zuverlässigere Automatisierung bereitstellen.

Möchten Sie diese Ideen mit Ihren eigenen Daten ausprobieren? Besuchen Sie die Plattform [Open Ticket AI Demo](https://open-ticket-ai.com), um mit echten Ticket-Datensätzen und integrierten Bewertungstools zu experimentieren.