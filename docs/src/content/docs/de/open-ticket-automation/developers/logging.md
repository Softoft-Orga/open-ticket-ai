---
title: Logging System
description: 'Entwicklerhandbuch zur Verwendung des Logging-Systems in Open Ticket AI mit abstrakten Schnittstellen und Dependency Injection.'
lang: de
nav:
  group: Entwickler
  order: 7
---

# Logging-System

Open Ticket AI verwendet eine abstrakte Logging-Schnittstelle, die es Entwicklern ermöglicht, das Logging-Verhalten zu konfigurieren, ohne den Anwendungscode zu ändern. Die aktuelle Implementierung basiert vollständig auf dem `logging`-Modul der Python-Standardbibliothek.

## Überblick

Das Logging-System bietet:

- **Abstrakte Schnittstellen**: `AppLogger`- und `LoggerFactory`-Protokolle
- **Standardbibliotheks-Implementierung**: `StdlibLoggerFactory`
- **Dependency Injection**: `AppModule` stellt `LoggerFactory` für die automatische Einrichtung bereit
- **Kontextbindung**: Strukturierten Kontext an Log-Nachrichten anhängen, über die Logger-API

## Schnellstart

### Verwendung mit Dependency Injection

Services können die `LoggerFactory` injizieren und verwenden, um Logger mit gebundenem Kontext zu erstellen. Die Factory gibt Instanzen von `StdlibLogger` zurück, die an `logging.getLogger` delegieren.

### Direkte Verwendung (ohne DI)

Der Standardbibliotheks-Adapter kann direkt ohne den Dependency-Injection-Container konfiguriert und verwendet werden. Konfigurieren Sie das Logging-System beim Start der Anwendung und erstellen Sie Logger nach Bedarf.

```python
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import (
    StdlibLoggerFactory,
    create_logger_factory,
)

config = LoggingConfig(level="INFO")
factory = create_logger_factory(config)

logger = factory.create("my_module")
logger.info("Application started")
```

## Konfiguration

### Laufzeitkonfiguration

Das Logging-System wird über die YAML-Konfigurationsdatei der Anwendung im Abschnitt `infrastructure.logging` konfiguriert, der vom `AppModule` während der Dependency-Injection-Einrichtung geladen wird.

### LoggingConfig-Felder

`LoggingConfig` definiert die unterstützte Laufzeitkonfiguration:

| Feld                    | Typ                                                                | Standard                                                 | Beschreibung                                                                                     |
| ----------------------- | ------------------------------------------------------------------ | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `level`                 | Literal[`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`] | `"INFO"`                                                 | Mindest-Schweregrad, der von Handlern erfasst wird.                                              |
| `log_to_file`           | `bool`                                                             | `False`                                                  | Aktiviert die Ausgabe von Logs in eine Datei über einen File-Handler.                            |
| `log_file_path`         | `str \| None`                                                      | `None`                                                   | Absoluter oder relativer Pfad für die Dateiausgabe. Erforderlich, wenn `log_to_file` `True` ist. |
| `format.message_format` | `str`                                                              | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"` | Format-String, der an `logging.Formatter` übergeben wird.                                        |
| `format.date_format`    | `str`                                                              | `"%Y-%m-%d %H:%M:%S"`                                    | Zeitstempel-Format, das vom Formatter verwendet wird.                                            |

## Logging-Implementierung

### Stdlib (Python-Standardbibliothek)

Der Standardbibliotheks-Adapter kapselt das eingebaute `logging`-Modul von Python.

**Merkmale:**

- Vertraute API für Python-Entwickler
- Kompatibel mit bestehenden Logging-Konfigurationen
- Respektiert die `LoggingConfig`-Optionen für Format, Level und optionale Dateiausgabe

**Beispielausgabe:**

```
2025-10-11 00:21:14 - my_module - INFO - Application started
```

### Handler-Verknüpfung

`create_logger_factory` bereitet den globalen Logging-Zustand vor:

1. Hole den Root-Logger und setze sein Level aus `LoggingConfig.level`.
2. Entferne alle zuvor registrierten Handler, um doppelte Nachrichten zu vermeiden.
3. Erstelle einen `logging.Formatter` mit `log_format` und `date_format`.
4. Füge einen `StreamHandler` hinzu, der nach `sys.stdout` schreibt, konfiguriert mit dem gewählten Level und Formatter.
5. Optional: Füge einen `FileHandler` hinzu, wenn `log_to_file` `True` ist und `log_file_path` angegeben ist.
6. Gib eine `StdlibLoggerFactory` zurück, die `StdlibLogger`-Instanzen erstellt, die an benannte Logger gebunden sind.

## Kontextbindung

Die Kontextbindung ermöglicht es, strukturierte Daten an Log-Nachrichten anzuhängen. Erstellen Sie einen Basis-Logger mit Service-Kontext und binden Sie dann anforderungsspezifischen Kontext. Alle nachfolgenden Log-Nachrichten von diesem Logger enthalten automatisch den gebundenen Kontext.

## Logger-Methoden

Das `AppLogger`-Protokoll definiert die folgenden Methoden:

- **`bind(**kwargs)`\*\*: Erstellt einen neuen Logger mit zusätzlichem Kontext
- **`debug(message, **kwargs)`\*\*: Loggt Debug-Informationen
- **`info(message, **kwargs)`\*\*: Loggt Informationsmeldungen
- **`warning(message, **kwargs)`\*\*: Loggt Warnungen
- **`error(message, **kwargs)`\*\*: Loggt Fehler
- **`exception(message, **kwargs)`\*\*: Loggt Exceptions mit Traceback

## Best Practices

### 1. Verwenden Sie Dependency Injection

Injizieren Sie immer die `LoggerFactory`, anstatt Logger direkt zu erstellen. Dies erleichtert das Testen und die Konfigurationsverwaltung.

### 2. Binden Sie Kontext frühzeitig

Erstellen Sie scoped Logger mit gebundenem Kontext für bessere Nachverfolgbarkeit. Binden Sie Kontextdaten wie Request-IDs, Benutzer-IDs oder Operationsnamen frühzeitig, damit alle nachfolgenden Logs diese Informationen enthalten.

### 3. Verwenden Sie angemessene Log-Level

- **DEBUG**: Detaillierte Diagnoseinformationen
- **INFO**: Allgemeine Informationsmeldungen
- **WARNING**: Warnmeldungen für potenziell problematische Situationen
- **ERROR**: Fehlerereignisse, die es der App möglicherweise noch erlauben, fortzufahren
- **EXCEPTION**: Wie ERROR, aber inklusive Exception-Traceback

### 4. Fügen Sie relevanten Kontext hinzu

Fügen Sie Kontext hinzu, der beim Debuggen und Monitoring hilft, wie z.B.:

- Abfrageausführungszeit
- Anzahl betroffener Zeilen
- Tabellen- oder Ressourcennamen
- Operations-Identifikatoren

### 5. Loggen Sie keine sensiblen Daten

Loggen Sie niemals Passwörter, Tokens oder persönliche Informationen. Loggen Sie immer Identifikatoren anstelle sensibler Werte.

## Testen mit Logging

Beim Schreiben von Tests können Sie das Logging-Verhalten überprüfen, indem Sie die Log-Ausgabe erfassen und die Nachrichten und Kontextdaten überprüfen.

## Migrationsleitfaden

### Von direktem `logging.getLogger()`

Ersetzen Sie die direkte Verwendung des Python-Logging-Moduls durch die Dependency Injection der `LoggerFactory`. Dies ermöglicht es, die Logging-Implementierung ohne Codeänderungen auszutauschen.

### Von `AppConfig.get_logger()`

Ersetzen Sie Verwendungen von Legacy-Factory-Helfern durch Dependency-Injected-Instanzen von `LoggerFactory`, die von `create_logger_factory` erstellt werden.

## Zukünftige Roadmap

Die Logging-Abstraktion ermöglicht die Einführung alternativer Adapter (wie Structlog oder OpenTelemetry-Exporter) in der Zukunft. Diese Integrationen werden derzeit evaluiert und sind noch nicht verfügbar. Diese Seite wird aktualisiert, wenn neue Implementierungen hinzugefügt werden, damit Leser sie sicher übernehmen können.
