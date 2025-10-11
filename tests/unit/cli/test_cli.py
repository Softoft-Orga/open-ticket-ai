from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from open_ticket_ai.cli.main import CLI, app
from open_ticket_ai.core.config.app_config import AppConfig


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def mock_templates_dir(tmp_path: Path) -> Path:
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()

    template_content = """# Example: Queue Classification
# This is a test template
open_ticket_ai:
  general_config:
    logging:
      version: 1
"""

    (templates_dir / "queue_classification.yml").write_text(template_content)
    (templates_dir / "priority_classification.yml").write_text(template_content)

    return templates_dir


@pytest.fixture
def mock_app_config(mock_templates_dir: Path) -> AppConfig:
    app_config = AppConfig()
    with patch.object(app_config, "get_templates_dir", return_value=mock_templates_dir):
        yield app_config


def test_init_command_success(cli_runner: CliRunner, mock_templates_dir: Path, tmp_path: Path) -> None:
    output_file = tmp_path / "config.yml"

    mock_app_config = AppConfig()
    with patch.object(AppConfig, "get_templates_dir", return_value=mock_templates_dir):
        cli = CLI(mock_app_config)
        result = cli_runner.invoke(
            cli.app,
            ["init", "queue_classification", "--output", str(output_file)],
        )

    assert result.exit_code == 0
    assert "Successfully initialized config" in result.stdout
    assert output_file.exists()
    assert "Example: Queue Classification" in output_file.read_text()


def test_init_command_template_not_found(cli_runner: CliRunner, mock_templates_dir: Path) -> None:
    mock_app_config = AppConfig()
    with patch.object(AppConfig, "get_templates_dir", return_value=mock_templates_dir):
        cli = CLI(mock_app_config)
        result = cli_runner.invoke(cli.app, ["init", "nonexistent_template"])

    assert result.exit_code == 1
    assert "not found" in result.stdout
    assert "Available templates:" in result.stdout


def test_init_command_file_exists_without_force(
    cli_runner: CliRunner, mock_templates_dir: Path, tmp_path: Path
) -> None:
    output_file = tmp_path / "config.yml"
    output_file.write_text("existing content")

    mock_app_config = AppConfig()
    with patch.object(AppConfig, "get_templates_dir", return_value=mock_templates_dir):
        cli = CLI(mock_app_config)
        result = cli_runner.invoke(
            cli.app,
            ["init", "queue_classification", "--output", str(output_file)],
        )

    assert result.exit_code == 1
    assert "already exists" in result.stdout


def test_init_command_file_exists_with_force(cli_runner: CliRunner, mock_templates_dir: Path, tmp_path: Path) -> None:
    output_file = tmp_path / "config.yml"
    output_file.write_text("existing content")

    mock_app_config = AppConfig()
    with patch.object(AppConfig, "get_templates_dir", return_value=mock_templates_dir):
        cli = CLI(mock_app_config)
        result = cli_runner.invoke(
            cli.app,
            ["init", "queue_classification", "--output", str(output_file), "--force"],
        )

    assert result.exit_code == 0
    assert "Successfully initialized config" in result.stdout
    assert "Example: Queue Classification" in output_file.read_text()


def test_plugin_list_command(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["plugin", "list"])

    assert result.exit_code == 1
    assert "not yet implemented" in result.stdout


def test_check_config_file_not_found(cli_runner: CliRunner, tmp_path: Path) -> None:
    nonexistent_file = tmp_path / "nonexistent.yml"

    result = cli_runner.invoke(app, ["check-config", str(nonexistent_file)])

    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_run_command_no_config(cli_runner: CliRunner) -> None:
    with patch.dict("os.environ", {}, clear=True):
        result = cli_runner.invoke(app, ["run"])

    assert result.exit_code == 1
    assert "OPEN_TICKET_AI_CONFIG" in result.stdout


def test_run_command_config_not_found(cli_runner: CliRunner, tmp_path: Path) -> None:
    nonexistent_file = tmp_path / "nonexistent.yml"

    result = cli_runner.invoke(app, ["run", "--config", str(nonexistent_file)])

    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_cli_get_available_templates(mock_templates_dir: Path) -> None:
    mock_app_config = AppConfig()
    with patch.object(AppConfig, "get_templates_dir", return_value=mock_templates_dir):
        cli = CLI(mock_app_config)
        templates = cli._get_available_templates()

    assert "queue_classification" in templates
    assert "priority_classification" in templates
    assert len(templates) == 2


def test_cli_extract_template_description(mock_templates_dir: Path) -> None:
    mock_app_config = AppConfig()
    cli = CLI(mock_app_config)

    template_path = mock_templates_dir / "queue_classification.yml"
    description = cli._extract_template_description(template_path)

    assert "Queue Classification" in description
