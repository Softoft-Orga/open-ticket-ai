---
title: Testleitfaden
description: 'Umfassender Testleitfaden für Open Ticket AI-Konfigurationen, Pipelines und benutzerdefinierte Komponenten mit Best Practices und configExamples.'
---

# Testleitfaden

Leitfaden zum Testen von Open Ticket AI-Konfigurationen, Pipelines und benutzerdefinierten Komponenten.

## Testphilosophie

Schreiben Sie Tests, die sich auf **Kernfunktionalität und Verträge** konzentrieren, nicht auf Implementierungsdetails:

### DO ✅

- Testen Sie das Haupt‑Eingabe/Ausgabe‑Verhalten
- Testen Sie Fehlerbehandlung und relevante Randfälle
- Testen Sie öffentliche Schnittstellen und Verträge
- Fokussieren Sie sich auf das „Was“ der Code tut, nicht auf das „Wie“
- Halten Sie Tests einfach und wartbar

### DON'T ❌

- Testen Sie keine trivialen Getter/Setter
- Verifizieren Sie nicht jedes Feld in komplexen Objekten
- Duplizieren Sie keine Testlogik über mehrere Dateien
- Testen Sie keine privaten Implementierungsdetails
- Erstellen Sie keine übermäßigen Randfalltests, die keinen Mehrwert bieten

### Beispiel: Gut vs Schlecht

```python
# ❌ Bad: Testing trivial field values
def test_config_fields():
    config = MyConfig(id="test", timeout=30, priority=5, workers=10)
    assert config._id == "test"
    assert config.timeout == 30
    assert config.priority == 5
    assert config.workers == 10


# ✅ Good: Testing behavior
def test_config_applies_defaults():
    config = MyConfig(id="test")
    # Only assert the key behavior
    assert config._id == "test"
    assert config.timeout > 0  # Has a valid default
```

```python
# ❌ Bad: Over-specific edge cases
def test_path_with_dots_at_start():
    result = process(".a.b")
    assert result == expected

def test_path_with_dots_at_end():
    result = process("a.b.")
    assert result == expected

def test_path_with_double_dots():
    result = process("a..b")
    assert result == expected

# ✅ Good: Core behavior with meaningful cases
def test_path_processing():
    assert process("a.b.c") == {"a": {"b": {"c": "value"}}}
    assert process("") == "value"  # Edge case that matters
```

## Testübersicht

Open Ticket AI unterstützt mehrere Testebenen:

- **Unit Tests**: Einzelne Komponenten
- **Integration Tests**: Komponenteninteraktionen
- **Contract Tests**: Schnittstellenkonformität
- **E2E Tests**: Vollständige Workflows

## Unit Tests

### Testen von Pipes

Testen Sie die Logik einzelner Pipes:

```python
from open_ticket_ai.pipeline import PipelineContext, PipeResult
from my_plugin.pipes import MyPipe


def test_my_pipe():
    # Arrange
    pipe = MyPipe()
    context = PipelineContext()
    context.set("input_data", test_data)

    # Act
    result = pipe.execute(context)

    # Assert
    assert result.succeeded
    assert context.get("output_data") == expected_output
```

### Testen von Services

Testen Sie Service-Implementierungen:

```python
from my_plugin.services import MyService

def test_my_service():
    service = MyService()
    result = service.process(input_data)
    assert result == expected_result
```

### Verwendung von Mocks

Mocken Sie externe Abhängigkeiten:

```python
from unittest.mock import Mock, patch


def test_pipe_with_mock():
    # Mock external service
    mock_service = Mock()
    mock_service.classify.return_value = {"queue": "billing"}

    pipe = ClassifyPipe(classifier=mock_service)
    context = PipelineContext()

    result = pipe.execute(context)

    assert result.succeeded
    mock_service.classify.assert_called_once()
```

## Integration Tests

### Testen von Pipe-Ketten

Testen Sie mehrere Pipes zusammen:

```python
def test_pipeline_flow():
    # Setup
    fetch_pipe = FetchTicketsPipe(adapter=test_adapter)
    classify_pipe = ClassifyPipe(classifier=test_classifier)

    context = PipelineContext()

    # Execute chain
    fetch_result = fetch_pipe.execute(context)
    assert fetch_result.succeeded

    classify_result = classify_pipe.execute(context)
    assert classify_result.succeeded

    # Verify data flow
    assert context.has("tickets")
    assert context.has("classifications")
```

### Testen mit echten Services

Testen Sie gegen tatsächliche APIs (Testumgebung):

```python
import pytest


@pytest.mark.integration
def test_otobo_integration():
    adapter = OtoboAdapter(
        base_url=TEST_OTOBO_URL,
        api_token=TEST_API_TOKEN
    )

    # Fetch tickets
    tickets = adapter.fetch_tickets({"limit": 1})
    assert len(tickets) >= 0

    # Test update (if tickets exist)
    if tickets:
        success = adapter.update_ticket(
            tickets[0]._id,
            {"PriorityID": 2}
        )
        assert success
```

## Contract Tests

### Verifizierung der Schnittstellenimplementierung

Testen Sie, dass Komponenten die erforderlichen Schnittstellen implementieren:

```python
from open_ticket_ai.integration import TicketSystemAdapter


def test_adapter_contract():
    adapter = MyCustomAdapter()

    # Verify isinstance
    assert isinstance(adapter, TicketSystemAdapter)

    # Verify methods exist
    assert hasattr(adapter, 'fetch_tickets')
    assert hasattr(adapter, 'update_ticket')
    assert hasattr(adapter, 'add_note')
    assert hasattr(adapter, 'search_tickets')

    # Verify methods are callable
    assert callable(adapter.fetch_tickets)
    assert callable(adapter.update_ticket)
```

### Testen von Methodensignaturen

```python
import inspect

def test_method_signatures():
    adapter = MyCustomAdapter()

    # Check fetch_tickets signature
    sig = inspect.signature(adapter.fetch_tickets)
    assert 'criteria' in sig.parameters

    # Check return type annotation
    assert sig.return_annotation == List[Ticket]
```

## E2E Tests

### Testen kompletter Workflows

Testen Sie die gesamte Pipeline-Ausführung:

```python
@pytest.mark.e2e
def test_full_pipeline():
    # Load configuration
    config = load_config("test_config.yml")

    # Create and run pipes
    pipeline = create_pipeline(config)
    result = pipeline.run()

    # Verify success
    assert result.succeeded
    assert result.tickets_processed > 0
```

### Konfigurationstests

Testen Sie verschiedene Konfigurationen:

```python
@pytest.mark.parametrize("config_file", [
    "queue_classification.yml",
    "priority_classification.yml",
    "complete_workflow.yml"
])
def test_config_examples(config_file):
    config_path = f"docs/raw_en_docs/config_examples/{config_file}"

    # Validate configuration
    config = load_config(config_path)
    assert validate_config(config)

    # Test in dry-run mode
    result = run_pipeline(config, dry_run=True)
    assert result.succeeded
```

## Ausführen der Testsuite

### Mit pytest

```bash
# Run all tests
uv run -m pytest

# Run specific test file
uv run -m pytest tests/unit/test_pipes.py

# Run specific test
uv run -m pytest tests/unit/test_pipes.py::test_classify_pipe

# Run with coverage
uv run -m pytest --cov=open_ticket_ai --cov-report=html

# Run only unit tests
uv run -m pytest tests/unit/

# Run integration tests
uv run -m pytest -m integration

# Skip slow tests
uv run -m pytest -m "not slow"
```

### Mit Testkategorien

```python
import pytest

@pytest.mark.unit
def test_unit():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.e2e
def test_e2e():
    pass

@pytest.mark.slow
def test_slow():
    pass
```

# Nur Unit Tests
uv run -m pytest -m unit

# Integration und e2e
uv run -m pytest -m "integration or e2e"

# Alles außer langsamen Tests
uv run -m pytest -m "not slow"

## Testkonfiguration

### pytest.ini Konfiguration

```ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow tests"
]
addopts = "-v --tb=short"
```

### Test-Fixtures

Erstellen Sie wiederverwendbare Fixtures:

```python
import pytest


@pytest.fixture
def sample_ticket():
    return Ticket(
        id="123",
        title="Test ticket",
        description="Test description",
        state="Open"
    )


@pytest.fixture
def pipeline_context():
    context = PipelineContext()
    context.set("test_mode", True)
    return context


@pytest.fixture
def mock_classifier():
    classifier = Mock()
    classifier._classify.return_value = {
        "queue": "billing",
        "confidence": 0.85
    }
    return classifier


# Use fixtures in tests
def test_with_fixtures(sample_ticket, pipeline_context, mock_classifier):
    # Test logic here
    pass
```

## Test-Best Practices

### Do:

- Schreiben Sie Tests für neue Features
- Testen Sie Fehlersituationen
- Verwenden Sie beschreibende Testnamen
- Halten Sie Tests unabhängig
- Verwenden Sie Fixtures für das Setup
- Mocken Sie externe Abhängigkeiten
- Testen Sie Randfälle

### Don't:

- Überspringen Sie keine Tests
- Schreiben Sie keine flüchtigen Tests
- Verlassen Sie sich nicht auf die Testreihenfolge
- Verwenden Sie keine Produktionsdaten
- Ignorieren Sie keine Testfehler
- Testen Sie keine Implementierungsdetails
- Schreiben Sie nicht untestbaren Code

## Kontinuierliche Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Run tests
        run: uv run -m pytest

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Testdatenverwaltung

### Verwendung von Testdatendateien

```python
import json
from pathlib import Path

def load_test_data(filename):
    data_dir = Path(__file__).parent / "data"
    with open(data_dir / filename) as f:
        return json.load(f)

def test_with_data_file():
    test_tickets = load_test_data("test_tickets.json")
    # Use test data
```

### Testdatenorganisation

```
tests/
├── unit/
│   ├── test_pipes.py
│   └── data/
│       └── test_tickets.json
├── integration/
│   ├── test_adapters.py
│   └── data/
│       └── test_config.yml
└── conftest.py
```

## Debuggen von Tests

### Verwendung des pytest-Debuggers

```bash
# Drop into debugger on failure
uv run -m pytest --pdb

# Drop into debugger at start
uv run -m pytest --trace
```

### Print-Debugging

```python
def test_with_debug():
    result = some_function()
    print(f"Result: {result}")  # Will show with -s flag
    assert result == expected
```

Ausführen mit Ausgabe:

```bash
uv run -m pytest -s
```

## Teststruktur und -organisation

### Repository-Testlayout

```
open-ticket-ai/
├── packages/
│   ├── otai_hf_local/
│   │   ├── src/otai_hf_local/
│   │   └── tests/              # Package-specific tests
│   │       ├── unit/
│   │       ├── integration/
│   │       ├── data/
│   │       └── conftest.py     # Package fixtures
│   └── otai_otobo_znuny/
│       ├── src/otai_otobo_znuny/
│       └── tests/
│           ├── unit/
│           ├── integration/
│           ├── data/
│           └── conftest.py
├── src/open_ticket_ai/         # NO TESTS HERE!
├── tests/                      # Root-level tests
│   ├── unit/                   # Root package unit tests
│   ├── integration/            # Cross-package integration
│   ├── e2e/                    # End-to-end workflows
│   ├── data/                   # Shared test data
│   └── conftest.py             # Workspace-level fixtures
└── pyproject.toml
```

### Kritische Regeln

**NEVER** place tests under `src/`:

- ❌ `src/**/tests/`
- ❌ `src/**/test_*.py`
- ✅ `tests/` or `packages/*/tests/`

**Test file naming**:

- ✅ `test_*.py`
- ❌ `*_test.py`

**Test directories**:

- ❌ Fügen Sie kein `__init__.py` zu Testverzeichnissen hinzu
- ✅ Testverzeichnisse sind KEINE Python-Pakete

### Wo Tests platzieren

| Testtyp                     | Ort                                 | Zweck                                        |
| --------------------------- | ----------------------------------- | -------------------------------------------- |
| **Package Unit**            | `packages/<name>/tests/unit/`       | Schnelle, isolierte Tests für Paketcode      |
| **Package Integration**     | `packages/<name>/tests/integration/`| Tests, die I/O oder Paketgrenzen berühren     |
| **Root Unit**               | `tests/unit/`                       | Tests für das Root-Paket (`src/open_ticket_ai/`) |
| **Cross-Package Integration**| `tests/integration/`                | Tests, die mehrere Pakete umfassen            |
| **End-to-End**              | `tests/e2e/`                        | Komplette Workflow-Tests                     |

### Testdatenverwaltung

Store test data near the tests that use it:

```
packages/otai_hf_local/tests/
├── unit/
│   └── test_text_classification.py
├── integration/
│   └── test_model_loading.py
└── data/
    ├── sample_tickets.json      # Used by multiple tests
    └── model_configs/
        └── test_config.yaml
```

Load test data using relative paths:

```python
from pathlib import Path

def load_test_data(filename: str):
    data_dir = Path(__file__).parent / "data"
    return (data_dir / filename).read_text()
```

## Conftest-Dateien und Fixtures

### Conftest-Hierarchie

```
tests/conftest.py              # Workspace-level (shared by all)
tests/unit/conftest.py         # Unit test level
tests/unit/core/conftest.py    # Core module level
packages/*/tests/conftest.py   # Package-level
```

**Fixture Resolution Order:**

1. Testdatei selbst
2. Nächstes conftest.py (gleiches Verzeichnis)
3. Eltern-conftest.py-Dateien (aufwärts im Baum)
4. Eingebaute pytest-Fixtures

### Workspace-Level Fixtures (tests/conftest.py)

```python
@pytest.fixture
def tmp_config(tmp_path: Path) -> Path:
    """Erstelle eine temporäre Konfigurationsdatei für Tests.

    Verfügbar für alle Tests im Workspace.
    Wird zum Testen des Ladens von Konfigurationen verwendet.
    """
    config_content = """
open_ticket_ai:
  plugins: []
  infrastructure:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")
    return config_path


@pytest.fixture
def app_injector(tmp_config: Path) -> Injector:
    """Stelle einen konfigurierten Dependency Injector für Tests bereit.

    Verwendet das tmp_config-Fixture, um einen Test-Injector zu erstellen.
    """
    from injector import Injector
    from open_ticket_ai.core import AppModule

    return Injector([AppModule(tmp_config)])


@pytest.fixture
def test_config(tmp_config: Path) -> RawOpenTicketAIConfig:
    """Lade Testkonfiguration zur Validierung."""
    from open_ticket_ai.core import load_config

    return load_config(tmp_config)
```

### Unit-Test-Fixtures (tests/unit/conftest.py)

```python
@pytest.fixture
def empty_pipeline_context() -> Context:
    """Leerer Pipes-Kontext für Tests."""
    return Context(pipes={}, config={})


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    """Mock Ticket-System-Service mit gängigen async-Methoden."""
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mocked_ticket_system() -> MockedTicketSystem:
    """Zustandsbehaftetes Mock-Ticket-System mit Beispieldaten.

    Enthält vorbefüllte Tickets für das Testen von Ticket-Operationen.
    """
    system = MockedTicketSystem()

    system.add_test_ticket(
        id="TICKET-1",
        subject="Test ticket 1",
        body="This is a test",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
    )

    return system
```

### Paket-Level-Fixtures

```python
# packages/otai_hf_local/tests/conftest.py

@pytest.fixture
def mock_hf_model():
    """Mock Hugging Face Modell für Tests."""
    return MagicMock(spec=TextClassificationPipeline)


@pytest.fixture
def sample_classification_config():
    """Beispielkonfiguration für Textklassifizierung."""
    return {
        "model_name": "bert-base-uncased",
        "threshold": 0.7,
    }
```

### Benennungskonventionen für Fixtures

| Muster      | Zweck                     | Beispiel                                   |
| ----------- | ------------------------ | ------------------------------------------ |
| `mock_*`   | Mock-Objekte             | `mock_ticket_system_service`               |
| `sample_*` | Sample-Daten             | `sample_ticket`, `sample_classification_config` |
| `tmp_*`    | Temporäre Ressourcen     | `tmp_config`, `tmp_path`                  |
| `empty_*`  | Leere/ minimale Instanzen| `empty_pipeline_context`                  |
| `*_factory`| Factory-Funktionen       | `pipe_config_factory`                     |

### Fixture-Umfang

Wählen Sie den passenden Umfang für Fixtures:

```python
@pytest.fixture(scope="function")  # Default: new instance per test
def per_test_resource():
    return Resource()


@pytest.fixture(scope="module")  # Shared within test module
def shared_resource():
    return ExpensiveResource()


@pytest.fixture(scope="session")  # Shared across entire test session
def session_resource():
    return VeryExpensiveResource()
```

### Factory-Fixtures

```python
@pytest.fixture
def pipe_config_factory():
    """Factory zum Erstellen von Pipe-Konfigurationen mit benutzerdefinierten Werten."""

    def factory(**kwargs) -> dict:
        defaults = {
            "id": "test_pipe",
            "use": "open_ticket_ai.base.DefaultPipe",
            "when": True,
            "steps": [],
        }
        defaults.update(kwargs)
        return defaults

    return factory


def test_with_custom_config(pipe_config_factory):
    """Verwenden Sie die Factory, um eine benutzerdefinierte Konfiguration zu erstellen."""
    config = pipe_config_factory(id="special_pipe", when=False)
    assert config["id"] == "special_pipe"
    assert config["when"] is False
```

### Fixture-Aufräumen

```python
@pytest.fixture
def database_connection():
    """Stelle Datenbankverbindung mit automatischer Aufräumung bereit."""
    conn = create_connection()
    yield conn
    conn.close()


@pytest.fixture
def temp_directory(tmp_path):
    """Erstelle temporäres Verzeichnis mit Dateien."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()

    yield test_dir

    # Cleanup happens automatically with tmp_path
```

### Vermeidung von Fixture-Duplizierung

**Bevor ein neues Fixture hinzugefügt wird:**

1. Überprüfen Sie vorhandene conftest-Dateien
2. Suche nach ähnlichen Fixtures: `grep -r "def fixture_name" tests/`
3. Prüfen Sie, ob ein vorhandenes Fixture wiederverwendet werden kann
4. Dokumentieren Sie den Zweck des Fixtures klar

**Beispiel für Konsolidierung:**

```python
# ❌ Schlecht: Duplizierte Fixtures
# tests/conftest.py
@pytest.fixture
def mock_ticket_system_config():
    return {"ticket_system_id": "test"}


# tests/unit/conftest.py
@pytest.fixture
def mock_ticket_system_pipe_config():
    return {"ticket_system_id": "test"}


# ✅ Gut: Einzelnes, wiederverwendbares Fixture
# tests/conftest.py
@pytest.fixture
def ticket_system_pipe_config():
    """Base configuration for ticket system pipes."""

    def factory(**overrides):
        config = {
            "id": "test_ticket_pipe",
            "use": "TestPipe",
            "when": True,
            "ticket_system_id": "test_system",
        }
        config.update(overrides)
        return config

    return factory
```

### Entdecken verfügbarer Fixtures

Alle verfügbaren Fixtures für einen Test auflisten:

```bash
# Show fixtures available to unit tests
uv run -m pytest tests/unit/ --fixtures

# Show specific fixture details
uv run -m pytest tests/unit/ --fixtures -v | grep mock_ticket
```

### Häufige Fixture-Muster

#### Konfigurations-Fixtures:

```python
@pytest.fixture
def minimal_config(tmp_path):
    """Minimal valid configuration."""
    config = {"open_ticket_ai": {"plugins": []}}
    path = tmp_path / "config.yml"
    path.write_text(yaml.dump(config))
    return path
```

#### Mock-Service-Fixtures:

```python
@pytest.fixture
def mock_classifier():
    """Mock classifier with deterministic responses."""
    mock = Mock()
    mock._classify.return_value = {
        "label": "billing",
        "confidence": 0.85
    }
    return mock
```

#### Parametrisierte Fixtures:

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """Test against multiple database types."""
    return request.param
```

## Tests ausführen

### Grundbefehle

```bash
# All tests
uv run -m pytest

# Specific directory
uv run -m pytest tests/unit/

# Specific package
uv run -m pytest packages/otai_hf_local/tests/

# Specific file
uv run -m pytest tests/unit/core/config/test_config_loader.py

# Specific test
uv run -m pytest tests/unit/core/config/test_config_loader.py::test_load_config
```

### Mit Markern

```bash
# Only unit tests
uv run -m pytest -m unit

# Integration tests
uv run -m pytest -m integration

# E2E tests
uv run -m pytest -m e2e
```

### Testsammlung

```bash
# Show what tests would run (don't execute)
uv run -m pytest --collect-only

# Verbose collection
uv run -m pytest --collect-only -v
```

## Pytest-Konfiguration

Das Projekt `pyproject.toml` konfiguriert pytest:

```toml
[tool.pytest.ini_options]
pythonpath = [".", "src"]
testpaths = ["tests", "packages/*/tests"]
python_files = "test_*.py"
addopts = "-q"
asyncio_mode = "auto"
markers = [
    "unit: fast isolated tests",
    "e2e: end-to-end flows",
]
```

### Hinzufügen neuer Test-Marker

Aktualisieren Sie `pyproject.toml`, um Marker zu registrieren:

```toml
markers = [
    "unit: fast isolated tests",
    "integration: tests with I/O",
    "e2e: end-to-end flows",
    "slow: tests that take >1 second",
]
```

Verwenden Sie Marker in Tests:

```python
import pytest

@pytest.mark.unit
def test_fast():
    pass

@pytest.mark.slow
@pytest.mark.integration
def test_database_migration():
    pass
```

## CI/CD-Integration

### Pre-commit-Prüfungen

Stellen Sie sicher, dass Tests vor dem Commit bestehen:

```bash
# Run linter
uv run ruff check .

# Run type checker
uv run mypy .

# Run tests
uv run -m pytest
```

### GitHub Actions

Tests werden automatisch bei Push/PR via GitHub Actions ausgeführt. Siehe `.github/workflows/` für die Konfiguration.

## Verwandte Dokumentation

- [Konfigurationsbeispiele](../details/configuration/examples.md)
- [Plugin-Entwicklung](plugin_development.mdx)
- [Benutzerdefinierte Adapter](../integration/custom_adapters.md)
- [AGENTS.md](../../../../AGENTS.md) – Autoritative Teststrukturregeln