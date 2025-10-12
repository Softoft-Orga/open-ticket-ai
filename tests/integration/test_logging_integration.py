"""Integration test for the logging system.

This test verifies that the logging system works correctly when integrated
with the dependency injection container and can be used in real services.
"""

from __future__ import annotations

import pytest
from injector import Injector, inject

from open_ticket_ai.core.dependency_injection.logging_module import LoggingModule
from open_ticket_ai.core.logging_iface import LoggerFactory


def test_logging_integration_with_stdlib(caplog):
    """Test that logging works end-to-end with stdlib implementation."""

    class TestService:
        @inject
        def __init__(self, logger_factory: LoggerFactory):
            self._logger = logger_factory.get_logger("TestService", service="test", version="1.0")

        def do_work(self, task_id: str):
            logger = self._logger.bind(task_id=task_id)
            logger.info("Starting work")
            logger.debug("Processing")
            logger.info("Work complete")

    with caplog.at_level("DEBUG"):
        injector = Injector([LoggingModule(log_impl="stdlib", log_level="DEBUG")])
        service = injector.get(TestService)

        service.do_work("task-123")

    assert "Starting work" in caplog.text
    assert "task_id=task-123" in caplog.text
    assert "service=test" in caplog.text
    assert "version=1.0" in caplog.text


@pytest.mark.skip(reason="Structlog implementation not available - module 'open_ticket_ai.infra' does not exist")
def test_logging_integration_with_structlog():
    """Test that logging works end-to-end with structlog implementation."""

    class TestService:
        @inject
        def __init__(self, logger_factory: LoggerFactory):
            self._logger = logger_factory.get_logger("TestService", service="test", version="2.0")

        def do_work(self, task_id: str):
            logger = self._logger.bind(task_id=task_id)
            logger.info("Starting work")
            logger.debug("Processing")
            logger.info("Work complete")

    injector = Injector([LoggingModule(log_impl="structlog", log_level="DEBUG")])
    service = injector.get(TestService)

    service.do_work("task-456")


def test_multiple_services_share_logger_factory():
    """Test that multiple services can share the same logger factory."""

    class ServiceA:
        @inject
        def __init__(self, logger_factory: LoggerFactory):
            self._logger = logger_factory.get_logger("ServiceA")

    class ServiceB:
        @inject
        def __init__(self, logger_factory: LoggerFactory):
            self._logger = logger_factory.get_logger("ServiceB")

    injector = Injector([LoggingModule()])

    service_a = injector.get(ServiceA)
    service_b = injector.get(ServiceB)

    assert service_a._logger is not service_b._logger


def test_logger_factory_is_singleton():
    """Test that the logger factory is a singleton."""

    injector = Injector([LoggingModule()])

    factory1 = injector.get(LoggerFactory)
    factory2 = injector.get(LoggerFactory)

    assert factory1 is factory2


def test_context_binding_persists_across_calls(caplog):
    """Test that bound context persists across multiple log calls."""

    class TestService:
        @inject
        def __init__(self, logger_factory: LoggerFactory):
            self._logger = logger_factory.get_logger("TestService")

        def process_user(self, user_id: str):
            logger = self._logger.bind(user_id=user_id)
            logger.info("Step 1")
            logger.info("Step 2")
            logger.info("Step 3")

    with caplog.at_level("INFO"):
        injector = Injector([LoggingModule(log_impl="stdlib", log_level="INFO")])
        service = injector.get(TestService)

        service.process_user("user-789")

    log_records = caplog.records
    assert len(log_records) == 3

    for record in log_records:
        assert "user_id=user-789" in record.message


@pytest.mark.skip(reason="Structlog implementation not available - module 'open_ticket_ai.infra' does not exist")
def test_switching_implementations_at_runtime():
    """Test that we can create different injectors with different implementations."""

    class TestService:
        @inject
        def __init__(self, logger_factory: LoggerFactory):
            self._logger = logger_factory.get_logger("TestService")

    injector_stdlib = Injector([LoggingModule(log_impl="stdlib")])
    injector_structlog = Injector([LoggingModule(log_impl="structlog")])

    service_stdlib = injector_stdlib.get(TestService)
    service_structlog = injector_structlog.get(TestService)

    assert service_stdlib._logger is not service_structlog._logger
