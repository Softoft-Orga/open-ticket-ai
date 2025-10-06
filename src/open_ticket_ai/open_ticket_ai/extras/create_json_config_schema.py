import json
from pathlib import Path

from pydantic import BaseModel

from open_ticket_ai.open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig


class RootConfig(BaseModel):
    open_ticket_ai: RawOpenTicketAIConfig


if __name__ == "__main__":
    """Generates JSON schema for RootConfig and writes it to config.schema.json."""
    schema: dict = RootConfig.model_json_schema()
    with open(Path.cwd() / "config.schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
