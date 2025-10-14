from unittest.mock import MagicMock, patch

from packages.otai_otobo_znuny.src.otai_otobo_znuny.cli import otobo_znuny
from typer.testing import CliRunner


def test_setup_command_exists():
    runner = CliRunner()
    result = runner.invoke(otobo_znuny, ["--help"])
    assert result.exit_code == 0
    assert "setup" in result.output


@patch("otobo_znuny.clients.otobo_client.OTOBOZnunyClient")
def test_setup_with_all_options(mock_client):
    runner = CliRunner()
    result = runner.invoke(
        otobo_znuny,
        [
            "--base-url",
            "https://example.com/otrs",
            "--webservice-name",
            "TestService",
            "--username",
            "testuser",
            "--password",
            "testpass",
            "--no-verify-connection",
        ],
    )
    assert result.exit_code == 0
    assert "Next Steps" in result.output


@patch("otobo_znuny.clients.otobo_client.OTOBOZnunyClient")
def test_setup_generates_config(mock_client):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            otobo_znuny,
            [
                "--base-url",
                "https://example.com/otrs",
                "--webservice-name",
                "TestService",
                "--username",
                "testuser",
                "--password",
                "testpass",
                "--no-verify-connection",
                "--output-config",
                "config.yml",
            ],
        )
        assert result.exit_code == 0
        with open("config.yml") as f:
            content = f.read()
            assert "otobo_znuny" in content
            assert "https://example.com/otrs" in content
