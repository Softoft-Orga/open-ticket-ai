import os
from pathlib import Path

import pytest


@pytest.fixture
def temp_config_file(tmp_path):
    config_content = """open_ticket_ai:
  api_version: ">=1.0.0"
  infrastructure:
    logging:
      level: "DEBUG"
      log_to_file: false

  services:
    jinja_default:
      use: "otai_base:JinjaRenderer"

  orchestrator:
    use: "otai_base:SimpleSequentialOrchestrator"
    steps:
      - id: test-runner
        use: "otai_base:SimpleSequentialRunner"
"""
    config_file = tmp_path / "config.yml"
    config_file.write_text(config_content)

    original_cwd = Path.cwd()
    os.chdir(tmp_path)

    yield config_file

    os.chdir(original_cwd)
