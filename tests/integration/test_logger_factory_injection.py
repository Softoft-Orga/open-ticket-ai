"""Integration test for LoggerFactory injection into pipes and services via RenderableFactory."""

from __future__ import annotations

import pytest
from injector import Injector

from open_ticket_ai.base.pipes.jinja_expression_pipe import JinjaExpressionParams, JinjaExpressionPipeConfig
from open_ticket_ai.base.template_renderers.jinja_renderer import JinjaRenderer
from open_ticket_ai.core import AppConfig
from open_ticket_ai.core.config.renderable_factory import RenderableFactory
from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule
from open_ticket_ai.core.logging_iface import AppLogger, LoggerFactory
from open_ticket_ai.core.pipeline.pipe_context import PipeContext
from open_ticket_ai.core.template_rendering.renderer_config import JinjaRendererConfig


def test_renderable_factory_injects_logger_factory_into_pipes():
    """Test that RenderableFactory correctly injects logger_factory into created pipes."""

    injector = Injector([LoggingModule(log_impl="stdlib", log_level="DEBUG")])

    logger_factory = injector.get(LoggerFactory)
    renderer_config = JinjaRendererConfig()
    template_renderer = JinjaRenderer(renderer_config)
    app_config = AppConfig()

    factory = RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[],
        logger_factory=logger_factory,
    )

    pipe_config = JinjaExpressionPipeConfig(
        id="test_jinja_pipe",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="Hello"),
    )
    context = PipeContext(pipes={}, params={}, parent=None)

    pipe = factory.create_pipe(pipe_config, context)

    assert pipe is not None
    assert hasattr(pipe, "_logger")
    assert isinstance(pipe._logger, AppLogger)


def test_logger_factory_creates_logger_with_class_name():
    """Test that logger_factory creates loggers with the correct class name."""

    injector = Injector([LoggingModule(log_impl="stdlib", log_level="DEBUG")])

    logger_factory = injector.get(LoggerFactory)
    renderer_config = JinjaRendererConfig()
    template_renderer = JinjaRenderer(renderer_config)
    app_config = AppConfig()

    factory = RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[],
        logger_factory=logger_factory,
    )

    pipe_config = JinjaExpressionPipeConfig(
        id="test_jinja_pipe",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="test"),
    )
    context = PipeContext(pipes={}, params={}, parent=None)

    pipe = factory.create_pipe(pipe_config, context)

    assert hasattr(pipe, "_logger")


@pytest.mark.asyncio
async def test_pipe_can_use_injected_logger():
    """Test that a pipe can successfully use the injected logger."""

    injector = Injector([LoggingModule(log_impl="stdlib", log_level="DEBUG")])

    logger_factory = injector.get(LoggerFactory)
    renderer_config = JinjaRendererConfig()
    template_renderer = JinjaRenderer(renderer_config)
    app_config = AppConfig()

    factory = RenderableFactory(
        template_renderer=template_renderer,
        app_config=app_config,
        registerable_configs=[],
        logger_factory=logger_factory,
    )

    pipe_config = JinjaExpressionPipeConfig(
        id="test_jinja_pipe",
        use="open_ticket_ai.base.pipes.jinja_expression_pipe:JinjaExpressionPipe",
        params=JinjaExpressionParams(expression="Hello World"),
    )
    context = PipeContext(pipes={}, params={}, parent=None)

    pipe = factory.create_pipe(pipe_config, context)

    result_context = await pipe.process(context)

    assert "test_jinja_pipe" in result_context.pipes
    assert result_context.pipes["test_jinja_pipe"].success is True
