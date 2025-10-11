import warnings

from open_ticket_ai.core.config.params_config_base import CONTROL_KEYS, ParamsConfigBase


def test_params_config_base_params_field_exists() -> None:
    config = ParamsConfigBase(params={"key": "value"})
    assert config.params == {"key": "value"}


def test_params_config_base_params_defaults_to_empty_dict() -> None:
    config = ParamsConfigBase()
    assert config.params == {}


def test_params_config_base_with_nested_params() -> None:
    config = ParamsConfigBase(
        params={
            "model": "my-model",
            "confidence": 0.8,
            "nested": {"key": "value"},
        }
    )
    assert config.params["model"] == "my-model"
    assert config.params["confidence"] == 0.8
    assert config.params["nested"]["key"] == "value"


def test_params_config_base_auto_migration() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ParamsConfigBase(my_field="value", another_field=42)

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "my_field" in str(w[0].message)
        assert "another_field" in str(w[0].message)

        assert config.params == {"my_field": "value", "another_field": 42}


def test_params_config_base_control_keys_not_migrated() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ParamsConfigBase(id="test", use="SomePipe")

        assert len(w) == 0
        assert config.params == {}


def test_params_config_base_mixed_params_and_top_level_fields_warns() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ParamsConfigBase(
            params={"field1": "value1"},
            field2="value2",
        )

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "field2" in str(w[0].message)
        assert "ignored" in str(w[0].message).lower()

        assert config.params == {"field1": "value1"}


def test_params_config_base_no_warnings_with_params() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ParamsConfigBase(
            params={"field1": "value1", "field2": "value2"}
        )

        assert len(w) == 0
        assert config.params == {"field1": "value1", "field2": "value2"}


def test_control_keys_includes_expected_fields() -> None:
    expected_keys = {
        "id",
        "uid",
        "use",
        "steps",
        "depends_on",
        "if",
        "params",
        "injects",
        "triggers",
        "on",
        "pipe",
        "settings",
    }
    assert expected_keys == CONTROL_KEYS


def test_params_config_base_extra_fields_allowed() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        config = ParamsConfigBase(
            params={"key": "value"},
            custom_field="custom_value",
        )

        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert config.custom_field == "custom_value"
        assert config.params == {"key": "value"}
