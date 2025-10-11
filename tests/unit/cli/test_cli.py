from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from open_ticket_ai.cli.main import app


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


def test_init_command_success(cli_runner: CliRunner, mock_templates_dir: Path, tmp_path: Path) -> None:
    output_file = tmp_path / "config.yml"

    with patch("open_ticket_ai.cli.main.get_templates_dir", return_value=mock_templates_dir):
        result = cli_runner.invoke(
            app,
            ["init", "queue_classification", "--output", str(output_file)],
        )

    assert result.exit_code == 0
    assert "Successfully initialized config" in result.stdout
    assert output_file.exists()
    assert "Example: Queue Classification" in output_file.read_text()


def test_init_command_template_not_found(cli_runner: CliRunner, mock_templates_dir: Path) -> None:
    with patch("open_ticket_ai.cli.main.get_templates_dir", return_value=mock_templates_dir):
        result = cli_runner.invoke(app, ["init", "nonexistent_template"])

    assert result.exit_code == 1
    assert "not found" in result.stdout
    assert "Available templates:" in result.stdout


def test_init_command_file_exists_without_force(
    cli_runner: CliRunner, mock_templates_dir: Path, tmp_path: Path
) -> None:
    output_file = tmp_path / "config.yml"
    output_file.write_text("existing content")

    with patch("open_ticket_ai.cli.main.get_templates_dir", return_value=mock_templates_dir):
        result = cli_runner.invoke(
            app,
            ["init", "queue_classification", "--output", str(output_file)],
        )

    assert result.exit_code == 1
    assert "already exists" in result.stdout


def test_init_command_file_exists_with_force(cli_runner: CliRunner, mock_templates_dir: Path, tmp_path: Path) -> None:
    output_file = tmp_path / "config.yml"
    output_file.write_text("existing content")

    with patch("open_ticket_ai.cli.main.get_templates_dir", return_value=mock_templates_dir):
        result = cli_runner.invoke(
            app,
            ["init", "queue_classification", "--output", str(output_file), "--force"],
        )

    assert result.exit_code == 0
    assert "Successfully initialized config" in result.stdout
    assert "Example: Queue Classification" in output_file.read_text()


def test_version_command(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Open Ticket AI version:" in result.stdout
    assert "1.0.0rc1" in result.stdout


def test_plugin_list_command(cli_runner: CliRunner) -> None:
    with patch("open_ticket_ai.cli.main.importlib.metadata.distributions") as mock_dists:
        mock_dist = MagicMock()
        mock_dist.name = "otai-test-plugin"
        mock_dist.version = "1.0.0"
        mock_dist.metadata = {"Summary": "Test plugin"}
        mock_dists.return_value = [mock_dist]

        result = cli_runner.invoke(app, ["plugin", "list"])

    assert result.exit_code == 0
    assert "Installed OTAI plugins" in result.stdout


def test_check_config_file_not_found(cli_runner: CliRunner, tmp_path: Path) -> None:
    nonexistent_file = tmp_path / "nonexistent.yml"

    result = cli_runner.invoke(app, ["check-config", str(nonexistent_file)])

    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_start_command_no_config(cli_runner: CliRunner) -> None:
    with patch.dict("os.environ", {}, clear=True):
        result = cli_runner.invoke(app, ["start"])

    assert result.exit_code == 1
    assert "OPEN_TICKET_AI_CONFIG" in result.stdout


def test_start_command_config_not_found(cli_runner: CliRunner, tmp_path: Path) -> None:
    nonexistent_file = tmp_path / "nonexistent.yml"

    result = cli_runner.invoke(app, ["start", "--config", str(nonexistent_file)])

    assert result.exit_code == 1
    assert "not found" in result.stdout


def test_get_available_templates(mock_templates_dir: Path) -> None:
    from open_ticket_ai.cli.main import get_available_templates

    with patch("open_ticket_ai.cli.main.get_templates_dir", return_value=mock_templates_dir):
        templates = get_available_templates()

    assert "queue_classification" in templates
    assert "priority_classification" in templates
    assert len(templates) == 2


def test_extract_template_description(mock_templates_dir: Path) -> None:
    from open_ticket_ai.cli.main import extract_template_description

    template_path = mock_templates_dir / "queue_classification.yml"
    description = extract_template_description(template_path)

    assert "Queue Classification" in description
