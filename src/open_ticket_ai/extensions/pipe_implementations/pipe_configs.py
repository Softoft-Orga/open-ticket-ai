from typing import Any, Dict, Literal, Optional

from open_ticket_ai.core.pipeline.base_pipe_config import BasePipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class TicketSystemServiceConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.TicketSystemService"]
    operation: str
    ticket_search_criteria: Optional["TicketSearchCriteria"] = None
    ticket_id: Optional[str] = None
    ticket: Optional[Dict[str, Any]] = None


class HFLocalAIInferenceServiceConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.HFLocalAIInferenceService"]
    prompt: str
    hf_model: str
    hf_token_env_var: str


class ContextModifierConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.ContextModifier"]
    # keine extra Felder, nur output vom BasePipeConfig


class TicketModifierConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.TicketModifier"]
    ticket_id: str
    ticket: Dict[str, Any]


class SimpleKeyValueMapperConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.SimpleKeyValueMapper"]
    from_key: str
    key_to_value_map: Dict[str, Any]
