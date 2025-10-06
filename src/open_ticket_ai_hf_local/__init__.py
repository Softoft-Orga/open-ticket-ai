from .hf_local_text_classification_pipe import HFLocalTextClassificationPipe

__version__ = "1.0.0rc1"

__all__ = ["HFLocalTextClassificationPipe"]


def get_metadata():
    return {
        "name": "open-ticket-ai-hf-local",
        "version": __version__,
        "core_api": "2.0",
        "description": "Hugging Face local text classification plugin for Open Ticket AI",
    }


def register_pipes():
    return [HFLocalTextClassificationPipe]


def register_services():
    return []
