"""Pydantic models describing the configuration for individual pipes.

Having dedicated models for every pipe makes it easier to validate the
configuration on start-up and provides typed access to the settings from the
pipe implementations.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TicketFilterConfig(BaseModel):
    """Configuration of a single ticket search filter."""

    field: str
    operator: str
    value: str


class TicketFetcherConfig(BaseModel):
    """Configuration for the ``TicketFetcher`` pipe."""

    filters: list[TicketFilterConfig] = Field(default_factory=list)
    output_field: str = "ticket"


class SubjectBodyPreparerConfig(BaseModel):
    """Configuration for the ``SubjectBodyPreparer`` pipe."""

    subject_field: str
    body_field: str
    output_field: str


class HFOutputStructureConfig(BaseModel):
    """Configuration describing how model outputs should be stored."""

    label_field: str
    confidence_field: str


class HFLocalAIInferenceServiceConfig(BaseModel):
    """Configuration for the ``HFLocalAIInferenceService`` pipe."""

    hf_model: str
    hf_token_env_var: str | None = None
    input_field: str
    output_structure: HFOutputStructureConfig


class ListValueMapperConfig(BaseModel):
    """Configuration for the ``ListValueMapper`` pipe."""

    model_config = ConfigDict(populate_by_name=True)

    input_field: str
    output_field: str
    mapping_rules: dict[str, list[str]] = Field(
        default_factory=dict,
        alias="to_value_from_list",
        validation_alias=AliasChoices("to_value_from_list", "to_values_from_list"),
    )


class LowConfidenceHandlerConfig(BaseModel):
    """Configuration for the ``LowConfidenceHandler`` pipe."""

    label_field: str
    confidence_field: str
    output_field: str
    threshold: float
    low_confidence_value: str


class TicketModifierSetOperation(BaseModel):
    """"Set" ticket update operation."""

    operation: Literal["Set"]
    ticket_field: str
    value: str


class TicketModifierAddNoteOperation(BaseModel):
    """"AddNote" ticket update operation."""

    operation: Literal["AddNote"]
    subject: str
    body: str


TicketModifierOperation = Annotated[
    TicketModifierSetOperation | TicketModifierAddNoteOperation,
    Field(discriminator="operation"),
]


class TicketModifierConfig(BaseModel):
    """Configuration for the ``TicketModifier`` pipe."""

    ticket_id_field: str
    update_operations: list[TicketModifierOperation] = Field(default_factory=list)


class PipesConfig(BaseModel):
    """Container model holding the configuration for every pipe."""

    ticket_fetcher: TicketFetcherConfig
    subject_body_preparer: SubjectBodyPreparerConfig
    queue_ai_model: HFLocalAIInferenceServiceConfig
    priority_ai_model: HFLocalAIInferenceServiceConfig
    queue_mapper: ListValueMapperConfig
    priority_mapper: ListValueMapperConfig
    queue_low_confidence_handler: LowConfidenceHandlerConfig
    priority_low_confidence_handler: LowConfidenceHandlerConfig
    queue_updater: TicketModifierConfig
    queue_note_adder: TicketModifierConfig
    priority_updater: TicketModifierConfig
    priority_note_adder: TicketModifierConfig

