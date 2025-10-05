import sys
from typing import Optional

import click
from otobo_znuny.clients.otobo_client import OTOBOZnunyClient
from otobo_znuny.domain_models.basic_auth_model import BasicAuth
from otobo_znuny.domain_models.otobo_client_config import ClientConfig
from otobo_znuny.domain_models.ticket_operation import TicketOperation
from pydantic import SecretStr


@click.group()
def otobo_znuny():
    pass


@otobo_znuny.command()
@click.option('--base-url', prompt='OTOBO/Znuny base URL', help='Base URL of the OTOBO/Znuny instance')
@click.option('--webservice-name', default='OpenTicketAI', prompt='Web service name', help='Name of the web service')
@click.option('--username', default='open_ticket_ai', prompt='Username', help='Username for authentication')
@click.option('--password', prompt=True, hide_input=True, help='Password for authentication')
@click.option('--verify-connection/--no-verify-connection', default=True, help='Verify the connection after setup')
@click.option('--output-config', type=click.Path(), help='Path to output a config.yml file')
def setup(
    base_url: str,
    webservice_name: str,
    username: str,
    password: str,
    verify_connection: bool,
    output_config: Optional[str]
):
    click.echo("\n=== OTOBO/Znuny Ticket System Setup ===\n")
    
    operation_urls = {
        TicketOperation.SEARCH.value: "ticket-search",
        TicketOperation.GET.value: "ticket-get",
        TicketOperation.UPDATE.value: "ticket-update",
    }
    
    click.echo(f"Base URL: {base_url}")
    click.echo(f"Web service: {webservice_name}")
    click.echo(f"Username: {username}")
    click.echo()
    
    if verify_connection:
        click.echo("Verifying connection...")
        try:
            config = ClientConfig(
                base_url=base_url,
                webservice_name=webservice_name,
                operation_url_map={TicketOperation(k): v for k, v in operation_urls.items()},
            )
            client = OTOBOZnunyClient(config=config)
            auth = BasicAuth(user_login=username, password=SecretStr(password))
            client.login(auth)
            click.echo(click.style("✓ Connection successful!", fg='green'))
        except Exception as e:
            click.echo(click.style(f"✗ Connection failed: {e}", fg='red'))
            if not click.confirm("\nContinue anyway?"):
                sys.exit(1)
    
    if output_config:
        click.echo(f"\nGenerating configuration file: {output_config}")
        config_content = f"""open_ticket_ai:
  defs:
    - id: "otobo_znuny"
      use: "open_ticket_ai_otobo_znuny_plugin:OTOBOZnunyTicketSystemService"
      base_url: "{base_url}"
      webservice_name: "{webservice_name}"
      username: "{username}"
      password: "{{{{ env.OTAI_OTOBO_ZNUNY_PASSWORD }}}}"
      operation_urls:
        search: "{operation_urls[TicketOperation.SEARCH.value]}"
        get: "{operation_urls[TicketOperation.GET.value]}"
        update: "{operation_urls[TicketOperation.UPDATE.value]}"
"""
        
        try:
            with open(output_config, 'w') as f:
                f.write(config_content)
            click.echo(click.style(f"✓ Configuration written to {output_config}", fg='green'))
            click.echo(f"\nNOTE: Set the OTAI_OTOBO_ZNUNY_PASSWORD environment variable before running.")
        except Exception as e:
            click.echo(click.style(f"✗ Failed to write config: {e}", fg='red'))
            sys.exit(1)
    
    click.echo("\n=== Next Steps ===")
    click.echo("1. In OTOBO/Znuny, create a dedicated API web service")
    click.echo("2. Create an agent with permissions to search, read, update tickets, and add articles")
    click.echo("3. Configure the web service with the following operations:")
    for op, url in operation_urls.items():
        click.echo(f"   - {op}: {url}")
    click.echo("4. Set the OTAI_OTOBO_ZNUNY_PASSWORD environment variable")
    click.echo("5. Test your configuration with Open Ticket AI")
    click.echo()


def get_commands():
    return [otobo_znuny]
