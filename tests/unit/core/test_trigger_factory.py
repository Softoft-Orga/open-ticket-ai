"""Tests for trigger instantiation via RenderableFactory."""

from typing import Any
from unittest.mock import MagicMock

from open_ticket_ai.base.triggers.interval_trigger import IntervalTrigger
from open_ticket_ai.core.orchestration.orchestrator_config import TriggerConfig
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.renderable.renderable_factory import RenderableFactory


def test_trigger_instantiation_via_factory() -> None:
    """Test that triggers can be instantiated via RenderableFactory."""
    trigger_def: TriggerConfig[Any] = TriggerConfig.model_validate(
        {
            "id": "test-trigger",
            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
            "params": {"seconds": 10},
        }
    )

    # Mock dependencies
    template_renderer = MagicMock()
    template_renderer.render_recursive.return_value = {"seconds": 10}
    app_config = MagicMock()
    logger_factory = MagicMock()
    logger_factory.get_logger.return_value = MagicMock()

    factory = RenderableFactory(template_renderer, app_config, [], logger_factory)
    scope = PipeContext()

    # Create trigger via factory
    trigger = factory.create_trigger(trigger_def, scope)

    # Verify it's an IntervalTrigger instance
    assert isinstance(trigger, IntervalTrigger)
    assert trigger.trigger_def.id == "test-trigger"
    assert trigger.seconds_interval == 10


def test_trigger_receives_logger_factory() -> None:
    """Test that triggers receive logger_factory through DI."""
    trigger_def: TriggerConfig[Any] = TriggerConfig.model_validate(
        {
            "id": "test-trigger",
            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
            "params": {"seconds": 5, "minutes": 1},
        }
    )

    # Mock dependencies
    template_renderer = MagicMock()
    template_renderer.render_recursive.return_value = {"seconds": 5, "minutes": 1}
    app_config = MagicMock()
    logger_factory = MagicMock()
    mock_logger = MagicMock()
    logger_factory.get_logger.return_value = mock_logger

    factory = RenderableFactory(template_renderer, app_config, [], logger_factory)
    scope = PipeContext()

    # Create trigger via factory
    trigger = factory.create_trigger(trigger_def, scope)

    # Verify logger was obtained from factory (called for both factory and trigger)
    assert logger_factory.get_logger.call_count >= 2
    # Check that IntervalTrigger got a logger and interval is correctly calculated
    assert isinstance(trigger, IntervalTrigger)
    assert trigger.seconds_interval == 65  # 5 seconds + 60 seconds (1 minute)


def test_trigger_config_rendering() -> None:
    """Test that trigger configs are rendered before instantiation."""
    trigger_def: TriggerConfig[Any] = TriggerConfig.model_validate(
        {
            "id": "test-trigger",
            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
            "params": {"seconds": "{{ context_value }}"},
        }
    )

    # Mock template renderer to simulate rendering
    template_renderer = MagicMock()

    def mock_render_recursive(config_dict, scope):
        # Simulate template rendering
        if isinstance(config_dict, dict):
            result = {}
            for key, value in config_dict.items():
                if value == "{{ context_value }}":
                    result[key] = 30  # Rendered value
                else:
                    result[key] = value
            return result
        return config_dict

    template_renderer.render_recursive.side_effect = mock_render_recursive

    app_config = MagicMock()
    logger_factory = MagicMock()
    logger_factory.get_logger.return_value = MagicMock()

    factory = RenderableFactory(template_renderer, app_config, [], logger_factory)
    scope = PipeContext()

    # Create trigger via factory
    trigger = factory.create_trigger(trigger_def, scope)

    # Verify template was rendered
    assert template_renderer.render_recursive.called
    # Verify the trigger received the rendered value
    assert isinstance(trigger, IntervalTrigger)
    assert trigger.seconds_interval == 30


def test_trigger_definition_has_unique_id() -> None:
    """Test that TriggerDefinition gets uid set automatically."""
    trigger_def: TriggerConfig[Any] = TriggerConfig.model_validate(
        {
            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
            "params": {"seconds": 10},
        }
    )

    # Even without explicit id, uid should be set
    assert trigger_def.uid is not None
    # And id should be set from uid (via set_id_from_uid validator)
    assert trigger_def.id is not None
    assert trigger_def.id == trigger_def.uid


def test_trigger_definition_with_explicit_id() -> None:
    """Test that explicit ID is preserved."""
    trigger_def: TriggerConfig[Any] = TriggerConfig.model_validate(
        {
            "id": "my-custom-trigger-id",
            "use": "open_ticket_ai.base.triggers.interval_trigger:IntervalTrigger",
            "params": {"seconds": 10},
        }
    )

    # Explicit id should be preserved
    assert trigger_def.id == "my-custom-trigger-id"
    # uid should still be generated
    assert trigger_def.uid is not None
    assert trigger_def.uid != trigger_def.id
