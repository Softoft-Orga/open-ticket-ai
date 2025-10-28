from open_ticket_ai import Injectable, Plugin

from otai_otobo_znuny.oto_znuny_ts_service import OTOBOZnunyTicketSystemService


class OTOBOZnunyPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            OTOBOZnunyTicketSystemService,
        ]
