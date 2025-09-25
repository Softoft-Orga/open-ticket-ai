from typing import Any, Dict, List, Optional, Union
from pydantic import Field, ConfigDict, AliasChoices

from open_ticket_ai.src.core.config.base_pipe_config import BasePipeConfig


class TicketSearchCriteria(BasePipeConfig):
    queue: Dict[str, str]
    limit: int


class TicketSystemServiceConfig(BasePipeConfig):
    operation: str
    ticket_search_criteria: Optional[TicketSearchCriteria] = None
    ticket_id: Optional[str] = None
    ticket: Optional[Dict[str, Any]] = None


class HFLocalAIInferenceServiceConfig(BasePipeConfig):
    prompt: str
    hf_model: str
    hf_token_env_var: str


class ListValueMapperConfig(BasePipeConfig):
    from_key: str
    key_to_value_map: Dict[str, str]


class ContextModifierConfig(BasePipeConfig):
    pass  # No additional fields needed as it only uses the base config with output


class TicketModifierConfig(BasePipeConfig):
    ticket_id: str
    ticket: Dict[str, Any]


# Alias for backward compatibility
TicketFetcherConfig = TicketSystemServiceConfig
