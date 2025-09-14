import logging
import sys
import types
from unittest.mock import Mock

from open_ticket_ai.src import main


def reset_logging():
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(logging.NOTSET)


def test_main_sets_warning_level_by_default():
    reset_logging()
    main.main(verbose=False, debug=False)
    assert logging.getLogger().level == logging.WARNING


def test_main_sets_info_level_with_verbose():
    reset_logging()
    main.main(verbose=True, debug=False)
    assert logging.getLogger().level == logging.INFO


def test_main_sets_debug_level_with_debug():
    reset_logging()
    main.main(verbose=False, debug=True)
    assert logging.getLogger().level == logging.DEBUG


def test_start_invokes_app_run(monkeypatch, capsys):
    fake_app = Mock()

    class DummyContainer:
        def get(self, cls):
            self.requested = cls
            return fake_app

    container = DummyContainer()
    app_module = types.SimpleNamespace(App=type("App", (), {}))
    container_module = types.SimpleNamespace(DIContainer=lambda: container)
    figlet_module = types.SimpleNamespace(Figlet=lambda font: types.SimpleNamespace(renderText=lambda text: "ASCII"))

    monkeypatch.setitem(sys.modules, "open_ticket_ai.src.core.app", app_module)
    monkeypatch.setitem(sys.modules, "open_ticket_ai.src.core.dependency_injection.container", container_module)
    monkeypatch.setitem(sys.modules, "pyfiglet", figlet_module)

    main.start()

    assert container.requested is app_module.App
    fake_app.run.assert_called_once()
    captured = capsys.readouterr()
    assert "ASCII" in captured.out
