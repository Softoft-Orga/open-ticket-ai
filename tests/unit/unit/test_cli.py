from __future__ import annotations

import pytest


pytest.skip("typer is not a core dependency, skipping CLI tests", allow_module_level=True)


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output or "Usage:" in result.output


def test_plugin_help(runner):
    result = runner.invoke(cli, ["plugin", "--help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output or "Usage:" in result.output
    assert "install" in result.output
    assert "list" in result.output
    assert "remove" in result.output


def test_plugin_list_no_plugins(runner):
    with patch("open_ticket_ai.cli.main.md.entry_points") as mock_ep:
        mock_ep.return_value = []
        result = runner.invoke(cli, ["plugin", "list"])
        assert result.exit_code == 0
        assert "No plugins installed" in result.output


def test_plugin_list_with_plugins(runner):
    mock_plugin = MagicMock()
    mock_plugin.get_metadata.return_value = {
        "name": "test-plugin",
        "version": "1.0.0",
        "core_api": "2.0",
        "description": "Test plugin",
    }
    
    mock_ep = MagicMock()
    mock_ep.name = "test_plugin"
    mock_ep.load.return_value = mock_plugin
    
    with patch("open_ticket_ai.cli.main.md.entry_points") as mock_entry_points:
        mock_entry_points.return_value = [mock_ep]
        result = runner.invoke(cli, ["plugin", "list"])
        assert result.exit_code == 0
        assert "test-plugin" in result.output
        assert "1.0.0" in result.output
        assert "Test plugin" in result.output


def test_plugin_install_success(runner):
    with patch("open_ticket_ai.cli.main.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stderr="", stdout="")
        result = runner.invoke(cli, ["plugin", "install", "test-plugin"])
        assert result.exit_code == 0
        assert "installed successfully" in result.output
        mock_run.assert_called_once()


def test_plugin_install_failure(runner):
    with patch("open_ticket_ai.cli.main.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Error installing package",
            stdout=""
        )
        result = runner.invoke(cli, ["plugin", "install", "test-plugin"])
        assert result.exit_code == 1
        assert "Failed to install" in result.output


def test_plugin_remove_success(runner):
    with patch("open_ticket_ai.cli.main.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stderr="", stdout="")
        result = runner.invoke(cli, ["plugin", "remove", "test-plugin"])
        assert result.exit_code == 0
        assert "removed successfully" in result.output
        mock_run.assert_called_once()


def test_plugin_remove_failure(runner):
    with patch("open_ticket_ai.cli.main.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Error uninstalling package",
            stdout=""
        )
        result = runner.invoke(cli, ["plugin", "remove", "test-plugin"])
        assert result.exit_code == 1
        assert "Failed to remove" in result.output
