from __future__ import annotations

import logging
import re
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from open_ticket_ai.core.logging.logging_models import LoggingConfig
from open_ticket_ai.core.logging.stdlib_logging_adapter import (
    StdlibLoggerFactory,
    create_logger_factory,
)


def test_create_logger_factory_returns_stdlib_factory() -> None:
    factory = create_logger_factory(LoggingConfig())
    assert isinstance(factory, StdlibLoggerFactory)


@pytest.mark.parametrize(
    "level",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
def test_logger_respects_log_level(level: str, caplog: LogCaptureFixture) -> None:
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


@pytest.mark.parametrize(
    "log_format,expected_pattern",
    [
        ("%(levelname)s - %(message)s", r"INFO - Test message"),
        ("%(name)s: %(message)s", r"test_logger: Test message"),
    ],
)
def test_logger_respects_log_format(log_format: str, expected_pattern: str, capsys: pytest.CaptureFixture[str]) -> None:
    factory = create_logger_factory(LoggingConfig(log_format=log_format))
    logger = factory.create("test_logger")

    logger.info("Test message")

    captured = capsys.readouterr()
    assert expected_pattern in captured.out


@pytest.mark.parametrize(
    "date_format,expected_pattern",
    [
        ("%Y-%m-%d", r"\d{4}-\d{2}-\d{2}"),
        ("%H:%M:%S", r"\d{2}:\d{2}:\d{2}"),
    ],
)
def test_logger_respects_date_format(
    date_format: str, expected_pattern: str, capsys: pytest.CaptureFixture[str]
) -> None:
    factory = create_logger_factory(
        LoggingConfig(
            date_format=date_format,
            log_format="%(asctime)s - %(message)s",
        )
    )
    logger = factory.create("test_logger")

    logger.info("Test message")

    captured = capsys.readouterr()
    assert re.search(expected_pattern, captured.out) is not None


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
