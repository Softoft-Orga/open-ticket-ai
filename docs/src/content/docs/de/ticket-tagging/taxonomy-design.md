---
title: Taxonomie-Design
description: 'Entwerfen und strukturieren Sie Ihre Ticketklassifizierungs‑Taxonomie für effektives automatisiertes Tagging und Kategorisierung.'
lang: en
nav:
  group: Ticket Tagging
  order: 1
---

# Taxonomie-Design

Erfahren Sie, wie Sie eine effektive Taxonomie für die automatisierte Ticket‑Kennzeichnung und -Klassifizierung entwerfen.

## Überblick

Eine gut gestaltete Taxonomie ist die Grundlage für erfolgreiches automatisiertes Ticket‑Tagging. Ihre Taxonomie sollte die Struktur, Prozesse und Anforderungen Ihrer Organisation an die Ticket‑Bearbeitung widerspiegeln.

## Prinzipien der Taxonomie

### Einfach halten

- **Erste Einführung**: 5‑10 Hauptkategorien
- **Reifes System**: maximal 15‑25 Kategorien
- **Zu viele Kategorien**: Reduziert die Klassifizierungsgenauigkeit

### Deutlich machen

- Vermeiden Sie überlappende Definitionen
- Verwenden Sie klare, beschreibende Namen
- Definieren Sie einen expliziten Umfang für jede Kategorie
- Dokumentieren Sie Randfälle und Grenzbedingungen

### An Geschäftsprozesse anpassen

- Spiegeln Sie bestehende Teamstrukturen wider
- Ordnen Sie Support‑Queues oder Abteilungen zu
- Berücksichtigen Sie SLA‑Anforderungen
- Berücksichtigen Sie Eskalationspfade

## Taxonomie‑Struktur

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
- Einfach zu verstehen und zu warten

**Nachteile**:

- Komplexer zu implementieren
- Erfordert sorgfältige Vorbereitung der Trainingsdaten
- Kann mehrstufige Klassifizierung erfordern

### Flache Taxonomie

Kategorien auf einer Ebene:

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
- Einfacher Modelle zu trainieren
- Schnellere Klassifizierung

**Nachteile**:

- Begrenzte Granularität
- Kann bei vielen Kategorien unhandlich werden

## Kategorien definieren

### Vorlage für Kategoriedefinition

Für jede Kategorie dokumentieren Sie:

```markdown
## Category Name: [Name]

**Description**: [Brief description of what belongs in this category]

**Scope**: [What is included]

**Examples**:

- Example ticket 1
- Example ticket 2
- Example ticket 3

**Exclusions**: [What is NOT included]

**Keywords**: [Common terms associated with this category]

**Priority**: [Typical priority level]

**Target Queue/Team**: [Where these tickets should be routed]
```

### Beispiel für Kategoriedefinition

```markdown
## Category Name: Password Reset

**Description**: Requests to reset forgotten passwords or unlock locked accounts

**Scope**:

- Forgotten password requests
- Account lockouts due to failed login attempts
- Password expiration issues

**Examples**:

- "I forgot my password and can't log in"
- "My account is locked after too many failed attempts"
- "I need to reset my password for the customer portal"

**Exclusions**:

- New account creation (→ Account Management)
- Permission/access level changes (→ Access Requests)
- Password policy questions (→ General IT Support)

**Keywords**: password, reset, locked, unlock, forgot, login, access

**Priority**: Medium (affects productivity)

**Target Queue/Team**: IT Help Desk
```

## Testen Ihrer Taxonomie

### Manueller Klassifikationstest

Testen Sie Ihre Taxonomie manuell, bevor Sie automatisieren:

1. **Stichprobenauswahl**: Wählen Sie 100‑200 aktuelle Tickets aus
2. **Mehrere Prüfer**: Lassen Sie 2‑3 Personen dieselben Tickets klassifizieren
3. **Übereinstimmung messen**: Berechnen Sie die Übereinstimmung zwischen Bewertern
4. **Ziel‑Übereinstimmung**: Streben Sie >80 % Übereinstimmung zwischen den Prüfern an

### Häufige Probleme

**Niedrige Übereinstimmung** (<60 %):

- Kategorien können zu stark überlappen
- Definitionen können unklar sein
- Bessere Beispiele und Dokumentation erforderlich

**Mittlere Übereinstimmung** (60‑80 %):

- Einige Randfälle benötigen Klarstellung
- Möglicherweise müssen ähnliche Kategorien zusammengeführt werden
- Verfeinerung der Kategoriegrenzen erforderlich

**Hohe Übereinstimmung** (>80 %):

- Taxonomie ist bereit für die Automatisierung
- Fahren Sie mit dem Model‑Training fort

## Iteration und Verfeinerung

### Klein anfangen

Beginnen Sie mit Kernkategorien:

```
Phase 1 (Week 1-2):
- 5-7 most common ticket types
- Cover 60-70% of ticket volume

Phase 2 (Week 3-4):
- Add 5-7 more categories
- Target 80-90% coverage

Phase 3 (Month 2+):
- Fine-tune and add edge cases
- Achieve >90% coverage
```

### Überwachen und Anpassen

Nach dem Rollout kontinuierlich überwachen:

- **Klassifizierungsgenauigkeit**: Nach Kategorie
- **Vertrauenswerte**: Unsichere Klassifizierungen identifizieren
- **Fehlklassifizierungen**: Muster suchen
- **Neue Ticket‑Typen**: Lücken in der Taxonomie identifizieren

### Wann Kategorien aufteilen

Berücksichtigen Sie das Aufteilen, wenn:

- Kategorie >20 % aller Tickets ausmacht
- Klare Unterkategorien vorhanden sind
- Unterschiedliche Bearbeitungsprozesse erforderlich sind
- SLA‑Anforderungen unterschiedlich sind

### Wann Kategorien zusammenführen

Berücksichtigen Sie das Zusammenführen, wenn:

- Kategorie <2 % der Tickets hat
- Kategorien häufig verwechselt werden
- Ähnliche Bearbeitungsprozesse
- Dasselbe Team beide bearbeitet

## Best Practices

### DO ✅

- Beginnen Sie mit geschäftsgetriebenen Kategorien
- Dokumentieren Sie jede Kategorie klar
- Testen Sie manuell, bevor Sie automatisieren
- Iterieren Sie basierend auf Feedback
- Leistung kontinuierlich überwachen

### DON'T ❌

- Erstellen Sie anfangs nicht zu viele Kategorien
- Verwenden Sie vage oder überlappende Definitionen
- Überspringen Sie die manuelle Validierung nicht
- Setzen und vergessen – Taxonomien entwickeln sich weiter
- Ignorieren Sie Vorhersagen mit geringem Vertrauen nicht

## Werkzeuge und Ressourcen

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
- **Vierteljährlich**: Große Taxonomie‑Überprüfung
- **Jährlich**: Vollständige Neugestaltung der Taxonomie in Betracht ziehen

## Nächste Schritte

Nach der Gestaltung Ihrer Taxonomie:

1. **Trainingsdaten vorbereiten**: Historische Tickets sammeln und kennzeichnen
2. **Model konfigurieren**: Klassifizierungs‑Model mit Ihren Kategorien einrichten
3. **Klassifizierung testen**: Auf Hold‑out‑Daten validieren
4. **Leistung überwachen**: Genauigkeit verfolgen und bei Bedarf anpassen

## Verwandte Dokumentation

- [Tag Mapping](tag-mapping.md) - Klassifikationen zu Ticket‑Feldern zuordnen
- [Using Model](using-model.md) - Klassifizierungs‑Modelle konfigurieren und nutzen
- [Hardware Sizing](hardware-sizing.md) - Infrastruktur‑Anforderungen für die Klassifizierung