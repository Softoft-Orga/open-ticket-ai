---
aside: false
description: "Planen Sie Ihr Projekt zur Ticket-Automatisierung. Wählen Sie den richtigen\
  \ Weg basierend auf Ihren Daten – klassifiziert, unklassifiziert oder keine – für\
  \ schnelles Training, Deployment und Support."
pageClass: full-page
---
# Planer für Ticket-Automatisierung – Wählen Sie Ihren besten Weg

Modernisieren Sie das Ticket-Routing schnell – egal, wo Sie anfangen. Dieser Planer hilft Ihnen, den richtigen Weg basierend auf Ihrer Datenrealität zu wählen: viele klassifizierte Tickets, viele unklassifizierte Tickets oder fast keine Daten. Jeder Weg endet mit einem konkreten Servicepaket mit klaren Ergebnissen und KPIs, sodass Sie ohne Raten von der Idee → zum Pilotprojekt → in die Produktion übergehen können.

**Für wen ist das:** IT-/Service-Teams, die Znuny/OTRS/OTOBO (oder ähnliches) verwenden und zuverlässige Vorhersagen für Queue/Priorität/Tags wünschen, entweder On-Prem oder über eine gehostete API.

**Was Sie erhalten:** ein kurzer Entscheidungsfluss, 4 umsetzbare Pfade (A–D), Add-ons (mehrsprachig, zusätzliche Attribute), Gates/Metriken, um zu wissen, wann Sie bereit sind, und eine Checkliste zur Datenbereitschaft.

**So verwenden Sie diese Seite**

* Beginnen Sie mit der Übersicht auf einer Seite und beantworten Sie drei Fragen: **Klassifiziert? → Unklassifiziert? → Schnell?**
* Klicken Sie auf das Feld für **Flow A/B/C/D**, um zu den jeweiligen Schritten, Ergebnissen und KPIs zu springen.
* Nutzen Sie die **Add-ons**, wenn Sie mehrere Sprachen oder mehr Ausgaben (Tags, Bearbeiter, Erstantwort) benötigen.
* Halten Sie die **Gates** eng (F1 pro Klasse + geschäftliche KPIs), damit Pilotprojekte zu Vertrauen in die Produktion führen.

Fahren Sie nun mit dem Übersichtsdiagramm und den detaillierten Abläufen unten fort.
Schön – hier ist eine ausführlichere Beschreibung, die Sie unter Ihre Diagramme einfügen können. Ich habe sie überfliegbar gehalten, aber echte Anleitungen und Schwellenwerte hinzugefügt, damit die Leser zuversichtlich einen Flow auswählen können.

Verstanden – ich behalte Ihre neuen kurzen Diagramme bei und füge für jeden Abschnitt klare, prägnante Erklärungen hinzu, damit sich der Artikel vollständig anfühlt und trotzdem leicht zu überfliegen ist.

---

## 0) Übersicht auf einer Seite

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  S((Start)) --> Q1{Labeled?}
  Q1 -- Yes --> A0[Flow A]
  Q1 -- No --> Q2{Unlabeled?}
  Q2 -- Yes --> B0[Flow B]
  Q2 -- No --> Q3{Fast?}
  Q3 -- Yes --> D0[Flow D]
  Q3 -- No --> C0[Flow C]

click A0 "#flow-a-many-labeled" "Flow A"
click B0 "#flow-b-many-unlabeled" "Flow B"
click C0 "#flow-c-few-or-no-tickets" "Flow C"
click D0 "#flow-d-quick-start-hosted-api" "Flow D"
```

**So verwenden Sie diese Übersicht:**
Beginnen Sie oben, beantworten Sie die Fragen und folgen Sie dem Zweig zu Ihrem passenden Flow. Klicken Sie auf einen Flow, um die Details anzuzeigen.

---

## <a id="flow-a-many-labeled"></a> Flow A – Viele klassifizierte Tickets

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Audit/Tax] --> B[Train]
  B --> C[Eval]
  C --> D[On-Prem]
  D --> E[Pilot]
  E --> F[Support]
```

**Wann Sie diesen Weg wählen sollten:**

* Sie haben bereits **Tausende von Tickets mit Klassifizierungen für Queue, Priorität oder Tags**.
* Sie möchten ein **individuell trainiertes** Model für maximale Genauigkeit.

**Was in diesem Flow passiert:**

1. **Audit/Taxonomie** – Überprüfung der Label-Qualität, der Klassenverteilung und der Benennung.
2. **Training** – Feinabstimmung des Klassifizierungsmodells mit Ihren Daten.
3. **Evaluierung** – Messung von Precision/Recall/F1 pro Klasse.
4. **On-Prem** – Deployment in Ihrer eigenen Infrastruktur.
5. **Pilot** – Test im Produktivbetrieb mit Monitoring.
6. **Support** – Iteration und erneutes Training nach Bedarf.

**Empfohlenes Paket:** Fine-Tune + On-Prem-Installation.

---

## <a id="flow-b-many-unlabeled"></a> Flow B – Viele unklassifizierte Tickets

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Ingest] --> B[Auto-Label]
  B --> C[QC]
  C --> D{OK?}
  D -- No --> B
  D -- Yes --> E[Train]
  E --> F[Eval]
  F --> G[On-Prem]
  G --> H[Support]
```

**Wann Sie diesen Weg wählen sollten:**

* Sie haben **große historische Ticket-Archive**, aber keine Labels.
* Sie können etwas Zeit für die manuelle Überprüfung zur Qualitätssicherung einplanen.

**Was in diesem Flow passiert:**

1. **Ingest** – Sammeln von Tickets aus Ihrem System.
2. **Auto-Label** – Verwendung von LLM-gestütztem Auto-Labeling.
3. **QS** – Stichprobenartige Überprüfung und Korrektur von Beispielen.
4. **OK?** – Wiederholen, bis die Qualität den Schwellenwert erreicht.
5. **Training** – Feinabstimmung mit dem kuratierten Datensatz.
6. **Evaluierung / On-Prem / Support** – Wie bei Flow A.

**Empfohlenes Paket:** Auto-Label + Fine-Tune.

---

## <a id="flow-c-few-or-no-tickets"></a> Flow C – Wenige oder keine Tickets

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Define Tax] --> B[Synth Data]
  B --> C[Baseline]
  C --> D[Eval]
  D --> E{Pilot}
  E -- API --> H[Hosted DE]
  E -- Local --> I[On-Prem]
  H --> J[Collect]
  I --> J
  J --> K[Fine-Tune]
  K --> L[Prod/Support]
```

**Wann Sie diesen Weg wählen sollten:**

* Sie fangen **bei Null an** oder haben zu wenige Tickets für ein Training.
* Sie möchten eine **Cold-Start**-Lösung, um schnell live zu gehen.

**Was in diesem Flow passiert:**

1. **Taxonomie definieren** – Festlegung von Queues, Prioritäten, Tonalität.
2. **Synthetische Daten** – Generierung realistischer Tickets (DE/EN).
3. **Baseline** – Training eines initialen Modells mit synthetischen Daten.
4. **Evaluierung** – Überprüfung der Leistung vor dem Rollout.
5. **Pilot** – Wahl zwischen gehosteter API für Geschwindigkeit oder On-Prem für Kontrolle.
6. **Sammeln** – Erfassen von echten Tickets während des Pilotprojekts.
7. **Fine-Tune** – Zusammenführen von echten und synthetischen Daten.
8. **Produktion/Support** – Live-Betrieb mit fortlaufender Iteration.

**Empfohlenes Paket:** Synthetic Cold-Start.

---

## <a id="flow-d-quick-start-hosted-api"></a> Flow D – Schnellstart über gehostete API

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
    A[Use API DE] --> B[Measure]
    B --> C{Tax OK?}
    C -- Yes --> D[Scale/Support]
    C -- No --> E[Auto/Synth - Train]
    E --> F[On-Prem]
```

**Wann Sie diesen Weg wählen sollten:**

* Sie benötigen **sofort Ergebnisse**.
* Sie möchten die Automatisierung ausprobieren, ohne vorher ein Training durchzuführen.

**Was in diesem Flow passiert:**

1. **API DE nutzen** – Sofortige Klassifizierung über ein gehostetes deutsches Model.
2. **Messen** – Verfolgung der Auswirkungen auf Routing, SLAs und Backlog.
3. **Taxonomie OK?** – Wenn Sie zufrieden sind, skalieren Sie die Nutzung; wenn nicht, wechseln Sie zu Flow B oder C für das Training.

**Empfohlenes Paket:** Hosted API Pilot → Fine-Tune (optional).

---

## Optionale Add-ons

### Mehrsprachige Erweiterung

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[More langs?] --> B{Hist per lang?}
  B -- Yes --> C[Auto-Label]
  B -- No --> D[Synth]
  C --> E[Train Multi]
  D --> E
  E --> F[Pilot/Eval]
```

Fügen Sie Unterstützung für weitere Sprachen durch mehrsprachiges Auto-Labeling oder synthetische Generierung hinzu, trainieren und evaluieren Sie dann pro Sprache/Region.

---

### Zusätzliche Attribute

```mermaid
---
config:
  theme: 'dark'
---
flowchart TD
  A[Add tags/assignee/FAA] --> B[Extend labels/gen]
  B --> C[Multi-task/Chain]
  C --> D[Deploy]
```

Sagen Sie mehr als nur Queues/Prioritäten voraus – z. B. Tags, Bearbeiter oder Erstantwortzeit – indem Sie das Labeling erweitern und ein Multi-Task-Modell trainieren.