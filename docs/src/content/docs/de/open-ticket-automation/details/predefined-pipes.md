---
title: Vordefinierte Pipe-Konzepte
draft: true
lang: de
nav:
  group: Details
  order: 3
---

# Vordefinierte Pipe-Konzepte

:::caution Exploratives Design
Diese Seite dokumentiert ein exploratives Design für vordefinierte Pipes. Die Funktion ist noch nicht in Produktionsreleases verfügbar und die hier beschriebenen Konzepte können sich durch die Validierung des Ansatzes mit internen Prototypen erheblich ändern.
:::

Dieses Dokument erfasst frühe Ideen für die Bereitstellung wiederverwendbarer, vordefinierter Pipes, die in projektbezogene YAML-Pipelines importiert werden können.

## Aktueller Status

Vordefinierte Pipes befinden sich in der Entdeckungsphase, es wurden bisher nur YAML-Prototypen für interne Reviews erstellt. Es gibt keine Laufzeitunterstützung in der Engine und der Katalog wurde noch nicht veröffentlicht. Das Engineering-Team validiert die Import-Mechanik, die Abhängigkeitsverwaltung und die Paketierungsabläufe, bevor ein Implementierungszeitplan festgelegt wird. Der unmittelbare Fokus liegt auf der Bereitstellung des Loaders, der Kompatibilitätstests und der unten beschriebenen Entwickler-Tools, gefolgt von iterativen Pilotprogrammen mit einer kleinen Gruppe von Design-Partnern.

## Ziele

- Bereitstellung eines Katalogs mit teilbaren Automatisierungsmustern für Support-Workflows.
- Ermöglichung für Teams, komplexe Automatisierungen durch den Import einer einzigen Datei zusammenzusetzen.
- Gewährleistung der Kompatibilität der vordefinierten Pipes mit der bestehenden Ausführungs-Engine, sodass ein importiertes YAML ohne zusätzliche Verkabelung lauffähig ist.

## Design-Prinzipien

1.  **Einzeldatei-Portabilität** – Jede vordefinierte Pipe lebt in ihrer eigenen YAML-Datei mit allen erforderlichen Schritten und Metadaten. Der Import der Datei sollte die Pipe sofort lauffähig machen.
2.  **Deklarative Parameter** – Pipes stellen einen `parameters`-Block bereit, in dem nachgelagerte YAMLs Standardwerte überschreiben können, ohne die gemeinsame Datei zu bearbeiten.
3.  **Idempotente Schritte** – Jede Pipe sollte sicher mehrfach ausgeführt werden können.
4.  **Observability-Hooks** – Standard-Annotationen für Logging, Metriken und Alerting, damit importierte Pipes sauber in die Überwachung integriert werden können.

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

Das YAML auf Team-Ebene verweist einfach auf die vordefinierte Pipe und überschreibt optional Parameter:

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

## Katalog-Ideen

| Pipe Name                    | Gelöstes Problem                                         | Wichtige Schritte                                                           | Anmerkungen                                 |
| ---------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- |
| `triage-basic`               | Klassifizierung und Einreihung neuer Tickets             | Normalisierung → Klassifizierung → SLA-Erinnerung                           | Basis für alle Teams                        |
| `triage-advanced`            | Mehrsprachige Klassifizierung mit Übersetzungs-Fallback  | Spracherkennung → Übersetzung → Klassifizierung → Routing                   | Erfordert Übersetzungs-Guthaben             |
| `auto-escalate`              | Eskalation dringender Tickets                            | Schweregrad-Erkennung → Benachrichtigung Senior Engineer → Incident-Logging | Integriert mit Bereitschaftsplänen          |
| `knowledge-base-suggest`     | Vorschlag von KB-Artikeln für Agents                     | Vektoreinbettung → Ähnlichkeitssuche → Vorschlagspost                       | Verbraucht Search-API-Quota                 |
| `customer-sentiment-monitor` | Verfolgung von Sentiment-Drift über Gesprächslebensdauer | Konversationsaggregation → Sentiment-Bewertung → Trend-Alerting             | Funktioniert am besten mit stündlichem Cron |
| `bug-report-digest`          | Aggregation von Bug-bezogenen Tickets                    | Label-Filter → Deduplizierung → wöchentlicher Digest-Email                  | Verknüpft mit Product Board                 |

## Validierungs-Checkliste

Vor der Veröffentlichung einer vordefinierten Pipe:

- [ ] Schema mit `python -m open_ticket.pipeline validate pipes/<pipe-name>.yaml` verifizieren.
- [ ] Integrationstests mit Staging-Daten durchführen.
- [ ] Erforderliche Secrets, externe Dienste und Quotas dokumentieren.
- [ ] Die Pipe-Version im Katalog-Repository taggen.

## Nächste Schritte

1.  Einen leichtgewichtigen Loader entwickeln, der importierte Parameter in den aktiven Pipeline-Kontext einfügt und Abhängigkeiten validiert.
2.  Automatisierte Smoke- und Contract-Tests erstellen, um sicherzustellen, dass importierte Pipes über Version-Updates hinweg kompatibel bleiben.
3.  Einen CLI-Befehl `ot pipe add triage-basic` prototypisieren, der das YAML abruft und verifiziert, bevor es einem Projekt-Repository hinzugefügt wird.
4.  Die Hosting-Optionen für den Katalog in einem Git-basierten Registry evaluieren, um eine versionierte Verteilung und kontrollierten Pilotzugang zu ermöglichen.
