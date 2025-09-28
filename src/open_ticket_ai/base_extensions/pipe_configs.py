from typing import Any

from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig, RenderedPipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicketBase,
    UnifiedNote,
)


# region --- HFLocalAIInferencePipe (backward compatibility) ---


class RenderedHFLocalAIInferencePipeConfig(RenderedPipeConfig):
    prompt: str
    hf_model: str
    hf_token: str


class HFLocalAIInferencePipeConfig(RawPipeConfig):
    prompt: str
    hf_model: str
    hf_token: str


# endregion


# region --- HfLocalTextClassificationPipe ---


class RenderedHfLocalTextClassificationPipeConfig(RenderedPipeConfig):
    prompt: str
    model: str
    token: str


class HfLocalTextClassificationPipeConfig(RawPipeConfig):
    prompt: str
    model: str
    token: str


# endregion


# region --- JinjaExpressionPipe ---


class RenderedJinjaExpressionPipeConfig(RenderedPipeConfig):
    expression: str


class JinjaExpressionPipeConfig(RawPipeConfig):
    expression: str


# endregion


# region --- TicketFetchPipe ---


class RenderedTicketFetchPipeConfig(RenderedPipeConfig):
    ticket_search_criteria: TicketSearchCriteria | None = None


class TicketFetchPipeConfig(RawPipeConfig):
    ticket_search_criteria: str | TicketSearchCriteria | dict[str, Any] | None = None


# endregion


# region --- TicketUpdatePipe ---


class RenderedTicketUpdatePipeConfig(RenderedPipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicketBase


class TicketUpdatePipeConfig(RawPipeConfig):
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicketBase


# endregion


# region --- TicketAddNotePipe ---


class RenderedTicketAddNotePipeConfig(RenderedPipeConfig):
    ticket_id: str | int
    note: UnifiedNote


class TicketAddNotePipeConfig(RawPipeConfig):
    ticket_id: str | int
    note: str | UnifiedNote | dict[str, Any]


# endregion


# Backward compatibility aliases
HFLocalAIInferencePipeModel = HFLocalAIInferencePipeConfig
RenderedHFLocalAIInferencePipeModel = RenderedHFLocalAIInferencePipeConfig

FetchTicketsPipeConfig = TicketFetchPipeConfig
RenderedFetchTicketsPipeConfig = RenderedTicketFetchPipeConfig
RenderedFetchTicketsPipeModel = RenderedTicketFetchPipeConfig
FetchTicketsPipeModel = TicketFetchPipeConfig

UpdateTicketPipeConfig = TicketUpdatePipeConfig
RenderedUpdateTicketPipeConfig = RenderedTicketUpdatePipeConfig
RenderedUpdateTicketPipeModel = RenderedTicketUpdatePipeConfig
UpdateTicketPipeModel = TicketUpdatePipeConfig

AddNotePipeConfig = TicketAddNotePipeConfig
RenderedAddNotePipeConfig = RenderedTicketAddNotePipeConfig
RenderedAddNotePipeModel = RenderedTicketAddNotePipeConfig
AddNotePipeModel = TicketAddNotePipeConfig
