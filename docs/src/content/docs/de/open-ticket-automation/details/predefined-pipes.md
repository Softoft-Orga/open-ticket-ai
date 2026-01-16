---
title: Vordefinierte Pipe-Konzepte
draft: true
lang: de
nav:
  group: Details
  order: 3
---

# Vordefinierte Pipe-Konzepte

:::caution Exploratorisches Design
Diese Seite dokumentiert ein exploratorisches Design für vordefinierte Pipes. Die Funktion ist in Produktionsreleases noch nicht verfügbar und die hier beschriebenen Konzepte können sich durch die Validierung des Ansatzes mit internen Prototypen erheblich ändern.
:::

Dieses Dokument erfasst frühe Ideen für die Bereitstellung wiederverwendbarer, vordefinierter Pipes, die in projektbezogene YAML-Pipelines importiert werden können.

## Aktueller Status

Vordefinierte Pipes befinden sich in der Entdeckungsphase, es wurden nur YAML-Prototypen für die interne Überprüfung erstellt. Es gibt keine Laufzeitunterstützung in der Engine, und der Katalog wurde nicht veröffentlicht. Die technische Entwicklung validiert die Importmechanik, die Abhängigkeitsbehandlung und die Verpackungsabläufe, bevor ein Implementierungszeitplan festgelegt wird. Der unmittelbare Fokus liegt auf der Bereitstellung des Loaders, der Kompatibilitätstests und der Entwicklertools, die unten aufgeführt sind, gefolgt von iterativen Pilotprogrammen mit einer kleinen Gruppe von Designpartnern.

## Ziele

- Bereitstellung eines Katalogs mit teilbaren Automatisierungsmustern für Support-Workflows.
- Ermöglichen, dass Teams komplexe Automatisierungen durch Import einer einzelnen Datei zusammenstellen.
- Sicherstellen, dass die vordefinierten Pipes mit der bestehenden Ausführungs-Engine kompatibel bleiben, sodass eine importierte YAML ohne zusätzliche Verkabelung ausgeführt werden kann.

## Designprinzipien

1.  **Einzeldatei-Portabilität** – Jede vordefinierte Pipe lebt in ihrer eigenen YAML-Datei mit allen erforderlichen Schritten und Metadaten. Der Import der Datei sollte die Pipe sofort ausführbar machen.
2.  **Deklarative Parameter** – Pipes stellen einen `parameters`-Block bereit, in dem nachgelagerte YAMLs Standardwerte überschreiben können, ohne die gemeinsame Datei zu bearbeiten.
3.  **Idempotente Schritte** – Jede Pipe sollte sicher mehrfach ausgeführt werden können.
4.  **Observability-Hooks** – Standard-Annotationen für Logging, Metriken und Alerting, damit importierte Pipes sauber in die Überwachung integriert werden.

## YAML-Struktur-Prototyp

```yaml
# file: pipes/triage-basic.yaml
pipe:
  name: triage-basic
  version: 0.1.0
  description: >-
    Basic triage workflow that classifies an incoming ticket, enriches context,
    and queues follow-up actions.

  parameters:
    classification_model: clf-ticket-small
    notification_channel: slack://#support-triage
    sla_minutes: 30

  steps:
    - id: normalize
      uses: actions/normalize-text@v1
      with:
        fields: [title, description]

    - id: classify
      uses: actions/classify@v2
      with:
        model: '${{ parameters.classification_model }}'
        input: ${{ steps.normalize.output.cleaned_text }}

    - id: sla_guard
      uses: actions/sla-reminder@v1
      when: ${{ ticket.created_at + parameters.sla_minutes < now() }}
      with:
        channel: '${{ parameters.notification_channel }}'
        message: 'SLA threshold reached for ticket ${{ ticket.id }}'

  outputs:
    classification: ${{ steps.classify.output.label }}
    confidence: ${{ steps.classify.output.confidence }}
```

### Import-Muster

Die YAML auf Team-Ebene verweist einfach auf die vordefinierte Pipe und überschreibt optional Parameter:

```yaml
imports:
  - from: pipes/triage-basic.yaml
    as: triage-basic

pipe:
  name: support-intake
  steps:
    - uses: triage-basic
      with:
        classification_model: clf-ticket-enterprise
        notification_channel: slack://#support-critical
```

## Katalogideen

| Pipe-Name                    | Gelöstes Problem                                       | Wichtige Schritte                                                           | Anmerkungen                                 |
| ---------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------- |
| `triage-basic`               | Klassifizierung und Einreihen neuer Tickets            | Normalisierung → Klassifizierung → SLA-Erinnerung                           | Basis für alle Teams                        |
| `triage-advanced`            | Mehrsprachige Klassifizierung mit Übersetzungsfallback | Spracherkennung → Übersetzung → Klassifizierung → Routing                   | Erfordert Übersetzungsguthaben              |
| `auto-escalate`              | Eskalation dringender Tickets                          | Schweregrad-Erkennung → Benachrichtigung Senior Engineer → Incident-Logging | Integriert mit Bereitschaftsplänen          |
| `knowledge-base-suggest`     | Vorschlagen von KB-Artikeln für Agents                 | Vektoreinbettung → Ähnlichkeitssuche → Vorschlag posten                     | Verbraucht Search-API-Kontingent            |
| `customer-sentiment-monitor` | Überwachen von Stimmungsänderungen im Gesprächsverlauf | Gesprächsaggregation → Sentiment-Bewertung → Trend-Alerting                 | Funktioniert am besten mit stündlichem Cron |
| `bug-report-digest`          | Aggregieren von fehlerbezogenen Tickets                | Label-Filter → Deduplizieren → wöchentliche Digest-E-Mail                   | Verknüpft mit Product Board                 |

## Validierungs-Checkliste

Vor der Veröffentlichung einer vordefinierten Pipe:

- [ ] Schema mit `python -m open_ticket.pipeline validate pipes/<pipe-name>.yaml` überprüfen.
- [ ] Integrationstests mit Staging-Daten durchführen.
- [ ] Erforderliche Secrets, externe Dienste und Kontingente dokumentieren.
- [ ] Pipe-Release im Katalog-Repository taggen.

## Nächste Schritte

1.  Einen schlanken Loader erstellen, der importierte Parameter in den aktiven Pipeline-Kontext einfügt und Abhängigkeiten validiert.
2.  Automatisierte Smoke- und Vertragstests erstellen, um sicherzustellen, dass importierte Pipes über Versionsänderungen hinweg kompatibel bleiben.
3.  Einen CLI-Befehl `ot pipe add triage-basic` prototypisieren, der die YAML abruft und überprüft, bevor sie einem Projekt-Repository hinzugefügt wird.
4.  Bewerten, ob der Katalog in einem Git-basierten Registry gehostet werden soll, um eine versionsgesteuerte Verteilung und kontrollierten Pilotzugang zu ermöglichen.
