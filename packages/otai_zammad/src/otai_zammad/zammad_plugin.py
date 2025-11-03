from open_ticket_ai import Injectable, Plugin

from otai_zammad.zammad_ticket_system_service import ZammadTicketsystemService


class ZammadPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            ZammadTicketsystemService,
        ]
