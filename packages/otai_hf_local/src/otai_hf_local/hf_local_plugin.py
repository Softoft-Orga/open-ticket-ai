from open_ticket_ai import Injectable, Plugin

from otai_hf_local.hf_classification_service import HFClassificationService


class HFLocalPlugin(Plugin):
    def _get_all_injectables(self) -> list[type[Injectable]]:
        return [
            HFClassificationService,
        ]
