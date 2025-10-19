# language: python
from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.plugins.plugin import CreatePluginFn, Plugin

from . import OTOBOZnunyTicketSystemService


class OTOBOZnunyPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            OTOBOZnunyTicketSystemService,
        ]


create_otobo_znuny_plugin: CreatePluginFn = OTOBOZnunyPlugin
