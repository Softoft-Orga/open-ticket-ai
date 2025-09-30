import json

from pydantic import BaseModel

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.util.path_util import find_python_code_root_path


class RootConfig(BaseModel):

    open_ticket_ai: RawOpenTicketAIConfig


if __name__ == "__main__":
    """Generates JSON schema for RootConfig and writes it to config.schema.json."""
    schema: dict = RootConfig.model_json_schema()
    project_root_dir = find_python_code_root_path().parent
    with open(project_root_dir / "config.schema.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
