# Testing Guide

Guide to testing Open Ticket AI configurations, pipelines, and custom components.

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
    assert result.success
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
    
    assert result.success
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
    assert fetch_result.success
    
    classify_result = classify_pipe.execute(context)
    assert classify_result.success
    
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
            tickets[0].id,
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
    
    # Create and run pipeline
    pipeline = create_pipeline(config)
    result = pipeline.run()
    
    # Verify success
    assert result.success
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
    assert result.success
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
    classifier.classify.return_value = {
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

## Related Documentation

- [Configuration Examples](../configuration/examples.md)
- [Plugin Development](../plugins/plugin_development.md)
- [Custom Adapters](../integration/custom_adapters.md)
