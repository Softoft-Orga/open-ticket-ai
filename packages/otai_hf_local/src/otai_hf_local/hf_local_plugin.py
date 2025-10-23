from open_ticket_ai.core.injectables.injectable import Injectable
from open_ticket_ai.core.plugins.plugin import CreatePluginFn, Plugin

from .hf_classification_service import HFClassificationService


class HFLocalPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            HFClassificationService,
        ]


create_hf_local_plugin: CreatePluginFn = HFLocalPlugin
