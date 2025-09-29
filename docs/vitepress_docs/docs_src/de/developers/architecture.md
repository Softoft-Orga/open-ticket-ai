---
description: Erfahren Sie mehr über die Architektur von Open Ticket AI. Entdecken Sie, wie die modulare Datenpipeline und die Hugging Face-Modelle eine intelligente Ticket-Klassifizierung und -Weiterleitung ermöglichen.
layout: page
pageClass: full-page
title: Architekturübersicht von Open Ticket AI
---
# Architekturübersicht

Open Ticket AI basiert auf einer modularen Ausführungs-Engine, die Support-Tickets über konfigurierbare Pipelines verarbeitet. Jede Pipeline kombiniert wiederverwendbare „Pipes“, die Daten abrufen, Hugging-Face-Modelle ausführen und Ergebnisse zurück in externe Systeme schreiben.

## Systemüberblick

- **Self-Hosted-Kern**: Läuft als Python-Dienst, lädt die Konfiguration, registriert Services und überwacht die Pipeline-Ausführung.
- **Dependency Injection**: Adapter, Modelle und Hilfsfunktionen werden von einem Inversion-of-Control-Container bereitgestellt, sodass Pipes nur das anfordern, was sie benötigen.
- **Komponierbare Pipelines**: YAML-Konfigurationen beschreiben, welche Pipes in welcher Reihenfolge laufen und welche `when`-Bedingungen gelten.
- **Gemeinsamer Ausführungskontext**: Zwischenergebnisse werden in einem Kontextobjekt gespeichert, damit spätere Schritte auf vorherige Ergebnisse zugreifen können, ohne Arbeit zu duplizieren.

## Zentrale Bausteine

### Pipeline-Orchestrator
Der Orchestrator lädt die aktive Pipeline-Konfiguration, rendert Jinja2-Templates und instanziiert jede Pipe just-in-time. Er beachtet `when`-Bedingungen, iteriert über die Schritte und schreibt den Pipe-Zustand zurück in den gemeinsamen Kontext.

### Pipes
Pipes kapseln eine Arbeitseinheit – etwa Ticketabruf, Textklassifikation, Metadaten-Aktualisierung oder Telemetrie. Sie sind zwischen den Läufen zustandslos; jede Ausführung erhält frische Eingaben vom Orchestrator und legt ihre Ergebnisse für nachgelagerte Schritte im Kontext ab.

### Services
Wiederverwendbare Fähigkeiten (HTTP-Clients, Hugging-Face-Pipelines, Speicher-Backends) leben im Service-Container. Pipes fordern Services über `get_instance` an, wodurch Infrastrukturlogik zentralisiert und leicht austauschbar bleibt.

### Ticket-System-Adapter
Adapter übersetzen zwischen Open Ticket AI und externen Helpdesk-Plattformen. Fetcher-Pipes nutzen einen Adapter, um Tickets zu laden, und Updater-Pipes verwenden denselben Adapter, um Queue-, Prioritäts- oder Kommentaränderungen zurück in das entfernte System zu schreiben.

### Machine-Learning-Modelle
Vorhersagen für Queue und Priorität stammen aus Hugging-Face-Modellen, die in eigenen Pipes laufen. Diese Pipes befüllen Eingaben aus dem Kontext, führen das Modell aus und ergänzen den Kontext mit strukturierten Vorhersagen für nachfolgende Schritte.

## End-to-End-Verarbeitungsfluss

1. Der Orchestrator initialisiert Services und Ausführungskontext und wählt die konfigurierte Pipeline.
2. Eine Fetch-Pipe verwendet einen Ticket-System-Adapter, um relevante Tickets abzurufen und im Kontext abzulegen.
3. Preprocessing-Pipes bereiten den Tickettext für die Modellausführung auf.
4. Klassifikations-Pipes führen Hugging-Face-Modelle aus, um Queue-, Prioritäts- oder Tag-Vorhersagen zu erzeugen.
5. Postprocessing-Pipes konsolidieren die Vorhersagen, wenden Geschäftsregeln an und bereiten Update-Payloads vor.
6. Update-Pipes rufen den Adapter erneut auf, um Ergebnisse (Queue-Wechsel, Prioritätsanpassungen, interne Notizen) auf das ursprüngliche Ticket zu schreiben.

## Erweiterungsmöglichkeiten

- **Neuen Adapter hinzufügen**: Implementieren Sie die Adapter-Schnittstelle für eine weitere Ticketplattform und registrieren Sie sie im Service-Container.
- **Pipelines anpassen**: Stellen Sie neue Pipe-Kombinationen in YAML zusammen und steuern Sie optionale Schritte mit `when`-Bedingungen.
- **Neue Intelligenz einbringen**: Ergänzen Sie zusätzliche Modell-Pipes oder regelbasierte Prozessoren, die den gemeinsamen Kontext lesen und schreiben.

Diese Architektur entkoppelt die Klassifikationslogik von den Integrationen und ermöglicht es Teams, den Pipeline-Ablauf an ihre Workflows anzupassen, ohne das Kernlaufzeitsystem ändern zu müssen.
