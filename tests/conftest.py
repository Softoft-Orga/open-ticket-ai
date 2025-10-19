import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_config_file(tmp_path):
    config_content = """open_ticket_ai:
  api_version: "1"
  infrastructure:
    logging:
      level: "DEBUG"
      log_to_file: false
  
  services:
    jinja_default:
      use: "base:JinjaRenderer"
  
  orchestrator:
    use: "base:SimpleSequentialOrchestrator"
    steps:
      - id: test-runner
        use: "base:SimpleSequentialRunner"
"""
    config_file = tmp_path / "config.yml"
    config_file.write_text(config_content)
    
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    
    yield config_file
    
    os.chdir(original_cwd)
