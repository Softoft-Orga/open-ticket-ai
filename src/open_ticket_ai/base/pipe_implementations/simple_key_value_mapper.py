from typing import Dict, Any, TypeVar

from open_ticket_ai.core.config.pipe_configs import SimpleKeyValueMapperConfig
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.config.base_pipe_config import BasePipeConfig

ConfigT = TypeVar("ConfigT", bound=BasePipeConfig)


class SimpleKeyValueMapper(Pipe[SimpleKeyValueMapperConfig]):
    ConfigModel = SimpleKeyValueMapperConfig

    async def _process(self, rendered_config: SimpleKeyValueMapperConfig) -> Dict[str, Any]:
        key = rendered_config.from_key
        value = rendered_config.key_to_value_map.get(key)
        return {"to_value": value}
