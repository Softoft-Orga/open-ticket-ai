from .oto_znuny_ts_service import OTOBOZnunyTicketSystemService

__all__ = [
    "OTOBOZnunyTicketSystemService",
]


def get_metadata() -> dict[str, str]:
    return {
        "name": "otobo_znuny",
        "version": "1.0.0rc1",
        "core_api": "1.0",
        "description": "OTOBO/Znuny ticket system plugin for Open Ticket AI",
    }


def register_pipes() -> list[type]:
    return []


def register_services() -> list[type]:
    return [OTOBOZnunyTicketSystemService]
