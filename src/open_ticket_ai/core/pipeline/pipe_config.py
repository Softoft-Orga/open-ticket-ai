from __future__ import annotations

import warnings
from collections.abc import Iterable
from functools import reduce
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from open_ticket_ai.core.config.registerable import RegisterableConfig

CONTROL_KEYS_FOR_MIGRATION = {
    "id",
    "uid",
    "use",
    "steps",
    "depends_on",
    "if",
    "if_",
    "params",
    "injects",
}


class RenderedPipeConfig(RegisterableConfig):
    model_config = ConfigDict(extra="allow")
    if_: bool = Field(default=True, alias="if")
    depends_on: list[str] = []
    params: dict[str, Any] = Field(default_factory=dict)

    @property
    def should_run(self) -> bool:
        return self.if_

    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        model_fields = set(cls.model_fields.keys())
        legacy_fields = {k: v for k, v in data.items() if k not in CONTROL_KEYS_FOR_MIGRATION and k not in model_fields}

        if legacy_fields and not data.get("params"):
            warnings.warn(
                f"Deprecated: Found user fields at top-level in rendered pipe config '{data.get('id', 'unknown')}': "
                f"{list(legacy_fields.keys())}. These should be in 'params' field. "
                "Auto-migrating for backwards compatibility, but this will be removed in a future version.",
                DeprecationWarning,
                stacklevel=4,
            )
            migrated = {k: v for k, v in data.items() if k in CONTROL_KEYS_FOR_MIGRATION or k in model_fields}
            migrated["params"] = legacy_fields
            return migrated

        if legacy_fields and data.get("params"):
            warnings.warn(
                f"Deprecated: Found user fields at both top-level and in 'params' in rendered pipe config "
                f"'{data.get('id', 'unknown')}'. Top-level fields {list(legacy_fields.keys())} "
                "will be ignored. Please use only the 'params' field.",
                DeprecationWarning,
                stacklevel=4,
            )

        return data


class RawPipeConfig(RegisterableConfig):
    model_config = ConfigDict(extra="allow")
    if_: str | bool = Field(default="True", alias="if")
    depends_on: str | list[str] = []
    params: dict[str, Any] = Field(default_factory=dict)

    @property
    def _if(self) -> str | bool:
        return self.if_

    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        model_fields = set(cls.model_fields.keys())
        legacy_fields = {k: v for k, v in data.items() if k not in CONTROL_KEYS_FOR_MIGRATION and k not in model_fields}

        if legacy_fields and not data.get("params"):
            warnings.warn(
                f"Deprecated: Found user fields at top-level in raw pipe config '{data.get('id', 'unknown')}': "
                f"{list(legacy_fields.keys())}. These should be in 'params' field. "
                "Auto-migrating for backwards compatibility, but this will be removed in a future version.",
                DeprecationWarning,
                stacklevel=4,
            )
            migrated = {k: v for k, v in data.items() if k in CONTROL_KEYS_FOR_MIGRATION or k in model_fields}
            migrated["params"] = legacy_fields
            return migrated

        if legacy_fields and data.get("params"):
            warnings.warn(
                f"Deprecated: Found user fields at both top-level and in 'params' in raw pipe config "
                f"'{data.get('id', 'unknown')}'. Top-level fields {list(legacy_fields.keys())} "
                "will be ignored. Please use only the 'params' field.",
                DeprecationWarning,
                stacklevel=4,
            )

        return data


class PipeResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    success: bool
    failed: bool
    message: str = ""
    data: dict[str, Any] = Field(default_factory=dict)

    def __and__(self, other: Self) -> Self:
        merged_data = {**self.data, **other.data}
        merged_msg = " ".join([m for m in [self.message, other.message] if m])
        return PipeResult(
            success=self.success and other.success,
            failed=self.failed and other.failed,
            message=merged_msg,
            data=merged_data,
        )

    @classmethod
    def union(cls, results: Iterable[PipeResult]) -> PipeResult:
        if not results:
            return PipeResult(success=True, failed=False)
        return reduce(lambda a, b: a & b, results)
