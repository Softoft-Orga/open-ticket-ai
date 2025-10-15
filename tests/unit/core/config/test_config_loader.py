from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from open_ticket_ai.core.config.config_loader import ConfigLoader
from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


def _minimal_valid_config() -> dict:
    return {"open_ticket_ai": {"infrastructure": {"default_template_renderer": "test_renderer"}}}


@pytest.mark.parametrize(
    "config_data,expected_error",
    [
        (_minimal_valid_config(), None),
        (
            {
                "open_ticket_ai": {
                    "plugins": [],
                    "infrastructure": {"default_template_renderer": "test_renderer"},
                }
            },
            None,
        ),
        ({"wrong_key": {}}, ValueError),
        (None, ValueError),
        ({"open_ticket_ai": {"infrastructure": {"default_template_renderer": None}}}, ValidationError),
    ],
)
def test_load_config_validation(
    config_loader: ConfigLoader, tmp_path: Path, config_data: dict | None, expected_error: type | None
) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    if expected_error is None:
        result = config_loader.load_config(config_file)
        assert isinstance(result, RawOpenTicketAIConfig)
    else:
        with pytest.raises(expected_error):
            config_loader.load_config(config_file)


def test_load_config_file_not_found(config_loader: ConfigLoader, tmp_path: Path) -> None:
    nonexistent = tmp_path / "nonexistent.yml"
    with pytest.raises(FileNotFoundError):
        config_loader.load_config(nonexistent)


@pytest.mark.parametrize(
    "use_env_var",
    [True, False],
)
def test_load_config_path_resolution(
    config_loader: ConfigLoader, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, use_env_var: bool
) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(_minimal_valid_config()))
    if use_env_var:
        monkeypatch.setenv("OPEN_TICKET_AI_CONFIG", str(config_file))
        result = config_loader.load_config()
    else:
        result = config_loader.load_config(config_file)
    assert isinstance(result, RawOpenTicketAIConfig)


def test_load_config_logs_success(
    config_loader: ConfigLoader, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    import logging

    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(_minimal_valid_config()))
    with caplog.at_level(logging.INFO):
        config_loader.load_config(config_file)
    assert "Loaded config from" in caplog.text

