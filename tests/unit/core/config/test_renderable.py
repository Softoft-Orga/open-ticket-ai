from pydantic import BaseModel

from open_ticket_ai.core.config.registerable import Renderable


class SimpleParams(BaseModel):
    name: str
    value: int


class SimpleConfig(Renderable[SimpleParams]):
    pass


def test_renderable_with_typed_params() -> None:
    params = SimpleParams(name="test", value=42)
    config = SimpleConfig(id="my-config", params=params)

    assert config.id == "my-config"
    assert isinstance(config.params, SimpleParams)
    assert config.params.name == "test"
    assert config.params.value == 42


def test_renderable_with_dict_params() -> None:
    config = SimpleConfig(id="my-config", params={"name": "test", "value": 42})

    assert config.id == "my-config"
    assert config.params.name == "test"
    assert config.params.value == 42


def test_renderable_backward_compatibility() -> None:
    config = Renderable(id="generic")

    assert config.id == "generic"
    assert config.params == {}
