from typing import Any, Literal, Optional

from open_ticket_ai.core.pipeline.base_pipe_config import BasePipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import TicketSearchCriteria


class TicketSystemServiceConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.TicketSystemService"]
    operation: str
    ticket_search_criteria: Optional["TicketSearchCriteria"] = None
    ticket_id: str | None = None
    ticket: dict[str, Any] | None = None


class HFLocalAIInferenceServiceConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.HFLocalAIInferenceService"]
    prompt: str
    hf_model: str
    hf_token_env_var: str


class JinjaExpressionPipeConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.JinjaExpressionPipe"]
    # Base config for Jinja expression processing pipes


class TicketModifierConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.TicketModifier"]
    ticket_id: str
    ticket: dict[str, Any]


class SimpleKeyValueMapperConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.SimpleKeyValueMapper"]
    from_key: str
    key_to_value_map: dict[str, Any]


class HFLocalAiInferencePipeConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.HFLocalAiInferencePipe"]
    prompt: str
    hf_model: str
    hf_token_env_var: str


class FetchTicketsPipeConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.FetchTicketsPipe"]
    ticket_search_criteria: Optional["TicketSearchCriteria"] = None


class UpdateTicketPipeConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.UpdateTicketPipe"]
    ticket_id: str
    ticket: dict[str, Any]


class AddNotePipeConfig(BasePipeConfig):
    type: Literal["open_ticket_ai.extensions.AddNotePipe"]
    ticket_id: str
    note: str
