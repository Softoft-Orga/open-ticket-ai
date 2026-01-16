---
title: Planen Sie Ihr Ticket-Automatisierungsprojekt
description: 'Ein praktischer Leitfaden zur Abgrenzung, Priorisierung und Reihenfolgeplanung Ihrer Ticket-Automatisierungseinführung.'
lang: en
nav:
  group: Guides
  order: 3
---

# Ticket Automation Planner — Wählen Sie Ihren besten Weg

Modernisieren Sie das Ticket-Routing schnell – egal, wo Sie starten. Dieser Planner hilft Ihnen, den richtigen Weg basierend auf Ihrer Datenrealität zu wählen: viele gelabelte Tickets, viele ungelabelte Tickets oder fast keine Daten. Jeder Weg endet in einem konkreten Service-Paket mit klaren Liefergegenständen und KPIs, sodass Sie ohne Rätselraten von der Idee → Pilot → Produktion gelangen.

**Für wen ist das:** IT-/Service-Teams auf Znuny/OTRS/OTOBO (oder ähnlich), die zuverlässige Queue-/Prioritäts-/Tag-Vorhersagen wünschen, entweder On-Prem oder über eine gehostete API.

**Was Sie erhalten:** kurzer Entscheidungsfluss, 4 umsetzbare Wege (A–D), Add-ons (mehrsprachig, zusätzliche Attribute), Gates/Metriken, um zu wissen, wann Sie bereit sind, und eine Checkliste zur Datenbereitschaft.

**So verwenden Sie diese Seite**

- Beginnen Sie mit der Ein-Bildschirm-Übersicht und beantworten Sie drei Fragen: **Gelabelt? → Ungelabelt? → Schnell?**
- Klicken Sie auf das Feld für **Flow A/B/C/D**, um zu seinen Schritten, Liefergegenständen und KPIs zu springen.
- Verwenden Sie die **Add-ons**, wenn Sie mehrere Sprachen oder mehr Ausgaben (Tags, Bearbeiter, erste Antwort) benötigen.
- Halten Sie die **Gates** streng (F1 pro Klasse + geschäftliche KPIs), damit Piloten in Produktionsvertrauen münden.

Fahren Sie nun mit dem Übersichtsdiagramm und den detaillierten Flows unten fort.
Gut – hier ist eine ausführlichere Beschreibung, die Sie unter Ihre Diagramme einfügen können. Ich habe sie überfliegbar gehalten, aber echte Anleitung und Schwellenwerte hinzugefügt, damit Leser sicher einen Flow wählen können.

Verstanden – ich behalte Ihre neuen kurzen Diagramme bei und füge jedem Abschnitt klaren, prägnanten Erklärungstext hinzu, damit der Artikel vollständig wirkt, während er dennoch leicht zu überfliegen ist.

---

## 0) Ein-Bildschirm-Übersicht

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
Beginnen Sie oben, beantworten Sie die Fragen und folgen Sie dem Zweig zu Ihrem passenden Flow. Klicken Sie auf einen Flow, um seine Details zu sehen.

---

## <a id="flow-a-many-labeled"></a> Flow A — Viele gelabelte Tickets

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

**Wann Sie diesen wählen sollten:**

- Sie haben bereits **Tausende von Tickets mit Queue-, Prioritäts- oder Tag-Labels**.
- Sie möchten ein **maßgeschneidert trainiertes** Modell für maximale Genauigkeit.

**Was in diesem Flow passiert:**

1. **Audit/Tax** — Label-Qualität, Klassenbalance und Namensgebung prüfen.
2. **Train** — Das Klassifikationsmodell mit Ihren Daten feinabstimmen.
3. **Eval** — Precision/Recall/F1 pro Klasse messen.
4. **On-Prem** — Innerhalb Ihrer eigenen Infrastruktur bereitstellen.
5. **Pilot** — In der Produktion mit Monitoring testen.
6. **Support** — Bei Bedarf iterieren und neu trainieren.

**Empfohlenes Paket:** Fine-Tune + On-Prem Install.

---

## <a id="flow-b-many-unlabeled"></a> Flow B — Viele ungelabelte Tickets

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

**Wann Sie diesen wählen sollten:**

- Sie haben **große historische Ticket-Archive**, aber keine Labels.
- Sie können etwas menschliche Prüfzeit für Qualitätskontrollen einplanen.

**Was in diesem Flow passiert:**

1. **Ingest** — Tickets aus Ihrem System sammeln.
2. **Auto-Label** — LLM-unterstützte automatische Labeling verwenden.
3. **QC** — Stichproben prüfen & korrigieren.
4. **OK?** — Schleife, bis die Qualität den Schwellenwert erreicht.
5. **Train** — Mit dem kuratierten Set feinabstimmen.
6. **Eval / On-Prem / Support** — Wie in Flow A.

**Empfohlenes Paket:** Auto-Label + Fine-Tune.

---

## <a id="flow-c-few-or-no-tickets"></a> Flow C — Wenige oder keine Tickets

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

**Wann Sie diesen wählen sollten:**

- Sie starten **von Grund auf** oder haben zu wenige Tickets zum Trainieren.
- Sie möchten eine **Cold-Start**-Lösung, um schnell live zu gehen.

**Was in diesem Flow passiert:**

1. **Define Tax** — Queues, Prioritäten, Ton festlegen.
2. **Synth Data** — Realistische Tickets generieren (DE/EN).
3. **Baseline** — Erstes Modell auf synthetischen Daten trainieren.
4. **Eval** — Leistung vor dem Rollout prüfen.
5. **Pilot** — Wählen Sie Hosted API für Geschwindigkeit oder On-Prem für Kontrolle.
6. **Collect** — Echte Tickets während des Piloten sammeln.
7. **Fine-Tune** — Reale + synthetische Daten zusammenführen.
8. **Prod/Support** — Live gehen mit fortlaufender Iteration.

**Empfohlenes Paket:** Synthetic Cold-Start.

---

## <a id="flow-d-quick-start-hosted-api"></a> Flow D — Schnellstart über Hosted API

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

**Wann Sie diesen wählen sollten:**

- Sie brauchen **sofort Ergebnisse**.
- Sie möchten Automatisierung ausprobieren, ohne zuerst zu trainieren.

**Was in diesem Flow passiert:**

1. **Use API DE** — Sofortige Klassifikation über gehostetes deutsches Modell.
2. **Measure** — Routing, SLA, Backlog-Auswirkung verfolgen.
3. **Tax OK?** — Wenn zufrieden, Nutzung skalieren; wenn nicht, zu Flow B oder C für Training gehen.

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

Fügen Sie Unterstützung für zusätzliche Sprachen über mehrsprachiges automatisches Labeling oder synthetische Generierung hinzu, dann trainieren und evaluieren Sie pro Sprache.

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

Vorhersagen über Queues/Prioritäten hinaus – z.B. Tags, Bearbeiter oder First Answer Time – durch Erweiterung des Labelings und Training eines Multi-Task-Modells.
