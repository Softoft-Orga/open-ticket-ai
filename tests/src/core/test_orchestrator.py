"""Unit tests for the :mod:`orchestrator` module."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import schedule

from pathlib import Path
import sys

# Ensure the project root is on the import path so the ``open_ticket_ai``
# package can be imported when tests are executed from the ``tests`` directory.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from open_ticket_ai.core.orchestrator import Orchestrator
from open_ticket_ai.core.pipeline.context import PipelineContext


def _make_pipeline(interval: int, unit: str) -> MagicMock:
    """Create a mock pipeline with a minimal schedule configuration."""

    pipeline = MagicMock()
    pipeline.config = SimpleNamespace(schedule=SimpleNamespace(interval=interval, unit=unit))
    return pipeline


def test_set_schedules_runs_each_pipeline_once() -> None:
    """Each pipeline should be scheduled independently."""

    schedule.clear()
    p1 = _make_pipeline(1, "seconds")
    p2 = _make_pipeline(1, "seconds")

    orchestrator = Orchestrator(pipelines=[p1, p2], config=MagicMock())
    orchestrator.set_schedules()

    # Two jobs should be registered, one for each pipeline
    assert len(schedule.get_jobs()) == 2

    schedule.run_all(delay_seconds=0)

    assert p1.execute.call_count == 1
    assert p2.execute.call_count == 1


def test_set_schedules_passes_pipeline_context_and_config() -> None:
    """Scheduled jobs should honour the interval/unit and supply a context."""

    schedule.clear()
    pipeline = _make_pipeline(2, "minutes")

    orchestrator = Orchestrator(pipelines=[pipeline], config=MagicMock())
    orchestrator.set_schedules()

    # Verify job was configured correctly
    job = schedule.get_jobs()[0]
    assert job.interval == 2
    assert job.unit == "minutes"

    schedule.run_all(delay_seconds=0)

    # Pipeline receives a PipelineContext instance
    (context,), _ = pipeline.execute.call_args
    assert isinstance(context, PipelineContext)

    schedule.clear()
