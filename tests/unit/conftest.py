from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.config.config_models import InfrastructureConfig, RawOpenTicketAIConfig
from open_ticket_ai.core.config.logging_config import LoggingDictConfig
from open_ticket_ai.core.orchestration.orchestrator_models import OrchestratorConfig
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.renderable.renderable_models import RenderableConfig
from open_ticket_ai.core.ticket_system_integration.ticket_system_service import (
    TicketSystemService,
)
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    UnifiedEntity,
    UnifiedNote,
)
from tests.unit.mocked_ticket_system import MockedTicketSystem

pytestmark = [pytest.mark.unit]


@pytest.fixture
def empty_pipeline_context() -> PipeContext:
    return PipeContext(pipe_results={}, params={})


@pytest.fixture
def mock_ticket_system_service() -> MagicMock:
    mock = MagicMock(spec=TicketSystemService)
    mock.create_ticket = AsyncMock(return_value="TICKET-123")
    mock.update_ticket = AsyncMock(return_value=True)
    mock.add_note = AsyncMock(return_value=True)
    mock.get_ticket = AsyncMock(return_value={})
    return mock


@pytest.fixture
def empty_mocked_ticket_system() -> MockedTicketSystem:
    """Empty MockedTicketSystem for custom test scenarios."""
    return MockedTicketSystem({})


@pytest.fixture(scope="function")
def mocked_ticket_system() -> MockedTicketSystem:
    system = MockedTicketSystem({})

    # Add sample tickets
    system.add_test_ticket(
        id="TICKET-1",
        subject="Test ticket 1",
        body="This is the first test ticket",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="3", name="Medium"),
        notes=[],
    )

    system.add_test_ticket(
        id="TICKET-2",
        subject="Test ticket 2",
        body="This is the second test ticket",
        queue=UnifiedEntity(id="2", name="Development"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[
            UnifiedNote(id="NOTE-1", subject="Initial note", body="First note on ticket 2"),
        ],
    )

    system.add_test_ticket(
        id="TICKET-3",
        subject="Urgent issue",
        body="This needs immediate attention",
        queue=UnifiedEntity(id="1", name="Support"),
        priority=UnifiedEntity(id="5", name="High"),
        notes=[],
    )

    return system


@pytest.fixture
def valid_raw_config() -> RawOpenTicketAIConfig:
    return RawOpenTicketAIConfig(
        infrastructure=InfrastructureConfig(
            logging=LoggingDictConfig(), default_template_renderer="jinja_renderer"
        ),
        services=[
            RenderableConfig(
                id="jinja_renderer",
                use="open_ticket_ai.base.template_renderers.jinja_renderer.JinjaRenderer",
                params={"type": "jinja"},
            )
        ],
        orchestrator=OrchestratorConfig(),
    )


@pytest.fixture
def invalid_raw_config() -> RawOpenTicketAIConfig:
    return RawOpenTicketAIConfig(
        infrastructure=InfrastructureConfig(
            logging=LoggingDictConfig(), default_template_renderer="nonexistent_renderer"
        ),
        services=[],
        orchestrator=OrchestratorConfig(),
    )
