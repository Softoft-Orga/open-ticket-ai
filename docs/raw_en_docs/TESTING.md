# Teststruktur und Best Practices

Dieses Dokument beschreibt die Testorganisation im Open Ticket AI Monorepo.

## Überblick

Das Repository verwendet eine mehrstufige Teststruktur:
- **Paket-Tests**: Unit-Tests in jedem Paket (Core und Plugins)
- **Zentrale Tests**: Integration-, E2E- und Contract-Tests auf Repo-Ebene

## Verzeichnisstruktur

```
.
├── pyproject.toml
├── src/
│   ├── open_ticket_ai/           # Core-Paket
│   │   └── core/...
│   ├── open_ticket_ai_hf_local/  # HuggingFace Plugin
│   │   ├── pyproject.toml
│   │   └── tests/                # Plugin-spezifische Unit-Tests
│   └── open_ticket_ai_otobo_znuny_plugin/  # OTOBO/Znuny Plugin
│       ├── pyproject.toml
│       └── tests/                # Plugin-spezifische Unit-Tests
│
├── packages/
│   └── open_ticket_ai_otobo_znuny_plugin/  # Standalone-Paket
│       ├── pyproject.toml
│       └── tests/
│
└── tests/                        # Zentrale Tests
    ├── unit/                     # Core Unit-Tests
    ├── integration/              # Core + Plugins zusammen
    ├── e2e/                      # End-to-End Workflows
    ├── contract/                 # Plugin-API-Contract-Tests
    ├── data/                     # Testdaten (klein, textbasiert)
    └── conftest.py               # Globale Fixtures
```

## Pytest-Konfiguration

### Root-Konfiguration (pyproject.toml)

```toml
[tool.pytest.ini_options]
pythonpath = [".", "src"]
testpaths = ["tests", "src/open_ticket_ai_hf_local", "src/open_ticket_ai_otobo_znuny_plugin"]
addopts = "-q"
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
markers = [
    "unit: schnelle, isolierte Tests",
    "integration: core + plugin zusammen",
    "contract: plugin-api-vertrag",
    "e2e: end-to-end flows",
    "slow: dauert länger"
]
```

### Plugin-Konfiguration

Jedes Plugin hat seine eigene pytest-Konfiguration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
markers = [
    "unit: schnelle, isolierte Tests",
    "integration: core + plugin zusammen",
    "slow: dauert länger"
]
```

## Testtypen

### Unit-Tests

**Speicherort**: `tests/unit/` (Core), `<plugin>/tests/` (Plugins)

**Eigenschaften**:
- Schnelle Ausführung
- Isoliert (keine Netz-/Filesystem-Abhängigkeiten)
- Mocks/Stubs für externe Systeme
- Testen einzelne Komponenten

**Markierung**: `@pytest.mark.unit`

**Beispiel**:
```python
import pytest

@pytest.mark.unit
def test_pipe_configuration():
    config = {"id": "test", "use": "TestPipe"}
    pipe = TestPipe(config)
    assert pipe.id == "test"
```

### Integration-Tests

**Speicherort**: `tests/integration/`

**Eigenschaften**:
- Testen Zusammenarbeit Core ↔ Plugin
- Verwenden temporäre Config-Files
- Können Testcontainers/Docker nutzen
- Längere Laufzeit als Unit-Tests

**Markierung**: `@pytest.mark.integration`

**Beispiel**:
```python
import pytest

@pytest.mark.integration
def test_plugin_registration_and_execution(app_injector, test_config):
    registry = app_injector.get(UnifiedRegistry)
    # Test plugin registration and execution
    assert registry.has_plugin("test_plugin")
```

### Contract-Tests

**Speicherort**: `tests/contract/`

**Eigenschaften**:
- Prüfen Plugin-API-Kompatibilität
- Parametrisiert über alle installierten Plugins
- Schnell, keine externen Abhängigkeiten
- Validieren Metadaten und Hooks

**Markierung**: `@pytest.mark.contract`

**Beispiel**:
```python
import importlib.metadata as md
import pytest

PLUGIN_GROUP = "open_ticket_ai.plugins"
REQUIRED_CORE_API = "2.0"

def discover_plugins():
    for ep in md.entry_points(group=PLUGIN_GROUP):
        plugin = ep.load()
        meta = getattr(plugin, "get_metadata", lambda: {})()
        yield ep.name, plugin, meta

@pytest.mark.contract
@pytest.mark.parametrize("name,plugin,meta", list(discover_plugins()), ids=lambda x: x[0])
def test_register_hooks_exist(name, plugin, meta):
    assert hasattr(plugin, "register_pipes")
    assert hasattr(plugin, "register_services")
    assert "name" in meta and "version" in meta
```

### End-to-End Tests

**Speicherort**: `tests/e2e/`

**Eigenschaften**:
- Blackbox-Tests kompletter Workflows
- Realistische Szenarien
- Längste Laufzeit

**Markierung**: `@pytest.mark.e2e`, oft auch `@pytest.mark.slow`

**Beispiel**:
```python
import pytest

@pytest.mark.e2e
@pytest.mark.slow
def test_ticket_classification_workflow():
    # Test complete ticket classification flow
    pass
```

## Globale Fixtures

Die Datei `tests/conftest.py` enthält gemeinsame Fixtures für alle Tests:

### tmp_config
Erstellt eine temporäre Konfigurationsdatei:
```python
def test_with_config(tmp_config):
    config = load_config(tmp_config)
    assert config.plugins == []
```

### app_injector
Liefert einen konfigurierten Dependency-Injection-Container:
```python
def test_with_injector(app_injector):
    registry = app_injector.get(UnifiedRegistry)
    assert registry is not None
```

### test_config
Lädt eine Test-Konfiguration:
```python
def test_with_loaded_config(test_config):
    assert isinstance(test_config, RawOpenTicketAIConfig)
```

## Tests ausführen

### Alle Tests
```bash
pytest
```

### Nach Marker filtern
```bash
# Nur Unit-Tests
pytest -m unit

# Nur Integration-Tests
pytest -m integration

# Contract-Tests
pytest -m contract

# E2E-Tests
pytest -m e2e

# Alle außer langsame Tests
pytest -m "not slow"
```

### Spezifisches Verzeichnis
```bash
# Core Unit-Tests
pytest tests/unit/

# Integration-Tests
pytest tests/integration/

# Plugin-Tests
pytest src/otai_hf_local/tests/
```

### Mit Coverage
```bash
pytest --cov=open_ticket_ai --cov-report=html tests/
```

## Testdaten

**Speicherort**: `tests/data/`

**Richtlinien**:
- Klein und textbasiert (YAML/JSON bevorzugt)
- Keine Binärdateien
- Keine sensiblen Daten
- Strukturiert nach Testtyp

**Beispiel** (`tests/data/sample_tickets.yml`):
```yaml
sample_tickets:
  - id: "TICKET-001"
    subject: "Test Ticket"
    body: "Test content"
    queue: "Support"
```

**Verwendung**:
```python
import yaml
from pathlib import Path

def test_with_data():
    data_path = Path(__file__).parent / "data" / "sample_tickets.yml"
    with open(data_path) as f:
        data = yaml.safe_load(f)
    assert len(data["sample_tickets"]) > 0
```

## CI/CD Integration

### GitHub Actions Matrix

**Core-Tests**:
```yaml
- name: Core Unit Tests
  run: pytest -m unit tests/unit/
```

**Plugin-Tests**:
```yaml
- name: Plugin Tests
  run: |
    pytest -m unit src/open_ticket_ai_hf_local/tests/
    pytest -m unit packages/open_ticket_ai_otobo_znuny_plugin/tests/
```

**Integration & Contract**:
```yaml
- name: Integration & Contract Tests
  run: |
    pytest -m integration tests/integration/
    pytest -m contract tests/contract/
```

**E2E (Nightly)**:
```yaml
- name: E2E Tests
  run: pytest -m e2e tests/e2e/
```

## Best Practices

### 1. Test-Isolation
- Jeder Test sollte unabhängig sein
- Verwenden Sie Fixtures für Setup/Teardown
- Keine globalen State-Änderungen

### 2. Aussagekräftige Namen
```python
# Gut
def test_pipe_processes_ticket_with_valid_queue():
    pass

# Schlecht
def test_pipe():
    pass
```

### 3. Arrange-Act-Assert
```python
def test_ticket_classification():
    # Arrange
    ticket = create_test_ticket()
    classifier = TicketClassifier()
    
    # Act
    result = classifier.classify(ticket)
    
    # Assert
    assert result.queue == "IT Support"
```

### 4. Marker verwenden
```python
@pytest.mark.unit
@pytest.mark.slow  # bei Bedarf
def test_complex_operation():
    pass
```

### 5. Parametrisierung nutzen
```python
@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### 6. Mocks sparsam einsetzen
- Mocken Sie nur externe Abhängigkeiten
- Bevorzugen Sie echte Implementierungen in Unit-Tests
- Verwenden Sie Testdoubles für Netzwerk/Filesystem

### 7. Async-Tests
```python
@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result is not None
```

## Troubleshooting

### Tests werden nicht gefunden
- Prüfen Sie `testpaths` in `pyproject.toml`
- Stellen Sie sicher, dass `__init__.py` existiert
- Testen Sie mit `pytest --collect-only`

### Import-Fehler
- Prüfen Sie `pythonpath` in `pyproject.toml`
- Installieren Sie das Paket in Development-Mode: `pip install -e .`

### Marker-Warnungen
- Alle Marker müssen in `markers` definiert sein
- Prüfen Sie die pytest-Konfiguration

### Async-Tests schlagen fehl
- Stellen Sie sicher, dass `pytest-asyncio` installiert ist
- Prüfen Sie `asyncio_mode` in der Konfiguration

## Weiterführende Ressourcen

- [Pytest Dokumentation](https://docs.pytest.org/)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [CONTRIBUTING.md](CONTRIBUTING.md)
