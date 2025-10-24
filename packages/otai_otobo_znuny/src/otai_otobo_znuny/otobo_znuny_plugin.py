# language: python
from open_ticket_ai import Injectable, Plugin

from . import OTOBOZnunyTicketSystemService


class OTOBOZnunyPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            OTOBOZnunyTicketSystemService,
        ]
