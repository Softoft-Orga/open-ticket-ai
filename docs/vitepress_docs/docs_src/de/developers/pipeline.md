---
title: Pipeline-Referenz
description: Verstehen Sie die YAML-Struktur, die den Orchestrator, Pipes und wiederverwendbare Definitionen von OpenTicketAI steuert.
---

# Pipeline-Referenz

OpenTicketAI wird vollständig über YAML konfiguriert. Diese Referenz erklärt den Aufbau der Konfiguration, wie Anker und Definitionen
funktionieren und wie der Orchestrator daraus zur Laufzeit `Pipe`-Instanzen und `PipeResult`-Objekte erzeugt.

## Grundaufbau

Alle Einstellungen liegen unter dem Schlüssel `open_ticket_ai`. Das Schema entspricht `RawOpenTicketAIConfig` und gliedert sich in vier
Bereiche:

- **`plugins`** – optionale Python-Module, die vor dem Instanziieren der Pipes importiert werden.
- **`general_config`** – globale Einstellungen wie Logging sowie `pipe_classes` (ein Katalog wiederverwendbarer Pipe-Vorlagen, die über
  YAML-Anker referenziert werden).
- **`defs`** – wiederverwendbare Definitionen (Services, Composite-Pipes, Parametersätze), die mit `<<: *anker` in geplante Pipes
  gemischt werden können.
- **`orchestrator`** – eine Liste von Zeitplaneinträgen. Jeder Eintrag definiert `run_every_milli_seconds` und die `pipe` (häufig eine
  Composite-Definition aus `defs`), die in diesem Intervall ausgeführt werden soll.

```yaml
open_ticket_ai:
  plugins: []
  general_config:
    pipe_classes:
      - &ticket_fetch_pipe
        use: "open_ticket_ai.base:FetchTicketsPipe"
  defs:
    - &default_ticket_fetcher
      <<: *ticket_fetch_pipe
      injects:
        ticket_system: "otobo_znuny"
  orchestrator:
    - run_every_milli_seconds: 10000
      pipe:
        <<: *default_ticket_fetcher
        ticket_search_criteria:
          state.name: "new"
```

## Wiederverwendbare Definitionen & Anker

OpenTicketAI nutzt intensiv YAML-Anker:

- Ein Block wird einmal mit `&name` definiert (z. B. `&ticket_classifier`) und bei Bedarf mit `<<: *ticket_classifier` eingefügt.
- Anker lassen sich kombinieren. Die Elternkonfiguration wird mittels `PipeFactory.resolve_config` mit kindlichen Überschreibungen
  zusammengeführt, daher müssen Kinder nur die Unterschiede angeben.
- Definitionen in `defs` können verschachtelte `steps`, weitere Anker oder injizierte Abhängigkeiten enthalten. Werden sie im
  Orchestrator referenziert, expandieren sie zu einem vollständigen Pipe-Baum.

## Felder einer Pipe-Konfiguration

Jede Pipe (auch verschachtelte Schritte) wird als `RegisterableConfig`/`RenderedPipeConfig` validiert. Wichtige Felder:

- `id` – eindeutiger Bezeichner der Pipe. Wenn nicht gesetzt, wird eine UUID generiert; besser ist eine feste ID, damit Templates das
  Ergebnis via `get_pipe_result('deine_id', 'value')` referenzieren können.
- `use` – Modul- und Klassenpfad (`modul:Klassenname`), der vom `PipeFactory` aufgelöst wird.
- `injects` – Zuordnung von Konstruktorparametern zu IDs aus `defs`. Diese Referenzen werden vor der Instanziierung aufgelöst.
- `steps` – Bei Composite-Pipes eine geordnete Liste von Kind-Pipes, die nacheinander ausgeführt werden.
- `if` – optionale Jinja2-Ausdruck, der zu einem Booleschen Wert gerendert wird. Das Ergebnis landet als `_if` im `RenderedPipeConfig`; ist es `False`, wird die Pipe übersprungen.
- `depends_on` – eine Zeichenkette oder Liste von Pipe-IDs, die erfolgreich (`PipeResult.success == True`) gewesen sein müssen, bevor
  die Pipe läuft.
- Weitere Felder – beliebige Werte, die als Attribute der gerenderten Konfiguration verfügbar sind und von der Pipe genutzt werden.

## Ausführungsmodell

1. Der Orchestrator wählt den nächsten Zeitplaneintrag, dessen `run_every_milli_seconds`-Intervall abgelaufen ist.
2. Die zugehörige `pipe`-Definition wird mit einem frischen `Context` gerendert (`context.config` enthält den Zeitplaneintrag,
   `context.pipes` startet leer).
3. Für jede Pipe bzw. jeden Schritt gilt:
   - Der `_if`-Ausdruck wird geprüft. Ergibt er `False`, wird die Pipe übersprungen.
   - Abhängigkeiten aus `depends_on` werden anhand früherer `PipeResult.success`-Werte kontrolliert.
   - Die `PipeFactory` ermittelt die Klasse aus `use`, injiziert Abhängigkeiten aus `injects` und ruft die asynchrone `process()`-
     Methode der Pipe auf (intern wartet sie auf `_process()`).
   - Der Rückgabewert wird in ein `PipeResult` (`success`, `failed`, `message`, `data`) verpackt und unter `context.pipes[id]` gespeichert.
4. Template-Hilfsfunktionen (`get_pipe_result`, `has_failed` usw.) lesen aus `context.pipes` und stellen Ergebnisse für nachfolgende
   Schritte bereit.
5. Composite-Pipes führen nach Abschluss ihrer Kinder `PipeResult.union` aus, sodass der Composite eine kombinierte Erfolgs-/Fehlerinformation
   und zusammengeführte Daten bereitstellt.

## Arbeiten mit `PipeResult`

Jeder gespeicherte Zustand ist ein `PipeResult` (siehe `open_ticket_ai.core.pipeline.pipe_config`). Beim Implementieren eigener Pipes:

- Entweder ein Dictionary zurückgeben, das `PipeResult.model_validate` verarbeiten kann, oder `PipeResult(...)` instanziieren und
  `.model_dump()` aufrufen.
- Nutzdaten kommen in `data`, damit nachfolgende Schritte sie verwenden können.
- `success`/`failed` und `message` passend setzen, damit Templates Entscheidungen treffen können.

## Hinweise zur Planung

- Zeitplaneinträge in `orchestrator` sind unabhängig; jeder Lauf erhält einen frischen `Context`.
- Mehrere Einträge können dieselbe Composite-Definition verwenden und nur Parameter überschreiben (z. B. Suchkriterien oder Schwellenwerte).
- Intervalle werden in Millisekunden angegeben; `run_every_milli_seconds: 60000` entspricht ungefähr einem Lauf pro Minute.

Mit diesem Aufbau lassen sich komplexe Ticket-Workflows ohne Python-Codeänderungen modellieren – Konfiguration anpassen und der
Orchestrator baut die Pipeline zur Laufzeit neu auf.
