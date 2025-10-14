import asyncio
from typing import Any
from unittest.mock import MagicMock

import pytest

from open_ticket_ai.core.logging_iface import AppLogger, LoggerFactory
from open_ticket_ai.core.orchestration.orchestrator import Orchestrator
from open_ticket_ai.core.orchestration.orchestrator_models import (
    OrchestratorConfig,
    RunnerDefinition,
    TriggerConfig,
)
from open_ticket_ai.core.orchestration.trigger import Trigger
from open_ticket_ai.core.pipeline.pipe_models import PipeConfig
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory

pytestmark = [pytest.mark.unit]


class FakeLogger(AppLogger):
    def debug(self, message: str, **kwargs: Any) -> None:
        pass

    def info(self, message: str, **kwargs: Any) -> None:
        pass

    def warning(self, message: str, **kwargs: Any) -> None:
        pass

    def error(self, message: str, **kwargs: Any) -> None:
        pass

    def exception(self, message: str, **kwargs: Any) -> None:
        pass


class FakeLoggerFactory(LoggerFactory):
    def create(self, name: str, **context: Any) -> AppLogger:
        del name, context
        return FakeLogger()


class MockTrigger(Trigger):
    def __init__(self, config: TriggerConfig, logger_factory: LoggerFactory, *args: Any, **kwargs: Any) -> None:
        del args, kwargs
        self.trigger_def = config
        self._observers: list[Any] = []
        self._running = False
        self._logger = logger_factory.create(self.__class__.__name__)
        self.started = False
        self.stopped = False

    def attach(self, observer: Any) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Any) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def start(self) -> None:
        self.started = True
        self._running = True

    def stop(self) -> None:
        self.stopped = True
        self._running = False

    @staticmethod
    def get_params_model() -> type:
        from pydantic import BaseModel

        return BaseModel


@pytest.fixture
def mock_logger_factory() -> LoggerFactory:
    return FakeLoggerFactory()


@pytest.fixture
def mock_renderable_factory(mock_logger_factory: LoggerFactory) -> RenderableFactory:
    factory = MagicMock(spec=RenderableFactory)
    factory.render.side_effect = lambda config, _scope: MockTrigger(config, mock_logger_factory)
    return factory


@pytest.fixture
def empty_orchestrator_config() -> OrchestratorConfig:
    return OrchestratorConfig(runners=[])


@pytest.fixture
def orchestrator_config_with_runners() -> OrchestratorConfig:
    trigger_config = TriggerConfig(id="test_trigger", use="test.MockTrigger")
    pipe_config = PipeConfig(id="test_pipe", use="test.TestPipe")
    runner_def = RunnerDefinition(id="test_runner", on=[trigger_config], run=pipe_config)
    return OrchestratorConfig(runners=[runner_def])


def test_orchestrator_start_stop_empty(
    mock_renderable_factory: RenderableFactory,
    empty_orchestrator_config: OrchestratorConfig,
    mock_logger_factory: LoggerFactory,
) -> None:
    orchestrator = Orchestrator(mock_renderable_factory, empty_orchestrator_config, mock_logger_factory)
    orchestrator.start()
    assert len(orchestrator._trigger_registry) == 0
    assert len(orchestrator._runners) == 0
    orchestrator.stop()
    assert len(orchestrator._trigger_registry) == 0
    assert len(orchestrator._runners) == 0


def test_orchestrator_start_registers_triggers(
    mock_renderable_factory: RenderableFactory,
    orchestrator_config_with_runners: OrchestratorConfig,
    mock_logger_factory: LoggerFactory,
) -> None:
    orchestrator = Orchestrator(mock_renderable_factory, orchestrator_config_with_runners, mock_logger_factory)
    orchestrator.start()
    assert len(orchestrator._trigger_registry) == 1
    assert len(orchestrator._runners) == 1
    trigger = orchestrator._trigger_registry["test_trigger"]
    assert isinstance(trigger, MockTrigger)
    assert trigger.started is True


def test_orchestrator_stop_clears_registry(
    mock_renderable_factory: RenderableFactory,
    orchestrator_config_with_runners: OrchestratorConfig,
    mock_logger_factory: LoggerFactory,
) -> None:
    orchestrator = Orchestrator(mock_renderable_factory, orchestrator_config_with_runners, mock_logger_factory)
    orchestrator.start()
    trigger = orchestrator._trigger_registry["test_trigger"]
    assert isinstance(trigger, MockTrigger)
    orchestrator.stop()
    assert len(orchestrator._trigger_registry) == 0
    assert len(orchestrator._runners) == 0
    assert trigger.stopped is True


@pytest.mark.asyncio
async def test_orchestrator_run_with_exception(
    mock_renderable_factory: RenderableFactory,
    orchestrator_config_with_runners: OrchestratorConfig,
    mock_logger_factory: LoggerFactory,
) -> None:
    orchestrator = Orchestrator(mock_renderable_factory, orchestrator_config_with_runners, mock_logger_factory)

    async def mock_run() -> None:
        orchestrator.start()
        await asyncio.sleep(0.01)
        raise KeyboardInterrupt("Test interrupt")

    try:
        await mock_run()
    except KeyboardInterrupt:
        orchestrator.stop()

    assert len(orchestrator._trigger_registry) == 0
    assert len(orchestrator._runners) == 0


def test_orchestrator_trigger_reuse(
    mock_renderable_factory: RenderableFactory, mock_logger_factory: LoggerFactory
) -> None:
    trigger_config = TriggerConfig(id="shared_trigger", use="test.MockTrigger")
    pipe_config_1 = PipeConfig(id="pipe_1", use="test.TestPipe")
    pipe_config_2 = PipeConfig(id="pipe_2", use="test.TestPipe")
    runner_def_1 = RunnerDefinition(id="runner_1", on=[trigger_config], run=pipe_config_1)
    runner_def_2 = RunnerDefinition(id="runner_2", on=[trigger_config], run=pipe_config_2)
    config = OrchestratorConfig(runners=[runner_def_1, runner_def_2])

    orchestrator = Orchestrator(mock_renderable_factory, config, mock_logger_factory)
    orchestrator.start()

    assert len(orchestrator._trigger_registry) == 1
    assert len(orchestrator._runners) == 2
    trigger = orchestrator._trigger_registry["shared_trigger"]
    assert len(trigger._observers) == 2
