from __future__ import annotations

import logging
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from open_ticket_ai import LoggingConfig
from open_ticket_ai.core.logging.logging_models import LogLevel
from open_ticket_ai.core.logging.stdlib_logging_adapter import StdlibLoggerFactory, create_logger_factory


def test_create_logger_factory_returns_stdlib_factory() -> None:
    factory = create_logger_factory(LoggingConfig())
    assert isinstance(factory, StdlibLoggerFactory)


@pytest.mark.parametrize(
    "level",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
def test_logger_respects_log_level(level: LogLevel, caplog: LogCaptureFixture) -> None:
    factory = create_logger_factory(LoggingConfig(level=level))
    logger = factory.create("test_logger")

    with caplog.at_level(logging.DEBUG):
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

    log_levels = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
    configured_level = log_levels[level]

    for record in caplog.records:
        assert record.levelno >= configured_level


def test_logger_writes_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"
    factory = create_logger_factory(
        LoggingConfig(
            log_to_file=True,
            log_file_path=str(log_file),
        )
    )
    logger = factory.create("test_logger")

    logger.info("Info message")
    logger.error("Error message")

    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Info message" in log_content
    assert "Error message" in log_content
