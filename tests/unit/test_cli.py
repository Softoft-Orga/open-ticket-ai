from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from open_ticket_ai_otobo_znuny_plugin.cli import otobo_znuny, setup


class TestOtoboZnunyCLI:
    def test_setup_command_exists(self):
        runner = CliRunner()
        result = runner.invoke(otobo_znuny, ["--help"])
        assert result.exit_code == 0
        assert "setup" in result.output

    def test_setup_prompts_for_required_fields(self):
        runner = CliRunner()
        result = runner.invoke(
            otobo_znuny,
            ["setup"],
            input="https://example.com/otrs\nOpenTicketAI\nopen_ticket_ai\npassword123\n"
        )
        assert "OTOBO/Znuny base URL" in result.output
        assert "Web service name" in result.output
        assert "Username" in result.output

    @patch("open_ticket_ai_otobo_znuny_plugin.cli.OTOBOZnunyClient")
    def test_setup_with_all_options_no_verify(self, mock_client):
        runner = CliRunner()
        result = runner.invoke(
            otobo_znuny,
            [
                "setup",
                "--base-url", "https://example.com/otrs",
                "--webservice-name", "TestService",
                "--username", "testuser",
                "--password", "testpass",
                "--no-verify-connection",
            ]
        )
        assert result.exit_code == 0
        assert "Next Steps" in result.output
        mock_client.assert_not_called()

    @patch("open_ticket_ai_otobo_znuny_plugin.cli.OTOBOZnunyClient")
    def test_setup_with_connection_verification_success(self, mock_client):
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        runner = CliRunner()
        result = runner.invoke(
            otobo_znuny,
            [
                "setup",
                "--base-url", "https://example.com/otrs",
                "--webservice-name", "TestService",
                "--username", "testuser",
                "--password", "testpass",
                "--verify-connection",
            ]
        )
        
        assert result.exit_code == 0
        assert "Verifying connection" in result.output
        assert "Connection successful" in result.output
        mock_client.assert_called_once()
        mock_instance.login.assert_called_once()

    @patch("open_ticket_ai_otobo_znuny_plugin.cli.OTOBOZnunyClient")
    def test_setup_with_connection_verification_failure_abort(self, mock_client):
        mock_client.side_effect = Exception("Connection failed")
        
        runner = CliRunner()
        result = runner.invoke(
            otobo_znuny,
            [
                "setup",
                "--base-url", "https://example.com/otrs",
                "--webservice-name", "TestService",
                "--username", "testuser",
                "--password", "testpass",
                "--verify-connection",
            ],
            input="n\n"
        )
        
        assert result.exit_code == 1
        assert "Connection failed" in result.output

    @patch("open_ticket_ai_otobo_znuny_plugin.cli.OTOBOZnunyClient")
    def test_setup_with_connection_verification_failure_continue(self, mock_client):
        mock_client.side_effect = Exception("Connection failed")
        
        runner = CliRunner()
        result = runner.invoke(
            otobo_znuny,
            [
                "setup",
                "--base-url", "https://example.com/otrs",
                "--webservice-name", "TestService",
                "--username", "testuser",
                "--password", "testpass",
                "--verify-connection",
            ],
            input="y\n"
        )
        
        assert result.exit_code == 0
        assert "Connection failed" in result.output
        assert "Next Steps" in result.output

    @patch("open_ticket_ai_otobo_znuny_plugin.cli.OTOBOZnunyClient")
    def test_setup_generates_config_file(self, mock_client):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(
                otobo_znuny,
                [
                    "setup",
                    "--base-url", "https://example.com/otrs",
                    "--webservice-name", "TestService",
                    "--username", "testuser",
                    "--password", "testpass",
                    "--no-verify-connection",
                    "--output-config", "config.yml",
                ]
            )
            
            assert result.exit_code == 0
            assert "Generating configuration file" in result.output
            
            with open("config.yml") as f:
                content = f.read()
                assert "open_ticket_ai:" in content
                assert "otobo_znuny" in content
                assert "https://example.com/otrs" in content
                assert "TestService" in content
                assert "testuser" in content
                assert "OTAI_OTOBO_ZNUNY_PASSWORD" in content
