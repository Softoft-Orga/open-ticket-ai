# End-to-End Tests

Dieses Verzeichnis enthält End-to-End-Tests, die vollständige Workflows testen.

## Zweck

- Blackbox-Tests vollständiger Anwendungsflows
- Testen von Prefect-Flows
- Testen kompletter Ticket-Verarbeitungspipelines
- Markierung: `@pytest.mark.e2e` und oft auch `@pytest.mark.slow`

## Richtlinien

- Tests sollten realistische Szenarien abbilden
- Können länger dauern (daher `@pytest.mark.slow`)
- Verwenden Sie kleine Testdaten und kurze Intervalle
- Mocken Sie externe Netzwerkzugriffe wenn möglich
