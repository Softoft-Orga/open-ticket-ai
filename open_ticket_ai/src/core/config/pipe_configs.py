from pydantic import AliasChoices, ConfigDict, Field

from open_ticket_ai.src.core.config.base_pipe_config import BasePipeConfig


class TicketFilterConfig(BasePipeConfig):
    field: str
    operator: str
    value: str


class TicketFetcherConfig(BasePipeConfig):
    filters: list[TicketFilterConfig] = Field(default_factory=list)
    output_field: str = "ticket"


class HFOutputStructureConfig(BasePipeConfig):
    label_field: str
    confidence_field: str


class HFLocalAIInferenceServiceConfig(BasePipeConfig):
    input_value: str
    hf_model: str
    hf_token_env_var: str | None = None
    output_structure: HFOutputStructureConfig


class ListValueMapperConfig(BasePipeConfig):
    model_config = ConfigDict(populate_by_name=True)

    input_value: str
    output_field: str
    mapping_rules: dict[str, list[str]] = Field(
        default_factory=dict,
        alias="to_value_from_list",
        validation_alias=AliasChoices("to_value_from_list", "to_values_from_list"),
    )


class LowConfidenceHandlerConfig(BasePipeConfig):
    label: str
    confidence: str
    output_field: str
    min_confidence: float
    low_confidence_value: str


class TicketModifierSetOperation(BasePipeConfig):
    ticket_field: str
    value: str | int | float | bool | dict[str, str] | None


class TicketModifierConfig(BasePipeConfig):
    ticket_id: str
    update_operations: list[TicketModifierSetOperation] = Field(default_factory=list)
