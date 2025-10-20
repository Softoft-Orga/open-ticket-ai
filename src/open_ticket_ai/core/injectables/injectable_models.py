from typing import Any

from pydantic import Field

from open_ticket_ai.core.base_model import StrictBaseModel


class InjectableConfigBase(StrictBaseModel):
    use: str = Field(
        default="base:CompositePipe",
        description=(
            "Fully qualified class path of the injectables implementation to instantiate for this configuration."
        ),
    )
    injects: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Mapping of parameter names to dependency injection bindings for resolving constructor dependencies."
        ),
    )
    params: dict[str, Any] = Field(
        default_factory=dict,
        description="Dictionary of configuration parameters passed to the injectables instance during initialization.",
    )

    def __hash__(self) -> int:
        """Hash based on content (excluding uid for semantic equality)."""
        return hash(self.model_dump_json())

    def __eq__(self, other: Any) -> bool:
        """Semantic equality - configs with same content are equal."""
        if not isinstance(other, InjectableConfigBase):
            return False
        return hash(self) == hash(other)


class InjectableConfig(InjectableConfigBase):
    id: str = Field(
        default="",
        description=(
            "Human-readable identifier for this injectables used for referencing in configurations and dependencies."
        ),
    )
