import pytest
import warnings

import pook
from pook.response import _BinaryDefault


pook.apply_binary_body_fix()


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        "markers",
        "undo_suppress_own_warnings: undo pook-warning suppression",
    )


@pytest.fixture(autouse=True)
def _suppress_own_deprecation_warnings(request: pytest.FixtureRequest):
    undo = request.node.get_closest_marker("undo_suppress_own_warnings")

    if undo:
        # Only relevant when testing the warnings themselves
        yield
        return

    with warnings.catch_warnings(record=True) as recorded_warnings:
        yield

    for warning in recorded_warnings:
        if "Non-binary pook response bodies are deprecated" not in str(warning.message):
            warnings.showwarning(warning)


@pytest.fixture(scope="function")
def without_binary_body_fix():
    _BinaryDefault.fixed = False
    yield
    pook.apply_binary_body_fix()
