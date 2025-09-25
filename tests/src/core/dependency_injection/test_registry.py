import pathlib
import sys

import pytest
from pydantic import BaseModel

from open_ticket_ai.src.core.config.config_models import ProvidableConfig

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

# Stub pretty_print_config to avoid yaml dependency during imports
import types

dummy_pp = types.ModuleType("open_ticket_ai.src.core.util.pretty_print_config")
dummy_pp.pretty_print_config = lambda config, console: None
sys.modules["open_ticket_ai.src.core.util.pretty_print_config"] = dummy_pp

from open_ticket_ai.src.core.dependency_injection.registry import Registry
from open_ticket_ai.src.core.mixins.registry_providable_instance import Providable
from open_ticket_ai.src.core.pipeline.pipe import Pipe


class DummyProvidable(Providable):
    """Simple providable used for registry tests."""

    def __init__(self, config):  # pragma: no cover - not used
        self.config = config

    @classmethod
    def get_description(cls) -> str:
        return "dummy providable"


class DummyPipe(Pipe[ProvidableConfig, BaseModel, BaseModel]):
    """Pipe subclass for type checking tests."""

    InputDataType = BaseModel
    OutputDataType = BaseModel

    def __init__(self, config):  # pragma: no cover - not used
        self.config = config

    def process(self, context):  # pragma: no cover - not used
        return context

    @classmethod
    def get_description(cls) -> str:
        return "dummy pipe"


def test_register_and_get_returns_class():
    registry = Registry()
    registry.register(DummyProvidable)
    assert registry.get("DummyProvidable", Providable) is DummyProvidable


def test_get_with_unknown_key_raises_key_error():
    registry = Registry()
    with pytest.raises(KeyError):
        registry.get("missing", Providable)


def test_get_with_wrong_type_raises_type_error():
    registry = Registry()
    registry.register(DummyProvidable)
    with pytest.raises(TypeError):
        registry.get("DummyProvidable", DummyPipe)


def test_contains_and_keys_and_description():
    registry = Registry()
    registry.register(DummyProvidable)
    assert registry.contains("DummyProvidable")
    assert registry.get_all_registry_keys() == ["DummyProvidable"]
    # description should mention provider key and description
    desc = registry.get_registry_types_descriptions()
    assert "DummyProvidable" in desc and "dummy providable" in desc


def test_get_type_from_key_unknown_raises_key_error():
    registry = Registry()
    with pytest.raises(KeyError):
        registry.get_type_from_key("unknown")
