# Test Writing Guidelines

**Location:** `/tests` directory in Open Ticket AI repository  
**Parent Guidelines:** [Root AGENTS.md](../AGENTS.md)  
**Related Documentation:** [Testing Guide](../docs/docs_src/en/developers/testing.md)  
**Last Updated:** 2025-10-14

This document is the **single source of truth** for test-writing practices in the Open Ticket AI project.

## Core Philosophy

Write tests that focus on **behavior and contracts**, not implementation details. Tests should validate that code works correctly, not how it works internally.

## Test Coverage Requirements

### What to Test

Every **public function and method** should have at least one test. Depending on complexity:

- **Simple functions** (1-2 inputs, straightforward logic): 1-2 tests
- **Moderate complexity** (multiple code paths, some edge cases): 2-3 tests  
- **Complex functions** (many branches, error handling, edge cases): 3-5 tests

**Use parametrization** (`@pytest.mark.parametrize`) to test multiple input variations efficiently rather than writing separate test functions.

### What NOT to Test

#### 1. Model Classes and Files

**DO NOT** write tests for files or classes named with `*_model` suffix:

- ❌ `foo_model.py`
- ❌ `bar_model.py`
- ❌ `config_models.py` (unless testing behavior beyond simple data validation)

**Rationale:** These are typically data containers validated by Pydantic. The validation is provided by the framework.

#### 2. Pydantic BaseModel Classes

**DO NOT** write tests for static Pydantic `BaseModel` classes that only define data structure:

```python
# ❌ Do NOT test this
class TicketData(BaseModel):
    id: str
    title: str
    priority: int = 3
```

**Exception:** Test Pydantic models if they have:
- Custom validators (`@field_validator`, `@model_validator`)
- Computed fields (`@computed_field`)
- Custom business logic methods
- Complex default factories

```python
# ✅ DO test this - has custom validation
class TicketData(BaseModel):
    id: str
    priority: int = 3
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError('Priority must be 1-5')
        return v
```

#### 3. Protected and Private Members

**DO NOT** test methods or functions with leading underscore:

- ❌ `_internal_helper()`
- ❌ `_calculate_internal_state()`
- ❌ `__private_method()`

**Rationale:** Private/protected members are implementation details. Test the public API that uses them instead.

#### 4. Trivial Code

**DO NOT** test:
- Simple getters/setters without logic
- Trivial property accessors
- Pass-through methods that just delegate
- Code with no branching logic

**Example of what NOT to test:**

```python
# ❌ Don't test these
@property
def name(self) -> str:
    return self._name

def set_timeout(self, value: int) -> None:
    self._timeout = value
```

## Test Structure and Organization

### File Placement

Follow the strict layout defined in [Root AGENTS.md](../AGENTS.md):

```
tests/
├── unit/              # Fast, isolated unit tests
├── integration/       # Cross-component integration tests
├── e2e/              # End-to-end workflow tests
├── data/             # Test fixtures and golden files
└── conftest.py       # Shared fixtures for all tests
```

**Critical Rules:**
- ✅ Test files: `test_*.py` only
- ❌ Never: `*_test.py`
- ❌ Never: `__init__.py` in test directories
- ❌ Never: tests under `src/` directory

### Test File Structure

```python
from __future__ import annotations

# Standard library imports
import subprocess
import sys
from pathlib import Path

# Third-party imports
import pytest

# First-party imports  
from open_ticket_ai.core.config import RootConfig


def test_simple_behavior() -> None:
    result = function_under_test()
    assert result == expected_value


def test_error_handling() -> None:
    with pytest.raises(ValueError, match="expected error message"):
        function_with_error()


@pytest.mark.parametrize("input_val,expected", [
    ("case1", "result1"),
    ("case2", "result2"),
    ("case3", "result3"),
])
def test_multiple_cases(input_val: str, expected: str) -> None:
    assert process(input_val) == expected
```

## Mocking and Fixtures

### Prefer Fixtures Over Monkeypatching

**DO:** Use pytest fixtures for dependency injection and mocking

```python
# ✅ Good: Fixture-based mock
@pytest.fixture
def mock_classifier():
    """Mock classifier with deterministic responses."""
    mock = Mock()
    mock.classify.return_value = {
        "label": "billing",
        "confidence": 0.85
    }
    return mock


def test_with_fixture(mock_classifier):
    pipe = ClassifyPipe(classifier=mock_classifier)
    result = pipe.execute(context)
    assert result.success
```

**AVOID:** Ad-hoc monkeypatching unless truly necessary

```python
# ⚠️ Less preferred: Monkeypatch
def test_with_monkeypatch(monkeypatch):
    monkeypatch.setattr('module.external_call', lambda: "mocked")
    # Only use when fixture approach isn't practical
```

### Check Existing Fixtures First

Before creating new fixtures, check what's already available:

```bash
uv run -m pytest --fixtures
```

Follow fixture naming conventions:
- `mock_*` - Mock objects
- `sample_*` - Sample data
- `tmp_*` - Temporary resources  
- `empty_*` - Empty/minimal instances
- `*_factory` - Factory functions

See [FIXTURES.md](../docs/FIXTURES.md) and [FIXTURE_TEMPLATES.md](../docs/FIXTURE_TEMPLATES.md) for complete reference.

### Fixture Guidelines

**Good fixture practices:**

```python
@pytest.fixture
def sample_ticket():
    """Provide a sample ticket for testing.
    
    Returns a ticket with minimal required fields set.
    """
    return Ticket(
        id="T-001",
        title="Test ticket",
        status="open"
    )


@pytest.fixture
def ticket_factory():
    """Factory to create customized tickets.
    
    Usage:
        ticket = ticket_factory(status="closed", priority=5)
    """
    def _make_ticket(**overrides):
        defaults = {
            "id": "T-999",
            "title": "Default ticket",
            "status": "open",
            "priority": 3,
        }
        defaults.update(overrides)
        return Ticket(**defaults)
    return _make_ticket
```

**Fixture scope:**
- `scope="function"` (default): New instance per test
- `scope="module"`: One instance per test file
- `scope="session"`: One instance for entire test run

Use broader scopes carefully—only for expensive, read-only resources.

## Testing Best Practices

### DO ✅

1. **Test behavior, not implementation**
   ```python
   # ✅ Test what it does
   def test_user_validation():
       assert validate_user("valid@email.com") is True
       assert validate_user("invalid") is False
   ```

2. **Test public interfaces and contracts**
   ```python
   # ✅ Test the public API
   def test_ticket_adapter_interface():
       adapter = MyAdapter()
       tickets = adapter.fetch_tickets({"status": "open"})
       assert isinstance(tickets, list)
   ```

3. **Test meaningful edge cases**
   ```python
   # ✅ Edge cases that matter
   def test_empty_input():
       assert process([]) == []
   
   def test_single_item():
       assert process([item]) == [transformed_item]
   ```

4. **Use descriptive test names**
   ```python
   # ✅ Clear intent
   def test_classify_assigns_billing_queue_for_invoice_keywords():
       ...
   
   def test_fetch_raises_auth_error_when_token_invalid():
       ...
   ```

5. **Keep tests independent**
   - No test should depend on another test's execution
   - No shared mutable state between tests
   - Each test should set up its own data

6. **Mock external dependencies**
   ```python
   # ✅ Mock network calls, databases, file I/O
   def test_api_call(mock_requests):
       mock_requests.get.return_value.json.return_value = {"data": "mocked"}
       result = fetch_from_api()
       assert result == {"data": "mocked"}
   ```

### DON'T ❌

1. **Don't test trivial field assignments**
   ```python
   # ❌ Bad: Testing Pydantic does its job
   def test_config_fields():
       config = MyConfig(id="test", timeout=30, workers=10)
       assert config.id == "test"
       assert config.timeout == 30
       assert config.workers == 10
   ```

2. **Don't assert every field in complex objects**
   ```python
   # ❌ Bad: Over-asserting
   def test_ticket_creation():
       ticket = create_ticket(data)
       assert ticket.id == "T-001"
       assert ticket.title == "Test"
       assert ticket.status == "open"
       assert ticket.priority == 3
       assert ticket.queue == "general"
       # ... 20 more assertions
   
   # ✅ Good: Assert key behavior
   def test_ticket_creation():
       ticket = create_ticket(data)
       assert ticket.id == "T-001"
       assert ticket.is_valid()  # One assertion about behavior
   ```

3. **Don't test private implementation details**
   ```python
   # ❌ Bad: Testing internal state
   def test_internal_cache():
       processor = Processor()
       processor.process(data)
       assert processor._cache == expected_cache_state
   
   # ✅ Good: Test observable behavior
   def test_processing_is_idempotent():
       processor = Processor()
       result1 = processor.process(data)
       result2 = processor.process(data)
       assert result1 == result2
   ```

4. **Don't create excessive edge case tests**
   ```python
   # ❌ Bad: Over-specific edge cases
   def test_path_with_dots_at_start():
       assert process(".a.b") == expected
   
   def test_path_with_dots_at_end():
       assert process("a.b.") == expected
   
   def test_path_with_double_dots():
       assert process("a..b") == expected
   
   # ✅ Good: Consolidated meaningful cases
   @pytest.mark.parametrize("path,expected", [
       ("a.b.c", {"a": {"b": {"c": "value"}}}),
       ("", "value"),  # Edge: empty
       (".", "value"),  # Edge: special char
   ])
   def test_path_processing(path, expected):
       assert process(path) == expected
   ```

5. **Don't write flaky tests**
   - Avoid time-dependent assertions
   - Don't rely on test execution order
   - Don't use random values without seeding
   - Mock non-deterministic operations

6. **Don't skip or ignore test failures**
   ```python
   # ❌ Bad: Hiding failures
   @pytest.mark.skip("TODO: fix later")
   def test_important_feature():
       ...
   
   # ✅ Good: Fix or document why skipping
   @pytest.mark.skip("Waiting for API v2 - ticket #123")
   def test_api_v2_feature():
       ...
   ```

## Parametrization

Use `@pytest.mark.parametrize` for testing multiple input cases:

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("user@", False),
    ("@example.com", False),
    ("", False),
    ("not-an-email", False),
])
def test_email_validation(email: str, valid: bool) -> None:
    assert validate_email(email) == valid
```

**Benefits:**
- Reduces code duplication
- Makes test cases explicit
- Easy to add new cases
- Better test failure reporting

**When to use:**
- Testing same logic with different inputs
- Boundary value testing
- Error condition variations

## Error Testing

Test error conditions explicitly:

```python
# Test specific exception type
def test_invalid_config_raises_error():
    with pytest.raises(ValueError):
        load_config("invalid.yml")


# Test exception message
def test_error_message_is_helpful():
    with pytest.raises(ValueError, match="Priority must be between 1 and 5"):
        Ticket(priority=10)


# Test multiple error conditions
@pytest.mark.parametrize("invalid_input", [
    None,
    "",
    "   ",
    123,  # Wrong type
])
def test_rejects_invalid_input(invalid_input):
    with pytest.raises((ValueError, TypeError)):
        process(invalid_input)
```

## Integration Testing

Integration tests verify components work together:

```python
@pytest.mark.integration
def test_pipeline_flow():
    """Test complete pipeline execution with real components."""
    # Use real (non-mocked) adapters when possible
    adapter = create_test_adapter()
    classifier = create_test_classifier()
    
    pipeline = Pipeline([
        FetchPipe(adapter),
        ClassifyPipe(classifier),
        UpdatePipe(adapter),
    ])
    
    result = pipeline.execute()
    assert result.success
    assert result.tickets_processed > 0
```

**Integration test guidelines:**
- Mark with `@pytest.mark.integration`
- May be slower than unit tests
- Test real interactions between components
- Use test environments/data, not production

## Documenting Test Omissions

If you intentionally skip testing something, document why:

```python
# Ticket.to_dict() not tested - simple Pydantic .dict() delegation
# ClassifyModel not tested - static Pydantic BaseModel per AGENTS.md
# _internal_cache not tested - private implementation detail per AGENTS.md
```

Reference this AGENTS.md in PR descriptions:
> "Model classes excluded from testing per tests/AGENTS.md guidelines"

## Running Tests

```bash
# All tests
uv run -m pytest

# Specific file
uv run -m pytest tests/unit/core/test_config.py

# Specific test
uv run -m pytest tests/unit/core/test_config.py::test_load_config

# With coverage
uv run -m pytest --cov=open_ticket_ai --cov-report=html

# Only unit tests
uv run -m pytest tests/unit/

# Only integration tests  
uv run -m pytest -m integration

# Verbose output
uv run -m pytest -v

# Show local variables on failure
uv run -m pytest -l

# Stop on first failure
uv run -m pytest -x
```

## Quality Checklist

Before submitting tests, verify:

- [ ] All public functions/methods have at least one test
- [ ] Model classes and static BaseModels are not tested (unless they have custom logic)
- [ ] No tests for private/protected members (prefix `_`)
- [ ] Fixtures are used for mocking dependencies
- [ ] Parametrization is used for multiple similar cases
- [ ] Tests are independent (no cross-test dependencies)
- [ ] Test names clearly describe what is being tested
- [ ] Error conditions are tested with `pytest.raises`
- [ ] No excessive assertions on trivial field values
- [ ] Integration tests are marked with `@pytest.mark.integration`
- [ ] `uv run ruff check .` passes
- [ ] `uv run mypy .` passes
- [ ] `uv run -m pytest` passes

## Summary

**Golden Rules:**

1. **Test behavior, not implementation**
2. **Every public function needs tests**
3. **Skip models, BaseModels, and private members**
4. **Use fixtures for mocking**
5. **Parametrize similar test cases**
6. **Keep tests simple and focused**
7. **Document intentional omissions**

For more examples and patterns, see:
- [Testing Guide](../docs/docs_src/en/developers/testing.md)
- [FIXTURES.md](../docs/FIXTURES.md)
- [FIXTURE_TEMPLATES.md](../docs/FIXTURE_TEMPLATES.md)
- [Root AGENTS.md](../AGENTS.md)
