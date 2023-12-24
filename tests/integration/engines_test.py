import subprocess
import pytest


@pytest.mark.parametrize(
    "test_command",
    (
        pytest.param("pytest tests/integration/engines/pytest_suite.py", id="pytest"),
        pytest.param(
            "python -m unittest tests.integration.engines.unittest_suite", id="unittest"
        ),
    ),
)
def test_engines(test_command):
    args = test_command.split(" ")
    assert (
        subprocess.call(args) == 0
    ), f"Engine smoke test failed for command '{test_command}'"
