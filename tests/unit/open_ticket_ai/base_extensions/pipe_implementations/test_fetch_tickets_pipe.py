"""
Pytest tests for FetchTicketsPipe.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from open_ticket_ai.core.pipeline.context import PipelineContext
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import TicketSystemAdapter
from open_ticket_ai.core.ticket_system_integration.unified_models import (
    TicketSearchCriteria,
    UnifiedEntity,
    UnifiedTicket,
)
from open_ticket_ai.base_extensions.pipe_implementations.fetch_tickets_pipe import FetchTicketsPipe
from open_ticket_ai.base_extensions.pipe_implementations.pipe_configs import FetchTicketsPipeConfig


@pytest.fixture
def sample_config():
    """Create a sample FetchTicketsPipeConfig for testing."""
    return FetchTicketsPipeConfig(
        name="test_fetch_tickets",
        use="open_ticket_ai.extensions.FetchTicketsPipe",
        ticket_search_criteria={"queue": {"id": 1, "name": "IT Support"}, "limit": 10, "offset": 0},
    )


@pytest.fixture
def sample_context():
    """Create a sample PipelineContext for testing."""
    return PipelineContext(pipes={}, config={})


@pytest.fixture
def mock_ticket_system():
    """Create a mock TicketSystemAdapter."""
    return MagicMock(spec=TicketSystemAdapter)


@pytest.fixture
def sample_tickets():
    """Create sample tickets for testing."""
    return [
        UnifiedTicket(
            id=1, subject="Test Ticket 1", queue=UnifiedEntity(id=1, name="IT Support"), body="Test ticket body 1"
        ),
        UnifiedTicket(
            id=2, subject="Test Ticket 2", queue=UnifiedEntity(id=1, name="IT Support"), body="Test ticket body 2"
        ),
    ]


class TestFetchTicketsPipe:
    """Test cases for FetchTicketsPipe."""

    def test_init(self, sample_config, mock_ticket_system):
        """Test pipe initialization."""
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)
        assert pipe.config == sample_config
        assert pipe.ticket_system == mock_ticket_system

    async def test_process_success(self, sample_config, sample_context, mock_ticket_system, sample_tickets):
        """Test successful ticket fetching."""
        mock_ticket_system.find_tickets = AsyncMock(return_value=sample_tickets)
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)

        result = await pipe._process(sample_context)

        assert "found_tickets" in result
        assert len(result["found_tickets"]) == 2
        assert result["found_tickets"][0]["id"] == 1
        assert result["found_tickets"][0]["subject"] == "Test Ticket 1"
        assert result["found_tickets"][1]["id"] == 2
        assert result["found_tickets"][1]["subject"] == "Test Ticket 2"

        # Verify the ticket system was called with correct criteria
        mock_ticket_system.find_tickets.assert_called_once()
        call_args = mock_ticket_system.find_tickets.call_args[0][0]
        assert isinstance(call_args, TicketSearchCriteria)
        assert call_args.limit == 10
        assert call_args.offset == 0

    async def test_process_no_tickets_found(self, sample_config, sample_context, mock_ticket_system):
        """Test when no tickets are found."""
        mock_ticket_system.find_tickets = AsyncMock(return_value=[])
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)

        result = await pipe._process(sample_context)

        assert result == {"found_tickets": []}
        mock_ticket_system.find_tickets.assert_called_once()

    async def test_process_no_search_criteria(self, sample_context, mock_ticket_system):
        """Test processing without search criteria."""
        config = FetchTicketsPipeConfig(name="test_fetch_tickets", use="open_ticket_ai.extensions.FetchTicketsPipe")
        pipe = FetchTicketsPipe(config, mock_ticket_system)

        result = await pipe._process(sample_context)

        assert result["_status"] == "error"
        assert "No search criteria provided" in result["_error"]
        mock_ticket_system.find_tickets.assert_not_called()

    async def test_process_none_search_criteria(self, sample_context, mock_ticket_system):
        """Test processing with None search criteria."""
        config = FetchTicketsPipeConfig(
            name="test_fetch_tickets", use="open_ticket_ai.extensions.FetchTicketsPipe", ticket_search_criteria=None
        )
        pipe = FetchTicketsPipe(config, mock_ticket_system)

        result = await pipe._process(sample_context)

        assert result["_status"] == "error"
        assert "No search criteria provided" in result["_error"]
        mock_ticket_system.find_tickets.assert_not_called()

    async def test_process_with_ticket_system_exception(self, sample_config, sample_context, mock_ticket_system):
        """Test processing when ticket system raises an exception."""
        mock_ticket_system.find_tickets = AsyncMock(side_effect=Exception("Database connection failed"))
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)

        with pytest.raises(Exception, match="Database connection failed"):
            await pipe._process(sample_context)

    def test_convert_to_search_criteria_dict(self, sample_config, mock_ticket_system):
        """Test _convert_to_search_criteria with dictionary input."""
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)
        criteria_dict = {"queue": {"id": 2, "name": "Bug Reports"}, "limit": 5, "offset": 10}

        result = pipe._convert_to_search_criteria(criteria_dict)

        assert isinstance(result, TicketSearchCriteria)
        assert result.limit == 5
        assert result.offset == 10
        assert result.queue.id == 2
        assert result.queue.name == "Bug Reports"

    def test_convert_to_search_criteria_object(self, sample_config, mock_ticket_system):
        """Test _convert_to_search_criteria with TicketSearchCriteria object input."""
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)
        criteria = TicketSearchCriteria(queue=UnifiedEntity(id=3, name="Feature Requests"), limit=20, offset=5)

        result = pipe._convert_to_search_criteria(criteria)

        assert result is criteria  # Should return the same object
        assert result.limit == 20
        assert result.offset == 5
        assert result.queue.id == 3

    async def test_process_with_single_ticket(self, sample_config, sample_context, mock_ticket_system):
        """Test processing with a single ticket result."""
        single_ticket = [
            UnifiedTicket(
                id=42,
                subject="Single Test Ticket",
                queue=UnifiedEntity(id=1, name="IT Support"),
                body="Single ticket body",
            )
        ]
        mock_ticket_system.find_tickets = AsyncMock(return_value=single_ticket)
        pipe = FetchTicketsPipe(sample_config, mock_ticket_system)

        result = await pipe._process(sample_context)

        assert "found_tickets" in result
        assert len(result["found_tickets"]) == 1
        assert result["found_tickets"][0]["id"] == 42
        assert result["found_tickets"][0]["subject"] == "Single Test Ticket"

    async def test_process_with_complex_search_criteria(self, sample_context, mock_ticket_system, sample_tickets):
        """Test processing with complex search criteria."""
        config = FetchTicketsPipeConfig(
            name="test_fetch_tickets",
            use="open_ticket_ai.extensions.FetchTicketsPipe",
            ticket_search_criteria={"queue": {"id": 5, "name": "Priority Queue"}, "limit": 100, "offset": 50},
        )
        mock_ticket_system.find_tickets = AsyncMock(return_value=sample_tickets)
        pipe = FetchTicketsPipe(config, mock_ticket_system)

        result = await pipe._process(sample_context)

        assert len(result["found_tickets"]) == 2

        # Verify the search criteria was properly converted
        call_args = mock_ticket_system.find_tickets.call_args[0][0]
        assert call_args.limit == 100
        assert call_args.offset == 50
        assert call_args.queue.id == 5
        assert call_args.queue.name == "Priority Queue"
