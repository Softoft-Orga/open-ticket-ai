import pytest
from abc import ABC, abstractmethod
from typing import Any

from open_ticket_ai.base.base_pipe import BasePipe


class BaseTicketSystemPipeTest(ABC):
    """Base class for ticket system pipe tests to reduce duplication."""
    
    @property
    @abstractmethod
    def pipe_class(self) -> type[BasePipe]:
        """Return the pipe class being tested."""
        pass
    
    @property
    @abstractmethod
    def base_config(self) -> dict[str, Any]:
        """Return base configuration for the pipe."""
        pass
    
    def test_pipe_skips_when_disabled(
        self,
        pipe_runner,
        empty_pipeline_context,
        mock_ticket_system_service,
    ) -> None:
        config = {**self.base_config, "when": False}
        
        result_context = pipe_runner(self.pipe_class, config, empty_pipeline_context)
        
        assert result_context is empty_pipeline_context
    
    def test_pipe_handles_service_failure(
        self,
        pipe_runner,
        empty_pipeline_context,
        mock_ticket_system_service,
    ) -> None:
        mock_ticket_system_service.configure_mock(**{
            f"{self._get_service_method()}.side_effect": RuntimeError("Service error")
        })
        
        config = self.base_config
        
        with pytest.raises(RuntimeError, match="Service error"):
            pipe_runner(self.pipe_class, config, empty_pipeline_context)
    
    @abstractmethod
    def _get_service_method(self) -> str:
        """Return the service method name that should be mocked."""
        pass
