from .otobo_znuny_ticket_system_service import OTOBOZnunyTicketSystemService

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
    return [OTOBOZnunyTicketSystemService]

def register_cli_commands():
    from .cli import get_commands
    return get_commands()
