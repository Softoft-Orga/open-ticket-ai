from open_ticket_ai_hf_local.hf_local_text_classification_pipe import (
    HFLocalTextClassificationPipe,
    HFLocalTextClassificationPipeConfig,
)

__version__ = "1.0.0rc1"

__all__ = [
    "HFLocalTextClassificationPipe",
    "HFLocalTextClassificationPipeConfig",
    "get_metadata",
    "register_pipes",
    "register_services",
]


def get_metadata() -> dict[str, str]:
    return {
        "name": "open-ticket-ai-hf-local",
        "version": __version__,
        "core_api": "2.0",
    }


def register_pipes(registry) -> None:
    pass


def register_services(registry) -> None:
    pass

