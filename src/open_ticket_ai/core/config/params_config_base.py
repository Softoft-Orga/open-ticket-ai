from __future__ import annotations

import warnings
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

CONTROL_KEYS = {
    "id",
    "uid",
    "use",
    "steps",
    "depends_on",
    "if",
    "params",
    "injects",
    "triggers",
    "on",
    "pipe",
    "settings",
}


class ParamsConfigBase(BaseModel):
    model_config = ConfigDict(extra="allow")
    params: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def migrate_legacy_fields_to_params(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        legacy_fields = {k: v for k, v in data.items() if k not in CONTROL_KEYS}

        if legacy_fields:
            existing_params = data.get("params", {})

            if existing_params and legacy_fields:
                warnings.warn(
                    f"Deprecated: Top-level fields {list(legacy_fields.keys())} are deprecated. "
                    "Use 'params' field instead. These fields are being ignored because 'params' is already set.",
                    DeprecationWarning,
                    stacklevel=4,
                )
            elif legacy_fields:
                warnings.warn(
                    f"Deprecated: Top-level fields {list(legacy_fields.keys())} are deprecated. "
                    "Use 'params' field instead. Auto-migrating for backwards compatibility.",
                    DeprecationWarning,
                    stacklevel=4,
                )
                data["params"] = {**existing_params, **legacy_fields}

        return data
