from collections.abc import Callable
from typing import Any

from packaging.specifiers import SpecifierSet
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class VersionSpecifier(SpecifierSet):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        def from_str(v: str) -> VersionSpecifier:
            return cls(v)

        from_str_schema = core_schema.chain_schema(
            [core_schema.str_schema(), core_schema.no_info_plain_validator_function(from_str)]
        )
        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema([core_schema.is_instance_schema(SpecifierSet), from_str_schema]),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())
