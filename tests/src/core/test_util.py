from pathlib import Path
from types import SimpleNamespace
import json
import runpy

import pytest
import yaml
from pydantic import BaseModel
from rich.syntax import Syntax

from open_ticket_ai.src.core.util import path_util, pretty_print_config, create_json_config_schema


class DummyModel(BaseModel):
    foo: int
    bar: str


def test_find_project_root_returns_project_directory():
    project_root = path_util.find_python_code_root_path()
    assert project_root.name == "open_ticket_ai"
    assert (project_root / "__init__.py").exists()


def test_find_project_root_invalid_name_raises():
    with pytest.raises(FileNotFoundError):
        path_util.find_python_code_root_path("does_not_exist")


def test_pretty_print_config_outputs_yaml():
    printed = []
    fake_console = SimpleNamespace(print=lambda x: printed.append(x))

    cfg = DummyModel(foo=1, bar="baz")
    pretty_print_config.pretty_print_config(cfg, fake_console)

    assert len(printed) == 1
    arg = printed[0]
    assert isinstance(arg, Syntax)
    expected_yaml = yaml.safe_dump(cfg.model_dump(), sort_keys=False)
    assert arg.code == expected_yaml


def test_pretty_print_config_non_model_raises():
    fake_console = SimpleNamespace(print=lambda x: None)
    with pytest.raises(AttributeError):
        pretty_print_config.pretty_print_config({"foo": 1}, fake_console)


def test_root_config_schema_contains_open_ticket_ai():
    schema = create_json_config_schema.RootConfig.model_json_schema()
    assert "open_ticket_ai" in schema.get("properties", {})


def test_schema_file_written_when_run_as_script(tmp_path, monkeypatch):
    monkeypatch.setattr(path_util, "find_python_code_root_path", lambda: tmp_path)
    runpy.run_module("open_ticket_ai.src.core.util.create_json_config_schema", run_name="__main__")
    schema_file = tmp_path / "config.schema.json"
    assert schema_file.exists()
    data = json.loads(schema_file.read_text())
    assert "open_ticket_ai" in data.get("properties", {})
