__version__ = "1.0.0rc1"

__all__ = ["OTOBOZnunyTicketSystemService"]


def get_metadata():
    return {
        "name": "open-ticket-ai-otobo-znuny-plugin",
        "version": __version__,
        "core_api": "2.0",
        "description": "OTOBO/Znuny ticket system integration plugin for Open Ticket AI",
    }


def register_pipes():
    return []


def register_services():
    from .otobo_znuny_ticket_system_service import OTOBOZnunyTicketSystemService
    return [OTOBOZnunyTicketSystemService]

def register_cli_commands():
    import typer
    
    otobo_znuny_plugin = typer.Typer()
    
    @otobo_znuny_plugin.command()
    def setup():
        typer.echo("OTOBO/Znuny plugin setup wizard")
        typer.echo("This command would guide you through configuring the plugin.")
        typer.echo("(Implementation placeholder)")
    
    return otobo_znuny_plugin
