import warnings
from typing import Any

from open_ticket_ai.core.pipeline.pipe_config import PipeConfig


def test_pipe_config_params_field_exists() -> None:
    config: PipeConfig[Any] = PipeConfig(id="test", params={"key": "value"})
    assert config.params == {"key": "value"}


def test_pipe_config_params_defaults_to_empty_dict() -> None:
    config: PipeConfig[Any] = PipeConfig(id="test")
    assert config.params.model_dump() == {}


def test_pipe_config_with_nested_params() -> None:
    config: PipeConfig[Any] = PipeConfig(
        id="test",
        params={
            "queue_model": "my-model",
            "min_confidence": 0.8,
            "nested": {"key": "value"},
        },
    )
    assert config.params["queue_model"] == "my-model"
    assert config.params["min_confidence"] == 0.8
    assert config.params["nested"]["key"] == "value"


def test_pipe_config_control_fields_not_migrated() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config: PipeConfig[Any] = PipeConfig(id="test", use="SomePipe", depends_on=["other"])

        assert len(w) == 0
        assert config.params.model_dump() == {}
        assert config.use == "SomePipe"
        assert config.depends_on == ["other"]


def test_pipe_config_new_style_no_warnings() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config: PipeConfig[Any] = PipeConfig(
            id="test",
            use="SomePipe",
            params={"queue_model": "my-model", "min_confidence": 0.8},
        )

        assert len(w) == 0
        assert config.params == {"queue_model": "my-model", "min_confidence": 0.8}
