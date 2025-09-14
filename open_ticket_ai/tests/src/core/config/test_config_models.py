import textwrap
from pathlib import Path

import pytest

from open_ticket_ai.src.core.config.config_models import (
    OpenTicketAIConfig,
    PipeConfig,
    PipelineConfig,
    ScheduleConfig,
    SystemConfig,
    load_config,
)


def test_load_config_success(tmp_path: Path) -> None:
    content = textwrap.dedent(
        """
        open_ticket_ai:
          system:
            id: system
            provider_key: SystemProvider
          pipes:
            - id: p1
              provider_key: Provider1
            - id: p2
              provider_key: Provider2
          pipelines:
            - id: pipe_line
              schedule:
                interval: 5
                unit: seconds
              pipes:
                - p1
                - p2
        """
    )
    path = tmp_path / "config.yml"
    path.write_text(content)

    cfg = load_config(path)

    assert cfg.system.id == "system"
    assert [p.id for p in cfg.pipes] == ["p1", "p2"]
    assert cfg.pipeline[0].run_every_seconds.unit == "seconds"


def test_load_config_missing_root_key(tmp_path: Path) -> None:
    path = tmp_path / "config.yml"
    path.write_text("system: {}\n")

    with pytest.raises(KeyError):
        load_config(path)


def test_pipeline_validation_unknown_pipe(tmp_path: Path) -> None:
    content = textwrap.dedent(
        """
        open_ticket_ai:
          system:
            id: system
            provider_key: SystemProvider
          pipes:
            - id: p1
              provider_key: Provider1
          pipelines:
            - id: pipe_line
              schedule:
                interval: 5
                unit: seconds
              pipes:
                - p1
                - p2
        """
    )
    path = tmp_path / "config.yml"
    path.write_text(content)

    with pytest.raises(ValueError):
        load_config(path)


def test_get_all_register_instance_configs() -> None:
    cfg = OpenTicketAIConfig(
        system=SystemConfig(id="sys", provider_key="SystemProvider"),
        pipes=[
            PipeConfig(id="p1", provider_key="Provider1"),
            PipeConfig(id="p2", provider_key="Provider2"),
        ],
        pipeline=[
            PipelineConfig(
                id="pl", run_every_seconds=ScheduleConfig(interval=1, unit="seconds"), pipes=["p1", "p2"]
            )
        ],
    )

    ids = [c.id for c in cfg.get_all_register_instance_configs()]
    assert ids == ["sys", "p1", "p2"]
