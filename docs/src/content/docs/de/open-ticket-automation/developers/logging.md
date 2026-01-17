.

---
title: Logging-System
description: 'Entwicklerhandbuch zur Verwendung des Logging-Systems in Open Ticket AI mit abstrakten Schnittstellen und Dependency Injection.'
lang: en
nav:
  group: Developers
  order: 7
---

# Logging-System

Open Ticket AI verwendet eine abstrakte Logging‑Schnittstelle, die es Entwicklern ermöglicht, das Logging‑Verhalten zu konfigurieren, ohne den Anwendungscode zu ändern. Die aktuelle Implementierung basiert vollständig auf dem Python‑Standard‑Library‑Modul `logging`.

## Überblick

Das Logging‑System bietet:

- **Abstract interfaces**: `AppLogger` und `LoggerFactory` Protokolle
- **Standard-library implementation**: `StdlibLoggerFactory`
- **Dependency injection**: `AppModule` stellt `LoggerFactory` für die automatische Einrichtung bereit
- **Context binding**: Strukturierte Kontextdaten über die Logger‑API an Log‑Nachrichten anhängen

## Schnellstart

### Verwendung mit Dependency Injection

Services können `LoggerFactory` injizieren und damit Logger mit gebundenem Kontext erstellen. Die Factory gibt Instanzen von `StdlibLogger` zurück, die zu `logging.getLogger` proxyen.

### Direkte Verwendung (ohne DI)

Der Standard‑Library‑Adapter kann konfiguriert und direkt ohne den Dependency‑Injection‑Container verwendet werden. Konfigurieren Sie das Logging‑System beim Anwendungsstart und erstellen Sie Logger nach Bedarf.

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

Das Logging‑System wird über die YAML‑Konfigurationsdatei der Anwendung im Abschnitt `infrastructure.logging` konfiguriert, der vom `AppModule` während des Dependency‑Injection‑Setups geladen wird.

### LoggingConfig‑Felder

`LoggingConfig` definiert die unterstützte Laufzeitkonfiguration:

| Feld                    | Typ                                                                 | Standardwert                                            | Beschreibung                                                                          |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `level`                 | Literal[`"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`] | `"INFO"`                                                | Minimaler Schweregrad, der von Handlers erfasst wird.                                 |
| `log_to_file`           | `bool`                                                              | `False`                                                 | Aktiviert das Schreiben der Log‑Ausgabe in einen File‑Handler.                        |
| `log_file_path`         | `str \| None`                                                       | `None`                                                  | Absoluter oder relativer Pfad für das File‑Logging. Erforderlich, wenn `log_to_file` `True` ist. |
| `format.message_format`| `str`                                                               | `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`| Format‑String, der an `logging.Formatter` übergeben wird.                             |
| `format.date_format`   | `str`                                                               | `"%Y-%m-%d %H:%M:%S"`                                   | Datums‑Format, das vom Formatter verwendet wird.                                      |

## Logging‑Implementierung

### Stdlib (Python‑Standard‑Library)

Der Standard‑Library‑Adapter kapselt das eingebaute Python‑Modul `logging`.

**Features:**

- Vertraute API für Python‑Entwickler
- Kompatibel mit bestehenden Logging‑Konfigurationen
- Respektiert die `LoggingConfig`‑Optionen für Format, Level und optionalen File‑Output

**Beispielausgabe:**

```
2025-10-11 00:21:14 - my_module - INFO - Application started
```

### Handler‑Verkabelung

`create_logger_factory` bereitet den globalen Logging‑Zustand vor:

1. Den Root‑Logger holen und sein Level aus `LoggingConfig.level` setzen.
2. Alle zuvor registrierten Handler entfernen, um doppelte Nachrichten zu vermeiden.
3. Einen `logging.Formatter` mit `log_format` und `date_format` erstellen.
4. Einen `StreamHandler`, der nach `sys.stdout` schreibt, anhängen und mit dem ausgewählten Level und Formatter konfigurieren.
5. Optional einen `FileHandler` anhängen, wenn `log_to_file` `True` ist und `log_file_path` angegeben wurde.
6. Einen `StdlibLoggerFactory` zurückgeben, der `StdlibLogger`‑Instanzen erzeugt, die an benannte Logger gebunden sind.

## Context binding

Context binding ermöglicht es, strukturierte Daten an Log‑Nachrichten anzuhängen. Erstellen Sie einen Basis‑Logger mit Service‑Kontext und binden Sie dann request‑spezifischen Kontext. Alle nachfolgenden Log‑Nachrichten dieses Loggers enthalten den gebundenen Kontext automatisch.

## Logger‑Methoden

Das `AppLogger`‑Protokoll definiert die folgenden Methoden:

- **`bind(**kwargs)`\*\*: Einen neuen Logger mit zusätzlichem Kontext erstellen
- **`debug(message, **kwargs)`\*\*: Debug‑Informationen protokollieren
- **`info(message, **kwargs)`\*\*: Informative Nachrichten protokollieren
- **`warning(message, **kwargs)`\*\*: Warnungen protokollieren
- **`error(message, **kwargs)`\*\*: Fehler protokollieren
- **`exception(message, **kwargs)`\*\*: Ausnahmen mit Traceback protokollieren

## Best Practices

### 1. Dependency Injection verwenden

Immer `LoggerFactory` injizieren statt Logger direkt zu erstellen. Das erleichtert Tests und das Konfigurations‑Management.

### 2. Kontext frühzeitig binden

Erstellen Sie scoped Logger mit gebundenem Kontext für bessere Rückverfolgbarkeit. Binden Sie Kontextdaten wie Request‑IDs, User‑IDs oder Operationsnamen früh, sodass alle nachfolgenden Logs diese Informationen enthalten.

### 3. Angemessene Log‑Levels verwenden

- **DEBUG**: Detaillierte Diagnoseinformationen
- **INFO**: Allgemeine Informationsnachrichten
- **WARNING**: Warnungen für potenziell schädliche Situationen
- **ERROR**: Fehlereignisse, die die Anwendung möglicherweise weiterlaufen lassen
- **EXCEPTION**: Wie ERROR, jedoch mit Ausnahme‑Traceback

### 4. Relevanten Kontext einbinden

Fügen Sie Kontext hinzu, der beim Debuggen und Monitoring hilft, z. B.:

- Ausführungszeit von Abfragen
- Anzahl betroffener Zeilen
- Tabellen‑ oder Ressourcennamen
- Operations‑Identifier

### 5. Keine sensiblen Daten protokollieren

Nie Passwörter, Tokens oder persönliche Informationen loggen. Stattdessen immer Identifier anstelle sensibler Werte loggen.

## Testing mit Logging

Beim Schreiben von Tests können Sie das Logging‑Verhalten prüfen, indem Sie die Log‑Ausgabe erfassen und die Nachrichten sowie Kontextdaten prüfen.

## Migrations‑Leitfaden

### Von direktem `logging.getLogger()`

Ersetzen Sie die direkte Nutzung des Python‑Logging‑Moduls durch Dependency Injection von `LoggerFactory`. Dadurch kann die Logging‑Implementierung ohne Code‑Änderungen ausgetauscht werden.

### Von `AppConfig.get_logger()`

Ersetzen Sie die Verwendung veralteter Factory‑Hilfsfunktionen durch dependency‑injected Instanzen von `LoggerFactory`, die von `create_logger_factory` erstellt werden.

## Zukünftige Roadmap

Die Logging‑Abstraktion ermöglicht das Einführen alternativer Adapter (wie Structlog oder OpenTelemetry‑Exporter) in der Zukunft. Diese Integrationen werden derzeit evaluiert und sind noch nicht verfügbar. Diese Seite wird aktualisiert, sobald neue Implementierungen hinzugefügt werden, damit Leser sie selbstbewusst übernehmen können.