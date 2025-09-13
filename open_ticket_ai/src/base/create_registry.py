# FILE_PATH: open_ticket_ai\src\ce\core\dependency_injection\create_registry.py
from open_ticket_ai.src.core.dependency_injection.registry import Registry
from open_ticket_ai.src.base.otobo_integration.otobo_adapter import OTOBOAdapter
from open_ticket_ai.src.base.pipe_implementations import SubjectBodyPreparer
from open_ticket_ai.src.base.pipe_implementations.hf_inference_services.hf_local_ai_inference_service import \
    HFLocalAIInferenceService


def create_registry() -> Registry:
    registry = Registry()
    registry.register_all(
        [
            OTOBOAdapter, SubjectBodyPreparer,
            HFLocalAIInferenceService,
        ],
    )
    return registry
