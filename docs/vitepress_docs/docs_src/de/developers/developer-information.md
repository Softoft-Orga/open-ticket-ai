---
description: Entwickler-Leitfaden für den On-Premise ATC Ticket-Klassifikator. Lernen
  Sie, wie Sie mit YAML konfigurieren, über die CLI ausführen und mit benutzerdefinierten
  Python-Komponenten & Adaptern erweitern.
title: Entwicklerinformationen
---
# Entwicklerinformationen für die ATC Community Edition

## Überblick

Die ATC Community Edition ist eine On-Premise-Lösung zur automatisierten Klassifizierung von Support-Tickets. Die aktuelle MVP-Version wird über eine YAML-Konfigurationsdatei gesteuert und per CLI gestartet. Es gibt keine REST API zum Hochladen von Trainingsdaten oder zum Auslösen eines Trainingslaufs.

## Softwarearchitektur

Die Anwendung besteht im Wesentlichen aus den folgenden Paketen:

* **core** – Konfigurationsmodelle, Dependency-Injection-Hilfen, Pipeline-Engine und Template-Rendering.
* **base** – Wiederverwendbare Pipe-Implementierungen (z. B. Ticket-Fetch/Update und Composite-Hilfen).
* **hf_local** – Beispielhafte HuggingFace-Inferenz-Pipes.
* **ticket\_system\_integration** – Adapter für verschiedene Ticketsysteme.
* **main.py** – CLI-Einstiegspunkt, der Injector, Scheduler und Orchestrator verbindet.

Der Orchestrator verarbeitet jetzt YAML-definierte `Pipe`-Graphen. Definitionen werden aus wiederverwendbaren `defs` zusammengesetzt, mit dem aktuellen Kontext gerendert und zur Laufzeit über den Dependency-Injection-Container aufgelöst. Jeder Zeitplaneintrag legt fest, welcher Pipe-Baum ausgeführt wird und in welchem Intervall der Orchestrator ihn startet.

Ein Beispielbefehl zum Starten der Anwendung:

```bash
python -m open_ticket_ai.src.ce.main start
```

## Pipeline-Architektur

Die Laufzeit-Pipeline wird in YAML beschrieben. `RawOpenTicketAIConfig` bündelt Plug-ins, globale Konfiguration, wiederverwendbare `defs` und den `orchestrator`-Zeitplan, der vorgibt, welche Pipes in welchem Intervall laufen. Beim Start lädt der Dependency-Injection-Container diese Datei, erstellt Singleton-Services aus den `defs` und registriert sie im `UnifiedRegistry`. Pipes und Templates können diese Dienste anschließend per ID referenzieren.

Jeder Pipeline-Eintrag wird in ein `RegisterableConfig` mit einer `id`, der Zielklasse in `use`, optionalen verschachtelten `steps` sowie Orchestrierungs-Metadaten wie `_if` und `depends_on` normalisiert. Zur Laufzeit wird die Konfiguration gegen den aktuellen `Context` gerendert, sodass Jinja2-Ausdrücke über Hilfsfunktionen wie `get_pipe_result('classify', 'label')` auf vorherige Ergebnisse zugreifen können. `if:`-Ausdrücke schalten Pipes pro Durchlauf an oder aus und `depends_on` stellt sicher, dass eine Pipe erst ausgeführt wird, wenn alle abhängigen Schritte erfolgreich waren.

Der `Context` enthält zwei Dictionaries: `pipes` speichert für jeden Schritt das `PipeResult` (success/failed/message/data) und `config` stellt die gerenderte Konfiguration für den aktiven Zeitplaneintrag bereit. Pipes lesen aus diesem Kontext, führen ihre Arbeit in der asynchronen `_process()`-Methode aus und geben Daten zurück, die als `PipeResult.data` abgelegt werden. So können nachfolgende Pipes und Templates Fehler erkennen oder Ergebnisse wiederverwenden.

Das Feld `orchestrator` in der YAML ist eine Liste von Zeitplaneinträgen. Jeder Eintrag enthält `run_every_milli_seconds` und eine `pipe`-Definition, die selbst eine Composite-Pipe mit verschachtelten `steps` sein kann. Der Scheduler läuft diese Liste durch, löst Durchläufe nach Ablauf der Intervalle aus und übergibt dem Orchestrator einen frischen `Context`, der mit der Zeitplan-Konfiguration vorbelegt ist.

## Training benutzerdefinierter Modelle

Ein direktes Training über die Anwendung ist im MVP nicht vorgesehen. Vor-trainierte Modelle können in der Konfiguration spezifiziert und verwendet werden. Wenn ein Modell angepasst oder neu erstellt werden muss, muss dies außerhalb der Anwendung geschehen.

## Erweiterung

Benutzerdefinierte Fetcher, Preparer, KI-Dienste oder Modifier können als Python-Klassen implementiert und über die Konfiguration registriert werden. Dank Dependency Injection können neue Komponenten einfach integriert werden.

## Wie man eine benutzerdefinierte Pipe hinzufügt

Die Verarbeitungs-Pipeline lässt sich mit eigenen Pipe-Klassen erweitern. Eine Pipe ist eine Arbeitseinheit, die einen `Context` nutzt, zuvor gespeicherte `PipeResult`-Objekte auswertet und ein neues `PipeResult` mit aktuellen Daten und Statusinformationen zurückliefert.

1. **Definieren Sie optional ein Konfigurationsmodell** für die Parameter Ihrer Pipe.
2. **Leiten Sie von `Pipe` ab** und implementieren Sie die asynchrone Methode `_process()`.
3. **Geben Sie ein Dictionary** im `PipeResult`-Format zurück (oder verwenden Sie `PipeResult(...).model_dump()`).

Das folgende vereinfachte Beispiel zeigt eine lokale Sentiment-Analyse-Pipe mit HuggingFace:

```python
from typing import Any

from pydantic import BaseModel
from transformers import pipeline

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.pipeline.pipe_config import PipeResult


class SentimentPipeConfig(BaseModel):
    model_name: str = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    text: str


class SentimentAnalysisPipe(Pipe):
    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.cfg = SentimentPipeConfig(**config)
        self.classifier = pipeline("sentiment-analysis", model=self.cfg.model_name)

    async def _process(self) -> dict[str, Any]:
        if not self.cfg.text:
            return PipeResult(success=False, failed=True, message="Kein Text vorhanden", data={}).model_dump()

        sentiment = self.classifier(self.cfg.text)[0]
        return PipeResult(
            success=True,
            failed=False,
            data={
                "label": sentiment["label"],
                "confidence": sentiment["score"],
            },
        ).model_dump()
```

Registrieren Sie die neue Klasse anschließend unter `open_ticket_ai.defs` (oder in `general_config.pipe_classes`), damit die YAML-Pipeline sie über ihre `id` referenzieren kann. Da der Orchestrator die Konfiguration per Jinja2 rendert, lassen sich in den Definitionen auch Umgebungsvariablen oder Ergebnisse vorheriger Pipes einbinden.

## Wie man ein neues Ticketsystem integriert

Um ein anderes Helpdesk-System anzubinden, implementieren Sie einen neuen Adapter, der von `TicketSystemAdapter` erbt. Der Adapter konvertiert zwischen der externen API und den einheitlichen Modellen des Projekts.

1. **Erstellen Sie eine Adapter-Klasse**, z.B. `FreshdeskAdapter(TicketSystemAdapter)`.
2. **Implementieren Sie alle abstrakten Methoden**:
    - `find_tickets`
    - `find_first_ticket`
    - `create_ticket`
    - `update_ticket`
    - `add_note`
3. **Übersetzen Sie Daten** in die und aus den `UnifiedTicket`- und `UnifiedNote`-Modellen.
4. **Stellen Sie ein Konfigurationsmodell** für Anmeldeinformationen oder API-Einstellungen bereit.
5. **Registrieren Sie den Adapter** in `create_registry.py`, damit er aus der YAML-Konfiguration instanziiert werden kann.

Nach der Registrierung geben Sie den Adapter im `system`-Abschnitt der `config.yml` an, und der Orchestrator wird ihn zur Kommunikation mit dem Ticketsystem verwenden.

## Zusammenfassung

Die ATC Community Edition bietet in ihrer MVP-Version einen lokal ausgeführten Workflow zur automatischen Ticket-Klassifizierung. Alle Einstellungen werden über YAML-Dateien verwaltet; es ist keine REST API verfügbar. Für das Training müssen externe Prozesse oder Skripte verwendet werden.