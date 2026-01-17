---
title: Taxonomie-Design
description: 'Entwerfen und strukturieren Sie Ihre Ticket-Klassifizierungstaxonomie für effektive automatische Tagging und Kategorisierung.'
lang: en
nav:
  group: Ticket Tagging
  order: 1
---

# Taxonomie-Design

Erfahren Sie, wie Sie eine effektive Taxonomie für automatisches Ticket-Tagging und -Klassifizierung entwerfen.

## Überblick

Eine gut gestaltete Taxonomie ist die Grundlage für erfolgreiches automatisches Ticket-Tagging. Ihre Taxonomie sollte die Struktur, Prozesse und Ticketbearbeitungsanforderungen Ihrer Organisation widerspiegeln.

## Taxonomie-Prinzipien

### Halten Sie es einfach

Beginnen Sie mit einer überschaubaren Anzahl von Kategorien:

- **Erstes Rollout**: 5-10 Hauptkategorien
- **Ausgereiftes System**: Maximal 15-25 Kategorien
- **Zu viele Kategorien**: Reduziert die Klassifizierungsgenauigkeit

### Machen Sie es eindeutig

Kategorien sollten klar voneinander abgegrenzt sein:

- Vermeiden Sie überlappende Definitionen
- Verwenden Sie klare, beschreibende Namen
- Definieren Sie einen expliziten Geltungsbereich für jede Kategorie
- Dokumentieren Sie Randfälle und Grenzbedingungen

### An Geschäftsprozesse anpassen

Ihre Taxonomie sollte der Arbeitsweise Ihrer Organisation entsprechen:

- Bestehende Teamstrukturen widerspiegeln
- Auf Support-Queues oder Abteilungen abbilden
- SLA-Anforderungen berücksichtigen
- Eskalationspfade einbeziehen

## Taxonomie-Struktur

### Hierarchische Taxonomie

Organisieren Sie Kategorien in einer Baumstruktur:

```
IT Support
├── Hardware
│   ├── Desktop Issues
│   ├── Laptop Issues
│   └── Peripherals
├── Software
│   ├── Application Errors
│   ├── License Requests
│   └── Installation Support
└── Network
    ├── Connectivity Issues
    ├── VPN Access
    └── WiFi Problems
```

**Vorteile**:

- Klare Organisation
- Unterstützt mehrstufige Klassifizierung
- Einfach zu verstehen und zu pflegen

**Nachteile**:

- Komplexer zu implementieren
- Erfordert sorgfältige Vorbereitung der Trainingsdaten
- Kann mehrstufige Klassifizierung erfordern

### Flache Taxonomie

Einzelstufige Kategorien:

```
- Hardware Issues
- Software Errors
- Network Problems
- Access Requests
- Password Resets
- Account Management
- Email Issues
- Printer Support
```

**Vorteile**:

- Einfach zu implementieren
- Einfacher, Modelle zu trainieren
- Schnellere Klassifizierung

**Nachteile**:

- Begrenzte Granularität
- Kann mit vielen Kategorien unhandlich werden

## Kategorien definieren

### Vorlage für Kategoriendefinition

Dokumentieren Sie für jede Kategorie:

```markdown
## Category Name: [Name]

**Description**: [Kurze Beschreibung, was in diese Kategorie gehört]

**Scope**: [Was ist enthalten]

**Examples**:

- Beispiel-Ticket 1
- Beispiel-Ticket 2
- Beispiel-Ticket 3

**Exclusions**: [Was ist NICHT enthalten]

**Keywords**: [Häufige Begriffe, die mit dieser Kategorie verbunden sind]

**Priority**: [Typische Prioritätsstufe]

**Target Queue/Team**: [Wohin diese Tickets weitergeleitet werden sollen]
```

### Beispiel für eine Kategoriendefinition

```markdown
## Category Name: Password Reset

**Description**: Anfragen zum Zurücksetzen vergessener Passwörter oder Entsperren gesperrter Konten

**Scope**:

- Anfragen für vergessene Passwörter
- Kontosperrungen aufgrund fehlgeschlagener Login-Versuche
- Probleme mit abgelaufenen Passwörtern

**Examples**:

- "Ich habe mein Passwort vergessen und kann mich nicht einloggen"
- "Mein Konto ist nach zu vielen fehlgeschlagenen Versuchen gesperrt"
- "Ich muss mein Passwort für das Kundenportal zurücksetzen"

**Exclusions**:

- Erstellung neuer Konten (→ Account Management)
- Änderungen von Berechtigungen/Zugriffsebenen (→ Access Requests)
- Fragen zur Passwortrichtlinie (→ General IT Support)

**Keywords**: password, reset, locked, unlock, forgot, login, access

**Priority**: Medium (beeinträchtigt die Produktivität)

**Target Queue/Team**: IT Help Desk
```

## Ihre Taxonomie testen

### Manueller Klassifizierungstest

Testen Sie Ihre Taxonomie vor der Automatisierung manuell:

1. **Stichprobenauswahl**: Wählen Sie 100-200 aktuelle Tickets aus
2. **Mehrere Prüfer**: Lassen Sie 2-3 Personen dieselben Tickets klassifizieren
3. **Übereinstimmung messen**: Berechnen Sie die Inter-Rater-Übereinstimmung
4. **Zielübereinstimmung**: Streben Sie >80% Übereinstimmung zwischen den Prüfern an

### Häufige Probleme

**Geringe Übereinstimmung** (<60%):

- Kategorien überschneiden sich möglicherweise zu stark
- Definitionen könnten unklar sein
- Bessere Beispiele und Dokumentation erforderlich

**Mittlere Übereinstimmung** (60-80%):

- Einige Randfälle müssen geklärt werden
- Ähnliche Kategorien müssen möglicherweise zusammengeführt werden
- Verfeinerung der Kategoriengrenzen erforderlich

**Hohe Übereinstimmung** (>80%):

- Taxonomie ist bereit für die Automatisierung
- Mit dem Modelltraining fortfahren

## Iteration und Verfeinerung

### Klein anfangen

Beginnen Sie mit Kernkategorien:

```
Phase 1 (Woche 1-2):
- 5-7 häufigste Tickettypen
- 60-70% des Ticketaufkommens abdecken

Phase 2 (Woche 3-4):
- 5-7 weitere Kategorien hinzufügen
- 80-90% Abdeckung anstreben

Phase 3 (Monat 2+):
- Feintuning und Hinzufügen von Randfällen
- >90% Abdeckung erreichen
```

### Überwachen und anpassen

Überwachen Sie nach dem Deployment kontinuierlich:

- **Klassifizierungsgenauigkeit**: Nach Kategorie
- **Konfidenzscores**: Unsichere Klassifizierungen identifizieren
- **Fehlklassifizierungen**: Nach Mustern suchen
- **Neue Tickettypen**: Lücken in der Taxonomie identifizieren

### Wann Kategorien aufgeteilt werden sollten

Erwägen Sie eine Aufteilung, wenn:

- Kategorie >20% aller Tickets ausmacht
- Klare Unterkategorien existieren
- Unterschiedliche Bearbeitungsprozesse erforderlich sind
- SLA-Anforderungen unterschiedlich sind

### Wann Kategorien zusammengeführt werden sollten

Erwägen Sie eine Zusammenführung, wenn:

- Kategorie <2% der Tickets ausmacht
- Kategorien häufig verwechselt werden
- Ähnliche Bearbeitungsprozesse
- Dasselbe Team beide bearbeitet

## Best Practices

### DO ✅

- Mit geschäftsgetriebenen Kategorien beginnen
- Jede Kategorie klar dokumentieren
- Vor der Automatisierung manuell testen
- Basierend auf Feedback iterieren
- Leistung kontinuierlich überwachen

### DON'T ❌

- Anfangs zu viele Kategorien erstellen
- Vage oder überlappende Definitionen verwenden
- Manuelle Validierung überspringen
- Einmal einrichten und vergessen - Taxonomien entwickeln sich weiter
- Niedrige Konfidenzvorhersagen ignorieren

## Tools und Ressourcen

### Dokumentationsvorlage

Verwenden Sie ein gemeinsames Dokument, um Ihre Taxonomie zu definieren:

```
docs/
├── taxonomy/
│   ├── overview.md
│   ├── categories/
│   │   ├── hardware.md
│   │   ├── software.md
│   │   └── ...
│   └── changelog.md
```

### Überprüfungsplan

- **Wöchentlich**: Fehlklassifizierungen überprüfen
- **Monatlich**: Kategorieverteilung analysieren
- **Vierteljährlich**: Hauptüberprüfung der Taxonomie
- **Jährlich**: Erwägung einer vollständigen Taxonomie-Neugestaltung

## Nächste Schritte

Nach dem Entwurf Ihrer Taxonomie:

1. **Trainingsdaten vorbereiten**: Historische Tickets sammeln und labeln
2. **Modell konfigurieren**: Klassifizierungsmodell mit Ihren Kategorien einrichten
3. **Klassifizierung testen**: Mit Hold-out-Daten validieren
4. **Leistung überwachen**: Genauigkeit verfolgen und bei Bedarf anpassen

## Verwandte Dokumentation

- [Tag Mapping](tag-mapping.md) - Klassifizierungen auf Ticket-Felder abbilden
- [Using Model](using-model.md) - Klassifizierungsmodelle konfigurieren und verwenden
- [Hardware Sizing](hardware-sizing.md) - Infrastrukturanforderungen für die Klassifizierung
