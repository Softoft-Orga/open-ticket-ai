from otai_otobo_znuny.cli import get_commands
from otai_otobo_znuny.otobo_znuny_ticket_system_service import OTOBOZnunyTicketSystemService


def get_metadata() -> dict[str, str]:
    return {
        "name": "otai-otobo-znuny",
        "version": "1.0.0rc1",
        "core_api": "2.0",
        "description": "OTOBO/Znuny ticket system plugin for Open Ticket AI",
    }


def register_pipes() -> list:
    return []


def register_services() -> list:
    return [
        {
            "name": "OTOBOZnunyTicketSystemService",
            "class": OTOBOZnunyTicketSystemService,
        }
    ]


__all__ = [
    "get_metadata",
    "register_pipes",
    "register_services",
    "get_commands",
    "OTOBOZnunyTicketSystemService",
]
