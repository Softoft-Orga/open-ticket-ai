import pytest
from pydantic import Field, ValidationError

from open_ticket_ai.core.base_model import StrictBaseModel


class SampleModel(StrictBaseModel):
    name: str = Field(description="Name of the item for identification purposes.")
    count: int = Field(default=0, description="Number of items in the collection.")
    tags: list[str] = Field(default_factory=list, description="List of tags for categorizing and organizing items.")
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Dictionary of key-value metadata for additional context."
    )


def test_openticketai_base_model_creation():
    model = SampleModel(name="test", count=5)
    assert model.name == "test"
    assert model.count == 5
    assert model.tags == []
    assert model.metadata == {}


def test_openticketai_base_model_with_defaults():
    model = SampleModel(name="test")
    assert model.name == "test"
    assert model.count == 0
    assert model.tags == []
    assert model.metadata == {}


def test_openticketai_base_model_with_mutable_defaults():
    model1 = SampleModel(name="model1")
    model2 = SampleModel(name="model2")

    assert model1.tags is not model2.tags
    assert model1.metadata is not model2.metadata


def test_openticketai_base_model_is_frozen():
    model = SampleModel(name="test", count=5)
    with pytest.raises(ValidationError):
        model.name = "new_name"


def test_openticketai_base_model_forbids_extra_fields():
    with pytest.raises(ValidationError):
        SampleModel(name="test", invalid_field="value")


def test_openticketai_base_model_field_descriptions():
    schema = SampleModel.model_json_schema()
    assert "name" in schema["properties"]
    assert schema["properties"]["name"]["description"] == "Name of the item for identification purposes."
    assert schema["properties"]["count"]["description"] == "Number of items in the collection."
    assert schema["properties"]["tags"]["description"] == "List of tags for categorizing and organizing items."
    assert schema["properties"]["metadata"]["description"] == "Dictionary of key-value metadata for additional context."


def test_openticketai_base_model_validation_error_on_missing_required():
    with pytest.raises(ValidationError) as exc_info:
        SampleModel(count=5)

    errors = exc_info.value.errors()
    assert any(error["loc"] == ("name",) for error in errors)


@pytest.mark.parametrize(
    "name,count,tags,metadata",
    [
        ("test1", 1, ["tag1"], {"key1": "value1"}),
        ("test2", 2, ["tag1", "tag2"], {"key1": "value1", "key2": "value2"}),
        ("test3", 0, [], {}),
    ],
)
def test_openticketai_base_model_parametrized_creation(name, count, tags, metadata):
    model = SampleModel(name=name, count=count, tags=tags, metadata=metadata)
    assert model.name == name
    assert model.count == count
    assert model.tags == tags
    assert model.metadata == metadata
