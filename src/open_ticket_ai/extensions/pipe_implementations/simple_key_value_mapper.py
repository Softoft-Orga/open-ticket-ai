from typing import Dict, Any, TypeVar

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.config.base_pipe_config import BasePipeConfig
from open_ticket_ai.extensions.pipe_implementations.pipe_configs import SimpleKeyValueMapperConfig

ConfigT = TypeVar("ConfigT", bound=BasePipeConfig)


class SimpleKeyValueMapper(Pipe[SimpleKeyValueMapperConfig]):
    ConfigModel = SimpleKeyValueMapperConfig

    async def _process(self, rendered_config: SimpleKeyValueMapperConfig) -> Dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")
        key = rendered_config.from_key
        if key not in rendered_config.key_to_value_map:
            raise ValueError(f"Key {key} not found in key_to_value_map")
        value = rendered_config.key_to_value_map.get(key)
        return {"to_value": value}
