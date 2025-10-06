# Contract Tests

Dieses Verzeichnis enthält Contract-Tests für die Plugin-API.

## Zweck

- Überprüfen, dass alle installierten Plugins die erwartete API implementieren
- Sicherstellen der Kompatibilität zwischen Core und Plugins
- Validieren der Plugin-Metadaten
- Markierung: `@pytest.mark.contract`

## Richtlinien

- Tests werden parametrisiert über alle installierten Plugins ausgeführt
- Prüfen erforderliche Methoden und Attribute
- Validieren API-Versionskompatibilität
- Schnell ausführbar, keine externen Abhängigkeiten
