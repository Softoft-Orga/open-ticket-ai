"""Runtime settings — read, update, and inspect the settings schema."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request

from open_ticket_ai.api.models import (
    SettingsFieldInfo,
    SettingsResponse,
    SettingsUpdateRequest,
    SettingsUpdateResponse,
)

if TYPE_CHECKING:
    from open_ticket_ai.api.dependencies import AppState

router = APIRouter(prefix="/api/settings", tags=["settings"])


def _state(request: Request) -> AppState:
    return request.app.state.app_state


@router.get("", response_model=SettingsResponse)
async def get_settings(request: Request) -> SettingsResponse:
    state = _state(request)
    return SettingsResponse(
        settings=state.get_settings_masked(),
        schema_info=state.get_settings_schema(),
    )


@router.put("", response_model=SettingsUpdateResponse)
async def update_settings(request: Request, body: SettingsUpdateRequest) -> SettingsUpdateResponse:
    state = _state(request)
    if not body.settings:
        raise HTTPException(status_code=400, detail="No settings provided")
    try:
        masked, updated = state.update_settings(body.settings)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return SettingsUpdateResponse(settings=masked, updated_fields=updated)


@router.get("/schema", response_model=dict[str, SettingsFieldInfo])
async def get_settings_schema(request: Request) -> dict[str, SettingsFieldInfo]:
    return _state(request).get_settings_schema()
