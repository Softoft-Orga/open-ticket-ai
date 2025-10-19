from .hf_classification_service import HFClassificationService

__all__ = ["HFClassificationService"]


def get_metadata() -> dict[str, str]:
    return {
        "name": "hf_local",
        "version": "1.0.0rc1",
        "core_api": "2.0",
        "description": "Hugging Face local text classification plugin for Open Ticket AI",
    }


def register_pipes() -> list[type]:
    return []


def register_services() -> list[type]:
    return [HFClassificationService]
