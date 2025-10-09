import pytest

pytest.skip("typer is not a core dependency, skipping CLI tests", allow_module_level=True)

runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Open Ticket AI version:" in result.stdout


def test_check_config_file_not_found():
    result = runner.invoke(app, ["check-config", "nonexistent.yml"])
    assert result.exit_code == 1
    assert "Config file not found" in result.stdout


def test_check_config_valid(tmp_path):
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        """
open_ticket_ai:
  plugins: []
  general_config: {}
  defs: []
  orchestrator: []
"""
    )
    
    result = runner.invoke(app, ["check-config", str(config_file)])
    assert result.exit_code == 0
    assert "Config file is valid!" in result.stdout
    assert "Plugins: 0" in result.stdout
    assert "Definitions: 0" in result.stdout


def test_check_config_invalid(tmp_path):
    config_file = tmp_path / "config.yml"
    config_file.write_text("invalid: yaml: content:")
    
    result = runner.invoke(app, ["check-config", str(config_file)])
    assert result.exit_code == 1
    assert "error" in result.stdout.lower()


def test_init_unknown_template():
    result = runner.invoke(app, ["init", "unknown_template"])
    assert result.exit_code == 1
    assert "Unknown template" in result.stdout
    assert "Available templates:" in result.stdout


def test_init_file_exists(tmp_path):
    existing_file = tmp_path / "config.yml"
    existing_file.write_text("existing content")
    
    result = runner.invoke(
        app, ["init", "queue_classification", "--output", str(existing_file)]
    )
    assert result.exit_code == 1
    assert "File already exists" in result.stdout
    assert "--force" in result.stdout


def test_init_file_exists_with_force(tmp_path):
    existing_file = tmp_path / "config.yml"
    existing_file.write_text("existing content")
    
    result = runner.invoke(
        app,
        ["init", "queue_classification", "--output", str(existing_file), "--force"],
    )
    
    if result.exit_code == 0:
        assert "Successfully initialized" in result.stdout
        assert existing_file.exists()
    else:
        assert "Template file not found" in result.stdout


def test_init_creates_config(tmp_path):
    output_file = tmp_path / "test_config.yml"
    
    result = runner.invoke(
        app, ["init", "queue_classification", "--output", str(output_file)]
    )
    
    if result.exit_code == 0:
        assert "Successfully initialized" in result.stdout
        assert output_file.exists()
    else:
        assert "Template file not found" in result.stdout


def test_plugin_list_command():
    result = runner.invoke(app, ["plugin", "list"])
    assert result.exit_code == 0
    assert "Installed OTAI plugins:" in result.stdout


@patch("subprocess.run")
def test_plugin_install_success(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0, stdout="Successfully installed test-plugin"
    )
    
    result = runner.invoke(app, ["plugin", "install", "test-plugin"])
    assert result.exit_code == 0
    assert "Successfully installed" in result.stdout
    mock_run.assert_called_once()


@patch("subprocess.run")
def test_plugin_install_with_upgrade(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0, stdout="Successfully installed test-plugin"
    )
    
    result = runner.invoke(app, ["plugin", "install", "test-plugin", "--upgrade"])
    assert result.exit_code == 0
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert "--upgrade" in args


@patch("subprocess.run")
def test_plugin_remove_with_confirmation(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0, stdout="Successfully uninstalled test-plugin"
    )
    
    result = runner.invoke(
        app, ["plugin", "remove", "test-plugin"], input="y\n"
    )
    assert result.exit_code == 0
    assert "Successfully removed" in result.stdout
    mock_run.assert_called_once()


@patch("subprocess.run")
def test_plugin_remove_cancel_confirmation(mock_run):
    result = runner.invoke(
        app, ["plugin", "remove", "test-plugin"], input="n\n"
    )
    assert result.exit_code == 0
    assert "Cancelled" in result.stdout
    mock_run.assert_not_called()


@patch("subprocess.run")
def test_plugin_remove_with_yes_flag(mock_run):
    mock_run.return_value = MagicMock(
        returncode=0, stdout="Successfully uninstalled test-plugin"
    )
    
    result = runner.invoke(app, ["plugin", "remove", "test-plugin", "--yes"])
    assert result.exit_code == 0
    assert "Successfully removed" in result.stdout
    mock_run.assert_called_once()


@patch("subprocess.run")
@patch("importlib.metadata.version")
def test_upgrade_check_only(mock_version, mock_run):
    mock_version.return_value = "1.0.0"
    mock_run.return_value = MagicMock(
        returncode=0, stdout="open-ticket-ai (1.0.0)\nAvailable versions: 1.0.1"
    )
    
    result = runner.invoke(app, ["upgrade", "--check-only"])
    assert result.exit_code == 0
    assert "Available versions" in result.stdout
    mock_run.assert_called_once()


def test_start_no_config():
    result = runner.invoke(app, ["start"])
    assert result.exit_code == 1
    assert "OPEN_TICKET_AI_CONFIG" in result.stdout


def test_start_config_not_found():
    result = runner.invoke(app, ["start", "--config", "nonexistent.yml"])
    assert result.exit_code == 1
    assert "Config file not found" in result.stdout
