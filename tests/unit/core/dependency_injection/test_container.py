from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from injector import Injector

from open_ticket_ai.core.config.config_models import RawOpenTicketAIConfig, GeneralConfig
from open_ticket_ai.core.dependency_injection.container import AppModule

@pytest.fixture(scope="function")
def test_model_to_yaml_direct_dump(tmp_path: Path):
    """Alternative: dump directly to file."""
    model = RawOpenTicketAIConfig()

    yaml_file = tmp_path / "config.yml"

    # Dump directly to file
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump({ "open_ticket_ai": model.model_dump()}, f)
    yield yaml_file

def test_app_module_binds_singleton_dependencies(test_model_to_yaml_direct_dump: Path) -> None:

    injector = Injector([AppModule(str(test_model_to_yaml_direct_dump))])

    resolved_config = injector.get(RawOpenTicketAIConfig)

    assert resolved_config == RawOpenTicketAIConfig()
