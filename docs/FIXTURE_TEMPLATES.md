# Common Fixture Templates

This file provides copy-paste templates for common fixture patterns.

## Configuration Fixtures

### Minimal Configuration

```python
@pytest.fixture
def minimal_config(tmp_path: Path) -> Path:
    """Minimal valid configuration for testing."""
    config_content = """
open_ticket_ai:
  plugins: []
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")
    return config_path
```

### Configuration with Plugins

```python
@pytest.fixture
def config_with_plugins(tmp_path: Path) -> Path:
    """Configuration with plugins enabled."""
    config_content = """
open_ticket_ai:
  plugins:
    - plugin_name_1
    - plugin_name_2
  general_config:
    logging:
      version: 1
  defs: []
  orchestrator:
    runners: []
    """
    config_path = tmp_path / "config.yml"
    config_path.write_text(config_content.strip(), encoding="utf-8")
    return config_path
```

### Configuration Factory

```python
@pytest.fixture
def config_factory(tmp_path: Path):
    """Factory for creating custom configurations."""
    def factory(plugins: list[str] | None = None, **overrides) -> Path:
        config = {
            "open_ticket_ai": {
                "plugins": plugins or [],
                "general_config": {"logging": {"version": 1}},
                "defs": [],
                "orchestrator": {"runners": []},
            }
        }
        
        # Apply overrides
        for key, value in overrides.items():
            config["open_ticket_ai"][key] = value
        
        config_path = tmp_path / f"config_{len(list(tmp_path.glob('*.yml')))}.yml"
        config_path.write_text(yaml.dump(config), encoding="utf-8")
        return config_path
    
    return factory
```

## Mock Service Fixtures

### Basic Mock Service

```python
@pytest.fixture
def mock_service() -> MagicMock:
    """Mock external service with common methods."""
    mock = MagicMock()
    mock.fetch_data.return_value = {"status": "success"}
    mock.update_data.return_value = True
    return mock
```

### Async Mock Service

```python
@pytest.fixture
def mock_async_service() -> MagicMock:
    """Mock async service with coroutine methods."""
    mock = MagicMock()
    mock.fetch_data = AsyncMock(return_value={"status": "success"})
    mock.update_data = AsyncMock(return_value=True)
    mock.delete_data = AsyncMock(return_value=True)
    return mock
```

### Mock with Side Effects

```python
@pytest.fixture
def mock_service_with_side_effects() -> MagicMock:
    """Mock service that simulates different responses."""
    mock = MagicMock()
    
    # First call succeeds, second fails, third succeeds
    mock.process.side_effect = [
        {"status": "success"},
        Exception("Service unavailable"),
        {"status": "success"},
    ]
    
    return mock
```

## Test Data Fixtures

### Sample Entities

```python
@pytest.fixture
def sample_ticket() -> UnifiedTicket:
    """Sample ticket for testing."""
    return UnifiedTicket(
        id="TICKET-123",
        subject="Test Ticket",
        body="This is a test ticket",
        state=UnifiedEntity(id="1", name="Open"),
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
        created="2024-01-01T00:00:00Z",
        owner=UnifiedEntity(id="1", name="user@example.com"),
    )
```

### Sample Data List

```python
@pytest.fixture
def sample_tickets() -> list[UnifiedTicket]:
    """Multiple sample tickets for testing."""
    return [
        UnifiedTicket(
            id=f"TICKET-{i}",
            subject=f"Test Ticket {i}",
            body=f"Body {i}",
            state=UnifiedEntity(id="1", name="Open"),
            queue=UnifiedEntity(id="1", name="Support"),
            priority=UnifiedEntity(id="3", name="Medium"),
        )
        for i in range(1, 6)
    ]
```

### Sample Data from File

```python
@pytest.fixture
def sample_data_from_file() -> dict:
    """Load sample data from JSON file."""
    data_file = Path(__file__).parent / "data" / "sample_data.json"
    with open(data_file) as f:
        return json.load(f)
```

## Database Fixtures

### In-Memory Database

```python
@pytest.fixture
def in_memory_db():
    """In-memory database for testing."""
    db = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(db)
    
    yield db
    
    db.dispose()
```

### Database with Sample Data

```python
@pytest.fixture
def db_with_data(in_memory_db):
    """Database pre-populated with test data."""
    session = Session(in_memory_db)
    
    # Add sample data
    session.add(User(id=1, name="Test User"))
    session.add(Ticket(id=1, title="Test Ticket", user_id=1))
    session.commit()
    
    yield session
    
    session.close()
```

## Temporary Resource Fixtures

### Temporary Directory with Files

```python
@pytest.fixture
def temp_directory_with_files(tmp_path: Path) -> Path:
    """Temporary directory with sample files."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    
    # Create sample files
    (test_dir / "file1.txt").write_text("Sample content 1")
    (test_dir / "file2.txt").write_text("Sample content 2")
    
    subdir = test_dir / "subdir"
    subdir.mkdir()
    (subdir / "file3.txt").write_text("Sample content 3")
    
    return test_dir
```

### Temporary Configuration Files

```python
@pytest.fixture
def temp_config_files(tmp_path: Path) -> dict[str, Path]:
    """Multiple temporary configuration files."""
    configs = {}
    
    for name, content in [
        ("minimal", "key: value"),
        ("full", "key: value\nother: data"),
    ]:
        path = tmp_path / f"{name}.yml"
        path.write_text(content)
        configs[name] = path
    
    return configs
```

## Factory Fixtures

### Generic Factory Pattern

```python
@pytest.fixture
def entity_factory():
    """Factory for creating customized entities."""
    def factory(entity_type: str = "default", **kwargs):
        defaults = {
            "id": "test-id",
            "name": "Test Entity",
            "created": "2024-01-01T00:00:00Z",
        }
        defaults.update(kwargs)
        return Entity(**defaults)
    
    return factory
```

### Parameterized Factory

```python
@pytest.fixture
def pipe_config_factory():
    """Factory for creating pipe configurations with variants."""
    def factory(
        pipe_id: str = "test_pipe",
        pipe_use: str = "DefaultPipe",
        when: bool = True,
        **extra_config
    ) -> dict:
        config = {
            "id": pipe_id,
            "use": pipe_use,
            "when": when,
            "steps": [],
        }
        config.update(extra_config)
        return config
    
    return factory
```

## Cleanup Fixtures

### Fixture with Cleanup

```python
@pytest.fixture
def resource_with_cleanup():
    """Resource that requires cleanup after test."""
    resource = create_resource()
    resource.initialize()
    
    yield resource
    
    # Cleanup
    resource.cleanup()
    resource.close()
```

### Fixture with Exception Handling

```python
@pytest.fixture
def safe_resource():
    """Resource with safe cleanup even on errors."""
    resource = None
    try:
        resource = create_resource()
        yield resource
    finally:
        if resource:
            resource.close()
```

## Scoped Fixtures

### Module-Scoped Fixture

```python
@pytest.fixture(scope="module")
def expensive_resource():
    """Resource shared across all tests in module."""
    resource = create_expensive_resource()
    
    yield resource
    
    resource.cleanup()
```

### Session-Scoped Fixture

```python
@pytest.fixture(scope="session")
def global_resource():
    """Resource shared across entire test session."""
    resource = create_very_expensive_resource()
    
    yield resource
    
    resource.cleanup()
```

## Parameterized Fixtures

### Simple Parameterization

```python
@pytest.fixture(params=["option1", "option2", "option3"])
def configuration_variant(request):
    """Test against multiple configuration variants."""
    return request.param
```

### Complex Parameterization

```python
@pytest.fixture(params=[
    {"type": "sqlite", "connection": ":memory:"},
    {"type": "postgresql", "connection": "postgres://test"},
])
def database_config(request):
    """Test against multiple database types."""
    return request.param
```

## Autouse Fixtures

### Setup Fixture

```python
@pytest.fixture(autouse=True)
def setup_environment():
    """Automatically run before each test."""
    # Setup
    os.environ["TEST_MODE"] = "true"
    
    yield
    
    # Cleanup
    os.environ.pop("TEST_MODE", None)
```

### Reset State Fixture

```python
@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test."""
    GlobalState.reset()
    yield
    GlobalState.reset()
```

## Fixture Composition

### Fixture Using Other Fixtures

```python
@pytest.fixture
def complex_fixture(mock_service, sample_data, tmp_config):
    """Fixture composed from multiple other fixtures."""
    return {
        "service": mock_service,
        "data": sample_data,
        "config": load_config(tmp_config),
    }
```

### Fixture Chain

```python
@pytest.fixture
def base_fixture():
    """Base fixture providing foundation."""
    return {"base": "data"}


@pytest.fixture
def derived_fixture(base_fixture):
    """Fixture building on base fixture."""
    base_fixture["derived"] = "additional data"
    return base_fixture
```

## Async Fixtures

### Basic Async Fixture

```python
@pytest.fixture
async def async_resource():
    """Async fixture for async tests."""
    resource = await create_async_resource()
    
    yield resource
    
    await resource.cleanup()
```

### Async Fixture with Setup

```python
@pytest.fixture
async def initialized_async_service():
    """Async service with initialization."""
    service = AsyncService()
    await service.initialize()
    await service.connect()
    
    yield service
    
    await service.disconnect()
    await service.shutdown()
```

## Best Practices

### Documented Fixture

```python
@pytest.fixture
def well_documented_fixture(dependency_fixture) -> ReturnType:
    """Clear, concise description of fixture purpose.
    
    Longer description if needed explaining what the fixture provides,
    when to use it, and any important details about its behavior.
    
    Args:
        dependency_fixture: Description of dependency
    
    Returns:
        Description of what is returned
        
    Example:
        def test_something(well_documented_fixture):
            result = do_something(well_documented_fixture)
            assert result
    """
    return create_fixture_value()
```

### Fixture with Type Hints

```python
from typing import Generator

@pytest.fixture
def typed_fixture() -> Generator[MyType, None, None]:
    """Fixture with proper type hints."""
    resource = MyType()
    
    yield resource
    
    resource.cleanup()
```

## Using These Templates

1. Copy the template that matches your needs
2. Rename the fixture appropriately
3. Customize the implementation
4. Add to appropriate conftest.py
5. Document the fixture in FIXTURES.md
6. Update tests to use the new fixture

## See Also

- [FIXTURES.md](./FIXTURES.md) - Complete fixture reference
- [Testing Guide](./raw_en_docs/en/guides/testing.md) - Testing best practices
- [AGENTS.md](../AGENTS.md) - Test structure requirements
