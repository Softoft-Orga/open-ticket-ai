from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

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
    config_loader_creator, tmp_path: Path, config_data: dict | None, expected_error: type[BaseException] | None
) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_data))
    config_loader = config_loader_creator(config_file)
    if expected_error is None:
        result = config_loader.load_config()
        assert isinstance(result, RawOpenTicketAIConfig)
    else:
        with pytest.raises(expected_error):
            config_loader.load_config()


def test_load_config_logs_success(config_loader_creator, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    import logging

    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(_minimal_valid_config()))
    config_loader = config_loader_creator(config_file)
    with caplog.at_level(logging.INFO):
        config_loader.load_config()
    assert "Loaded config from" in caplog.text
