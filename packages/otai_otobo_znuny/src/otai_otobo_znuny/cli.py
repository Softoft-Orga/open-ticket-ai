import typer

otobo_znuny = typer.Typer()


@otobo_znuny.command()
def setup(
    base_url: str = typer.Option(
        ...,
        "--base-url",
        prompt="OTOBO/Znuny base URL",
        help="Base URL of the OTOBO/Znuny instance",
    ),
    webservice_name: str = typer.Option(
        "OpenTicketAI",
        "--webservice-name",
        prompt="Web service name",
        help="Name of the web service",
    ),
    username: str = typer.Option(
        "open_ticket_ai",
        "--username",
        prompt="Username",
        help="Username for authentication",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        prompt=True,
        hide_input=True,
        help="Password for authentication",
    ),
    verify_connection: bool = typer.Option(
        True,
        "--verify-connection/--no-verify-connection",
        help="Verify the connection after setup",
    ),
    output_config: str | None = typer.Option(
        None,
        "--output-config",
        help="Path to output a config.yml file",
    ),
):
    typer.echo("\n=== OTOBO/Znuny Ticket System Setup ===\n")

    operation_urls = {
        "search": "ticket-search",
        "get": "ticket-get",
        "update": "ticket-update",
    }

    typer.echo(f"Base URL: {base_url}")
    typer.echo(f"Web service: {webservice_name}")
    typer.echo(f"Username: {username}")
    typer.echo()

    if verify_connection:
        from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
        from otobo_znuny.domain_models.basic_auth_model import BasicAuth
        from otobo_znuny.domain_models.otobo_client_config import ClientConfig
        from otobo_znuny.domain_models.ticket_operation import TicketOperation
        from pydantic import SecretStr

        typer.echo("Verifying connection...")
        try:
            operation_url_map = {
                TicketOperation.SEARCH: operation_urls["search"],
                TicketOperation.GET: operation_urls["get"],
                TicketOperation.UPDATE: operation_urls["update"],
            }
            config = ClientConfig(
                base_url=base_url,
                webservice_name=webservice_name,
                operation_url_map=operation_url_map,
            )
            client = OTOBOZnunyClient(config=config)
            auth = BasicAuth(user_login=username, password=SecretStr(password))
            client.login(auth)
            typer.echo(typer.style("✓ Connection successful!", fg=typer.colors.GREEN))
        except Exception as e:
            typer.echo(typer.style(f"✗ Connection failed: {e}", fg=typer.colors.RED))
            if not typer.confirm("\nContinue anyway?"):
                raise typer.Exit(code=1) from None

    if output_config:
        typer.echo(f"\nGenerating configuration file: {output_config}")
        config_content = f"""open_ticket_ai:
  services:
    - id: "otobo_znuny"
      use: "open_ticket_ai_otobo_znuny_plugin:OTOBOZnunyTicketSystemService"
      base_url: "{base_url}"
      webservice_name: "{webservice_name}"
      username: "{username}"
      password: "{{{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}}}"
      operation_urls:
        search: "{operation_urls["search"]}"
        get: "{operation_urls["get"]}"
        update: "{operation_urls["update"]}"
"""

        try:
            with open(output_config, "w") as f:
                f.write(config_content)
            typer.echo(typer.style(f"✓ Configuration written to {output_config}", fg=typer.colors.GREEN))
            typer.echo("\nNOTE: Set the OTAI_OTOBO_ZNUNY_PASSWORD environment variable before running.")
        except Exception as e:
            typer.echo(typer.style(f"✗ Failed to write config: {e}", fg=typer.colors.RED))
            raise typer.Exit(code=1) from None

    typer.echo("\n=== Next Steps ===")
    typer.echo("1. In OTOBO/Znuny, create a dedicated API web service")
    typer.echo("2. Create an agent with permissions to search, read, update tickets, and add articles")
    typer.echo("3. Configure the web service with the following operations:")
    for op, url in operation_urls.items():
        typer.echo(f"   - {op}: {url}")
    typer.echo("4. Set the OTAI_OTOBO_ZNUNY_PASSWORD environment variable")
    typer.echo("5. Test your configuration with Open Ticket AI")
    typer.echo()


def get_commands():
    return [otobo_znuny]
