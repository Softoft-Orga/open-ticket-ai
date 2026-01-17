---
title: Predefined Pipe Concepts
draft: true
lang: en
nav:
  group: Details
  order: 3
---

# Vordefinierte Pipe-Konzepte

:::caution Exploratory design
Dieses Dokument dokumentiert ein exploratives Design für vordefinierte Pipes. Die Funktion ist noch nicht in Produktions‑Releases verfügbar und die hier dargestellten Konzepte können sich erheblich ändern, wenn wir den Ansatz mit internen Prototypen validieren.
:::

Dieses Dokument erfasst frühe Ideen für die Bereitstellung wiederverwendbarer, vordefinierter Pipes, die in projektbezogene YAML‑Pipelines importiert werden können.

## Aktueller Stand

Vordefinierte Pipes befinden sich in der Discover‑Phase, wobei nur YAML‑Prototypen für interne Reviews erstellt wurden. Laufzeitunterstützung im Engine fehlt, und der Katalog wurde noch nicht veröffentlicht. Das Engineering validiert die Import‑Mechanik, das Abhängigkeits‑Handling und die Verpackungs‑Flows, bevor ein Implementierungs‑Zeitplan festgelegt wird. Der unmittelbare Fokus liegt darauf, den Loader, Kompatibilitätstests und die unten beschriebenen Entwickler‑Tools bereitzustellen, gefolgt von iterativen Pilotprogrammen mit einer kleinen Gruppe von Design‑Partnern.

## Ziele

- Ein Katalog von teilbaren Automatisierungsmustern für Support‑Workflows bereitstellen.
- Teams ermöglichen, komplexe Automatisierungen zu komponieren, indem sie eine einzelne Datei importieren.
- Die vordefinierten Pipes kompatibel zum bestehenden Ausführungs‑Engine halten, sodass ein importiertes YAML ohne zusätzliche Verkabelung ausgeführt werden kann.

## Gestaltungsprinzipien

1. **Einzeldatei‑Portabilität** – Jede vordefinierte Pipe befindet sich in einer eigenen YAML‑Datei mit allen erforderlichen Schritten und Metadaten. Das Importieren der Datei sollte die Pipe sofort ausführbar machen.
2. **Deklarative Parameter** – Pipes stellen einen `parameters`‑Block bereit, in dem nachgelagerte YAMLs Standardwerte überschreiben können, ohne die geteilte Datei zu bearbeiten.
3. **Idempotente Schritte** – Jede Pipe sollte sicher mehrfach ausführbar sein.
4. **Observability‑Hooks** – Standard‑Annotationen für Logging, Metriken und Alarmierung, damit importierte Pipes sauber in das Monitoring integriert werden.

## YAML‑Struktur‑Prototyp

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

### Import‑Muster

Das teambezogene YAML verweist einfach auf die vordefinierte Pipe und überschreibt optional Parameter:

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

## Katalog‑Ideen

| Pipe-Name                    | Gelöstes Problem                                          | Wichtige Schritte                                                            | Hinweise                             |
| ---------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------- |
| `triage-basic`               | Klassifizieren und neue Tickets einreihen                        | Normalisierung → Klassifizierung → SLA‑Erinnerung                        | Basis für alle Teams            |
| `triage-advanced`            | Mehrsprachige Klassifizierung mit Übersetzungs‑Fallback | Spracherkennung → Übersetzung → Klassifizierung → Routing          | Benötigt Übersetzungsguthaben      |
| `auto-escalate`              | Dringende Tickets eskalieren                                 | Schweregrad‑Erkennung → Benachrichtigung Senior‑Engineer → Vorfalls‑Logging | Integriert sich in Bereitschaftspläne |
| `knowledge-base-suggest`     | KB‑Artikel für Agenten vorschlagen                           | Vektor‑Einbettung → Ähnlichkeitssuche → Vorschlag‑Post                   | Verbraucht Such‑API‑Kontingent         |
| `customer-sentiment-monitor` | Sentiment‑Drift über die Lebensdauer einer Konversation verfolgen        | Gesprächs‑Aggregation → Sentiment‑Bewertung → Trend‑Alarmierung        | Funktioniert am besten mit stündlichem Cron       |
| `bug-report-digest`          | Bug‑bezogene Tickets aggregieren                           | Label‑Filter → Duplikate entfernen → Wöchentliche Digest‑E‑Mail                     | Verknüpft mit dem Produkt‑Board           |

## Validierungs‑Checkliste

Bevor eine vordefinierte Pipe veröffentlicht wird:

- [ ] Schema mit `python -m open_ticket.pipeline validate pipes/<pipe-name>.yaml` überprüfen.
- [ ] Integrationstests gegen Staging‑Daten ausführen.
- [ ] Erforderliche Secrets, externe Services und Kontingente dokumentieren.
- [ ] Pipe‑Release im Katalog‑Repository taggen.

## Nächste Schritte

1. Einen leichten Loader erstellen, der importierte Parameter in den aktiven Pipeline‑Kontext zusammenführt und Abhängigkeiten validiert.
2. Automatisierte Smoke‑ und Contract‑Tests erstellen, um sicherzustellen, dass importierte Pipes bei Versionssprüngen kompatibel bleiben.
3. Einen CLI‑Befehl `ot pipe add triage-basic` prototypisieren, der das YAML abruft und prüft, bevor es zu einem Projekt‑Repository hinzugefügt wird.
4. Evaluieren, den Katalog in einem Git‑basierten Registry für versionierte Verteilung und kontrollierten Pilot‑Zugang zu hosten.