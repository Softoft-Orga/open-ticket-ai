# Pytest Fixture Templates

This document provides common patterns and templates for creating pytest fixtures in the Open Ticket AI project.

## Naming Conventions

Follow these naming conventions for fixtures:

- `mock_*` - Mock objects and services
- `sample_*` - Sample data and inputs
- `tmp_*` - Temporary resources (files, directories)
- `empty_*` - Empty/minimal instances
- `*_factory` - Factory fixtures that create instances

## Common Fixture Patterns

### Mock Service Fixtures

Use for mocking external services or dependencies:

```python
from unittest.mock import MagicMock, AsyncMock
import pytest

@pytest.fixture
def mock_ticket_service() -> MagicMock:
    """Mock ticket service for testing."""
    service = MagicMock()
    service.get_ticket.return_value = {"id": "123", "subject": "Test"}
    service.create_ticket.return_value = {"id": "456"}
    return service

@pytest.fixture
def mock_async_client() -> AsyncMock:
    """Mock async HTTP client."""
    client = AsyncMock()
    client.get.return_value.status_code = 200
    client.get.return_value.json.return_value = {"data": "test"}
    return client
```

### Sample Data Fixtures

Use for providing test data:

```python
import pytest

@pytest.fixture
def sample_ticket() -> dict[str, str]:
    """Sample ticket data."""
    return {
        "id": "TICKET-123",
        "subject": "Test Subject",
        "description": "Test Description",
        "priority": "high",
        "status": "open"
    }

@pytest.fixture
def sample_tickets() -> list[dict[str, str]]:
    """List of sample tickets."""
    return [
        {"id": "TICKET-1", "subject": "First", "priority": "high"},
        {"id": "TICKET-2", "subject": "Second", "priority": "medium"},
        {"id": "TICKET-3", "subject": "Third", "priority": "low"},
    ]
```

### Temporary Resource Fixtures

Use for temporary files, directories, or other resources:

```python
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

@pytest.fixture
def tmp_config_file(tmp_path: Path) -> Path:
    """Create a temporary config file."""
    config_file = tmp_path / "config.yml"
    config_file.write_text("""
server:
  host: localhost
  port: 8080
""")
    return config_file

@pytest.fixture
def tmp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace with structure."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "input").mkdir()
    (workspace / "output").mkdir()
    return workspace
```

### Empty/Minimal Instance Fixtures

Use for creating minimal valid instances:

```python
import pytest
from pydantic import BaseModel

class TicketConfig(BaseModel):
    """Ticket configuration model."""
    max_priority: int = 5
    auto_assign: bool = False

@pytest.fixture
def empty_ticket_config() -> TicketConfig:
    """Empty ticket config with defaults."""
    return TicketConfig()

@pytest.fixture
def minimal_ticket() -> dict[str, str]:
    """Minimal valid ticket data."""
    return {
        "id": "MIN-1",
        "subject": "Minimal",
    }
```

### Factory Fixtures

Use for creating multiple instances with variations:

```python
import pytest
from typing import Callable

@pytest.fixture
def ticket_factory() -> Callable[[str], dict[str, str]]:
    """Factory for creating tickets."""
    def _create_ticket(
        subject: str,
        priority: str = "medium",
        **kwargs
    ) -> dict[str, str]:
        ticket = {
            "id": f"TICKET-{hash(subject) % 1000}",
            "subject": subject,
            "priority": priority,
        }
        ticket.update(kwargs)
        return ticket
    return _create_ticket

@pytest.fixture
def user_factory() -> Callable[[str], dict[str, str]]:
    """Factory for creating users."""
    counter = 0
    def _create_user(name: str, **kwargs) -> dict[str, str]:
        nonlocal counter
        counter += 1
        user = {
            "id": str(counter),
            "name": name,
            "email": f"{name.lower()}@example.com",
        }
        user.update(kwargs)
        return user
    return _create_user
```

### Database/Model Fixtures

Use for setting up database state or model instances:

```python
import pytest
from pydantic import BaseModel

class Ticket(BaseModel):
    """Ticket model."""
    id: str
    subject: str
    priority: str = "medium"

@pytest.fixture
def sample_ticket_model() -> Ticket:
    """Sample ticket model instance."""
    return Ticket(
        id="TICKET-123",
        subject="Test Ticket",
        priority="high"
    )

@pytest.fixture
def sample_ticket_models() -> list[Ticket]:
    """List of sample ticket model instances."""
    return [
        Ticket(id=f"TICKET-{i}", subject=f"Ticket {i}")
        for i in range(1, 4)
    ]
```

### Dependency Injection Fixtures

Use for setting up injected dependencies:

```python
import pytest
from injector import Injector, Module, provider

class TestModule(Module):
    """Test dependency injection module."""
    
    @provider
    def provide_config(self) -> dict[str, str]:
        return {"env": "test"}

@pytest.fixture
def test_injector() -> Injector:
    """Injector configured for testing."""
    return Injector([TestModule()])
```

## Fixture Scopes

Choose the appropriate scope for your fixture:

- `function` (default) - Run once per test function
- `class` - Run once per test class
- `module` - Run once per test module
- `package` - Run once per test package
- `session` - Run once per test session

Example:

```python
@pytest.fixture(scope="module")
def expensive_resource():
    """Resource that's expensive to create."""
    resource = setup_expensive_resource()
    yield resource
    resource.cleanup()
```

## Parametrized Fixtures

Use for testing multiple scenarios:

```python
import pytest

@pytest.fixture(params=["high", "medium", "low"])
def priority_level(request) -> str:
    """Parametrized priority levels."""
    return request.param

@pytest.fixture(params=[
    {"format": "json", "ext": ".json"},
    {"format": "yaml", "ext": ".yml"},
])
def config_format(request) -> dict[str, str]:
    """Parametrized config formats."""
    return request.param
```

## Autouse Fixtures

Use for setup that should always run:

```python
import pytest

@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test."""
    import os
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture(autouse=True, scope="module")
def configure_logging():
    """Configure logging for tests."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
```

## Fixture Dependencies

Fixtures can depend on other fixtures:

```python
import pytest

@pytest.fixture
def database_connection():
    """Database connection."""
    return connect_to_db()

@pytest.fixture
def database_session(database_connection):
    """Database session using connection."""
    session = database_connection.create_session()
    yield session
    session.close()

@pytest.fixture
def populated_database(database_session, sample_tickets):
    """Database populated with sample data."""
    for ticket in sample_tickets:
        database_session.insert(ticket)
    database_session.commit()
    return database_session
```

## Best Practices

1. **Document all fixtures** with clear docstrings
2. **Keep fixtures focused** - one responsibility per fixture
3. **Use appropriate scopes** to optimize test performance
4. **Clean up resources** using yield or finalizers
5. **Avoid fixture interdependencies** when possible
6. **Use factories** for variations instead of many similar fixtures
7. **Check existing fixtures** before creating new ones: `uv run -m pytest --fixtures`
8. **Keep fixtures close to tests** that use them
9. **Use conftest.py** for shared fixtures across multiple test files
10. **Name fixtures clearly** to indicate their purpose

## Checking Existing Fixtures

Before creating a new fixture, check what's already available:

```bash
# List all available fixtures
uv run -m pytest --fixtures

# List fixtures with full docstrings
uv run -m pytest --fixtures -v

# List fixtures from specific conftest
uv run -m pytest --fixtures tests/conftest.py
```

## Example: Complete Test with Fixtures

```python
import pytest

@pytest.fixture
def mock_classifier():
    """Mock ticket classifier."""
    from unittest.mock import MagicMock
    classifier = MagicMock()
    classifier.classify.return_value = "bug"
    return classifier

@pytest.fixture
def sample_ticket():
    """Sample ticket for classification."""
    return {
        "subject": "Application crashes on startup",
        "description": "The app crashes when I try to open it",
    }

def test_ticket_classification(mock_classifier, sample_ticket):
    """Test ticket classification with fixtures."""
    result = mock_classifier.classify(sample_ticket)
    assert result == "bug"
    mock_classifier.classify.assert_called_once_with(sample_ticket)
```

## See Also

- [pytest fixtures documentation](https://docs.pytest.org/en/stable/fixture.html)
- [pytest parametrize documentation](https://docs.pytest.org/en/stable/parametrize.html)
- Project-specific fixtures in `tests/conftest.py` and `packages/*/tests/conftest.py`
