from typing import Any

from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig, RenderedPipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicketBase,
    UnifiedNote,
)


class RenderedJinjaExpressionPipeConfig(RenderedPipeConfig):
    expression: str


class RawJinjaExpressionPipeConfig(RawPipeConfig):
    expression: str


class RenderedTicketFetchPipeConfig(RenderedPipeConfig):
    ticket_search_criteria: TicketSearchCriteria | None = None


class RawTicketFetchPipeConfig(RawPipeConfig):
    ticket_search_criteria: str | TicketSearchCriteria | dict[str, Any] | None = None

class RenderedTicketUpdatePipeConfig(RenderedPipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicketBase


class RawTicketUpdatePipeConfig(RawPipeConfig):
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicketBase


class RenderedTicketAddNotePipeConfig(RenderedPipeConfig):
    ticket_id: str | int
    note: UnifiedNote


class RawTicketAddNotePipeConfig(RawPipeConfig):
    ticket_id: str | int
    note: str | UnifiedNote | dict[str, Any]
