from typing import Any, Dict

from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.extensions.pipe_implementations.pipe_configs import ContextModifierConfig


class ContextModifier(Pipe[ContextModifierConfig]):
    """
    A pipe implementation that modifies the pipeline context.
    This is a base class that can be extended with specific context modification logic.
    """

    ConfigModel = ContextModifierConfig

    async def _process(self, rendered_config: ContextModifierConfig) -> Dict[str, Any]:
        self._logger.info(f"Running {self.__class__.__name__}")
        # Base implementation does nothing and returns an empty dict
        return {}
