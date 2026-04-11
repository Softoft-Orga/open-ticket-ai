"""Manages running workflow instances as background asyncio tasks."""

from __future__ import annotations

import asyncio
import datetime
import logging
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from open_ticket_ai.core.pipes.pipe import Pipe
from open_ticket_ai.core.pipes.pipe_context_model import PipeContext

logger = logging.getLogger(__name__)


class WorkflowStatus(StrEnum):
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class WorkflowInstance:
    workflow_id: str
    template_name: str
    parameters: dict[str, Any]
    status: WorkflowStatus = WorkflowStatus.RUNNING
    started_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(tz=datetime.UTC))
    stopped_at: datetime.datetime | None = None
    error: str | None = None
    _task: asyncio.Task[None] | None = field(default=None, repr=False)


class WorkflowManager:
    """Creates, tracks, and stops workflow instances backed by asyncio tasks."""

    def __init__(self) -> None:
        self._workflows: dict[str, WorkflowInstance] = {}

    def start(
        self,
        template_name: str,
        parameters: dict[str, Any],
        pipe: Pipe,
    ) -> WorkflowInstance:
        workflow_id = uuid.uuid4().hex[:12]
        instance = WorkflowInstance(
            workflow_id=workflow_id,
            template_name=template_name,
            parameters=parameters,
        )
        task = asyncio.create_task(
            self._run(instance, pipe),
            name=f"workflow-{workflow_id}",
        )
        instance._task = task
        self._workflows[workflow_id] = instance
        logger.info("Started workflow %s (template=%s)", workflow_id, template_name)
        return instance

    def stop(self, workflow_id: str) -> WorkflowInstance:
        instance = self._workflows.get(workflow_id)
        if instance is None:
            raise KeyError(workflow_id)
        if instance._task and not instance._task.done():
            instance._task.cancel()
        instance.status = WorkflowStatus.STOPPED
        instance.stopped_at = datetime.datetime.now(tz=datetime.UTC)
        logger.info("Stopped workflow %s", workflow_id)
        return instance

    def get(self, workflow_id: str) -> WorkflowInstance:
        instance = self._workflows.get(workflow_id)
        if instance is None:
            raise KeyError(workflow_id)
        self._sync_status(instance)
        return instance

    def list_all(self) -> list[WorkflowInstance]:
        for inst in self._workflows.values():
            self._sync_status(inst)
        return list(self._workflows.values())

    def stop_all(self) -> None:
        for wf_id in list(self._workflows):
            inst = self._workflows[wf_id]
            if inst.status == WorkflowStatus.RUNNING:
                self.stop(wf_id)

    @staticmethod
    def _sync_status(instance: WorkflowInstance) -> None:
        if instance.status != WorkflowStatus.RUNNING:
            return
        if instance._task is None or not instance._task.done():
            return
        exc = instance._task.exception() if not instance._task.cancelled() else None
        if instance._task.cancelled():
            instance.status = WorkflowStatus.STOPPED
        elif exc:
            instance.status = WorkflowStatus.FAILED
            instance.error = str(exc)
        else:
            instance.status = WorkflowStatus.COMPLETED
        instance.stopped_at = datetime.datetime.now(tz=datetime.UTC)

    @staticmethod
    async def _run(instance: WorkflowInstance, pipe: Pipe) -> None:
        try:
            await pipe.process(PipeContext.empty())
        except asyncio.CancelledError:
            logger.info("Workflow %s cancelled", instance.workflow_id)
        except Exception:
            logger.exception("Workflow %s failed", instance.workflow_id)
            instance.status = WorkflowStatus.FAILED
            instance.stopped_at = datetime.datetime.now(tz=datetime.UTC)
            raise
