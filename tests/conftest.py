# FILE_PATH: open_ticket_ai\tests\conftest.py
import importlib

import pytest


def pytest_collection_modifyitems(config, items):
    """Skip heavy experimental tests if dependencies are missing.

    This pytest hook function checks for the availability of SpaCy and the German language model.
    If either module fails to import, marks all tests from 'test_anonymize_data.py' to be skipped.

    Modifies the test items list in-place by adding skip markers to relevant tests.

    Args:
        config (pytest.Config):
            The pytest configuration object (unused in this function but required by hook signature).
        items (list[pytest.Item]):
            List of collected test items. Will be modified in-place by adding skip markers.
    """
    try:
        importlib.import_module("spacy")
        importlib.import_module("de_core_news_sm")
    except Exception:
        skip_reason = "SpaCy or the German model is not available"
        for item in list(items):
            if "test_anonymize_data.py" in str(item.fspath):
                item.add_marker(pytest.mark.skip(reason=skip_reason))