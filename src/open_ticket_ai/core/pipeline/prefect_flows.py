# prefect_flows.py
from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any

from prefect import flow, task
from prefect.context import TaskRunContext

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig
from open_ticket_ai.core.pipeline.context import Context
from open_ticket_ai.core.pipeline.orchestrator_config import RunnerDefinition
from open_ticket_ai.core.pipeline.pipe_factory import PipeFactory
from open_ticket_ai.core.template_rendering.jinja_renderer import JinjaRenderer
from open_ticket_ai.core.template_rendering.template_renderer import TemplateRenderer

log = logging.getLogger(__name__)


def _build_template_renderer_from_app_config(app_config_dict: dict[str, Any]) -> TemplateRenderer:
    gen = app_config_dict.get("general_config", {})
    tr = gen.get("template_renderer", {})
    rtype = tr.get("type", "jinja")
    if rtype != "jinja":
        raise ValueError(f"Unsupported template renderer type: {rtype}")
    params = tr.get("params", {}) or {}
    return JinjaRenderer(**params)  # same as DI provider


def _build_factory(app_config_dict: dict[str, Any]) -> PipeFactory:
    app_cfg = RawOpenTicketAIConfig.model_validate(app_config_dict)
    renderer = _build_template_renderer_from_app_config(app_config_dict)
    return PipeFactory(app_cfg, renderer)


def is_in_prefect_context() -> bool:
    try:
        TaskRunContext.get()
        return True
    except RuntimeError:
        return False


async def _execute_pipe_internal(
    app_config: dict[str, Any],
    pipe_config: dict[str, Any],
    context_data: dict[str, Any],
    pipe_id: str,
) -> dict[str, Any]:
    context = Context(**context_data)
    pipe_factory = _build_factory(app_config)
    pipe = pipe_factory.create_pipe({}, deepcopy(pipe_config), context.model_dump())
    updated_context = await pipe.process(context)
    return updated_context.model_dump()


def create_pipe_task(pipe_id: str, retries: int = 2, retry_delay_seconds: int = 30):
    @task(name=f"pipe_{pipe_id}", retries=retries, retry_delay_seconds=retry_delay_seconds)
    async def pipe_task(
        app_config: dict[str, Any],
        pipe_config: dict[str, Any],
        context_data: dict[str, Any],
    ) -> dict[str, Any]:
        log.info("Executing pipe '%s' as Prefect task", pipe_id)
        return await _execute_pipe_internal(app_config, pipe_config, context_data, pipe_id)
    
    return pipe_task


async def execute_single_pipe_task(
    app_config: dict[str, Any],
    pipe_config: dict[str, Any],
    context_data: dict[str, Any],
    pipe_id: str,
    retries: int = 2,
    retry_delay_seconds: int = 30,
) -> dict[str, Any]:
    log.info("Creating and executing individual pipe task for '%s'", pipe_id)
    pipe_task = create_pipe_task(pipe_id, retries, retry_delay_seconds)
    return await pipe_task(app_config, pipe_config, context_data)


@task(name="execute_pipe", retries=2, retry_delay_seconds=30)
async def execute_pipe_task(
    app_config: dict[str, Any],
    pipe_config: dict[str, Any],
    context_data: dict[str, Any],
    pipe_id: str,
) -> dict[str, Any]:
    log.info("Executing pipe '%s' as Prefect task (legacy wrapper)", pipe_id)
    retries = pipe_config.get("retries", 2)
    retry_delay_seconds = pipe_config.get("retry_delay_seconds", 30)
    return await execute_single_pipe_task(
        app_config=app_config,
        pipe_config=pipe_config,
        context_data=context_data,
        pipe_id=pipe_id,
        retries=retries,
        retry_delay_seconds=retry_delay_seconds,
    )


@flow(name="execute_scheduled_pipe", log_prints=True)
async def execute_scheduled_pipe_flow(
    app_config: dict[str, Any],
    definition: dict[str, Any],
) -> dict[str, Any]:
    defn = RunnerDefinition.model_validate(definition)
    context_data = Context(config=deepcopy(defn.pipe)).model_dump()
    return await execute_pipe_task(
        app_config=app_config,
        pipe_config=deepcopy(defn.pipe),
        context_data=context_data,
        pipe_id=defn.pipe_id,
    )


from datetime import timedelta


def create_interval_schedule(interval_seconds: float) -> timedelta:
    return timedelta(seconds=interval_seconds)
