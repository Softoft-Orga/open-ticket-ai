import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from open_ticket_ai.src.core.app import App


def create_app():
    config = MagicMock()
    validator = MagicMock()
    orchestrator = MagicMock()
    app = App(config, validator, orchestrator)
    app._logger = MagicMock()
    return app, validator, orchestrator


def test_run_successful_validation():
    app, validator, orchestrator = create_app()

    with (
        patch('open_ticket_ai.src.core.app.console') as mock_console,
        patch('open_ticket_ai.src.core.app.schedule.run_pending', side_effect=KeyboardInterrupt),
        patch('open_ticket_ai.src.core.app.time.sleep'),
    ):
        with pytest.raises(KeyboardInterrupt):
            app.run()

    validator.validate_registry.assert_called_once()
    mock_console.print.assert_called_once_with('[bold green]Configuration validation passed![/bold green]')
    orchestrator.set_schedules.assert_called_once()
    app._logger.error.assert_not_called()


def test_run_validation_failure_logs_error_and_continues():
    app, validator, orchestrator = create_app()
    validator.validate_registry.side_effect = ValueError('bad config')

    with (
        patch('open_ticket_ai.src.core.app.console') as mock_console,
        patch('open_ticket_ai.src.core.app.schedule.run_pending', side_effect=KeyboardInterrupt),
        patch('open_ticket_ai.src.core.app.time.sleep'),
    ):
        with pytest.raises(KeyboardInterrupt):
            app.run()

    app._logger.error.assert_called_once_with('Configuration validation failed: bad config')
    mock_console.print.assert_not_called()
    orchestrator.set_schedules.assert_called_once()
    validator.validate_registry.assert_called_once()
