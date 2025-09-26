import pytest

from open_ticket_ai.core.config.config_models import (
    OpenTicketAIConfig,
    PipeConfig,
    PipelineConfig,
    ScheduleConfig,
    SystemConfig,
)
from open_ticket_ai.core.config.config_validator import OpenTicketAIConfigValidator
from open_ticket_ai.core.dependency_injection.registry import Registry


class DummySystemProvider:
    @classmethod
    def get_provider_key(cls) -> str:  # pragma: no cover - simple provider
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return "system"


class DummyPipe1Provider:
    @classmethod
    def get_provider_key(cls) -> str:  # pragma: no cover - simple provider
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return "pipe1"


class DummyPipe2Provider:
    @classmethod
    def get_provider_key(cls) -> str:  # pragma: no cover - simple provider
        return cls.__name__

    @classmethod
    def get_description(cls) -> str:
        return "pipe2"


def build_config() -> OpenTicketAIConfig:
    return OpenTicketAIConfig(
        system=SystemConfig(id="sys", provider_key=DummySystemProvider.get_provider_key()),
        pipes=[
            PipeConfig(id="p1", provider_key=DummyPipe1Provider.get_provider_key()),
            PipeConfig(id="p2", provider_key=DummyPipe2Provider.get_provider_key()),
        ],
        pipeline=[
            PipelineConfig(id="pl", run_every_seconds=ScheduleConfig(interval=1, unit="seconds"), pipes=["p1", "p2"])
        ],
    )


def test_validate_registry_success() -> None:
    cfg = build_config()
    registry = Registry()
    registry.register_all([DummySystemProvider, DummyPipe1Provider, DummyPipe2Provider])
    validator = OpenTicketAIConfigValidator(cfg, registry)

    # Should not raise
    validator.validate_registry()


def test_validate_registry_missing_provider() -> None:
    cfg = build_config()
    registry = Registry()
    registry.register_all([DummySystemProvider, DummyPipe1Provider])
    validator = OpenTicketAIConfigValidator(cfg, registry)

    with pytest.raises(ValueError) as exc:
        validator.validate_registry()

    assert DummyPipe2Provider.get_provider_key() in str(exc.value)
