---
description: Comprehensive testing guide for Open Ticket AI configurations, pipelines, and custom components with best practices and configExamples.
---

# Testing Guide

Guide to testing Open Ticket AI configurations, pipelines, and custom components.

## Testing Philosophy

Write tests that focus on **core functionality and contracts**, not implementation details:

### DO ✅

- Test main input/output behavior
- Test error handling and edge cases that matter
- Test public interfaces and contracts
- Focus on "what" the code does, not "how"
- Keep tests simple and maintainable

### DON'T ❌

- Don't test trivial getters/setters
- Don't assert every field value in complex objects
- Don't duplicate test logic across multiple files
- Don't test private implementation details
- Don't create excessive edge case tests that don't add value

### Example: Good vs Bad

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

## Testing Overview

Open Ticket AI supports multiple testing levels:

- **Unit Tests**: Individual components
- **Integration Tests**: Component interactions
- **Contract Tests**: Interface compliance
- **E2E Tests**: Complete workflows

## Unit Tests

### Testing Pipes

Test individual pipe logic:

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

### Testing Services

Test service implementations:

```python
from my_plugin.services import MyService

def test_my_service():
    service = MyService()
    result = service.process(input_data)
    assert result == expected_result
```

### Using Mocks

Mock external dependencies:

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

### Testing Pipe Chains

Test multiple pipes together:

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

### Testing with Real Services

Test against actual APIs (test environment):

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

### Verifying Interface Implementation

Test that components implement required interfaces:

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

### Testing Method Signatures

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

### Testing Complete Workflows

Test entire pipeline execution:

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

### Configuration Testing

Test various configurations:

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

## Running Test Suite

### With pytest

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

### With Test Categories

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

Run specific categories:

```bash
# Only unit tests
uv run -m pytest -m unit

# Integration and e2e
uv run -m pytest -m "integration or e2e"

# Everything except slow
uv run -m pytest -m "not slow"
```

## Test Configuration

### pytest.ini Configuration

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

### Test Fixtures

Create reusable fixtures:

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

## Testing Best Practices

### Do:

- Write tests for new features
- Test error conditions
- Use descriptive test names
- Keep tests independent
- Use fixtures for setup
- Mock external dependencies
- Test edge cases

### Don't:

- Skip tests
- Write flaky tests
- Depend on test order
- Use production data
- Ignore test failures
- Test implementation details
- Write untestable code

## Continuous Integration

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

## Test Data Management

### Using Test Data Files

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

### Test Data Organization

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

## Debugging Tests

### Using pytest debugger

```bash
# Drop into debugger on failure
uv run -m pytest --pdb

# Drop into debugger at start
uv run -m pytest --trace
```

### Print debugging

```python
def test_with_debug():
    result = some_function()
    print(f"Result: {result}")  # Will show with -s flag
    assert result == expected
```

Run with output:

```bash
uv run -m pytest -s
```

## Test Structure and Organization

### Repository Test Layout

Open Ticket AI follows a strict test organization pattern compliant with `AGENTS.md`:

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

### Critical Rules

**NEVER** place tests under `src/`:

- ❌ `src/**/tests/`
- ❌ `src/**/test_*.py`
- ✅ `tests/` or `packages/*/tests/`

**Test file naming**:

- ✅ `test_*.py`
- ❌ `*_test.py`

**Test directories**:

- ❌ Do NOT add `__init__.py` to test directories
- ✅ Test directories are NOT Python packages

### Where to Place Tests

| Test Type                     | Location                             | Purpose                                        |
|-------------------------------|--------------------------------------|------------------------------------------------|
| **Package Unit**              | `packages/<name>/tests/unit/`        | Fast, isolated tests for package code          |
| **Package Integration**       | `packages/<name>/tests/integration/` | Tests touching I/O or package boundaries       |
| **Root Unit**                 | `tests/unit/`                        | Tests for root package (`src/open_ticket_ai/`) |
| **Cross-Package Integration** | `tests/integration/`                 | Tests spanning multiple packages               |
| **End-to-End**                | `tests/e2e/`                         | Complete workflow tests                        |

### Test Data Management

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

## Conftest Files and Fixtures

### Conftest Hierarchy

The project uses a three-level conftest hierarchy:

```
tests/conftest.py              # Workspace-level (shared by all)
tests/unit/conftest.py         # Unit test level
tests/unit/core/conftest.py    # Core module level
packages/*/tests/conftest.py   # Package-level
```

**Fixture Resolution Order:**

1. Test file itself
2. Nearest conftest.py (same directory)
3. Parent conftest.py files (up the tree)
4. pytest built-in fixtures

### Workspace-Level Fixtures (tests/conftest.py)

These fixtures are available to ALL tests across the entire workspace:

```python
@pytest.fixture
def tmp_config(tmp_path: Path) -> Path:
    """Create a temporary configuration file for testing.

    Available to all tests in workspace.
    Used for testing configuration loading.
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
    """Provide a configured dependency injector for testing.

    Uses tmp_config fixture to create a test injector.
    """
    from injector import Injector
    from open_ticket_ai.core import AppModule

    return Injector([AppModule(tmp_config)])


@pytest.fixture
def test_config(tmp_config: Path) -> RawOpenTicketAIConfig:
    """Load test configuration for validation."""
    from open_ticket_ai.core import load_config

    return load_config(tmp_config)
```

### Unit Test Fixtures (tests/unit/conftest.py)

Fixtures specific to unit tests:

```python
@pytest.fixture
def empty_pipeline_context() -> Context:
    """Empty pipes context for testing."""
    return Context(pipes={}, config={})


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    """Mock ticket system service with common async methods."""
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mocked_ticket_system() -> MockedTicketSystem:
    """Stateful mock ticket system with sample data.

    Includes pre-populated tickets for testing ticket operations.
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

### Package-Level Fixtures

Each package can define its own fixtures:

```python
# packages/otai_hf_local/tests/conftest.py

@pytest.fixture
def mock_hf_model():
    """Mock Hugging Face model for testing."""
    return MagicMock(spec=TextClassificationPipeline)


@pytest.fixture
def sample_classification_config():
    """Sample configuration for text classification."""
    return {
        "model_name": "bert-base-uncased",
        "threshold": 0.7,
    }
```

### Fixture Naming Conventions

Follow these naming patterns for consistency:

| Pattern     | Purpose                 | Example                                         |
|-------------|-------------------------|-------------------------------------------------|
| `mock_*`    | Mock objects            | `mock_ticket_system_service`                    |
| `sample_*`  | Sample data             | `sample_ticket`, `sample_classification_config` |
| `tmp_*`     | Temporary resources     | `tmp_config`, `tmp_path`                        |
| `empty_*`   | Empty/minimal instances | `empty_pipeline_context`                        |
| `*_factory` | Factory functions       | `pipe_config_factory`                           |

### Fixture Scope

Choose appropriate scope for fixtures:

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

### Factory Fixtures

Use factory fixtures when tests need customized instances:

```python
@pytest.fixture
def pipe_config_factory():
    """Factory for creating pipe configurations with custom values."""

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
    """Use factory to create custom configuration."""
    config = pipe_config_factory(id="special_pipe", when=False)
    assert config["id"] == "special_pipe"
    assert config["when"] is False
```

### Fixture Cleanup

Use `yield` for fixtures requiring cleanup:

```python
@pytest.fixture
def database_connection():
    """Provide database connection with automatic cleanup."""
    conn = create_connection()
    yield conn
    conn.close()


@pytest.fixture
def temp_directory(tmp_path):
    """Create temporary directory with files."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()

    yield test_dir

    # Cleanup happens automatically with tmp_path
```

### Avoiding Fixture Duplication

**Before adding a new fixture:**

1. Check existing conftest files
2. Search for similar fixtures: `grep -r "def fixture_name" tests/`
3. Consider if an existing fixture can be reused
4. Document fixture purpose clearly

**Example of consolidation:**

```python
# ❌ Bad: Duplicate fixtures
# tests/conftest.py
@pytest.fixture
def mock_ticket_system_config():
    return {"ticket_system_id": "test"}


# tests/unit/conftest.py
@pytest.fixture
def mock_ticket_system_pipe_config():
    return {"ticket_system_id": "test"}


# ✅ Good: Single, reusable fixture
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

### Discovering Available Fixtures

List all available fixtures for a test:

```bash
# Show fixtures available to unit tests
uv run -m pytest tests/unit/ --fixtures

# Show specific fixture details
uv run -m pytest tests/unit/ --fixtures -v | grep mock_ticket
```

### Common Fixture Patterns

**Configuration Fixtures:**

```python
@pytest.fixture
def minimal_config(tmp_path):
    """Minimal valid configuration."""
    config = {"open_ticket_ai": {"plugins": []}}
    path = tmp_path / "config.yml"
    path.write_text(yaml.dump(config))
    return path
```

**Mock Service Fixtures:**

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

**Parameterized Fixtures:**

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """Test against multiple database types."""
    return request.param
```

## Running Tests

### Basic Commands

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

### With Markers

```bash
# Only unit tests
uv run -m pytest -m unit

# Integration tests
uv run -m pytest -m integration

# E2E tests
uv run -m pytest -m e2e
```

### Test Collection

```bash
# Show what tests would run (don't execute)
uv run -m pytest --collect-only

# Verbose collection
uv run -m pytest --collect-only -v
```

## Pytest Configuration

The project's `pyproject.toml` configures pytest:

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

### Adding New Test Markers

Update `pyproject.toml` to register markers:

```toml
markers = [
    "unit: fast isolated tests",
    "integration: tests with I/O",
    "e2e: end-to-end flows",
    "slow: tests that take >1 second",
]
```

Use markers in tests:

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

## CI/CD Integration

### Pre-commit Checks

Ensure tests pass before committing:

```bash
# Run linter
uv run ruff check .

# Run type checker
uv run mypy .

# Run tests
uv run -m pytest
```

### GitHub Actions

Tests run automatically on push/PR via GitHub Actions. Check `.github/workflows/` for configuration.

## Related Documentation

- [Configuration Examples](../details/configuration/examples.md)
- [Plugin Development](plugin_development.md)
- [Custom Adapters](../integration/custom_adapters.md)
- [AGENTS.md](../../../../AGENTS.md) - Authoritative test structure rules
