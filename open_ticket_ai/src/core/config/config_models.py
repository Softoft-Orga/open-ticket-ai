# FILE_PATH: open_ticket_ai\src\ce\core\config\config_models.py
# In open_ticket_ai/src/ce/core/config/config_models.py
from pathlib import Path

from pydantic import BaseModel, Field

from open_ticket_ai.src.base.otobo_integration.otobo_adapter_config import OTOBOAdapterConfig


class OpenTicketAIConfig(BaseModel):
    """Root configuration model for Open Ticket AI."""
    system: OTOBOAdapterConfig
    # Pipe-specific configurations (now global)
    filter_by_queue: str = Field(..., description="The queue to fetch tickets from.")

    hf_model_queue: str = Field(..., description="The Hugging Face model to use for inference.")
    hf_model_queue_token_env_var: str = Field(..., description="The environment variable for the Hugging Face token.")

    queue_confidence_threshold: float = Field(..., gt=0, lt=1,
                                              description="The confidence threshold for AI predictions.")
    low_confidence_queue: str = Field(...,
                                      description="The queue to move tickets to if confidence is below the threshold.")

    hf_model_priority: str = Field(..., description="The Hugging Face model to use for inference.")
    hf_model_priority_token_env_var: str = Field(...,
                                                 description="The environment variable for the Hugging Face token.")
    priority_confidence_threshold: float = Field(..., gt=0, lt=1,
                                                 description="The confidence threshold for AI predictions.")
    low_confidence_priority: str = Field(...,
                                         description="The queue to move tickets to if confidence is below the threshold.")

    run_every_milli_seconds: int = Field(..., gt=0, description="Execution interval in milli seconds.")


def load_config(path: str | Path) -> OpenTicketAIConfig:
    """Load YAML config with root key 'open_ticket_ai'."""
    import yaml

    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    if "open_ticket_ai" not in data:
        raise KeyError("Missing 'open_ticket_ai' root key")

    return OpenTicketAIConfig(**data["open_ticket_ai"])
