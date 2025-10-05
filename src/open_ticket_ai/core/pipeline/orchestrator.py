# orchestrator.py
from __future__ import annotations

import logging
from typing import Any

from injector import inject, singleton
from prefect import aserve
from prefect.deployments.runner import RunnerDeployment

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.pipeline.orchestrator_config import OrchestratorConfig, RunnerDefinition
from open_ticket_ai.core.pipeline.prefect_flows import (
    execute_scheduled_pipe_flow,
    create_interval_schedule,
)


@singleton
class Orchestrator:
    @inject
    def __init__(self, app_config: RawOpenTicketAIConfig) -> None:
        self._app_config = app_config
        self._config = OrchestratorConfig.from_raw(app_config.orchestrator)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.warning(self._config)
        self._deployments: list[RunnerDeployment] = []
        self._running = False

    async def _create_deployment(self, definition: RunnerDefinition, index: int) -> RunnerDeployment:
        deployment_name = f"{definition.pipe_id}_{index}"

        params = {
            "app_config": self._app_config.model_dump(mode="json"),
            "definition": definition.model_dump(mode="json"),
        }

        deployment_params: dict[str, Any] = {"name": deployment_name, "parameters": params,
                                             "tags": ["open-ticket-ai", definition.pipe_id]
                                             }

        if definition.interval_seconds > 0:
            deployment_params["interval"] = create_interval_schedule(max(definition.interval_seconds, 0.5))
            self._logger.info(
                "Creating Prefect deployment for pipe '%s' with %.2f second interval",
                definition.pipe_id,
                definition.interval_seconds,
            )
        else:
            self._logger.info(
                "Creating Prefect deployment for pipe '%s' (manual trigger only)",
                definition.pipe_id,
            )

        return await execute_scheduled_pipe_flow.ato_deployment(**deployment_params)

    async def start(self) -> None:
        self._logger.warning(self._config)
        if self._running:
            self._logger.debug("Prefect orchestrator already running")
            return

        self._logger.info("Starting Prefect orchestrator with %d runner(s)", len(self._config.runners))
        for index, definition in enumerate(self._config.runners):
            deployment = await self._create_deployment(definition, index)
            self._deployments.append(deployment)

        self._running = True
        self._logger.info("Prefect orchestrator started successfully")

    async def stop(self) -> None:
        if not self._running:
            self._logger.debug("Prefect orchestrator stop requested but it is not running")
            return

        self._logger.info("Stopping Prefect orchestrator")
        self._deployments.clear()
        self._running = False
        self._logger.info("Prefect orchestrator stopped successfully")

    async def run(self) -> None:
        await self.start()
        if not self._deployments:
            self._logger.warning("No deployments to serve")
            return
        try:
            self._logger.info("Serving %d Prefect deployment(s)", len(self._deployments))
            await aserve(*self._deployments)
        finally:
            await self.stop()

    async def run_once(self, pipe_id: str) -> dict[str, Any]:
        definition = next((d for d in self._config.runners if d.pipe_id == pipe_id), None)
        if definition is None:
            raise ValueError(f"Pipe '{pipe_id}' not found in orchestrator configuration")

        return await execute_scheduled_pipe_flow(
            app_config=self._app_config.model_dump(mode="json"),
            definition=definition.model_dump(mode="json"),
        )
