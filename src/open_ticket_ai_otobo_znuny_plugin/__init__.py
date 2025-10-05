from .otobo_znuny_ticket_system_service import OTOBOZnunyTicketSystemService

__version__ = "1.0.0rc1"

__all__ = [
    "OTOBOZnunyTicketSystemService",
    "get_metadata",
    "register_pipes",
    "register_services",
]


def get_metadata() -> dict[str, str]:
    return {
        "name": "open-ticket-ai-otobo-znuny-plugin",
        "version": __version__,
        "core_api": "2.0",
    }


def register_pipes(registry) -> None:
    pass


def register_services(registry) -> None:
    pass

