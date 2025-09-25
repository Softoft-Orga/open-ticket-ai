from typing import Dict, Any
from open_ticket_ai.core.config.pipe_configs import ContextModifierConfig
from open_ticket_ai.core.pipeline.pipe import Pipe


class ContextModifier(Pipe[ContextModifierConfig]):
    """
    A pipe implementation that modifies the pipeline context.
    This is a base class that can be extended with specific context modification logic.
    """

    ConfigModel = ContextModifierConfig

    async def _process(self, rendered_config: ContextModifierConfig) -> Dict[str, Any]:
        """
        Process the context modification.

        Args:
            rendered_config: The rendered configuration for the context modification

        Returns:
            An empty dictionary as this is a no-op implementation
        """
        # Base implementation does nothing and returns an empty dict
        return {}
