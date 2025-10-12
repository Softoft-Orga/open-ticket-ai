import warnings

from open_ticket_ai.core.pipeline.pipe_config import PipeConfig


def test_pipe_config_params_field_exists() -> None:
    config = PipeConfig(id="test", params={"key": "value"})
    assert config.params == {"key": "value"}


def test_pipe_config_params_defaults_to_empty_dict() -> None:
    config = PipeConfig(id="test")
    assert config.params == {}


def test_pipe_config_with_nested_params() -> None:
    config = PipeConfig(
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


def test_pipe_config_backwards_compatibility_auto_migration() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = PipeConfig(id="test", queue_model="my-model", min_confidence=0.8)

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "queue_model" in str(w[0].message)
        assert "min_confidence" in str(w[0].message)

        assert config.params == {"queue_model": "my-model", "min_confidence": 0.8}


def test_pipe_config_control_fields_not_migrated() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = PipeConfig(id="test", use="SomePipe", depends_on=["other"])

        assert len(w) == 0
        assert config.params == {}
        assert config.use == "SomePipe"
        assert config.depends_on == ["other"]


def test_pipe_config_mixed_params_and_top_level_fields_warns() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = PipeConfig(
            id="test",
            params={"queue_model": "my-model"},
            min_confidence=0.8,
        )

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "min_confidence" in str(w[0].message)

        assert config.params == {"queue_model": "my-model"}


def test_pipe_config_new_style_no_warnings() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = PipeConfig(
            id="test",
            use="SomePipe",
            params={"queue_model": "my-model", "min_confidence": 0.8},
        )

        assert len(w) == 0
        assert config.params == {"queue_model": "my-model", "min_confidence": 0.8}
