import pytest

from open_ticket_ai.core.config.errors import InjectableNotFoundError, RegistryError
from open_ticket_ai.core.dependency_injection.component_registry import ComponentRegistry
from tests.unit.conftest import SimpleInjectable, SimplePipe


class DummyNonInjectable:
    pass


class TestRegister:
    def test_register_invalid_class_raises_error(self):
        registry = ComponentRegistry()

        with pytest.raises(RegistryError):
            # noinspection PyTypeChecker
            registry.register("invalid", DummyNonInjectable)


class TestGetPipe:
    def test_get_pipe_success(self):
        registry = ComponentRegistry()
        registry.register("test_pipe", SimplePipe)

        result = registry.get_pipe(by_identifier="test_pipe")

        assert result == SimplePipe

    def test_get_pipe_not_found_raises_error(self):
        registry = ComponentRegistry()

        with pytest.raises(InjectableNotFoundError, match="not found in the ComponentRegistry"):
            registry.get_pipe(by_identifier="nonexistent_pipe")


class TestGetInjectable:
    def test_get_injectable_success(self):
        registry = ComponentRegistry()
        # noinspection PyTypeChecker
        registry.register("test_service", SimpleInjectable)

        result = registry.get_injectable(by_identifier="test_service")

        assert result == SimpleInjectable

    def test_get_injectable_not_found_raises_error(self):
        registry = ComponentRegistry()

        with pytest.raises(InjectableNotFoundError):
            registry.get_injectable(by_identifier="nonexistent_service")


class TestFindByType:
    def test_find_by_type_success(self):
        registry = ComponentRegistry()
        registry.register("pipe1", SimplePipe)
        registry.register("service1", SimpleInjectable)

        result = registry.find(by_type=SimplePipe)

        assert "pipe1" in result
        assert result["pipe1"] == SimplePipe
        assert "service1" not in result

    def test_find_by_type_empty_when_no_matches(self):
        registry = ComponentRegistry()
        registry.register("service1", SimpleInjectable)

        result = registry.find(by_type=SimplePipe)

        assert result == {}


class TestGetAvailableInjectables:
    def test_get_available_injectables_returns_all(self):
        registry = ComponentRegistry()
        registry.register("pipe1", SimplePipe)
        registry.register("service1", SimpleInjectable)

        result = registry.get_available_injectables()

        assert "service1" in result
        assert "pipe1" in result
        assert len(result) == 2

    def test_get_available_injectables_empty_when_empty(self):
        registry = ComponentRegistry()

        result = registry.get_available_injectables()

        assert list(result) == []
