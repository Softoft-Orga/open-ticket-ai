---
title: Taxonomie-Design
description: 'Entwerfen und strukturieren Sie Ihre Ticket-Klassifizierungstaxonomie für effektives automatisches Tagging und Kategorisierung.'
lang: de
nav:
  group: Ticket-Tagging
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

- Vermeiden Sie sich überschneidende Definitionen
- Verwenden Sie klare, beschreibende Namen
- Definieren Sie einen expliziten Geltungsbereich für jede Kategorie
- Dokumentieren Sie Grenzfälle und Randbedingungen

### Passen Sie es an Geschäftsprozesse an

Ihre Taxonomie sollte widerspiegeln, wie Ihre Organisation arbeitet:

- Reflektieren Sie bestehende Teamstrukturen
- Ordnen Sie Support-Warteschlangen oder Abteilungen zu
- Berücksichtigen Sie SLA-Anforderungen
- Berücksichtigen Sie Eskalationspfade

## Taxonomie-Struktur

### Hierarchische Taxonomie

Organisieren Sie Kategorien in einer Baumstruktur:

```
IT-Support
├── Hardware
│   ├── Desktop-Probleme
│   ├── Laptop-Probleme
│   └── Peripheriegeräte
├── Software
│   ├── Anwendungsfehler
│   ├── Lizenzanfragen
│   └── Installationssupport
└── Netzwerk
    ├── Verbindungsprobleme
    ├── VPN-Zugang
    └── WLAN-Probleme
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
- Hardware-Probleme
- Software-Fehler
- Netzwerk-Probleme
- Zugriffsanfragen
- Passwort-Zurücksetzungen
- Kontoverwaltung
- E-Mail-Probleme
- Drucker-Support
```

**Vorteile**:

- Einfach zu implementieren
- Einfacher, Modelle zu trainieren
- Schnellere Klassifizierung

**Nachteile**:

- Begrenzte Granularität
- Kann mit vielen Kategorien unhandlich werden

## Kategorien definieren

### Kategoriendefinitions-Vorlage

Dokumentieren Sie für jede Kategorie:

```markdown
## Kategoriename: [Name]

**Beschreibung**: [Kurze Beschreibung, was in diese Kategorie gehört]

**Geltungsbereich**: [Was ist enthalten]

**Beispiele**:

- Beispiel-Ticket 1
- Beispiel-Ticket 2
- Beispiel-Ticket 3

**Ausschlüsse**: [Was ist NICHT enthalten]

**Schlüsselwörter**: [Häufige Begriffe, die mit dieser Kategorie verbunden sind]

**Priorität**: [Typische Prioritätsstufe]

**Ziel-Warteschlange/Team**: [Wohin diese Tickets geroutet werden sollen]
```

### Beispiel-Kategoriendefinition

```markdown
## Kategoriename: Passwort-Zurücksetzung

**Beschreibung**: Anfragen zum Zurücksetzen vergessener Passwörter oder Entsperren gesperrter Konten

**Geltungsbereich**:

- Anfragen für vergessene Passwörter
- Kontosperrungen aufgrund fehlgeschlagener Login-Versuche
- Probleme mit abgelaufenen Passwörtern

**Beispiele**:

- "Ich habe mein Passwort vergessen und kann mich nicht einloggen"
- "Mein Konto ist nach zu vielen fehlgeschlagenen Versuchen gesperrt"
- "Ich muss mein Passwort für das Kundenportal zurücksetzen"

**Ausschlüsse**:

- Erstellung neuer Konten (→ Kontoverwaltung)
- Änderungen von Berechtigungen/Zugriffsebenen (→ Zugriffsanfragen)
- Fragen zur Passwortrichtlinie (→ Allgemeiner IT-Support)

**Schlüsselwörter**: Passwort, zurücksetzen, gesperrt, entsperren, vergessen, Login, Zugriff

**Priorität**: Mittel (beeinträchtigt die Produktivität)

**Ziel-Warteschlange/Team**: IT-Helpdesk
```

## Ihre Taxonomie testen

### Manueller Klassifizierungstest

Testen Sie Ihre Taxonomie vor der Automatisierung manuell:

1. **Stichprobenauswahl**: Wählen Sie 100-200 aktuelle Tickets aus
2. **Mehrere Prüfer**: Lassen Sie 2-3 Personen dieselben Tickets klassifizieren
3. **Übereinstimmung messen**: Berechnen Sie die Inter-Rater-Übereinstimmung
4. **Ziel-Übereinstimmung**: Streben Sie >80% Übereinstimmung zwischen den Prüfern an

### Häufige Probleme

**Geringe Übereinstimmung** (<60%):

- Kategorien überschneiden sich möglicherweise zu stark
- Definitionen könnten unklar sein
- Bessere Beispiele und Dokumentation erforderlich

**Mittlere Übereinstimmung** (60-80%):

- Einige Grenzfälle müssen geklärt werden
- Möglicherweise müssen ähnliche Kategorien zusammengeführt werden
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
- Deckung von 60-70% des Ticketvolumens

Phase 2 (Woche 3-4):
- Fügen Sie 5-7 weitere Kategorien hinzu
- Ziel: 80-90% Abdeckung

Phase 3 (Monat 2+):
- Feinabstimmung und Hinzufügen von Grenzfällen
- Erreichen Sie >90% Abdeckung
```

### Überwachen und anpassen

Überwachen Sie nach dem Deployment kontinuierlich:

- **Klassifizierungsgenauigkeit**: Nach Kategorie
- **Konfidenzscores**: Identifizieren Sie unsichere Klassifizierungen
- **Fehlklassifizierungen**: Suchen Sie nach Mustern
- **Neue Tickettypen**: Identifizieren Sie Lücken in der Taxonomie

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

### TUN ✅

- Beginnen Sie mit geschäftsgetriebenen Kategorien
- Dokumentieren Sie jede Kategorie klar
- Testen Sie manuell vor der Automatisierung
- Iterieren Sie basierend auf Feedback
- Überwachen Sie die Leistung kontinuierlich

### NICHT TUN ❌

- Erstellen Sie anfangs nicht zu viele Kategorien
- Verwenden Sie keine vagen oder sich überschneidenden Definitionen
- Überspringen Sie keine manuelle Validierung
- Setzen und vergessen Sie nicht - Taxonomien entwickeln sich weiter
- Ignorieren Sie keine Vorhersagen mit geringer Konfidenz

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

- **Wöchentlich**: Überprüfen Sie Fehlklassifizierungen
- **Monatlich**: Analysieren Sie die Kategorieverteilung
- **Vierteljährlich**: Hauptüberprüfung der Taxonomie
- **Jährlich**: Prüfung einer kompletten Taxonomie-Neugestaltung

## Nächste Schritte

Nach dem Entwurf Ihrer Taxonomie:

1. **Trainingsdaten vorbereiten**: Sammeln und labeln Sie historische Tickets
2. **Modell konfigurieren**: Richten Sie das Klassifizierungsmodell mit Ihren Kategorien ein
3. **Klassifizierung testen**: Validieren Sie mit Hold-out-Daten
4. **Leistung überwachen**: Verfolgen Sie die Genauigkeit und passen Sie sie bei Bedarf an

## Verwandte Dokumentation

- [Tag-Mapping](tag-mapping.md) - Klassifizierungen auf Ticket-Felder abbilden
- [Modell verwenden](using-model.md) - Klassifizierungsmodelle konfigurieren und verwenden
- [Hardware-Dimensionierung](hardware-sizing.md) - Infrastrukturanforderungen für die Klassifizierung
