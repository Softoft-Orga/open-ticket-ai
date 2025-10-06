from __future__ import annotations

import pytest
from open_ticket_ai.open_ticket_ai.core import (
    ConflictingClassRegistration,
    NotRegistered,
    UnifiedRegistry,
)


class _DummyService:
    pass


class _AnotherService:
    pass


@pytest.fixture(autouse=True)
def reset_registry_singleton() -> None:
    UnifiedRegistry._singleton = None  # type: ignore[attr-defined]
    yield
    UnifiedRegistry._singleton = None  # type: ignore[attr-defined]


def test_get_registry_instance_returns_singleton() -> None:
    first = UnifiedRegistry.get_registry_instance()
    second = UnifiedRegistry.get_registry_instance()

    assert first is second


def test_register_and_get_instance_by_class_name() -> None:
    registry = UnifiedRegistry.get_registry_instance()
    instance = _DummyService()

    returned = registry.register_instance(instance)

    assert returned is instance
    assert registry.get_instance("_DummyService") is instance


def test_get_instance_raises_not_registered_for_unknown_service() -> None:
    registry = UnifiedRegistry.get_registry_instance()

    with pytest.raises(NotRegistered) as exc:
        registry.get_instance("_UnknownService")

    assert "_UnknownService" in str(exc.value)


def test_register_instance_raises_for_conflicting_registration() -> None:
    registry = UnifiedRegistry.get_registry_instance()
    registry.register_instance(_AnotherService())

    with pytest.raises(ConflictingClassRegistration):
        registry.register_instance(_AnotherService())
