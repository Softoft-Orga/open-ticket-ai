from .hf_local_text_classification_pipe import HFLocalTextClassificationPipe

__all__ = ["HFLocalTextClassificationPipe"]


def get_metadata() -> dict[str, str]:
    return {
        "name": "hf_local",
        "version": "1.0.0rc1",
        "core_api": "2.0",
        "description": "Hugging Face local text classification plugin for Open Ticket AI",
    }


def register_pipes() -> list[type]:
    return [HFLocalTextClassificationPipe]


def register_services() -> list[type]:
    return []
