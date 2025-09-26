import enum
import importlib
import pathlib
import sys
import types

from pydantic import BaseModel

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

# Stub pretty_print_config to avoid yaml dependency during imports
dummy_pp = types.ModuleType("open_ticket_ai.src.core.util.pretty_print_config")
dummy_pp.pretty_print_config = lambda config, console: None
sys.modules["open_ticket_ai.src.core.util.pretty_print_config"] = dummy_pp

from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
    PipeConfig,
    PipelineConfig,
    ScheduleConfig,
    SystemConfig,
    ProvidableConfig,
)
from open_ticket_ai.core.dependency_injection.registry import Registry
from open_ticket_ai.core.pipeline.pipe import Pipe
from open_ticket_ai.core.ticket_system_integration.ticket_system_adapter import (
    TicketSystemAdapter,
)


class DummyTicketSystemAdapter(TicketSystemAdapter):
    def __init__(self, config):  # pragma: no cover - simple stub
        self.config = config

    async def update_ticket(self, ticket_id, updates):  # pragma: no cover - not used
        return True

    async def find_tickets(self, criteria):  # pragma: no cover - not used
        return []

    async def find_first_ticket(self, criteria):  # pragma: no cover - not used
        return None

    @classmethod
    def get_description(cls) -> str:  # pragma: no cover - not used
        return "dummy adapter"


class DummyPipe(Pipe[ProvidableConfig, BaseModel, BaseModel]):
    InputDataType = BaseModel
    OutputDataType = BaseModel

    def __init__(self, config):  # pragma: no cover - simple stub
        self.config = config

    def process(self, context):  # pragma: no cover - not used
        return context

    @classmethod
    def get_description(cls) -> str:  # pragma: no cover - not used
        return "dummy pipe"


def _setup_otobo_stub():
    """Ensure a minimal 'otobo' module exists for import."""
    dummy_otobo = types.ModuleType("otobo")

    class DummyTicketOperation(enum.Enum):  # pragma: no cover - simple enum
        SEARCH = "search"
        GET = "get"
        UPDATE = "update"

    dummy_otobo.AuthData = object
    dummy_otobo.OTOBOClient = object
    dummy_otobo.OTOBOClientConfig = object
    dummy_otobo.TicketOperation = DummyTicketOperation
    sys.modules.setdefault("otobo", dummy_otobo)


def _setup_schedule_stub():
    """Provide a minimal 'schedule' module for import."""
    dummy_schedule = types.ModuleType("schedule")

    class DummyJob:
        def __getattr__(self, _):
            return self

        def do(self, _):
            return None

    dummy_schedule.every = lambda *_, **__: DummyJob()
    sys.modules.setdefault("schedule", dummy_schedule)


def test_di_container_get_pipeline(monkeypatch):
    _setup_otobo_stub()
    _setup_schedule_stub()
    # Stub out create_registry to avoid importing heavy dependencies during container import
    dummy_create_registry = types.ModuleType("open_ticket_ai.src.base.create_registry")
    dummy_create_registry.create_registry = lambda: Registry()
    sys.modules["open_ticket_ai.src.base.create_registry"] = dummy_create_registry

    container_module = importlib.import_module("open_ticket_ai.src.core.dependency_injection.container")

    # Build minimal config and registry
    config = OpenTicketAIConfig(
        system=SystemConfig(id="sys", provider_key="DummyTicketSystemAdapter"),
        pipes=[PipeConfig(id="pipe1", provider_key="DummyPipe")],
        pipeline=[
            PipelineConfig(
                id="pl1",
                run_every_seconds=ScheduleConfig(interval=1, unit="hours"),
                pipes=["pipe1"],
            )
        ],
    )
    registry = Registry()
    registry.register(DummyTicketSystemAdapter)
    registry.register(DummyPipe)

    # Patch functions used during DIContainer creation
    monkeypatch.setattr(container_module, "load_config", lambda path: config)
    monkeypatch.setattr(container_module, "create_registry", lambda: registry)

    di = container_module.DIContainer()

    pipeline = di.get_pipeline("pl1")
    assert pipeline.config.id == "pl1"
    assert len(pipeline.pipes) == 1
    assert isinstance(pipeline.pipes[0], DummyPipe)
