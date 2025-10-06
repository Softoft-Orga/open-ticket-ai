# Integration Tests

Dieses Verzeichnis enthält Integrationstests, die die Zusammenarbeit zwischen Core und Plugins testen.

## Zweck

- Testen der Interaktion zwischen Core-Komponenten und Plugins
- Verwenden temporäre Konfigurationsdateien
- Können Testcontainers/Docker verwenden
- Markierung: `@pytest.mark.integration`

## Richtlinien

- Tests sollten die Zusammenarbeit mehrerer Komponenten prüfen
- Verwenden Sie Mocks nur, wenn externe Systeme nicht verfügbar sind
- Tests sollten deterministisch und wiederholbar sein
