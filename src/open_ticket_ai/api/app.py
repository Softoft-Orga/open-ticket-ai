"""FastAPI application factory for Open Ticket AI runtime."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI

from open_ticket_ai.api.dependencies import AppState
from open_ticket_ai.api.routers import tickets, workflows

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from open_ticket_ai.settings import Settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Open Ticket AI API starting up")
    yield
    state: AppState = app.state.app_state
    logger.info("Shutting down — stopping all running workflows")
    state.workflow_manager.stop_all()


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title="Open Ticket AI",
        description="REST API for ticket system integration and workflow management",
        version="0.1.0",
        lifespan=_lifespan,
    )
    app.state.app_state = AppState(settings)

    app.include_router(tickets.router)
    app.include_router(workflows.router)

    @app.get("/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
