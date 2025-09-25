from typing import Any, Dict, Optional, DefaultDict
from collections import defaultdict
from pydantic import BaseModel, Field, field_validator

from open_ticket_ai.src.core.pipeline.status import PipelineStatus


class MetaInfo(BaseModel):
    """Metadata about pipeline execution, including status, errors, and events.
    
    Events are stored in a nested dictionary structure where each level can have
    arbitrary string keys mapping to other dictionaries or values.
    """
    status: PipelineStatus = PipelineStatus.RUNNING
    events: Dict[str, Any] = Field(
        default_factory=lambda: defaultdict(dict),
        description="Nested dictionary for tracking pipeline events and their statuses"
    )
    
    def add_event(self, *keys: str, value: Any) -> None:
        """Add an event to the events dictionary with nested keys.
        
        Example:
            meta_info.add_event("queue_update_operation", "success", value=True)
            # Results in: {"queue_update_operation": {"success": True}}
        """
        if not keys:
            raise ValueError("At least one key must be provided")
            
        current = self.events
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value
    
    def get_event(self, *keys: str, default: Any = None) -> Any:
        """Get an event value using nested keys.
        
        Example:
            success = meta_info.get_event("queue_update_operation", "success", default=False)
        """
        current = self.events
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current
    
    @property
    def has_error(self) -> bool:
        """Check if there is an error."""
        return self.error is not None
