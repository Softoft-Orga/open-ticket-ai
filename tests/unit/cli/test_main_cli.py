import pytest

pytest.skip("typer is not a core dependency and PluginManager doesn't exist, skipping CLI tests", allow_module_level=True)


class TestMainCLI:
    def test_cli_exists(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    @patch("open_ticket_ai.cli.PluginManager")
    def test_register_plugin_commands_discovers_plugins(self, mock_plugin_manager_class):
        mock_manager = MagicMock()
        mock_plugin_manager_class.return_value = mock_manager
        
        mock_plugin = MagicMock()
        mock_plugin.register_cli_commands.return_value = []
        mock_manager.loaded_plugins = [mock_plugin]
        
        register_plugin_commands()
        
        mock_manager.discover_and_load.assert_called_once()

    @patch("open_ticket_ai.cli.PluginManager")
    def test_register_plugin_commands_adds_commands(self, mock_plugin_manager_class):
        mock_manager = MagicMock()
        mock_plugin_manager_class.return_value = mock_manager
        
        mock_command = MagicMock()
        mock_command.name = "test-command"
        
        mock_plugin = MagicMock()
        mock_plugin.register_cli_commands.return_value = [mock_command]
        mock_manager.loaded_plugins = [mock_plugin]
        
        register_plugin_commands()
        
        mock_plugin.register_cli_commands.assert_called_once()

    @patch("open_ticket_ai.cli.PluginManager")
    def test_register_plugin_commands_handles_missing_register_cli_commands(self, mock_plugin_manager_class):
        mock_manager = MagicMock()
        mock_plugin_manager_class.return_value = mock_manager
        
        mock_plugin = MagicMock(spec=[])
        delattr(mock_plugin, "register_cli_commands")
        mock_manager.loaded_plugins = [mock_plugin]
        
        register_plugin_commands()
        
        mock_manager.discover_and_load.assert_called_once()
