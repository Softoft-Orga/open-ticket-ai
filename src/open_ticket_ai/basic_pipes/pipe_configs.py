from typing import Any

from open_ticket_ai.core.pipeline.base_pipe_config import RawPipeConfig, RenderedPipeConfig, _BasePipeConfig, PipeConfig
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedTicketBase,
    UnifiedNote,
)


# ----- Jinja Expression -----

class BaseJinjaExpressionPipeConfig(_BasePipeConfig):
    expression: str


class RenderedJinjaExpressionPipeConfig(RenderedPipeConfig, BaseJinjaExpressionPipeConfig):
    pass


class RawJinjaExpressionPipeConfig(RawPipeConfig, BaseJinjaExpressionPipeConfig):
    pass


class JinjaExpressionPipeConfig(PipeConfig[RawJinjaExpressionPipeConfig, RenderedJinjaExpressionPipeConfig]):
    pass


# ----- Ticket Fetch -----
class BaseTicketFetchPipeConfig(_BasePipeConfig):
    ticket_search_criteria: TicketSearchCriteria | None = None


class RenderedTicketFetchPipeConfig(RenderedPipeConfig, BaseTicketFetchPipeConfig):
    pass


class RawTicketFetchPipeConfig(RawPipeConfig, BaseTicketFetchPipeConfig):
    ticket_search_criteria: str | TicketSearchCriteria | dict[str, Any] | None = None


class TicketFetchPipeConfig(PipeConfig[RawTicketFetchPipeConfig, RenderedTicketFetchPipeConfig]):
    pass


# ----- Ticket Update -----
class BaseTicketUpdatePipeConfig(_BasePipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicketBase


class RenderedTicketUpdatePipeConfig(RenderedPipeConfig, BaseTicketUpdatePipeConfig):
    ticket_id: str | int
    updated_ticket: UnifiedTicketBase


class RawTicketUpdatePipeConfig(RawPipeConfig, BaseTicketUpdatePipeConfig):
    ticket_id: str | int
    updated_ticket: str | dict[str, Any] | UnifiedTicketBase


class TicketUpdatePipeConfig(PipeConfig[RawTicketUpdatePipeConfig, RenderedTicketUpdatePipeConfig]):
    pass


# ----- Ticket Add Note -----

class BaseTicketAddNotePipeConfig(_BasePipeConfig):
    ticket_id: str | int
    note: UnifiedNote


class RenderedTicketAddNotePipeConfig(RenderedPipeConfig, BaseTicketAddNotePipeConfig):
    ticket_id: str | int
    note: UnifiedNote


class RawTicketAddNotePipeConfig(RawPipeConfig, BaseTicketAddNotePipeConfig):
    ticket_id: str | int
    note: str | UnifiedNote | dict[str, Any]


class TicketAddNotePipeConfig(PipeConfig[RawTicketAddNotePipeConfig, RenderedTicketAddNotePipeConfig]):
    pass
